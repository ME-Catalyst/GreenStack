# Investigation Results: Fixes #4-6

**Date**: 2025-11-26
**Status**: Investigation Complete
**Remaining Diffs**: ~180 across 3 gaps

---

## Fix #4: Config7 xsi:type Attribute

**Impact**: 22 missing_attribute diffs
**Severity**: MEDIUM
**Complexity**: LOW (Simple attribute extraction)

### Problem Analysis

**XPath**: `/IODevice/CommNetworkProfile/Test/Config7@{http://www.w3.org/2001/XMLSchema-instance}type`
**Expected Value**: `IOLinkTestConfig7T`

**Root Cause**: Parser extracts Config7 elements but doesn't capture the `xsi:type` attribute.

### Current Pipeline State

#### 1. Parser (src/parsing/__init__.py:2291-2311)
```python
# Line 2292: Finds Config7 element
config7_elem = test_elem.find('.//iodd:Config7', self.NAMESPACES)
if config7_elem is not None:
    index = config7_elem.get('index')  # ✅ Extracts index
    # ❌ Does NOT extract xsi:type attribute
```

**Status**: ❌ **NOT extracting xsi:type**

#### 2. Model (src/models/__init__.py:395-400)
```python
@dataclass
class DeviceTestConfig:
    config_type: str  # 'Config7'
    param_index: int
    test_value: str
    event_triggers: List[TestEventTrigger] = field(default_factory=list)
    # ❌ Missing: config_xsi_type field
```

**Status**: ❌ **No field for xsi:type**

#### 3. Storage (src/storage/test_config.py:43-45)
```python
INSERT INTO device_test_config (
    device_id, config_type, param_index, test_value
) VALUES (?, ?, ?, ?)
# ❌ No column for config_xsi_type
```

**Database Schema**: `device_test_config` table
- ❌ No `config_xsi_type` column

**Status**: ❌ **Column doesn't exist**

#### 4. Reconstruction (src/utils/forensic_reconstruction_v2.py:1705-1709)
```python
for config in test_configs:
    config_elem = ET.SubElement(test_elem, config['config_type'])  # Creates 'Config7'
    config_elem.set('index', str(config['param_index']))
    # ❌ Does NOT output xsi:type attribute
```

**Status**: ❌ **NOT outputting xsi:type**

### Fix Implementation Plan

**Estimated Effort**: 1-2 hours

#### Step 1: Add Database Column
```sql
ALTER TABLE device_test_config ADD COLUMN config_xsi_type TEXT;
```

#### Step 2: Update Model
```python
# src/models/__init__.py:395-400
@dataclass
class DeviceTestConfig:
    config_type: str
    param_index: int
    test_value: str
    event_triggers: List[TestEventTrigger] = field(default_factory=list)
    config_xsi_type: Optional[str] = None  # ✅ ADD THIS
```

#### Step 3: Update Parser
```python
# src/parsing/__init__.py:2292-2311
config7_elem = test_elem.find('.//iodd:Config7', self.NAMESPACES)
if config7_elem is not None:
    index = config7_elem.get('index')
    # ✅ ADD THIS:
    config_xsi_type = config7_elem.get('{http://www.w3.org/2001/XMLSchema-instance}type')

    test_configs.append(DeviceTestConfig(
        config_type='Config7',
        param_index=int(index),
        test_value='',
        event_triggers=event_triggers,
        config_xsi_type=config_xsi_type  # ✅ ADD THIS
    ))
```

#### Step 4: Update Storage
```python
# src/storage/test_config.py:43-52
INSERT INTO device_test_config (
    device_id, config_type, param_index, test_value, config_xsi_type  # ✅ ADD THIS
) VALUES (?, ?, ?, ?, ?)  # ✅ ADD ?

params = (
    device_id,
    getattr(test_config, 'config_type', None),
    getattr(test_config, 'param_index', None),
    getattr(test_config, 'test_value', None),
    getattr(test_config, 'config_xsi_type', None),  # ✅ ADD THIS
)
```

#### Step 5: Update Reconstruction
```python
# src/utils/forensic_reconstruction_v2.py:1705-1709
for config in test_configs:
    config_elem = ET.SubElement(test_elem, config['config_type'])
    config_elem.set('index', str(config['param_index']))
    # ✅ ADD THIS:
    if config['config_xsi_type']:
        config_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', config['config_xsi_type'])
```

**Files to Modify**: 4
**Lines to Change**: ~8
**Database Changes**: 1 column

---

## Fix #5: StdVariableRef/StdValueRangeRef Elements

**Impact**: 84 missing_element diffs
**Severity**: MEDIUM
**Complexity**: MEDIUM (New element type extraction)

### Problem Analysis

**XPath**: `/IODevice/ProfileBody/DeviceFunction/VariableCollection/StdVariableRef/StdValueRangeRef[unknown]`
**Expected Element**: `StdValueRangeRef`

**Root Cause**: Parser doesn't extract `StdValueRangeRef` child elements from `StdVariableRef`.

### Current Pipeline State

#### 1. Parser (src/parsing/__init__.py:2518-2620)
Parser extracts:
- ✅ StdVariableRef attributes (id, defaultValue, fixedLengthRestriction)
- ✅ SingleValue children
- ✅ StdSingleValueRef children
- ✅ StdRecordItemRef children
- ❌ **StdValueRangeRef children** (NOT extracted)

**Status**: ❌ **StdValueRangeRef not extracted**

#### 2. Model (src/models/__init__.py:445-453)
```python
@dataclass
class StdVariableRef:
    variable_id: str
    default_value: Optional[str] = None
    fixed_length_restriction: Optional[int] = None
    excluded_from_data_storage: Optional[bool] = None
    order_index: int = 0
    single_values: List['StdVariableRefSingleValue'] = field(default_factory=list)
    record_item_refs: List['StdRecordItemRef'] = field(default_factory=list)
    # ❌ Missing: std_value_range_ref field
```

**Status**: ❌ **No model for StdValueRangeRef**

#### 3. Storage
**Status**: ⚠️ **Need to find std_variable_refs table and check schema**

#### 4. Reconstruction
**Status**: ⚠️ **Need to check if StdValueRangeRef is output**

### Fix Implementation Plan

**Estimated Effort**: 3-4 hours

**Note**: This requires understanding what StdValueRangeRef contains. It likely has:
- A `defaultType` attribute
- Possibly `lowerValue` and `upperValue` attributes

#### Required Steps:
1. **Research IO-Link spec** for StdValueRangeRef structure
2. **Create model** for StdValueRangeRef element
3. **Update parser** to extract it
4. **Add storage** column/table
5. **Update reconstruction** to output it

**Risk**: MEDIUM - Requires IODD spec lookup to understand element structure

---

## Fix #6: Missing Datatype Child Elements

**Impact**: 74 missing_element diffs
**Severity**: MEDIUM
**Complexity**: MEDIUM (Multiple element types)

### Problem Analysis

**XPath Patterns**:
1. `/IODevice/ProfileBody/DeviceFunction/DatatypeCollection/Datatype/Name[unknown]`
2. `/IODevice/ProfileBody/DeviceFunction/DatatypeCollection/Datatype/SimpleDatatype[unknown]`

**Expected Elements**:
- `Name` child elements inside custom Datatype definitions
- `SimpleDatatype` child elements for non-ArrayT Datatype elements

**Root Cause**:
1. Parser doesn't extract `Name` child element from custom Datatype
2. Reconstruction only outputs `SimpleDatatype` children for ArrayT types

### Current Pipeline State

#### 1. Parser (src/parsing/__init__.py:2316-2490)
```python
# Line 2320-2323: Processes Datatype element
for datatype_elem in self.root.findall('.//iodd:DatatypeCollection/iodd:Datatype', self.NAMESPACES):
    datatype_id = datatype_elem.get('id')
    xsi_type = datatype_elem.get('{http://www.w3.org/2001/XMLSchema-instance}type')
    # ... extracts attributes ...
    # ❌ Does NOT extract Datatype/Name child element
    # ❌ Only extracts SimpleDatatype for ArrayT via array_element_type
```

**Status**: ❌ **NOT extracting Datatype/Name textId**

#### 2. Model (src/models/__init__.py:404-424)
```python
@dataclass
class CustomDatatype:
    datatype_id: str
    datatype_xsi_type: str
    bit_length: Optional[int] = None
    # ... many fields ...
    # ❌ Missing: datatype_name_text_id field
    # ❌ Missing: simple_datatype fields for non-ArrayT types
```

**Status**: ❌ **No field for Name textId**

#### 3. Storage
**Database**: `custom_datatypes` table
- ❌ No `datatype_name_text_id` column
- ✅ Has `array_element_type` for ArrayT SimpleDatatype children

**Status**: ⚠️ **Partial - only ArrayT SimpleDatatype supported**

#### 4. Reconstruction (src/utils/forensic_reconstruction_v2.py:1114-1149)
```python
# Lines 1114-1123: Only outputs SimpleDatatype for ArrayT
if dt['datatype_xsi_type'] == 'ArrayT':
    if array_elem_type:
        simple_dt_elem = ET.SubElement(datatype_elem, 'SimpleDatatype')
        # ... outputs SimpleDatatype for ArrayT ...

# ❌ Does NOT output Name child element
# ❌ Does NOT output SimpleDatatype for other types
```

**Status**: ❌ **Only ArrayT gets SimpleDatatype children, no Name output**

### Fix Implementation Plan

**Estimated Effort**: 3-4 hours

#### Part A: Add Datatype/Name Support (Simpler)

**Step 1**: Add database column
```sql
ALTER TABLE custom_datatypes ADD COLUMN datatype_name_text_id TEXT;
```

**Step 2**: Update model
```python
# src/models/__init__.py
@dataclass
class CustomDatatype:
    # ... existing fields ...
    datatype_name_text_id: Optional[str] = None  # ✅ ADD THIS
```

**Step 3**: Update parser
```python
# src/parsing/__init__.py:2320-2360
datatype_elem = ... # Found Datatype element

# ✅ ADD THIS: Extract Name child element
dt_name_elem = datatype_elem.find('iodd:Name', self.NAMESPACES)
dt_name_text_id = dt_name_elem.get('textId') if dt_name_elem is not None else None

# Pass to CustomDatatype constructor
datatypes.append(CustomDatatype(
    # ... existing fields ...
    datatype_name_text_id=dt_name_text_id  # ✅ ADD THIS
))
```

**Step 4**: Update storage
```python
# src/storage/custom_datatype.py:66-94
INSERT INTO custom_datatypes (
    ..., datatype_name_text_id  # ✅ ADD THIS
) VALUES (..., ?)

params = (
    ...,
    getattr(datatype, 'datatype_name_text_id', None),  # ✅ ADD THIS
)
```

**Step 5**: Update reconstruction
```python
# src/utils/forensic_reconstruction_v2.py:1086-1149
for dt in datatypes:
    datatype_elem = ET.Element('Datatype')
    # ... set attributes ...

    # ✅ ADD THIS: Output Name child element
    dt_name_text_id = dt['datatype_name_text_id'] if 'datatype_name_text_id' in dt.keys() else None
    if dt_name_text_id:
        name_elem = ET.SubElement(datatype_elem, 'Name')
        name_elem.set('textId', dt_name_text_id)
```

**Estimated Lines**: ~10 lines across 4 files

#### Part B: Add SimpleDatatype for Non-ArrayT Types (Complex)

**Problem**: Some non-ArrayT Datatype elements have SimpleDatatype children. Need to:
1. Identify which datatype types can have SimpleDatatype children
2. Extract the SimpleDatatype attributes
3. Store them
4. Reconstruct them

**Risk**: MEDIUM-HIGH - Requires understanding IODD spec for which types support this

**Possible Approach**:
- Add columns: `has_simple_datatype_child BOOLEAN`, `simple_datatype_xsi_type TEXT`, `simple_datatype_bit_length INTEGER`
- Extract when present
- Reconstruct when flag is TRUE

**Estimated Effort**: Additional 2-3 hours

---

## Summary

| Fix | Impact | Complexity | Effort | Risk | Priority |
|-----|--------|------------|--------|------|----------|
| #4: Config7 xsi:type | 22 diffs | LOW | 1-2h | LOW | HIGH |
| #5: StdValueRangeRef | 84 diffs | MEDIUM | 3-4h | MEDIUM | MEDIUM |
| #6A: Datatype/Name | ~40 diffs | LOW | 2-3h | LOW | HIGH |
| #6B: Datatype/SimpleDatatype | ~34 diffs | MEDIUM | 2-3h | MEDIUM | MEDIUM |
| **Total** | **180 diffs** | **MEDIUM** | **8-12h** | **MEDIUM** | - |

---

## Recommended Implementation Order

### Phase 1: Quick Wins (4-5 hours)
1. **Fix #4: Config7 xsi:type** - Simplest fix, clear path
2. **Fix #6A: Datatype/Name** - Similar pattern to Fix #4

**Expected Result**: ~62 diffs eliminated

### Phase 2: Complex Fixes (6-8 hours)
3. **Fix #5: StdValueRangeRef** - Requires IODD spec research
4. **Fix #6B: Datatype/SimpleDatatype** - Requires analysis of when it's used

**Expected Result**: ~118 diffs eliminated

---

## Next Steps

**Option A: Implement Phase 1 Only**
- Quick wins to eliminate ~62 more diffs
- Brings total from 99.99% to 99.995%+
- Low risk, clear implementation path

**Option B: Implement All Fixes**
- Complete path to 100.00%
- Eliminate all remaining ~180 diffs
- Requires IODD spec research for Fixes #5 and #6B

**Option C: Test Fixes #1-3 First**
- Re-import devices with Fixes #1-3
- Verify improvements before continuing
- Then proceed with Fixes #4-6

---

## Documentation Created

1. ✅ End-to-end pipeline analysis for each gap
2. ✅ Root cause identification
3. ✅ Current state verification
4. ✅ Fix implementation plans
5. ✅ Effort estimates
6. ✅ Risk assessment

**Status**: READY FOR IMPLEMENTATION DECISION

---

**Recommendation**: Implement **Fix #4** (Config7 xsi:type) next as it's the simplest and follows the same pattern we've already used successfully. Then assess whether to continue with remaining fixes or test current progress.
