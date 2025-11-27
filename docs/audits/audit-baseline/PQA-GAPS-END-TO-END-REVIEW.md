# PQA Gaps - End-to-End Process Review

**Date:** 2025-11-26
**Status:** Implementation Ready
**Goal:** Reach 100.00% PQA scores across all 6,639 devices

---

## Current State

- **Average Score**: 99.99%
- **Devices at 100.0%**: 0 (0%)
- **Total Diffs**: 1,392 (0.21 diffs/device)
- **Status**: EXCELLENT but not PERFECT

---

## PQA Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. PARSE (src/parsing/__init__.py)                             │
│    Extract data from original IODD XML                          │
│    → Create model objects (Parameter, ProcessData, etc.)        │
├─────────────────────────────────────────────────────────────────┤
│ 2. STORAGE (src/storage/__init__.py)                           │
│    Save model objects to database tables                        │
│    → INSERT into parameters, process_data, custom_datatypes     │
├─────────────────────────────────────────────────────────────────┤
│ 3. RECONSTRUCTION (src/utils/forensic_reconstruction_v2.py)    │
│    Query database and rebuild IODD XML from scratch             │
│    → Generate complete XML matching original structure          │
├─────────────────────────────────────────────────────────────────┤
│ 4. DIFF ANALYSIS (src/utils/pqa_diff_analyzer.py)             │
│    Compare original vs reconstructed XML                        │
│    → Identify missing/incorrect elements and attributes         │
├─────────────────────────────────────────────────────────────────┤
│ 5. SCORING (src/utils/pqa_diff_analyzer.py)                   │
│    Calculate quality metrics from diffs                         │
│    → Structural (40%) + Attribute (35%) + Value (25%)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Gap Analysis - Full Pipeline Trace

### GAP 1: SimpleDatatype@id Attribute ⚠️ HIGH PRIORITY

**Impact**: ~100 missing_attribute diffs across 6,639 devices
**Estimated Improvement**: +0.05% overall score

#### Original XML (Example)
```xml
<ProcessDataIn id="V_ProcessDataIn">
  <Datatype xsi:type="RecordT">
    <RecordItem subindex="1">
      <SimpleDatatype xsi:type="UIntegerT" id="DT_cc450541-02fc-4f2a-842e-8d2ce9f67a1e" bitLength="8"/>
    </RecordItem>
  </Datatype>
</ProcessDataIn>
```

#### Pipeline Trace

**1. PARSE** (src/parsing/__init__.py:1056-1143)
```python
# Line 1056: Finds SimpleDatatype element
simple_dt = record_item.find('.//iodd:SimpleDatatype', self.NAMESPACES)
if simple_dt is not None:
    item_type = simple_dt.get('{http://www.w3.org/2001/XMLSchema-instance}type', 'UIntegerT')
    item_bit_length = int(simple_dt.get('bitLength')) if simple_dt.get('bitLength') else None
    item_fixed_length = int(simple_dt.get('fixedLength')) if simple_dt.get('fixedLength') else None
    item_encoding = simple_dt.get('encoding')
    # ❌ MISSING: item_datatype_id = simple_dt.get('id')

# Line 1126-1143: Creates RecordItem model object
record_items.append(RecordItem(
    subindex=subindex,
    name=item_name,
    bit_offset=bit_offset,
    bit_length=item_bit_length,
    data_type=item_type,
    # ... other fields ...
    fixed_length=item_fixed_length,  # ✅ Extracted
    encoding=item_encoding,  # ✅ Extracted
    # ❌ MISSING: datatype_id=item_datatype_id
))
```

**Status**: ❌ **Parser NOT extracting `id` attribute**

**2. STORAGE** (src/storage/__init__.py - ProcessDataSaver)
```python
# Assuming parser extracts it, storage would save to:
# Table: process_data_record_items
# Column: datatype_id VARCHAR(100) ✅ EXISTS

# Current population:
# - process_data_record_items: 0 / 63,683 (0.00%)
# - parameter_record_items: 350 / 70,725 (0.49%) ← Some parameters have it
```

**Status**: ⚠️ **Column exists, but parser not providing data**

**3. RECONSTRUCTION** (src/utils/forensic_reconstruction_v2.py:802-811)
```python
# Line 802-811: Reconstruction code ALREADY handles this!
# PQA: Add optional SimpleDatatype attributes
fixed_len = item['fixed_length'] if 'fixed_length' in item.keys() else None
if fixed_len:
    simple_dt.set('fixedLength', str(fixed_len))
encoding = item['encoding'] if 'encoding' in item.keys() else None
if encoding:
    simple_dt.set('encoding', encoding)
dt_id = item['datatype_id'] if 'datatype_id' in item.keys() else None
if dt_id:
    simple_dt.set('id', dt_id)  # ✅ Reconstruction code READY
```

**Status**: ✅ **Reconstruction code already in place**

**4. DIFF ANALYSIS**
```
Expected: <SimpleDatatype xsi:type="UIntegerT" id="DT_cc450541-02fc-4f2a-842e-8d2ce9f67a1e" bitLength="8"/>
Actual:   <SimpleDatatype xsi:type="UIntegerT" bitLength="8"/>
Diff:     missing_attribute: id @ DT_cc450541-02fc-4f2a-842e-8d2ce9f67a1e
```

**Status**: ❌ **Diff correctly identifies missing attribute**

#### Root Cause
Parser does not extract `id` attribute from inline `<SimpleDatatype>` elements within RecordItems.

#### Fix Required
**File**: `src/parsing/__init__.py`
**Line**: ~1066 (after extracting encoding)
**Change**: Add extraction of `id` attribute

```python
# Line 1066: After extracting encoding
item_encoding = simple_dt.get('encoding')
# ✅ ADD THIS:
item_datatype_id = simple_dt.get('id')

# Line 1142: Pass to RecordItem constructor
record_items.append(RecordItem(
    # ... existing fields ...
    encoding=item_encoding,
    datatype_id=item_datatype_id,  # ✅ ADD THIS
))
```

**Verification**:
1. Import device with SimpleDatatype@id
2. Check database: `SELECT datatype_id FROM process_data_record_items WHERE datatype_id IS NOT NULL`
3. Trigger PQA analysis
4. Verify diff count drops

---

### GAP 2: ArrayT Count Attribute ⚠️ HIGH PRIORITY

**Impact**: 18 missing_attribute diffs
**Estimated Improvement**: +0.01% overall score

#### Original XML (Example)
```xml
<DatatypeCollection>
  <Datatype id="DT_Array123" xsi:type="ArrayT" count="16">
    <SimpleDatatype xsi:type="UIntegerT" bitLength="8"/>
  </Datatype>
</DatatypeCollection>
```

#### Pipeline Trace

**1. PARSE** (src/parsing/__init__.py:2316-2318)
```python
# Line 2316-2318: Parser EXTRACTS count attribute!
# PQA Fix #98: Extract ArrayT count attribute
count_attr = datatype_elem.get('count')
array_count = int(count_attr) if count_attr else None
```

**Status**: ✅ **Parser extracts count**

**2. STORAGE** (Need to verify CustomDatatypeSaver)
```python
# Table: custom_datatypes
# Column: array_count INTEGER ✅ EXISTS

# Current population:
# ArrayT datatypes: 25 total
# array_count populated: 0 (0.00%)
```

**Status**: ❌ **Column exists, but not being saved**

**3. RECONSTRUCTION** (src/utils/forensic_reconstruction_v2.py - need to find ArrayT reconstruction)

**Status**: ⚠️ **Need to verify reconstruction outputs count attribute**

#### Root Cause
Parser extracts `count` attribute, but storage layer not saving it to database.

#### Fix Required
1. **Storage**: Verify CustomDatatypeSaver saves `array_count` to database
2. **Reconstruction**: Verify IODDReconstructor outputs `count` attribute for ArrayT

---

### GAP 3: Empty EventCollection ⚠️ HIGH PRIORITY

**Impact**: 101 missing_element diffs
**Estimated Improvement**: +0.01% overall score

#### Original XML (Example)
```xml
<DeviceFunction>
  <EventCollection/>  <!-- Empty but present -->
</DeviceFunction>
```

#### Pipeline Trace

**1. PARSE** (src/parsing/__init__.py - _extract_events method)
```python
# Parser extracts Event and StdEventRef elements
# If EventCollection is empty, no rows inserted into events table
```

**Status**: ⚠️ **Parser doesn't track "empty but present" state**

**2. STORAGE**
```python
# Table: events
# If no events exist, table is empty for device

# NO FLAG to indicate "EventCollection was present but empty"
```

**Status**: ❌ **No way to distinguish "no EventCollection" from "empty EventCollection"**

**3. RECONSTRUCTION** (src/utils/forensic_reconstruction_v2.py:2153-2154)
```python
# Line 2153-2154: Returns None if no events
if not events:
    return None  # ❌ Loses information about empty EventCollection!
```

**Status**: ❌ **Reconstruction doesn't output empty EventCollection**

#### Root Cause
No database flag to track whether EventCollection element existed (even if empty).

#### Fix Required
1. **Database Migration**: Add `iodd_files.has_event_collection BOOLEAN`
2. **Parser**: Set flag when `<EventCollection>` element exists
3. **Storage**: Save flag to database
4. **Reconstruction**: Output empty `<EventCollection/>` when flag=TRUE and no events

---

### GAP 4: Config7 xsi:type Attribute ⚠️ MEDIUM PRIORITY

**Impact**: 22 missing_attribute diffs
**Estimated Improvement**: +0.002% overall score

#### Original XML (Example)
```xml
<CommNetworkProfile>
  <Test>
    <Config7 xsi:type="IOLinkTestConfig7T" offset="10" delay="500"/>
  </Test>
</CommNetworkProfile>
```

#### Pipeline Trace

**1. PARSE**
**Status**: ⚠️ **Need to verify if parser extracts xsi:type for Config7**

**2. STORAGE**
**Status**: ❌ **No column for config_xsi_type in test_configurations table**

**3. RECONSTRUCTION**
**Status**: ❌ **Reconstruction doesn't output xsi:type**

#### Root Cause
TestConfig7 xsi:type attribute not extracted/stored/reconstructed.

#### Fix Required
1. **Database Migration**: Add column (if needed)
2. **Parser**: Extract xsi:type
3. **Storage**: Save to database
4. **Reconstruction**: Output xsi:type attribute

---

### GAP 5: Missing StdVariableRef Elements ⚠️ MEDIUM PRIORITY

**Impact**: 84 missing_element diffs
**Estimated Improvement**: +0.01% overall score

#### Root Cause
**Status**: ⚠️ **NEEDS INVESTIGATION**

**Action Items**:
1. Query database to find devices with diff_type='missing_element' and xpath LIKE '%StdVariableRef%'
2. Get specific device IDs
3. Compare original XML to reconstructed XML manually
4. Identify which StdVariableRef elements are missing
5. Trace through parser → storage → reconstruction

---

### GAP 6: Missing DatatypeCollection Elements ⚠️ LOW PRIORITY

**Impact**: 74 missing_element diffs
**Estimated Improvement**: +0.01% overall score

#### Root Cause
**Status**: ⚠️ **NEEDS INVESTIGATION**

**Action Items**:
1. Query database to find devices with missing Datatype elements
2. Compare original to reconstructed
3. Identify why certain Datatype definitions aren't being saved/reconstructed

---

## Implementation Plan

### Phase 1: Quick Wins (4-6 hours)

**1.1 Fix SimpleDatatype@id Extraction** (2 hours)
- [ ] Modify parser to extract `id` attribute (1 line change)
- [ ] Pass to RecordItem constructor (1 line change)
- [ ] Test: Import device with SimpleDatatype@id
- [ ] Verify: Check database population
- [ ] PQA: Re-analyze and verify diff reduction

**1.2 Fix ArrayT Count Storage** (2 hours)
- [ ] Verify parser extraction (already done)
- [ ] Check CustomDatatypeSaver saves array_count
- [ ] Fix storage if needed
- [ ] Check reconstruction outputs count attribute
- [ ] Test: Import ArrayT device
- [ ] PQA: Verify scores improve

**1.3 Add Empty EventCollection Tracking** (2 hours)
- [ ] Create migration: `ALTER TABLE iodd_files ADD COLUMN has_event_collection BOOLEAN DEFAULT FALSE`
- [ ] Update parser to detect EventCollection element
- [ ] Update IODDFileSaver to save flag
- [ ] Update reconstruction to output empty EventCollection when flag=TRUE
- [ ] Test and verify

### Phase 2: Investigations (4-6 hours)

**2.1 Config7 xsi:type** (2 hours)
- [ ] Trace Config7 parsing
- [ ] Add storage column if needed
- [ ] Update reconstruction

**2.2 StdVariableRef Investigation** (2 hours)
- [ ] Identify specific missing elements
- [ ] Trace root cause
- [ ] Implement fix

**2.3 Missing Datatype Investigation** (2 hours)
- [ ] Identify specific missing datatypes
- [ ] Trace root cause
- [ ] Implement fix

### Phase 3: Verification (2 hours)

**3.1 Full PQA Re-Analysis**
- [ ] Delete all PQA metrics: `DELETE FROM pqa_quality_metrics`
- [ ] Trigger full re-analysis on all 6,639 devices
- [ ] Wait for completion (~30 minutes)

**3.2 Results Validation**
- [ ] Run analysis script: `python analyze_pqa_results.py`
- [ ] Verify average score ≥ 99.995%
- [ ] Check diff counts reduced
- [ ] Document remaining gaps (if any)

---

## Success Criteria

✅ **Minimum Success** (Phase 1 only):
- Average score ≥ 99.995%
- SimpleDatatype@id diffs eliminated (~100 diffs)
- ArrayT count diffs eliminated (18 diffs)
- EventCollection diffs eliminated (101 diffs)
- **Total reduction**: ~220 diffs → **1,392 → 1,172** (16% reduction)

🎯 **Full Success** (Phases 1-3):
- Average score = 100.00% (or ≥ 99.998%)
- Total diffs < 50 across all 6,639 devices
- All HIGH severity diffs eliminated
- Path to 100% documented

---

## Risk Assessment

**Phase 1 Risks**: **LOW**
- Changes are surgical (1-2 line modifications)
- Reconstruction code already supports these attributes
- Database columns already exist
- No schema migrations needed (except EventCollection flag)

**Phase 2 Risks**: **MEDIUM**
- Requires investigation to identify root causes
- May uncover deeper parser issues
- Fixes depend on what is discovered

**Mitigation**:
- Test each fix independently with single device
- Verify database before PQA re-analysis
- Keep backup of greenstack.db before re-analysis

---

## Notes

1. **Reconstruction code is excellent**: Most attributes are already handled in reconstruction, the problem is the parser not extracting them.

2. **Database schema is complete**: Columns exist for most missing attributes, they're just not populated.

3. **PQA system is honest**: It correctly identifies every missing attribute, which is why we can fix them systematically.

4. **Incremental fixes are safe**: Each gap can be fixed independently and tested before moving to the next.

---

**Next Step**: Begin Phase 1.1 - Fix SimpleDatatype@id extraction
