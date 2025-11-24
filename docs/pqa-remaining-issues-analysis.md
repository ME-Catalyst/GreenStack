# PQA Remaining Issues - Comprehensive Analysis
**Date**: 2025-11-24
**Total Files**: 247
**Perfect (100%)**: 229 (92.7%)
**Total Remaining Diffs**: 299

---

## ⚠️ IMPORTANT: Backend Server Restart Required

**The Fix #86-92 changes have NOT been applied yet** because the backend server was not restarted after the code changes were pushed. The statistics show the same 299 diffs as before the fixes.

**Action Required**: Restart the backend server, then re-import to see the impact of Fix #86-92 (~140 diffs should be resolved).

---

## 📊 Current Issue Breakdown

### **Category 1: UserInterface Menu Issues** (~144 diffs - Should be FIXED by #86-92)
These issues should be resolved once the backend server is restarted and re-import is performed:

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| Fix #86 | 48 | incorrect_attribute | Menu/VariableRef@variableId |
| Fix #87 | 40 | incorrect_attribute | Menu/RecordItemRef@subindex |
| Fix #88 | 33 | incorrect_attribute | Menu/RecordItemRef@variableId |
| Fix #89 | 17 | incorrect_attribute | Menu/RecordItemRef@unitCode |
| Fix #92 | 6 | incorrect_attribute | Menu/MenuRef@menuId |

**Status**: ✅ FIXED in code (commit 6d171c2), awaiting server restart + re-import

---

### **Category 2: Menu Missing Attributes** (~21 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #93a | 3 | missing_attribute | Menu/RecordItemRef@displayFormat |
| #93b | 3 | missing_attribute | Menu/RecordItemRef@gradient |
| #93c | 3 | missing_attribute | Menu/RecordItemRef@offset |
| #93d | 3 | missing_attribute | Menu/RecordItemRef@unitCode |
| #93e | 3 | missing_attribute | Menu/VariableRef@accessRightRestriction |
| #93f | 3 | missing_attribute | Menu/VariableRef@displayFormat |
| #93g | 3 | missing_attribute | Menu/VariableRef@unitCode |
| #93h | 2 | missing_attribute | Menu/VariableRef@gradient |
| #93i | 2 | missing_attribute | Menu/VariableRef@offset |

**Root Cause**: Parser not extracting certain optional attributes from Menu items
**Priority**: Medium (spread across multiple files)
**Complexity**: Low - Add attribute extraction to parser

---

### **Category 3: Menu Incorrect Attributes** (~8 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #95a | 3 | incorrect_attribute | Menu/MenuRef/Condition@value |
| #95b | 3 | incorrect_attribute | Menu/VariableRef/Button/Description@textId |
| #95c | 3 | incorrect_attribute | Menu/VariableRef/Button@buttonValue |
| #95d | 2 | incorrect_attribute | Menu/MenuRef/Condition@variableId |
| #95e | 2 | incorrect_attribute | Menu/VariableRef/Button/ActionStartedMessage@textId |

**Root Cause**: Likely ID lookup/mapping issues in Button/Condition reconstruction
**Priority**: Low (3 files affected)
**Complexity**: Medium

---

### **Category 4: StdVariableRef SingleValue Issues** (12 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #90a | 6 | incorrect_attribute | StdVariableRef/SingleValue/Name@textId |
| #90b | 6 | incorrect_attribute | StdVariableRef/SingleValue@value |

**Root Cause**: Values/textIds getting misaligned in reconstruction
**Priority**: Low (**all 12 diffs in outlier file FS1xxx-2UPN8**)
**Complexity**: Medium - Ordering issue

---

### **Category 5: DatatypeCollection Missing Elements** (10 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #91a | 4 | missing_element | VariableCollection/Variable/Datatype/Name |
| #91b | 3 | missing_element | DatatypeCollection/Datatype/SimpleDatatype |
| #91c | 3 | missing_element | DatatypeCollection/Datatype/SingleValue |

**Root Cause**: Custom Datatype child elements not being extracted/reconstructed
**Files Affected**:
- #91a: 4 files (Variable/Datatype/Name)
- #91b: 3 files (CX4_v12, CX4_v24, CX4_v32)
- #91c: 3 files (VEGAPULS 42 IO-Link - all 3 diffs in this file)

**Priority**: Medium
**Complexity**: Medium - Requires parser + reconstruction updates

---

### **Category 6: Menu Missing Elements** (4 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #96a | 3 | missing_element | Menu/VariableRef/Button |
| #96b | 1 | extra_element | Menu/VariableRef/Button |

**Root Cause**: Button elements not being properly extracted or incorrectly added
**Priority**: Low (net 2 issues)
**Complexity**: Low

---

### **Category 7: ProcessData/Connection Missing Elements** (4 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #97a | 2 | missing_element | CommNetworkProfile/.../Connection/ProductRef |
| #97b | 2 | missing_element | ProcessData/.../Datatype/RecordItem/SimpleDatatype/Name |

**Root Cause**: ProductRef and nested RecordItem/Name not being reconstructed
**Priority**: Low (2 files each)
**Complexity**: Medium

---

### **Category 8: DatatypeCollection Missing Attributes** (3 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #98 | 3 | missing_attribute | DatatypeCollection/Datatype@count |

**Root Cause**: ArrayT datatype @count attribute not being extracted
**Files Affected**: 3 files
**Priority**: Low
**Complexity**: Low

---

### **Category 9: schemaLocation Issues** (2 diffs)

| Issue | Count | Type | XPath |
|-------|-------|------|-------|
| #94 | 2 | incorrect_attribute | IODevice@xsi:schemaLocation |

**Root Cause**: Namespace/XSD mapping incorrect for specific IODD versions
**Priority**: Low
**Complexity**: Low - Check SCHEMA_CONFIGS

---

## 🎯 Outlier Files Analysis

### **SL-x-TRIO IOLINK** (Vendor 1270, Device 16)
- **156 diffs** (52% of all diffs)
- **Score**: 96.52%
- **Issues**: Primarily Menu-related (should be mostly fixed by #86-92)

### **FS1xxx-2UPN8** (Vendor 317, Device 196608)
- **110 diffs** (37% of all diffs)
- **Score**: 95.80%
- **Issues**: Mixed (Menu + StdVariableRef + other)

**Combined**: These 2 files account for **266 diffs (89% of total!)**

---

## 📋 Recommended Fix Order (Next Session)

### **Phase 1: Verify Fix #86-92 Applied** (Expected: -140 diffs)
1. Restart backend server
2. Re-import IODDs
3. Verify Menu issues resolved
4. Check if outlier files improved

### **Phase 2: Quick Wins** (Expected: -30 diffs)
1. **Fix #93**: Menu missing attributes (21 diffs) - Low complexity
2. **Fix #98**: Datatype@count attribute (3 diffs) - Low complexity
3. **Fix #96**: Menu/Button elements (4 diffs) - Low complexity
4. **Fix #94**: schemaLocation (2 diffs) - Low complexity

### **Phase 3: Medium Complexity** (Expected: -10 diffs)
1. **Fix #91**: DatatypeCollection missing elements (10 diffs)
   - Subtask #91a: Variable/Datatype/Name (4 diffs)
   - Subtask #91b: Datatype/SimpleDatatype (3 diffs)
   - Subtask #91c: Datatype/SingleValue (3 diffs)

### **Phase 4: Complex Issues** (Expected: -8 diffs)
1. **Fix #95**: Menu incorrect attributes (8 diffs) - Condition/Button textId issues

### **Phase 5: Outlier-Specific** (Deferred if low ROI)
1. **Fix #90**: StdVariableRef SingleValue (12 diffs - all in FS1xxx-2UPN8)
2. **Fix #97**: Connection/ProcessData missing elements (4 diffs)

---

## 📈 Expected Results After All Fixes

| Metric | Current | After Phase 1 | After Phase 2-5 |
|--------|---------|---------------|-----------------|
| Total Diffs | 299 | ~159 | ~107 |
| Perfect (100%) | 229 | ~235 | ~240+ |
| Near Perfect (99-100%) | 16 | ~10 | ~5 |
| Below 98% | 2 | 2 | 1-2 |

**Target**: Achieve **240+ perfect files (97%+)** with **<110 total diffs** across all 247 files.

---

## 🔧 Implementation Checklist

For each fix:
- [ ] Investigate root cause with sample data
- [ ] Update parser (`src/parsing/__init__.py`) if needed
- [ ] Update model (`src/models/__init__.py`) if needed
- [ ] Update storage (`src/storage/*.py`) if needed
- [ ] Create migration if schema changes needed
- [ ] Update reconstruction (`src/utils/forensic_reconstruction_v2.py`) if needed
- [ ] Commit with descriptive message
- [ ] Update session log
- [ ] Notify for re-import when milestone reached

---

## 📝 Notes

1. **Always restart backend server** after code changes before re-importing
2. **Commit after each fix** - don't batch multiple fixes
3. **Create migrations** for any schema changes
4. **Update session log** with details of each fix
5. **Test with sample files** from `F:\github\GreenStack\test-data\iodd-files`
6. **Focus on high-impact fixes first** (those affecting multiple files)
7. **Consider ROI** - don't spend hours on issues affecting 1-2 outlier files

---

**Next Action**: Restart backend server → Re-import → Verify Fix #86-92 impact → Continue with Phase 2 fixes
