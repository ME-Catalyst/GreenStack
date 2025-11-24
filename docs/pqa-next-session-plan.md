# PQA Next Session Plan - Detailed Implementation Guide

## 🚨 CRITICAL: Backend Server Restart Required FIRST

**Before ANY new fixes**, the backend server must be restarted for Fix #86-92 to take effect.

**Expected Impact**: ~140 diffs resolved (Menu duplicates)
**Current Stats**: 299 diffs → Expected after restart: ~159 diffs

---

## Phase 2: Quick Wins (30-60 minutes, ~30 diffs)

### Fix #98: Datatype@count Attribute (3-4 diffs)

**Complexity**: Medium (requires migrations + schema changes)

**Files Affected**: CX4_v12, CX4_v24, CX4_v32, CANEO series4x

**Root Cause**: ArrayT datatypes (in both DatatypeCollection and ProcessDataCollection) have a `count` attribute that's not being stored or reconstructed.

**Implementation Steps**:

1. **Model Updates** (`src/models/__init__.py`):
   - CustomDatatype model: Add `array_count: Optional[int] = None`
   - ProcessData model: Already has array_count, array_element_type, array_element_bit_length

2. **Migration 099** - Add array_count to custom_datatypes:
   ```python
   op.add_column('custom_datatypes',
                 sa.Column('array_count', sa.INTEGER, nullable=True))
   ```

3. **Migration 100** - Add array fields to process_data:
   ```python
   op.add_column('process_data',
                 sa.Column('array_count', sa.INTEGER, nullable=True))
   op.add_column('process_data',
                 sa.Column('array_element_type', sa.TEXT, nullable=True))
   op.add_column('process_data',
                 sa.Column('array_element_bit_length', sa.INTEGER, nullable=True))
   ```

4. **Parser** (`src/parsing/__init__.py`):
   - `_extract_custom_datatypes()`: Extract count attribute for ArrayT types
   - `_extract_process_data()`: Extract count/element info for inline ArrayT datatypes

5. **Storage** (`src/storage/custom_datatype.py` and `src/storage/process_data.py`):
   - Add array_count to INSERT queries

6. **Reconstruction** (`src/utils/forensic_reconstruction_v2.py`):
   - `_create_datatype_collection()`: Line ~1073, add:
     ```python
     if dt['array_count']:
         datatype_elem.set('count', str(dt['array_count']))
     ```
   - `_add_process_data()`: Similar for ProcessData inline datatypes

**Testing**: Check CX4_v12 IODD file for ArrayT with count attribute

---

### Fix #96: Menu Button Elements (4 diffs)

**Complexity**: Low

**Root Cause**: 3 missing Button elements + 1 extra Button element

**Implementation**: Investigate Button extraction/reconstruction logic in Menu parsing

---

### Fix #94: schemaLocation Incorrect (2 diffs)

**Complexity**: Low

**Root Cause**: Namespace/XSD mapping incorrect for specific IODD versions

**Files Affected**: 2 files

**Check**: `SCHEMA_CONFIGS` in `src/utils/forensic_reconstruction_v2.py`

---

## Phase 3: Medium Complexity (60-90 minutes, ~10 diffs)

### Fix #91: DatatypeCollection Missing Elements (10 diffs)

#### Subtask #91a: Variable/Datatype/Name Missing (4 diffs)
**Root Cause**: Name element within Variable/Datatype not being extracted/reconstructed

#### Subtask #91b: Datatype/SimpleDatatype Missing (3 diffs)
**Files**: CX4_v12, CX4_v24, CX4_v32
**Root Cause**: ArrayT datatypes should have SimpleDatatype child element

#### Subtask #91c: Datatype/SingleValue Missing (3 diffs)
**Files**: VEGAPULS 42 IO-Link (all 3 diffs)
**Root Cause**: Custom datatype SingleValue elements not being extracted

---

## Phase 4: Complex Issues (45-60 minutes, ~8 diffs)

### Fix #95: Menu Incorrect Attributes (8 diffs)

**Issues**:
- MenuRef/Condition@value (3 diffs)
- VariableRef/Button/Description@textId (3 diffs)
- VariableRef/Button@buttonValue (3 diffs)
- MenuRef/Condition@variableId (2 diffs)
- VariableRef/Button/ActionStartedMessage@textId (2 diffs)

**Root Cause**: ID lookup/mapping issues in Button/Condition reconstruction

---

## Deferred (Outlier-Specific, Low ROI)

### Fix #93: Menu Missing Attributes (21 diffs)
**All in FS1xxx-2UPN8 outlier file**
**Complexity**: Unknown - requires IODD file investigation

### Fix #90: StdVariableRef SingleValue (12 diffs)
**All in FS1xxx-2UPN8 outlier file**
**Complexity**: Medium - ordering/alignment issue

### Fix #97: Connection/ProcessData Missing Elements (4 diffs)
**Low impact, spread across files**

---

## Expected Results Timeline

| Milestone | Total Diffs | Perfect Files | Perfect % |
|-----------|-------------|---------------|-----------|
| Current | 299 | 229 | 92.7% |
| After Server Restart (Fix #86-92) | ~159 | ~235 | 95.1% |
| After Phase 2 (Quick Wins) | ~129 | ~238 | 96.4% |
| After Phase 3 (Medium) | ~119 | ~240 | 97.2% |
| After Phase 4 (Complex) | ~111 | ~242 | 98.0% |
| Target | <100 | 245+ | 99%+ |

---

## Implementation Checklist Template

For each fix:
- [ ] Read relevant IODD test file to understand structure
- [ ] Verify model has necessary fields
- [ ] Create migration if schema changes needed
- [ ] Update parser extraction logic
- [ ] Update storage INSERT queries
- [ ] Update reconstruction output logic
- [ ] Test with sample file if available
- [ ] Commit with descriptive message
- [ ] Update session log
- [ ] Notify for re-import at milestones

---

## Test Files Available

`F:\github\GreenStack\test-data\iodd-files\`

Key files for testing:
- CX4 variants (for ArrayT count attribute)
- VEGAPULS (for Datatype SingleValue)
- FS1xxx-2UPN8 (outlier with many issues)
- SL-x-TRIO (outlier with Menu issues)

---

## Migration Strategy

**Migrations to Create**:
- 099: Add array_count to custom_datatypes
- 100: Add array fields to process_data
- (Additional migrations as needed for other fixes)

**Run Migrations After**: Each batch of schema changes

**Re-import Triggers**:
- After Phase 2 complete (new data needed for Fix #98)
- After Phase 3 complete
- After Phase 4 complete

---

## Session Flow

1. **START**: Notify to restart backend server
2. **WAIT**: User restarts server
3. **IMPORT**: User re-imports IODDs
4. **VERIFY**: Check stats show ~140 diffs resolved
5. **BEGIN**: Work through Phase 2, 3, 4 fixes
6. **COMMIT**: After each fix completion
7. **MILESTONE**: Notify for re-import after each phase
8. **LOG**: Update session log continuously
9. **COMPLETE**: Final summary with results

---

**Next Action**: Request backend server restart → Await re-import → Verify Fix #86-92 → Begin Phase 2
