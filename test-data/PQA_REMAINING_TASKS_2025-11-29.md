# GreenStack PQA Remaining Tasks and Next Steps
**Date**: 2025-11-29
**Current Status**: 99.9922% Overall Score (7,162/7,423 devices at 100%)

---

## Current Status Summary

### Overall Progress
- **Total Devices**: 7,423
- **Perfect Scores (100%)**: 7,162 (96.5%)
- **Average Score**: 99.9922%
- **Remaining Errors**:
  - HIGH severity: 149 errors
  - MEDIUM severity: 307 errors

### Recent Accomplishments
- ✅ **PQA Fix #137**: DirectParameterOverlay ValueRange elements (fixed 18 HIGH errors)
- ✅ **Testing Infrastructure**: Dataset-based partial import system created
- ⚠️ **PQA Fix #138**: ArrayT SingleValue extraction (implemented, awaiting testing)

---

## BLOCKING ISSUE: UTF-8 BOM Parsing

### Problem
The XML parser cannot handle files with UTF-8 BOM (Byte Order Mark), causing all imports to fail with:
```
not well-formed (invalid token): line 1, column 9
```

### Impact
- Blocks testing of PQA Fix #138 (ArrayT SingleValue)
- Affects quick-test dataset (all 15 files have BOM)
- Unknown how many of the 9,887 extracted IODD files are affected

### Root Cause
Files start with `﻿<?xml` (BOM character: `0xEF 0xBB 0xBF`) which XML parser doesn't handle.

### Solutions (Priority Order)

#### Option 1: Fix XML Parser (RECOMMENDED)
**Location**: `src/parsing/__init__.py` (IODDParser.__init__)

**Implementation**:
```python
def __init__(self, iodd_file_path):
    self.iodd_file = iodd_file_path

    # Read file and strip BOM if present
    with open(iodd_file_path, 'rb') as f:
        content = f.read()
        # Remove UTF-8 BOM if present
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]

    # Parse from bytes
    self.tree = ET.ElementTree(ET.fromstring(content))
    # ... rest of init
```

**Pros**:
- Fixes issue for all future imports
- Robust solution
- No manual dataset curation needed

**Cons**:
- Requires modifying parser
- Need to test doesn't break existing functionality

#### Option 2: Create BOM-Free Dataset (TEMPORARY)
Use the `find_files_without_bom.py` script to create a clean dataset.

**Pros**:
- Quick workaround for immediate testing
- No code changes

**Cons**:
- Only solves problem for specific dataset
- Need to manually curate files
- Doesn't fix underlying issue

#### Option 3: Strip BOM from Extracted Files (NOT RECOMMENDED)
Modify all 9,887 extracted files to remove BOM.

**Pros**:
- Fixes all existing files

**Cons**:
- Destructive operation
- Slow to process
- Future extractions will still have BOM

### Next Steps
1. Implement Option 1 (parser fix)
2. Test with existing quick-test dataset
3. Validate PQA Fix #138 results

---

## HIGH PRIORITY: PQA Fix #138 - ArrayT SingleValue Elements

### Status
✅ **IMPLEMENTED** (awaiting testing)
⚠️ **BLOCKED** by UTF-8 BOM parsing issue

### Background
- **Errors**: 46 HIGH severity (42 SingleValue + 21 nested Name elements)
- **Devices Affected**: 34 devices
- **Pattern**: ArrayT datatypes with SingleValue enumeration elements

### Code Changes Made

#### Parser (`src/parsing/__init__.py:2799-2821`)
Extracts SingleValue from ArrayT SimpleDatatype children:
```python
# PQA Fix #138: Extract SingleValue elements from ArrayT SimpleDatatype child
array_single_values = []
for sv_idx, single_val in enumerate(simple_dt_child.findall('iodd:SingleValue', self.NAMESPACES)):
    value = single_val.get('value')
    if value is not None:
        name_elem = single_val.find('.//iodd:Name', self.NAMESPACES)
        text_id = name_elem.get('textId') if name_elem is not None else None
        text_value = self._resolve_text(text_id) if text_id else None
        sv_xsi_type = single_val.get('{http://www.w3.org/2001/XMLSchema-instance}type')
        array_single_values.append(SingleValue(
            value=value,
            name=text_value or '',
            text_id=text_id,
            xsi_type=sv_xsi_type,
            xml_order=sv_idx
        ))

if array_single_values:
    single_values = array_single_values
```

#### Reconstruction (`src/utils/forensic_reconstruction_v2.py:1143-1157`)
Adds SingleValue to SimpleDatatype child for ArrayT:
```python
if dt['datatype_xsi_type'] == 'ArrayT':
    array_elem_type = dt['array_element_type'] if 'array_element_type' in dt.keys() else None
    array_elem_bit_length = dt['array_element_bit_length'] if 'array_element_bit_length' in dt.keys() else None
    if array_elem_type:
        simple_dt_elem = ET.SubElement(datatype_elem, 'SimpleDatatype')
        simple_dt_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', array_elem_type)
        if array_elem_bit_length:
            simple_dt_elem.set('bitLength', str(array_elem_bit_length))
        # Add SingleValue elements to SimpleDatatype child, not Datatype parent
        self._add_single_values(conn, simple_dt_elem, dt['id'])
else:
    # Add SingleValue enumerations as direct children for non-ArrayT types
    self._add_single_values(conn, datatype_elem, dt['id'])
```

#### Storage
No changes needed - existing methods handle the data correctly.

### Testing Plan
1. Fix UTF-8 BOM parsing issue
2. Run: `python import_dataset.py quick-test --fresh --pqa`
3. Check for reduction in SingleValue missing errors
4. Expected improvement: 46 HIGH errors → 0 (or near 0)
5. Save results to: `test_fix_138_results.txt`

### Git Commit
Already committed with message:
```
fix(pqa): Extract and reconstruct SingleValue in ArrayT datatypes (Fix #138)

- Parser: Extract SingleValue from ArrayT/SimpleDatatype children
- Reconstruction: Add SingleValue to SimpleDatatype child for ArrayT
- Follows same pattern as PQA Fix #126 for Parameters
- Addresses 46 HIGH severity missing_element errors in 34 devices
```

---

## REMAINING HIGH SEVERITY ERRORS (149 Total)

### Priority 1: Variable DatatypeRef Missing (18 errors)
**Pattern**: Variable elements missing DatatypeRef attribute
**Example Error**: `Variable[SSC_DataChannel]/DatatypeRef[unknown]`

**Investigation Needed**:
1. Check if parser extracts DatatypeRef from Variable elements
2. Verify storage saves Variable DatatypeRef
3. Confirm reconstruction outputs DatatypeRef attribute

**Files to Review**:
- `src/parsing/__init__.py` - Variable parsing section
- `src/storage/variable.py` - Variable storage
- `src/utils/forensic_reconstruction_v2.py` - Variable reconstruction

**SQL Query to Find Affected Devices**:
```sql
SELECT DISTINCT device_id, error_path, error_type
FROM pqa_diff_details
WHERE error_path LIKE '%Variable%DatatypeRef%'
AND severity = 'HIGH'
ORDER BY device_id;
```

### Priority 2: ValueRange Missing in Other Contexts (29 errors)
**Pattern**: ValueRange elements missing outside DirectParameterOverlay
**Contexts**:
- SimpleDatatype/ValueRange
- Variable/Datatype/ValueRange
- RecordItem/Datatype/ValueRange

**Note**: DirectParameterOverlay ValueRange was fixed in PQA Fix #137. Need to check if other contexts have same issue.

**Investigation**:
1. Determine which datatype contexts are missing ValueRange
2. Check if parser extracts ValueRange in these contexts
3. Verify storage and reconstruction

**SQL Query**:
```sql
SELECT error_path, COUNT(*) as count
FROM pqa_diff_details
WHERE error_path LIKE '%ValueRange%'
AND severity = 'HIGH'
AND error_path NOT LIKE '%DirectParameterOverlay%'
GROUP BY error_path
ORDER BY count DESC;
```

### Priority 3: Other HIGH Severity Patterns
After fixing SingleValue (46), DatatypeRef (18), and ValueRange (29), there are ~56 remaining HIGH errors.

**Next Steps**:
1. Run query to group remaining HIGH errors by pattern
2. Identify common root causes
3. Prioritize by error count and complexity

**SQL Query**:
```sql
SELECT
    CASE
        WHEN error_path LIKE '%SingleValue%' THEN 'SingleValue'
        WHEN error_path LIKE '%DatatypeRef%' THEN 'DatatypeRef'
        WHEN error_path LIKE '%ValueRange%' THEN 'ValueRange'
        ELSE error_path
    END as error_category,
    COUNT(*) as error_count,
    COUNT(DISTINCT device_id) as devices_affected
FROM pqa_diff_details
WHERE severity = 'HIGH'
GROUP BY error_category
ORDER BY error_count DESC;
```

---

## MEDIUM SEVERITY ERRORS (307 Total)

### Strategy
Address MEDIUM severity errors after all HIGH severity errors are resolved.

### Common Patterns (from previous analysis)
- Attribute ordering differences
- Optional element presence/absence
- Text content whitespace normalization

### Approach
1. Complete all HIGH severity fixes first
2. Run full reimport to get updated error counts
3. Group MEDIUM errors by pattern
4. Implement fixes in order of impact (errors fixed per change)

---

## Testing Infrastructure Overview

### Dataset System
Created comprehensive dataset-based testing infrastructure to enable rapid iteration without 3-4 hour full imports.

### Key Components

#### `create_dataset.py`
Creates curated test datasets from 9,887 extracted IODD files.

**Features**:
- Quick test mode: `--quick-test --limit 15`
- Vendor filtering: `--vendor 303`
- Filename pattern: `--pattern "ArrayT"`
- Content search: `--content-pattern "ArrayT.*SingleValue"` (slower)
- Manifest generation

**Example**:
```bash
python create_dataset.py --quick-test --output quick-test --limit 15
```

#### `import_dataset.py`
Imports specific datasets with options for fresh database and automatic PQA.

**Features**:
- Fresh import: `--fresh` (deletes existing database)
- Auto PQA: `--pqa` (runs analysis after import)
- Progress reporting
- Error summary

**Example**:
```bash
python import_dataset.py quick-test --fresh --pqa
```

#### Directory Structure
```
test-data/
├── iodd-files/          # Original ZIP packages
├── iodd-extracted/      # 9,887 extracted XML files
├── datasets/            # Curated test datasets
│   ├── quick-test/      # 15 files for rapid testing
│   └── ...              # Additional datasets as needed
├── README.md            # Comprehensive documentation
└── QUICKSTART.md        # Quick start guide
```

### Performance Benchmarks

| Dataset Size | Import Time | PQA Time | Total     |
|-------------|-------------|----------|-----------|
| 15 files    | ~1 min      | ~5 sec   | ~1 min    |
| 50 files    | ~3 min      | ~15 sec  | ~3.5 min  |
| 100 files   | ~6 min      | ~30 sec  | ~6.5 min  |
| 500 files   | ~30 min     | ~2.5 min | ~33 min   |
| Full (9887) | ~3 hours    | ~50 min  | ~4 hours  |

### TDD Workflow Example
```bash
# 1. Create test dataset
python create_dataset.py --quick-test --output pqa-fix-138 --limit 20

# 2. Baseline test (before fix)
git stash
python import_dataset.py pqa-fix-138 --fresh --pqa
# Save baseline results

# 3. Apply fix and test
git stash pop
python import_dataset.py pqa-fix-138 --fresh --pqa

# 4. Compare results
# Check improvement in PQA scores
```

---

## Critical Lessons Learned

### 1. Parser-Storage-Reconstruction Triangle
Every PQA fix requires checking all three components:
- **Parser**: Extracts data from XML → Python objects
- **Storage**: Saves Python objects → Database
- **Reconstruction**: Queries database → Rebuilds XML

**Common Pitfall**: Assuming storage or reconstruction handles new data automatically. Always verify all three.

### 2. Context Matters for XML Elements
Elements like ValueRange, SingleValue, and DatatypeRef can appear in multiple contexts:
- Parameters
- Variables
- RecordItems
- DirectParameterOverlay
- Custom Datatypes (ArrayT, RecordT, etc.)

**Lesson**: Fixing one context doesn't fix all. Must check each context separately.

### 3. Attribute vs Element Ordering
IODD schema has specific ordering requirements:
- Attributes: Order usually doesn't matter (except for PQA exact match)
- Elements: Order is defined by schema and must be preserved

**Implementation**: Use `xml_order` field to preserve original element ordering.

### 4. ArrayT Special Cases
ArrayT datatypes have nested structure:
```xml
<Datatype xsi:type="ArrayT" count="4">
    <SimpleDatatype xsi:type="UIntegerT" bitLength="8">
        <SingleValue value="0">
            <Name textId="TID_001"/>
        </SingleValue>
    </SimpleDatatype>
</Datatype>
```

**Key Points**:
- SimpleDatatype is child of ArrayT Datatype, not sibling
- SingleValue belongs to SimpleDatatype child, not ArrayT parent
- Must extract/reconstruct in correct hierarchical position

### 5. UTF-8 BOM Handling
Real-world IODD files may have UTF-8 BOM from various vendor tools.

**Lesson**: Parser must handle BOM gracefully, can't assume clean XML.

### 6. Dataset-Based Testing is Essential
Full imports are too slow for iterative development.

**Best Practice**:
- Create targeted datasets (15-50 files) for specific issues
- Use `--fresh` flag to ensure clean database state
- Save baseline results before code changes
- Compare before/after PQA scores to validate fixes

### 7. SQL Queries are Critical for PQA Analysis
The `pqa_diff_details` table is the source of truth for remaining errors.

**Useful Queries**:
```sql
-- Group errors by pattern
SELECT error_path, severity, COUNT(*) as count
FROM pqa_diff_details
GROUP BY error_path, severity
ORDER BY severity, count DESC;

-- Find devices with specific error
SELECT DISTINCT device_id, d.product_name
FROM pqa_diff_details pdd
JOIN devices d ON pdd.device_id = d.id
WHERE error_path LIKE '%ArrayT%SingleValue%';

-- Count perfect scores
SELECT COUNT(*) FROM pqa_quality_metrics WHERE overall_score = 100.0;
```

---

## Troubleshooting Guide

### Issue: Import Fails with "not well-formed (invalid token)"
**Cause**: UTF-8 BOM in XML file
**Solution**: Implement parser BOM stripping (see Option 1 above)
**Workaround**: Create dataset without BOM files

### Issue: PQA Score Doesn't Improve After Fix
**Checklist**:
1. Did you delete database before reimport? (`--fresh` flag)
2. Did you commit the code changes?
3. Did you restart any background processes?
4. Did you check the correct devices were imported?
5. Did you run PQA analysis after import?

**Debugging**:
```bash
# Check database has new data
sqlite3 greenstack.db "SELECT COUNT(*) FROM devices;"

# Check specific device was imported
sqlite3 greenstack.db "SELECT id, product_name FROM devices WHERE id = 548;"

# Manually run PQA on one device
python -c "
from src.utils.forensic_reconstruction_v2 import ForensicReconstructor
from pathlib import Path

reconstructor = ForensicReconstructor('greenstack.db')
result = reconstructor.reconstruct_device(548, output_path='test_device_548.xml')
print(f'Reconstruction result: {result}')
"
```

### Issue: Dataset Creation is Slow
**Cause**: Using `--content-pattern` which reads every file
**Solution**: Use filename-based `--pattern` when possible
**Alternative**: Pre-filter files with grep/find, then create dataset from list

### Issue: Database Locked Error
**Cause**: Background process still running
**Solution**:
```bash
# Check for Python processes
tasklist | findstr python

# Kill specific process
taskkill /PID <process_id> /F
```

### Issue: Git Merge Conflicts in Database Files
**Cause**: Database files committed to git
**Solution**: Database files should be in `.gitignore`
**Check**: Ensure `greenstack.db*` is in `.gitignore`

---

## Immediate Next Steps (Priority Order)

### Step 1: Fix UTF-8 BOM Parsing ⚠️ BLOCKING
1. Implement BOM stripping in `src/parsing/__init__.py`
2. Test with existing quick-test dataset
3. Commit fix

**Time Estimate**: 30 minutes

### Step 2: Validate PQA Fix #138 (ArrayT SingleValue)
1. Run: `python import_dataset.py quick-test --fresh --pqa`
2. Check error reduction in SingleValue category
3. Save results: `test_fix_138_results.txt`
4. If successful, proceed to Step 3
5. If issues found, debug and fix

**Time Estimate**: 15 minutes (after BOM fix)

### Step 3: Full Database Reimport
1. Delete database: `cmd /c "if exist greenstack.db del /f greenstack.db"`
2. Run full import: `python import_all_iodds.py 2>&1 | tee import_log_post_arrayt_singlevalue_fix.txt`
3. Run PQA: `python run_pqa_analysis.py 2>&1 | tee pqa_analysis_post_arrayt_singlevalue_fix.txt`
4. Analyze results

**Time Estimate**: 4 hours

**Expected Improvement**:
- HIGH errors: 149 → ~103 (46 errors fixed)
- Average score: 99.9922% → 99.9960%
- Perfect scores: 7,162 → ~7,196 (34 more devices at 100%)

### Step 4: Fix Variable DatatypeRef (18 HIGH errors)
1. Investigate where Variable DatatypeRef is missing
2. Implement parser/storage/reconstruction fixes
3. Test with targeted dataset
4. Full reimport and validate

**Time Estimate**: 2-3 hours

### Step 5: Fix ValueRange in Other Contexts (29 HIGH errors)
1. Identify which contexts are affected
2. Adapt PQA Fix #137 solution to other contexts
3. Test and validate
4. Full reimport

**Time Estimate**: 2-3 hours

### Step 6: Address Remaining HIGH Severity Errors (~56 after above)
1. Group by pattern using SQL query
2. Investigate root causes
3. Implement fixes in order of impact
4. Iterative test and reimport

**Time Estimate**: 4-6 hours

### Step 7: MEDIUM Severity Errors (307 errors)
Begin after all HIGH severity errors are resolved.

**Time Estimate**: 8-12 hours

---

## Path to 100% PQA Score

### Current Status
- 99.9922% average score
- 7,162/7,423 devices at 100% (96.5%)
- 261 devices with errors

### Remaining Work Estimate

| Phase | Errors Fixed | Time Estimate | Cumulative Score |
|-------|-------------|---------------|------------------|
| Fix #138 (SingleValue) | 46 HIGH | 30 min | ~99.9960% |
| Variable DatatypeRef | 18 HIGH | 2-3 hours | ~99.9975% |
| ValueRange contexts | 29 HIGH | 2-3 hours | ~99.9985% |
| Other HIGH errors | ~56 HIGH | 4-6 hours | ~99.9995% |
| MEDIUM errors | 307 MED | 8-12 hours | ~100.0000% |

### Total Time to 100%
**Estimated**: 17-25 hours of focused work
**Contingency**: Add 25% for unexpected issues = 21-31 hours

### Success Criteria
- All devices achieve 100% PQA score
- Full reimport completes without errors
- All tests pass with various datasets
- Documentation is complete and accurate

---

## Documentation Created

### Files in test-data/
1. **README.md** - Comprehensive guide to dataset system
2. **QUICKSTART.md** - Quick start guide for rapid testing
3. **PQA_REMAINING_TASKS_2025-11-29.md** - This file

### Scripts Created
1. **create_dataset.py** - Dataset creation tool
2. **import_dataset.py** - Dataset import tool
3. **find_files_without_bom.py** - BOM detection utility

### Git Status
- ✅ Scripts committed
- ⚠️ Documentation in test-data/ (not committed due to .gitignore)
- ⚠️ Dataset files (not committed due to .gitignore)

**Note**: If documentation should be version controlled, add exception to `.gitignore`:
```gitignore
# In .gitignore
test-data/*
!test-data/*.md
!test-data/scripts/
```

---

## Contact and Collaboration

### Code Review Checklist
Before committing PQA fixes:
- [ ] Parser changes extract all required data
- [ ] Storage saves all extracted data
- [ ] Reconstruction outputs data in correct XML structure
- [ ] Tested with small dataset (15-50 files)
- [ ] Validated error reduction with SQL queries
- [ ] Git commit message follows PQA Fix #N format
- [ ] Documentation updated if needed

### Handoff Notes
When passing this work to another developer:
1. Read this document completely
2. Review test-data/README.md and QUICKSTART.md
3. Run quick-test import to familiarize with workflow
4. Start with UTF-8 BOM fix (blocking issue)
5. Follow priority order listed in "Immediate Next Steps"

---

**Last Updated**: 2025-11-29
**Next Review**: After PQA Fix #138 validation
