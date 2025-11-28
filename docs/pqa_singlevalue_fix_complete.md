# PQA SingleValue Duplicate Fix - COMPLETED

## Problem Statement

PQA analysis revealed duplicate SingleValue entries causing incorrect scores:
- 547 occurrences of "incorrect Name@textId"
- 541 occurrences of "incorrect SingleValue@value"
- RecordT parameters incorrectly extracting parameter-level SingleValues (should be ZERO)
- RecordItem SingleValues appearing with duplicate TI_ and TN_ prefixes

## Root Cause

**File:** `src/parsing/__init__.py` line 702 (in `_parse_variable_datatype()` method)

**Bug:** Used `.//iodd:SingleValue` which finds ALL descendant SingleValue elements, including those inside RecordItem/SimpleDatatype elements.

**Impact:** For RecordT datatypes with inline RecordItems, ALL RecordItem SingleValues were incorrectly extracted as parameter-level SingleValues.

## Solution

**Changed line 702 from:**
```python
for idx, single_val in enumerate(datatype_elem.findall('.//iodd:SingleValue', self.NAMESPACES)):
```

**To:**
```python
# PQA Fix: Use direct children only (not .// which finds descendants including RecordItem SingleValues)
for idx, single_val in enumerate(datatype_elem.findall('iodd:SingleValue', self.NAMESPACES)):
```

**Explanation:**
- `.//iodd:SingleValue` finds ALL descendants (including nested elements)
- `iodd:SingleValue` finds only direct children
- For RecordT datatypes, the Datatype element has NO direct SingleValue children
- All SingleValues are inside RecordItem/SimpleDatatype elements
- Therefore, RecordT parameters correctly get ZERO parameter-level SingleValues

## Verification

**Test:** `test_singlevalue_fix.py`

**Results (with forced re-import):**
```
=== Parameter SingleValues ===
[OK] V_Configuration has 0 parameter-level SingleValues (expected 0)

=== RecordItem SingleValues ===
No duplicates found

[SUCCESS] FIX VERIFIED: No duplicates found!
```

## Impact Assessment

**Devices Affected:** All devices with RecordT parameters containing inline RecordItems with SingleValues

**Expected PQA Score Improvement:**
- Eliminates 547 "incorrect Name@textId" issues
- Eliminates 541 "incorrect SingleValue@value" issues
- Should bring majority of affected devices to 100% PQA scores

## Next Steps

1. ✅ **COMPLETED:** Fix parsing code (line 702)
2. **PENDING:** Re-import all affected devices (devices with RecordT parameters)
3. **PENDING:** Run PQA re-analysis on all devices
4. **PENDING:** Verify PQA scores improved to 100%

## Files Modified

1. `src/parsing/__init__.py` - Line 702: Changed `.//iodd:SingleValue` to `iodd:SingleValue`

## Migration Notes

**For existing database:**
- All devices with RecordT parameters need to be re-imported to apply the fix
- The fix only affects parsing - no database schema changes required
- No migration script needed - just re-import affected IODDs
