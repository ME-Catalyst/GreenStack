# PQA Analysis: Duplicate SingleValue Entries

## Problem Summary

Analysis of device 550 revealed DUPLICATE SingleValue entries in both `parameter_single_values` and `record_item_single_values` tables, causing incorrect PQA scores.

## Evidence

### Database Query Results

**Parameter 14931 (V_Configuration, RecordT type):**
- parameter_single_values table contains 19 entries (wrong - should have ZERO)
- These are ALL the SingleValues from ALL RecordItems incorrectly extracted at parameter level

**RecordItem 19087 (subindex=1):**
```
id=9877: value=false, textId=TI_Configuration_LED_colors_normal, xsi_type=BooleanValueT
id=9878: value=true, textId=TI_Configuration_LED_colors_inverted, xsi_type=BooleanValueT
id=9905: value=false, textId=TN_Configuration_LED_colors_normal, xsi_type=None
id=9906: value=true, textId=TN_Configuration_LED_colors_inverted, xsi_type=None
```

### Original IODD XML

```xml
<RecordItem subindex="1" bitOffset="0">
    <SimpleDatatype xsi:type="BooleanT">
        <SingleValue value="false">
            <Name textId="TN_Configuration_LED_colors_normal" />
        </SingleValue>
        <SingleValue value="true">
            <Name textId="TN_Configuration_LED_colors_inverted" />
        </SingleValue>
    </SimpleDatatype>
    <Name textId="TN_Configuration_LED_colors" />
</RecordItem>
```

**Expected:** Only 2 entries in record_item_single_values:
- value=false, textId=TN_Configuration_LED_colors_normal, xsi_type=None
- value=true, textId=TN_Configuration_LED_colors_inverted, xsi_type=None

**Actual:** 4 entries (2x duplicates with incorrect TI_ prefix and xsi_type)

## Root Causes

### Issue #1: Parameter-Level Extraction Bug
**Location:** `src/parsing/__init__.py` line 701

```python
for idx, single_val in enumerate(datatype_elem.findall('.//iodd:SingleValue', self.NAMESPACES)):
```

**Problem:** The `.//` descendant selector finds ALL SingleValue elements anywhere in the subtree, including those inside RecordItem/SimpleDatatype elements. For RecordT types, this incorrectly extracts RecordItem SingleValues as parameter-level SingleValues.

**Impact:** All RecordItem SingleValues are ALSO saved to `parameter_single_values` table for RecordT parameters.

### Issue #2: Duplicate RecordItem SingleValues with TI_ Prefix
**Location:** Unknown (investigation ongoing)

**Problem:** RecordItem SingleValues are being extracted/saved TWICE:
1. First pass: Generates TI_ prefix entries with xsi_type=BooleanValueT (incorrect)
2. Second pass: Generates TN_ prefix entries with xsi_type=None (correct but creates duplicates)

**Theories:**
- Text ID manipulation during extraction
- Multiple code paths extracting the same SingleValues
- Incorrect text resolution fallback logic

## Fix Strategy

### Fix #1: Change `.//` to `./` for direct children only

**File:** `src/parsing/__init__.py` line 701

Change from:
```python
for idx, single_val in enumerate(datatype_elem.findall('.//iodd:SingleValue', self.NAMESPACES)):
```

To:
```python
# Only extract direct SingleValue children (not those inside RecordItems)
for idx, single_val in enumerate(datatype_elem.findall('iodd:SingleValue', self.NAMESPACES)):
```

This ensures that for RecordT types, only direct Datatype/SingleValue children are extracted (which is typically none), and RecordItem SingleValues are ONLY extracted via the RecordItem extraction logic.

### Fix #2: Investigate TI_ prefix generation

Need to trace through code to find where TI_ prefix is being generated and remove that code path.

## Impact Assessment

**Affected Devices:** Analysis shows:
- 547 occurrences of "incorrect Name@textId"
- 541 occurrences of "incorrect SingleValue@value"

These are likely ALL caused by duplicate SingleValues in RecordT parameters.

## Next Steps

1. Apply Fix #1 (change `.//` to `./`)
2. Find and remove TI_ generation logic
3. Re-import affected devices
4. Run PQA re-analysis
5. Verify all duplicates are eliminated
