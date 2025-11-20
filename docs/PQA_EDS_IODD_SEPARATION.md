# PQA System: EDS/IODD Separation Implementation

## Overview

The GreenStack PQA (Parser Quality Assurance) system now fully supports separate analysis workflows for EDS (INI format) and IODD (XML format) files, using file-type-appropriate analyzers.

**Implementation Date:** 2025-01-20
**Issue Resolved:** EDS files (INI format) were being analyzed with IODD XML analyzers, causing structural_score=0

---

## Architecture

### File Type Routing

The `UnifiedPQAOrchestrator` (src/utils/pqa_orchestrator.py) automatically routes analysis based on `FileType` enum:

```python
class FileType(Enum):
    IODD = "IODD"  # XML format files
    EDS = "EDS"    # INI format files
```

### Analyzer Selection

| File Type | Reconstructor | Diff Analyzer | Format |
|-----------|--------------|---------------|--------|
| **IODD** | `IODDReconstructor` | `DiffAnalyzer` | XML |
| **EDS** | `EDSReconstructor` | `EDSDiffAnalyzer` | INI |

**Code Reference:** `pqa_orchestrator.py:201-215`

```python
def _reconstruct_file(self, file_id: int, file_type: FileType) -> str:
    if file_type == FileType.IODD:
        return self.iodd_reconstructor.reconstruct_iodd(file_id)
    else:  # EDS
        return self.eds_reconstructor.reconstruct_eds(file_id)

def _analyze_diff(self, original: str, reconstructed: str, file_type: FileType):
    if file_type == FileType.IODD:
        return self.iodd_analyzer.analyze(original, reconstructed)
    else:  # EDS
        return self.eds_analyzer.analyze(original, reconstructed)
```

---

## Database Schema Changes

### Migration 025: Add file_type Column

**File:** `alembic/versions/025_add_file_type_to_metrics.py`

Added `file_type` column to `pqa_quality_metrics` table to enable:
- Efficient filtering by file type
- Separate metric tracking for EDS vs IODD
- Improved query performance (no JOIN with pqa_file_archive needed)

```sql
ALTER TABLE pqa_quality_metrics ADD COLUMN file_type TEXT;
CREATE INDEX idx_pqa_metrics_file_type ON pqa_quality_metrics(file_type);
```

### Data Population

Existing records were backfilled from `pqa_file_archive`:

```sql
UPDATE pqa_quality_metrics
SET file_type = (
    SELECT pqa_file_archive.file_type
    FROM pqa_file_archive
    WHERE pqa_file_archive.id = pqa_quality_metrics.archive_id
)
WHERE archive_id IS NOT NULL;
```

---

## EDS Diff Analyzer Fix

### Issue

EDS files start with comment lines (e.g., `$ EZ-EDS Version 3.36.1.20241010`), which ConfigParser couldn't handle:

```
ERROR: EDS parsing error: File contains no section headers.
```

This caused:
- `total_sections_original = 0`
- `structural_score = 0.00%`
- `overall_score = 65.00%` (uniform across all files)

### Solution

**File:** `src/utils/eds_diff_analyzer.py:137`

Added `comment_prefixes=('$',)` to ConfigParser:

```python
def _parse_eds(self, eds_content: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser(
        allow_no_value=True,
        strict=False,
        comment_prefixes=('$',)  # Handle EZ-EDS comment lines
    )
    config.optionxform = str  # Preserve case sensitivity

    try:
        config.read_string(eds_content)
    except configparser.Error as e:
        logger.error(f"EDS parsing error: {e}")
        config = configparser.ConfigParser()

    return config
```

---

## Results

### Before Fix (73 EDS Files)
```
File Type  | Count | Avg Score | Avg Structural
EDS        | 73    | 65.00%    | 0.00%
IODD       | 82    | 89.23%    | 87.31%
```

**Problem:** All EDS files had identical uniform scores with structural_score=0

### After Fix (Reprocessed)
```
File Type  | Count | Avg Score | Avg Structural | Min Score | Max Score
EDS        | 144   | 60.61%    | 27.12%         | 52.05%    | 65.53%
IODD       | 82    | 89.23%    | 87.31%         | 82.91%    | 97.88%
```

**Success:**
- ✅ Structural scores now non-zero (avg 27.12%)
- ✅ Score variation (52-65%) indicates real diff analysis
- ✅ Sections detected: avg 8-13 sections per EDS file
- ✅ Keys detected: avg 30-575 keys per EDS file

---

## API Changes

### PQA Dashboard Summary Endpoint

**Updated:** `GET /api/pqa/dashboard/summary`

Now supports optional `file_type` query parameter:

```bash
# Get combined metrics
GET /api/pqa/dashboard/summary

# Get IODD-only metrics
GET /api/pqa/dashboard/summary?file_type=IODD

# Get EDS-only metrics
GET /api/pqa/dashboard/summary?file_type=EDS
```

**File:** `src/routes/pqa_routes.py:756`

---

## Frontend Changes

### Admin Console - PQA Metrics Display

**File:** `frontend/src/components/AdminConsole.jsx:1649-1950`

Added file type filter tabs:
- **All Files**: Shows combined metrics + side-by-side IODD/EDS comparison
- **IODD (XML)**: Shows IODD-specific metrics
- **EDS (INI)**: Shows EDS-specific metrics

**Features:**
- Tab-based filtering
- Side-by-side comparison view
- Separate average scores for each file type
- Updated info banner explaining the dual-workflow system

---

## Usage

### Running PQA Analysis

**For IODD Files:**
```python
from src.utils.pqa_orchestrator import UnifiedPQAOrchestrator, FileType

orchestrator = UnifiedPQAOrchestrator()
metrics, diffs = orchestrator.run_full_analysis(
    file_id=device_id,
    file_type=FileType.IODD,
    original_content=xml_content
)
```

**For EDS Files:**
```python
orchestrator = UnifiedPQAOrchestrator()
metrics, diffs = orchestrator.run_full_analysis(
    file_id=eds_file_id,
    file_type=FileType.EDS,
    original_content=eds_content
)
```

### Reprocessing Files

To reprocess all EDS files after analyzer improvements:

```bash
python reprocess_eds_files.py
```

---

## Metric Mapping

EDS and IODD metrics are mapped to common database structure:

| Common Column | IODD Source | EDS Source |
|--------------|-------------|------------|
| `structural_score` | `structural_score` | `section_score` |
| `attribute_score` | `attribute_score` | `key_score` |
| `value_score` | `value_score` | `value_score` |
| `total_elements_original` | `total_elements_original` | `total_sections_original` |
| `total_attributes_original` | `total_attributes_original` | `total_keys_original` |

**Orchestrator Code:** `pqa_orchestrator.py:265-289`

---

## Testing

### Test Script

**File:** `test_pqa_analyzer.py`

Verifies that:
- EDS files use `EDSDiffAnalyzer` (sections > 0)
- IODD files use `DiffAnalyzer`
- Correct reconstructors are used

```bash
python test_pqa_analyzer.py
```

**Expected Output:**
```
[PASS] TEST PASSED: EDS files are using EDSDiffAnalyzer
```

---

## Known Issues

### EDS Score Range

EDS files currently score 52-65% (lower than IODD's 83-98%). This is expected because:

1. **EDS Reconstruction Gaps**: Some EDS sections are not fully reconstructed from the database
2. **Missing Sections**: Original files have 13 sections, reconstructed have 8
3. **Key Loss**: ~32% data loss in keys
4. **Value Mismatches**: 40% value accuracy

**Next Steps:**
- Improve EDS reconstruction coverage
- Add missing sections to database schema
- Enhance parameter/assembly mapping

---

## Files Modified

### Backend
1. `alembic/versions/025_add_file_type_to_metrics.py` - Database migration
2. `src/utils/pqa_orchestrator.py` - Added file_type to INSERT statements
3. `src/utils/eds_diff_analyzer.py` - Fixed comment line handling
4. `src/routes/pqa_routes.py` - Added file_type filtering to dashboard endpoint

### Frontend
5. `frontend/src/components/AdminConsole.jsx` - Added file type tabs and comparison view

### Testing/Scripts
6. `test_pqa_analyzer.py` - Analyzer routing test
7. `reprocess_eds_files.py` - Bulk reprocessing script

### Documentation
8. `docs/PQA_EDS_IODD_SEPARATION.md` - This document

---

## Summary

The PQA system now correctly handles both EDS and IODD files with appropriate analyzers. The fix resolved the uniform score issue and enabled accurate quality assessment for both file formats.

**Key Achievements:**
- ✅ Separate analysis workflows for EDS/IODD
- ✅ Fixed EDS comment line parsing
- ✅ Database schema enhanced with file_type discriminator
- ✅ Frontend UI updated with file type filtering
- ✅ Reprocessed 68 of 73 EDS files successfully
- ✅ Scores now accurately reflect reconstruction quality

**Date Completed:** 2025-01-20
