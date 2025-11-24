# Session Progress Log

## Current Date: 2025-11-21

---

## FIXES IN PROGRESS (Session 2025-11-21)

### Fix #1: RecordItem/Description Missing (513 issues) - COMMITTED

**Commit**: `2838891` feat(pqa): add RecordItem/Description extraction and reconstruction

**Problem**: RecordItem/Description elements were not being extracted, stored, or reconstructed for:
- VariableCollection: 396 issues
- DatatypeCollection: 76 issues
- ProcessDataCollection: 41 issues

**Changes Made**:
1. `src/models/__init__.py` - Added `description` and `description_text_id` fields to RecordItem model
2. `src/parsing/__init__.py` - Extract Description from RecordItems in:
   - `_extract_variable_record_items()` (Variable RecordItems)
   - `_extract_custom_datatypes()` (Custom Datatype RecordItems)
   - ProcessDataIn/Out parsing (Process Data RecordItems)
3. `src/storage/parameter.py` - Save description_text_id for parameter_record_items
4. `src/storage/custom_datatype.py` - Save description_text_id for custom_datatype_record_items
5. `src/storage/process_data.py` - Save description_text_id for process_data_record_items
6. `src/utils/forensic_reconstruction_v2.py` - Generate Description elements in all three contexts
7. `alembic/versions/046_add_record_item_description.py` - Add description_text_id columns

**Expected Impact**: ~513 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #2: SimpleDatatype/SingleValue Missing (822 issues) - COMMITTED

**Commit**: `e84a2a7` feat(pqa): add SingleValue reconstruction for ProcessData and ArrayT Variables

**Problem**: SingleValue elements inside SimpleDatatype were not being reconstructed for:
- ProcessDataCollection: 487 issues
- VariableCollection (ArrayT): 259 issues
- DatatypeCollection: 64 issues (deferred)

**Changes Made**:
1. `src/parsing/__init__.py` - Store text_id for ProcessData RecordItem SingleValues
2. `src/storage/process_data.py` - Save name_text_id for process_data_single_values
3. `src/utils/forensic_reconstruction_v2.py`:
   - Add SingleValue generation in `_add_process_data_record_items()`
   - Add SingleValue generation for ArrayT Variable SimpleDatatype
4. `alembic/versions/047_add_process_data_single_value_text_id.py` - Add name_text_id column

**Expected Impact**: ~746 of 822 issues resolved (requires re-import)

**Remaining Work**: DatatypeCollection/RecordItem/SimpleDatatype/SingleValue (~64 issues)
requires new table `custom_datatype_record_item_single_values`

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #3: Name@textId Incorrect (682 issues) - PARTIALLY FIXED

**Commit**: `6da5958` fix(pqa): use direct child selectors for RecordItem Name/Description

**Problem**: RecordItem Name@textId was incorrect because parser used `.//iodd:Name`
which found SingleValue/Name descendants instead of direct child Name element.

**Changes Made**:
1. `src/parsing/__init__.py` - Changed from `.//iodd:Name` to `iodd:Name` (direct child) in:
   - ProcessDataIn/Out RecordItem parsing
   - Custom Datatype RecordItem parsing
   - Also fixed Description selectors

**Expected Impact**: ~264 of 682 issues resolved (ProcessData + DatatypeCollection RecordItems)

**Remaining Issues**:
- Variable/Name (181) - may need investigation
- SingleValue/Name (97) - text_id fallback issues
- DeviceName/VendorText etc (221) - use lookup instead of stored values

**Status**: PARTIALLY COMMITTED - Requires re-import

---

### Fix #4: Extra SimpleDatatype@bitLength (385 issues) - COMMITTED

**Commit**: `979bf89` fix(pqa): store None for bitLength when not in original IODD

**Problem**: `SimpleDatatype@bitLength` attribute was being added to RecordItem/SimpleDatatype
when it wasn't present in the original IODD. Parser defaulted to `8` when bitLength was absent.

**Root Cause**: Parser stored a default value (8) instead of None when bitLength wasn't present.
Reconstruction then output bitLength for all RecordItems, even when not in original.

**Changes Made**:
1. `src/models/__init__.py` - Changed `bit_length: int` to `bit_length: Optional[int]` in RecordItem
2. `src/parsing/__init__.py` - Multiple locations updated:
   - `_extract_variable_record_items()` - Store None when bitLength not present
   - ProcessDataIn/Out RecordItem parsing - Store None when bitLength not present
   - `_extract_custom_datatypes()` - Get bitLength from SimpleDatatype child, not RecordItem

**Expected Impact**: ~385 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #5: RecordItem/SimpleDatatype/ValueRange Missing (271 issues) - COMMITTED

**Commit**: `34ec9ab` feat(pqa): add ValueRange extraction and reconstruction for RecordItems

**Problem**: `ValueRange` elements inside `RecordItem/SimpleDatatype` were not being extracted,
stored, or reconstructed. This affected ~271 issues across:
- VariableCollection: 201 issues
- ProcessDataCollection: 25 issues
- DatatypeCollection: 15 issues

**Changes Made**:
1. `src/models/__init__.py` - Added `min_value`, `max_value`, `value_range_xsi_type` to RecordItem
2. `src/parsing/__init__.py` - Extract ValueRange from RecordItem/SimpleDatatype in:
   - `_extract_variable_record_items()` (Variable RecordItems)
   - ProcessDataIn/Out RecordItem parsing
   - `_extract_custom_datatypes()` (Custom Datatype RecordItems)
3. `src/storage/parameter.py` - Save ValueRange fields for parameter_record_items
4. `src/storage/process_data.py` - Save ValueRange fields for process_data_record_items
5. `src/storage/custom_datatype.py` - Save ValueRange fields for custom_datatype_record_items
6. `src/utils/forensic_reconstruction_v2.py` - Generate ValueRange elements in all three contexts
7. `alembic/versions/048_add_record_item_value_range.py` - Add ValueRange columns to all tables

**Expected Impact**: ~241 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #6: Variable@id/@index Ordering (400 issues) - COMMITTED

**Commit**: `40ec80b` feat(pqa): preserve original XML order for Variables

**Problem**: Variables were being reconstructed in `param_index` order (the index attribute value),
not the original XML document order. This caused ~400 issues where Variable id/index appeared mismatched.

**Root Cause**: The parser didn't track original XML order. Reconstruction sorted by `param_index`
which doesn't match how Variables appear in the original IODD file.

**Changes Made**:
1. `src/models/__init__.py` - Added `xml_order: Optional[int]` to Parameter model
2. `src/parsing/__init__.py` - Track xml_order when parsing Variable elements
3. `src/storage/parameter.py` - Save xml_order to parameters table
4. `src/utils/forensic_reconstruction_v2.py` - Order by xml_order (with fallback to param_index)
5. `alembic/versions/049_add_parameter_xml_order.py` - Add xml_order column to parameters

**Expected Impact**: ~400 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #7: RecordItem@accessRightRestriction (187 issues) - COMMITTED

**Commit**: `3a2dd77` feat(pqa): add RecordItem accessRightRestriction extraction and reconstruction

**Problem**: RecordItem elements have an optional `accessRightRestriction` attribute that was not
being extracted, stored, or reconstructed. This affected ~187 issues across:
- VariableCollection: Variable/Datatype/RecordItem
- ProcessDataCollection: ProcessDataIn/Out/Datatype/RecordItem
- DatatypeCollection: Datatype/RecordItem

**Changes Made**:
1. `src/models/__init__.py` - Already had `access_right_restriction` field in RecordItem model
2. `src/parsing/__init__.py` - Extract accessRightRestriction from RecordItems in:
   - `_extract_variable_record_items()` (Variable RecordItems)
   - ProcessDataIn/Out RecordItem parsing
   - `_extract_custom_datatypes()` (Custom Datatype RecordItems)
3. `src/storage/parameter.py` - Save access_right_restriction for parameter_record_items
4. `src/storage/process_data.py` - Save access_right_restriction for process_data_record_items
5. `src/storage/custom_datatype.py` - Save access_right_restriction for custom_datatype_record_items
6. `src/utils/forensic_reconstruction_v2.py` - Output accessRightRestriction attribute in all three contexts
7. `alembic/versions/050_add_record_item_access_right_restriction.py` - Add access_right_restriction columns

**Expected Impact**: ~187 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #8: CommNetworkProfile Missing (63 issues) - COMMITTED

**Commit**: `3a5d85e` feat(pqa): add CommNetworkProfile reconstruction

**Problem**: CommNetworkProfile element was not being reconstructed at all. This is a direct child of
ProfileBody that contains TransportLayers/PhysicalLayer with bitrate, minCycleTime, mSequenceCapability,
sioSupported attributes, plus Connection with wire configurations, and Test section with Config elements.

**Changes Made**:
1. `src/utils/forensic_reconstruction_v2.py`:
   - Added `_create_comm_network_profile()` method to generate the entire CommNetworkProfile structure
   - Called from `_create_profile_body()` after DeviceFunction
   - Generates TransportLayers/PhysicalLayer with all attributes
   - Generates Connection with xsi:type, ProductRef, and Wire1-Wire5 elements
   - Generates Test section with Config1-Config7 and EventTrigger elements

**Expected Impact**: ~63 issues resolved (no re-import needed - uses existing data)

**Status**: COMMITTED

---

### Fix #9: Stamp Missing (58 issues) - COMMITTED

**Commit**: `90c88de` feat(pqa): add Stamp element reconstruction

**Problem**: Stamp element was not being reconstructed. The Stamp element contains:
- `crc` attribute with CRC checksum value
- `Checker` child element with `name` and `version` attributes

**Changes Made**:
1. `src/utils/forensic_reconstruction_v2.py`:
   - Added `_create_stamp()` method to generate Stamp element
   - Called from `_create_profile_body()` after CommNetworkProfile
   - Retrieves stamp_crc, checker_name, checker_version from iodd_files table

**Expected Impact**: ~58 issues resolved (no re-import needed - uses existing data)

**Status**: COMMITTED

---

### Fix #10: CommNetworkProfile/Stamp Location (644 issues) - COMMITTED

**Commit**: `18a0f43` fix(pqa): move CommNetworkProfile and Stamp to correct XML location

**Problem**: CommNetworkProfile and Stamp elements were being placed under `/IODevice/ProfileBody/`
but IODD schema requires them to be direct children of `/IODevice/`. This caused:
- 322 extra_element issues for `/IODevice/ProfileBody/CommNetworkProfile`
- 322 missing_element issues for `/IODevice/CommNetworkProfile`
- Same pattern for Stamp element

**Changes Made**:
1. `src/utils/forensic_reconstruction_v2.py`:
   - Removed `_create_comm_network_profile()` and `_create_stamp()` calls from `_create_profile_body()`
   - Added them to `reconstruct_iodd()` so they are appended to `root` (IODevice) directly
   - Elements now appear after ProfileBody and before ExternalTextCollection

**Expected Impact**: ~644 issues resolved (no re-import needed)

**Actual Results**:
- Location issues (ProfileBody/CommNetworkProfile): 0 (was 322)
- Location issues (ProfileBody/Stamp): 0 (was 322)
- Total issues reduced from 9,915 to 9,792
- Average score improved from 98.36% to 98.45%

**Status**: COMMITTED & PUSHED

---

### Fix #11: Gradient/Offset Float Formatting (1,782 issues) - COMMITTED

**Commit**: `a93ea3c` feat(pqa): preserve original string format for gradient/offset attributes

**Problem**: RecordItemRef and VariableRef gradient/offset attributes losing original format:
- Original "0.0" becoming "0" (886 gradient issues)
- Original "4.0" becoming "4" (257 offset issues)
- Total ~1,782 issues (RecordItemRef + VariableRef)

**Root Cause**: `_format_number()` converts floats to integers when they're whole numbers,
losing the ".0" suffix that was in the original IODD.

**Changes Made**:
1. `src/models/__init__.py` - Add `gradient_str`, `offset_str` fields to MenuItem
2. `src/parsing/__init__.py` - Store original string values for VariableRef and RecordItemRef
3. `src/storage/menu.py` - Save gradient_str, offset_str to ui_menu_items table
4. `src/utils/forensic_reconstruction_v2.py` - Use string values when available
5. `alembic/versions/051_add_gradient_offset_str.py` - Add new columns

**Expected Impact**: ~1,782 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #12: Condition@subindex Missing (456 issues) - COMMITTED

**Commit**: `51171bc` feat(pqa): add Condition@subindex extraction and reconstruction

**Problem**: Condition elements in ProcessData can have a `subindex` attribute that was not being
extracted, stored, or reconstructed. Affected 456 issues across 9 devices.

**Sample Original**: `<Condition variableId="V_tankAndProduct_config" value="1" subindex="1" />`

**Changes Made**:
1. `src/models/__init__.py` - Add `subindex` field to ProcessDataCondition
2. `src/parsing/__init__.py` - Extract subindex from Condition elements
3. `src/storage/process_data.py` - Save condition_subindex to process_data_conditions
4. `src/utils/forensic_reconstruction_v2.py` - Output subindex attribute when present
5. `alembic/versions/052_add_condition_subindex.py` - Add condition_subindex column

**Expected Impact**: ~456 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #13: StdErrorTypeRef Issues (305 issues) - COMMITTED

**Commit**: `9d5e782` feat(pqa): fix StdErrorTypeRef code attribute and ordering

**Problem**: Two issues with StdErrorTypeRef elements:
- extra_element (228): Always outputting `code` attribute even when not in original
- incorrect_attribute (77): `additionalCode` values mismatched due to wrong ordering

**Root Cause**:
- Parser always stored code with default 128, didn't track if attribute existed
- Reconstruction ordered by additionalCode instead of original XML order

**Changes Made**:
1. `src/models/__init__.py` - Add `has_code_attr`, `xml_order` fields to ErrorType
2. `src/parsing/__init__.py` - Track whether code exists and element order
3. `src/storage/event.py` - Save has_code_attr and xml_order
4. `src/utils/forensic_reconstruction_v2.py` - Conditionally output code, order by xml_order
5. `alembic/versions/053_add_error_type_pqa_fields.py` - Add columns

**Expected Impact**: ~305 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #14: SimpleDatatype Missing Attributes (295 issues) - COMMITTED

**Commit**: `3cd2c58` feat(pqa): add SimpleDatatype fixedLength, encoding, id attributes

**Problem**: RecordItem/SimpleDatatype elements missing attributes:
- @fixedLength (106 issues) - String length for StringT types
- @encoding (98 issues) - Character encoding (e.g., UTF-8)
- @id (89 issues) - Unique identifier for the SimpleDatatype

**Changes Made**:
1. `src/models/__init__.py` - Add `fixed_length`, `encoding`, `datatype_id` to RecordItem
2. `src/parsing/__init__.py` - Extract these from SimpleDatatype elements
3. `src/storage/parameter.py` - Save new attributes to parameter_record_items
4. `src/utils/forensic_reconstruction_v2.py` - Output attributes when present
5. `alembic/versions/054_add_simple_datatype_attrs.py` - Add columns to record_items tables

**Expected Impact**: ~295 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #15: Text/Language Element Ordering (4,063 issues) - COMMITTED

**Commit**: `598aa81` feat(pqa): fix Text and Language element ordering in ExternalTextCollection

**Problem**: Text elements in ExternalTextCollection were in wrong order:
- incorrect_attribute:Text@id (4,063 issues) - Text elements out of order
- Language elements in wrong order - secondary languages not preserving order

**Root Cause**:
- Text element order tracked per text_id but different languages have different orderings
- Language element order not preserved at all
- Reconstruction used database `id` for ordering instead of original XML order

**Changes Made**:
1. `src/models/__init__.py` - Add `text_xml_order` (per language) and `language_order` fields
2. `src/parsing/__init__.py` - Track Text order per language, track Language element order
3. `src/storage/text.py` - Save xml_order and language_order per text entry
4. `src/storage/__init__.py` - Pass language_order to TextSaver
5. `src/utils/forensic_reconstruction_v2.py` - Order Languages by language_order, Text by xml_order
6. `alembic/versions/055_add_text_xml_order.py` - Add xml_order column
7. `alembic/versions/056_add_language_order.py` - Add language_order column

**Expected Impact**: ~4,063 issues resolved (requires re-import)

**Actual Results After Re-import**:
- ExternalTextCollection issues: 0 (was 4,063)
- Total issues: 5,725 (was 9,915 at session start)
- Average score: 98.94% (was 98.36%)

**Status**: COMMITTED & PUSHED - Re-import completed

---

### Fix #16: MenuRef/Condition@subindex (450 issues) - COMMITTED

**Commit**: `74065e0` feat(pqa): add MenuRef/Condition@subindex extraction and reconstruction

**Problem**: Condition elements inside MenuRef have a `subindex` attribute that was not being
extracted, stored, or reconstructed. This is different from ProcessData Condition subindex (Fix #12).

**Sample Original**: `<MenuRef menuId="M_Level"><Condition variableId="V_Mode" value="0" subindex="1"/></MenuRef>`

**Changes Made**:
1. `src/models/__init__.py` - Add `condition_subindex` field to MenuItem
2. `src/parsing/__init__.py` - Extract subindex from MenuRef Condition elements
3. `src/storage/menu.py` - Save condition_subindex to ui_menu_items
4. `src/utils/forensic_reconstruction_v2.py` - Output subindex attribute when present
5. `alembic/versions/057_add_menu_condition_subindex.py` - Add condition_subindex column

**Expected Impact**: ~450 issues resolved (requires re-import)

**Actual Results After Re-import**:
- Condition@subindex issues: 0 (was 450)
- Total issues: 2,683 (was 3,133)
- Average score: 99.18%

**Status**: COMMITTED & PUSHED - Re-import completed

---

### Fix #17: Name@textId incorrect (296 issues) - COMMITTED

**Commit**: `f3be9a4` fix(pqa): fix Name@textId extraction and add DeviceName textId storage

**Problem**: Name@textId values were incorrect in two areas:
1. ProcessDataIn/Out Name elements: Parser used `.//iodd:Name` (recursive search) which found
   nested SingleValue/Name elements instead of the direct child Name element.
2. DeviceName@textId: No storage - reconstruction was guessing using `_lookup_textid()`.

**Root Cause Analysis**:
- Original XML: ProcessDataIn has `<Name textId="TN_PI"/>` as direct child
- Parser found first descendant Name which was inside RecordItem/SingleValue
- Result: wrong textId like `TN_for_overrun_message` instead of `TN_PI`

**Changes Made**:
1. `src/parsing/__init__.py` - Changed ProcessDataIn/Out Name selectors:
   - `.//iodd:Name` -> `iodd:Name` (direct child only)
   - Added `device_name_text_id` to DeviceInfo extraction
2. `src/models/__init__.py` - Added `device_name_text_id` field to DeviceInfo
3. `src/storage/device.py` - Save device_name_text_id to devices table
4. `src/utils/forensic_reconstruction_v2.py` - Use stored textId for DeviceName, fallback to lookup
5. `alembic/versions/058_add_device_name_text_id.py` - Add device_name_text_id column

**Actual Results After Re-import**:
- Name@textId issues: 296 -> 48 (248 fixed, 84% reduction)
- Remaining 48 issues are all DatatypeCollection/SingleValue ordering (different issue)
- Total issues: 2,683 -> 2,287 (396 fewer)
- Average score: 99.18% -> 99.26%

**Status**: COMMITTED & PUSHED - Re-import completed

---

## CURRENT SESSION SUMMARY (2025-11-21)

### Progress Summary

Starting stats:
- Average score: 98.36%
- Total issues: 9,915

Current stats:
- Average score: 99.26%
- Total issues: 2,287
- Issues fixed: 7,628 (77% reduction!)

### Fixes Completed This Session

| Fix | Issue | Count | Status |
|-----|-------|-------|--------|
| #10 | CommNetworkProfile/Stamp location | 644 | COMMITTED |
| #11 | Float formatting gradient/offset | 1,782 | COMMITTED |
| #12 | ProcessData Condition@subindex | 456 | COMMITTED |
| #13 | StdErrorTypeRef code/ordering | 305 | COMMITTED |
| #14 | SimpleDatatype attributes | 295 | COMMITTED |
| #15 | Text/Language ordering | 4,063 | COMMITTED |
| #16 | MenuRef Condition@subindex | 450 | COMMITTED |
| #17 | Name@textId incorrect | 248 | COMMITTED |
| #18 | ProcessData@id incorrect | 164 | COMMITTED |
| #19 | Connection@connectionSymbol | 108 | COMMITTED |
| #20 | Variable/Datatype@fixedLength | 162 | COMMITTED |
| #21 | RecordItem/SingleValue duplication | 98 | COMMITTED |
| #22 | Wire/Name element | 140 | COMMITTED |
| #23 | Test@xsi:type conditional | 112 | COMMITTED |

### Fix #20: Variable/Datatype@fixedLength Incorrect (169 issues) - COMMITTED

**Commit**: `f63e938` feat(pqa): extract and store Variable/Datatype fixedLength and encoding

**Problem**: StringT/OctetStringT Variable/Datatype elements had `fixedLength` and `encoding`
attributes that weren't being stored - reconstruction hardcoded `fixedLength="32"` for all.

**Root Cause**: Parser extracted these attributes but didn't store them. The Parameter model
lacked `string_fixed_length` and `string_encoding` fields. Reconstruction hardcoded values.

**Changes Made**:
1. `src/models/__init__.py` - Added `string_fixed_length` and `string_encoding` to Parameter
2. `src/parsing/__init__.py` - Extract fixedLength/encoding from Variable/Datatype elements
3. `src/storage/parameter.py` - Save string_fixed_length and string_encoding columns
4. `src/utils/forensic_reconstruction_v2.py` - Use stored values instead of hardcoding

**Result**: 162 → 7 issues (96% resolved). Remaining 7 are in DatatypeCollection (different context)

---

### Fix #18: ProcessData@id Incorrect (164 issues) - COMMITTED

**Commit**: `6727d58` feat(pqa): add ProcessData wrapper_id

**Problem**: ProcessData wrapper element ID was derived incorrectly from child ID.
Example: Wrapper=`PD`, Child=`PDI`, but reconstruction output `PDI` instead of `PD`.

**Root Cause**: Only storing child ProcessDataIn/Out ID, not wrapper ProcessData ID.

**Changes Made**:
1. `src/models/__init__.py` - Added `wrapper_id` to ProcessData model
2. `src/parsing/__init__.py` - Build wrapper_id lookup, store wrapper ID
3. `src/storage/process_data.py` - Save wrapper_id column
4. `src/utils/forensic_reconstruction_v2.py` - Use stored wrapper_id
5. `alembic/versions/059_add_process_data_wrapper_id.py` - Add wrapper_id column

**Result**: 164 → 0 issues (100% resolved)

---

### Fix #19: Connection@connectionSymbol (108 issues) - COMMITTED

**Commit**: `28f6bf9` feat(pqa): add Connection@connectionSymbol extraction and reconstruction

**Problem**: Connection elements have `connectionSymbol` attribute that wasn't being stored or reconstructed.

**Root Cause**: Parser extracted xsi:type but not connectionSymbol. Also, some Connection
elements have no Wire children, so connectionSymbol wasn't stored at all.

**Changes Made**:
1. `src/models/__init__.py` - Added `connection_symbol` to WireConfiguration and CommunicationProfile
2. `src/parsing/__init__.py` - Extract connectionSymbol in both wire config and comm profile parsing
3. `src/storage/communication.py` - Save connection_symbol in both tables
4. `src/utils/forensic_reconstruction_v2.py` - Output connectionSymbol with fallback
5. `alembic/versions/060_add_connection_symbol.py` - Add to wire_configurations
6. `alembic/versions/061_add_connection_symbol_to_comm_profile.py` - Add to communication_profile

**Result**: 108 → 0 issues (100% resolved)

---

### Fix #21: RecordItem/SimpleDatatype/SingleValue Duplication (98 issues) - COMMITTED

**Commit**: `19a0091` fix(pqa): Fix #21 - correct RecordItem/SimpleDatatype/SingleValue extraction

**Problem**: SingleValue elements inside DatatypeCollection RecordItem/SimpleDatatype were being:
1. Incorrectly extracted at BOTH Datatype level AND RecordItem level (duplication)
2. Result: 98 extra SingleValue elements in reconstruction

**Root Cause**: Parser used `.//iodd:SingleValue` XPath which found ALL descendant SingleValues
including those nested inside RecordItem/SimpleDatatype. These were stored in both:
- `custom_datatype_single_values` (wrong - Datatype level)
- `custom_datatype_record_item_single_values` (correct - RecordItem level)

**Changes Made**:
1. `src/parsing/__init__.py` - Changed XPath from `.//iodd:SingleValue` to `iodd:SingleValue`
   to extract only direct children, preventing duplication in custom datatypes
2. `src/storage/custom_datatype.py` - Store RecordItem-level SingleValues separately
3. `src/utils/forensic_reconstruction_v2.py` - Reconstruct SingleValues in correct location
4. `alembic/versions/062_add_custom_datatype_record_item_single_values.py` - New table

**Result**: 98 extra_element:SingleValue issues resolved (1900 -> 1802 total issues)

**Status**: COMMITTED & PUSHED

---

### Fix #22: Wire/Name Element Missing (140 issues) - COMMITTED

**Commit**: `d3a8ec8` feat(pqa): Fix #22 - add Wire/Name element reconstruction

**Problem**: Wire1-Wire5 elements inside CommNetworkProfile/Connection have Name children
with textId attributes that were not being stored or reconstructed.

**Root Cause**: Parser extracted name_text_id from Wire/Name element to resolve wire_description,
but didn't store the textId itself for reconstruction.

**Changes Made**:
1. `src/models/__init__.py` - Added `name_text_id` to WireConfiguration model
2. `src/parsing/__init__.py` - Pass name_text_id to WireConfiguration (already extracted)
3. `src/storage/communication.py` - Save name_text_id to wire_configurations table
4. `src/utils/forensic_reconstruction_v2.py` - Add Name element with textId to Wire elements
5. `alembic/versions/063_add_wire_name_text_id.py` - Add name_text_id column

**Result**: 140 issues resolved (1802 → 1662 total issues)

**Status**: COMMITTED & PUSHED

---

### Fix #23: Test@xsi:type Conditional Output (112 issues) - COMMITTED

**Commit**: `5bfd55e` feat(pqa): Fix #23 - conditional Test@xsi:type reconstruction

**Problem**: CommNetworkProfile/Test element had `xsi:type="IOLinkTestT"` always added
during reconstruction, but only 35 out of 148 files with Test elements have this attribute.

**Root Cause**: Reconstruction hardcoded `xsi:type="IOLinkTestT"` on all Test elements
without checking if the original had it.

**Changes Made**:
1. `src/models/__init__.py` - Added `test_xsi_type` to CommunicationProfile
2. `src/parsing/__init__.py` - Extract Test@xsi:type if present
3. `src/storage/communication.py` - Save test_xsi_type to communication_profile
4. `src/utils/forensic_reconstruction_v2.py` - Conditionally output Test@xsi:type
5. `alembic/versions/064_add_test_xsi_type.py` - Add test_xsi_type column

**Result**: 112 extra_element:xsi:type issues resolved (1662 → 1550 total issues)

**Status**: COMMITTED & PUSHED

---

### Remaining Top Issues (After Fix #23)

| Count | Issue Pattern |
|-------|---------------|
| 114 | missing_attribute:xsi:type |
| 97 | missing_element:ValueRange |
| 64 | extra_element:RecordItem@bitOffset |
| 63 | missing_element:Description |
| 61 | incorrect_attribute:VendorText@textId |
| 61 | incorrect_attribute:VendorUrl@textId |
| 61 | incorrect_attribute:DeviceFamily@textId |
| 57 | missing_element:Name |
| 56 | missing_element:ProcessDataRefCollection |
| 48 | incorrect_attribute:SingleValue@value |
| 48 | incorrect_attribute:Name@textId |
| 45 | incorrect_attribute:RecordItemRef@variableId |
| 44 | incorrect_attribute:StdErrorTypeRef@additionalCode |
| 41 | incorrect_attribute:VariableRef@variableId |
| 39 | missing_element:IdentificationMenu |

**Total Issues**: 1,550 (down from 1,662 - 112 fixed with Fix #23)

---

### Fix #24: DeviceIdentity textId Storage (141 issues) - COMMITTED

**Commit**: `a098cd7`

**Problem**: VendorText@textId, VendorUrl@textId, and DeviceFamily@textId elements were using
lookup-based textIds (TI_VendorText) instead of storing the original textIds from the IODD.
This affected 47 devices with 141 issues total (3 elements x 47 devices).

**Root Cause**: Parser didn't store original textIds for these DeviceIdentity elements.
Reconstruction used `_lookup_textid()` which guesses based on common prefixes.

**Changes Made**:
1. `src/models/__init__.py` - Added `vendor_text_text_id`, `vendor_url_text_id`, `device_family_text_id` to DeviceInfo
2. `src/parsing/__init__.py` - Extract textIds from VendorText, VendorUrl, DeviceFamily elements
3. `src/storage/device.py` - Save new textId fields to devices table
4. `src/utils/forensic_reconstruction_v2.py` - Use stored textIds with fallback to lookup
5. `alembic/versions/065_add_device_identity_text_ids.py` - Add new columns

**Expected Impact**: ~141 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #25: Wire xsi:type Storage (33 issues) - COMMITTED

**Commit**: `21baabc`

**Problem**: Wire1, Wire3, Wire4 elements inside Connection missing `xsi:type` attribute.
Expected values like `Wire1T`, `Wire3T`, `Wire4T`. Affected 33 issues across 10 devices.

**Root Cause**: Parser didn't extract xsi:type from Wire elements. Reconstruction didn't output it.

**Changes Made**:
1. `src/models/__init__.py` - Added `xsi_type` field to WireConfiguration
2. `src/parsing/__init__.py` - Extract xsi:type from Wire elements
3. `src/storage/communication.py` - Save xsi_type to wire_configurations table
4. `src/utils/forensic_reconstruction_v2.py` - Output xsi:type when present
5. `alembic/versions/066_add_wire_xsi_type.py` - Add xsi_type column

**Expected Impact**: ~33 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #26: Connection/ProductRef@productId (24 issues) - COMMITTED

**Commit**: `89d2060`

**Problem**: Connection/ProductRef@productId was using device_variants.product_id instead
of the original productId from the IODD. This caused 24 issues across 24 devices where
the ProductRef productId differs (e.g., different cable lengths, model variants).

**Root Cause**: Parser didn't extract ProductRef@productId. Reconstruction used device_variants
which may have a different productId than what's in Connection/ProductRef.

**Changes Made**:
1. `src/models/__init__.py` - Added `product_ref_id` field to CommunicationProfile
2. `src/parsing/__init__.py` - Extract productId from Connection/ProductRef element
3. `src/storage/communication.py` - Save product_ref_id to communication_profile table
4. `src/utils/forensic_reconstruction_v2.py` - Use stored product_ref_id with fallback
5. `alembic/versions/067_add_product_ref_id.py` - Add product_ref_id column

**Expected Impact**: ~24 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #27: Menu xsi:type UIMenuRefT (78 issues) - COMMITTED

**Commit**: `85c4292`

**Problem**: Role menu elements (IdentificationMenu, ParameterMenu, DiagnosisMenu, ObservationMenu)
inside RoleMenuSets were missing `xsi:type="UIMenuRefT"` attribute. Affected 78 issues across 13 devices.

**Root Cause**: Parser didn't extract xsi:type from role menu elements. Reconstruction didn't output it.

**Changes Made**:
1. `src/models/__init__.py` - Added xsi_type tracking dicts to UserInterfaceMenus
2. `src/parsing/__init__.py` - Extract xsi:type from role menu elements
3. `src/storage/menu.py` - Save has_xsi_type flag to ui_menu_roles table
4. `src/utils/forensic_reconstruction_v2.py` - Output xsi:type when has_xsi_type is true
5. `alembic/versions/068_add_role_menu_xsi_type.py` - Add has_xsi_type column

**Expected Impact**: ~78 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #28: Menu Structure Namespace Handling (63 issues) - COMMITTED

**Commit**: `3be75fb`

**Problem**: Role menu elements (IdentificationMenu, ParameterMenu, DiagnosisMenu, ObservationMenu)
were not matching during reconstruction because the menu_type was stored with full namespace prefix
like `{http://www.io-link.com/IODD/2009/11}IdentificationMenu` instead of just `IdentificationMenu`.
Affected 63 issues across 7 devices.

**Root Cause**: Parser used `replace('{http://www.io-link.com/IODD/2010/10}', '')` to strip namespace
from tag names, but some IODDs use the 2009/11 namespace. This caused menu_type to include the
full namespace prefix, and reconstruction couldn't match element names.

**Changes Made**:
1. `src/parsing/__init__.py` - Added `get_local_name()` helper function that splits on '}' to handle any namespace
2. `src/utils/forensic_reconstruction_v2.py` - Handle legacy data with namespace prefix using `if '}' in menu_type`

**Expected Impact**: ~63 issues resolved (no migration needed - code fix only, requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #29: VariableRef@buttonValue Missing (23 issues) - COMMITTED

**Commit**: `d73b3d2`

**Problem**: VariableRef elements inside MenuCollection/Menu missing `buttonValue` attribute.
Expected values like 128, 160, 130, etc. Affected 23 issues.

**Root Cause**: Parser didn't extract buttonValue from VariableRef element. Reconstruction didn't output it.
Note: This is the buttonValue attribute directly ON VariableRef, not on nested Button children.

**Changes Made**:
1. `src/parsing/__init__.py` - Extract buttonValue from VariableRef elements
2. `src/utils/forensic_reconstruction_v2.py` - Output buttonValue attribute when present

**Expected Impact**: ~23 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #30a: RecordItem ValueRange/Name Missing (47 issues) - COMMITTED

**Commit**: `74c360f`

**Problem**: RecordItem/SimpleDatatype/ValueRange elements missing Name child element with textId.
Affected 42 issues in VariableCollection, 3 in DatatypeCollection, 2 in ProcessDataCollection.

**Root Cause**: Parser extracted ValueRange min/max/xsi:type but not the Name child element.
RecordItem model lacked value_range_name_text_id field.

**Changes Made**:
1. `src/models/__init__.py` - Added `value_range_name_text_id` to RecordItem model
2. `src/parsing/__init__.py` - Extract ValueRange/Name@textId in all 3 contexts:
   - `_extract_variable_record_items()` (Variable RecordItems)
   - ProcessDataIn/Out RecordItem parsing
   - `_extract_custom_datatypes()` (DatatypeCollection RecordItems)
3. `src/storage/parameter.py` - Save value_range_name_text_id to parameter_record_items
4. `src/storage/process_data.py` - Save value_range_name_text_id to process_data_record_items
5. `src/storage/custom_datatype.py` - Save value_range_name_text_id to custom_datatype_record_items
6. `src/utils/forensic_reconstruction_v2.py` - Output ValueRange/Name with textId in all contexts
7. `alembic/versions/069_add_value_range_name_text_id.py` - Add column to all 3 tables

**Expected Impact**: ~47 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #30b: DatatypeCollection Datatype/ValueRange Missing (35 issues) - COMMITTED

**Commit**: `ff3e248`

**Problem**: Datatype elements in DatatypeCollection can have ValueRange child elements
directly (not inside RecordItem). This is for scalar custom datatypes with value ranges.
Affected 35 issues.

**Root Cause**: Parser and CustomDatatype model didn't support ValueRange at Datatype level.
Only ValueRange inside RecordItem/SimpleDatatype was implemented.

**Changes Made**:
1. `src/models/__init__.py` - Added `min_value`, `max_value`, `value_range_xsi_type`, `value_range_name_text_id` to CustomDatatype
2. `src/parsing/__init__.py` - Extract Datatype-level ValueRange (direct child, not in RecordItem)
3. `src/storage/custom_datatype.py` - Save ValueRange fields to custom_datatypes table
4. `src/utils/forensic_reconstruction_v2.py` - Output ValueRange with Name at Datatype level
5. `alembic/versions/070_add_datatype_value_range.py` - Add columns to custom_datatypes

**Expected Impact**: ~35 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

### Fix #30c: ArrayT Variable SimpleDatatype/ValueRange Missing (30 issues) - COMMITTED

**Commit**: `8cf2291` feat(pqa): Fix #30c - add ArrayT SimpleDatatype ValueRange extraction

**Problem**: ArrayT Variables have SimpleDatatype child elements that can contain ValueRange.
These ValueRanges with lowerValue, upperValue, xsi:type, and Name@textId were not extracted.
Affected 30 issues.

**Root Cause**: Parser extracted ArrayT SimpleDatatype attributes (type, bitLength, fixedLength)
but didn't extract ValueRange inside the SimpleDatatype.

**Changes Made**:
1. `src/models/__init__.py` - Added `array_element_min_value`, `array_element_max_value`, `array_element_value_range_xsi_type`, `array_element_value_range_name_text_id` to Parameter
2. `src/parsing/__init__.py` - Extract ValueRange from ArrayT SimpleDatatype
3. `src/storage/parameter.py` - Save ArrayT ValueRange fields to parameters table
4. `src/utils/forensic_reconstruction_v2.py` - Output ValueRange with Name in ArrayT SimpleDatatype
5. `alembic/versions/071_add_array_element_value_range.py` - Add columns to parameters

**Expected Impact**: ~30 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

---

## SESSION 2025-11-23 - PQA ANALYSIS AND PLANNING

### Current IODD PQA Status (After Previous Fixes)

| Metric | Value |
|--------|-------|
| **Average Score** | 99.67% |
| **Min Score** | 93.71% (Device 18 - SL-x-TRIO IOLINK) |
| **Max Score** | 100.00% |
| **Total Diffs** | 878 |
| **Devices at 100%** | 27 |
| **Devices 99-99.99%** | 123 |
| **Devices < 99%** | 11 |

### Score Distribution

| Range | Count |
|-------|-------|
| 100% | 27 |
| 99-99.99% | 123 |
| 95-98.99% | 9 |
| 90-94.99% | 2 |
| <90% | 0 |

### Remaining Issues by Type (878 total)

| Diff Type | Count |
|-----------|-------|
| missing_element | 331 |
| incorrect_attribute | 253 |
| extra_element | 139 |
| missing_attribute | 116 |
| value_changed | 39 |

### Top Issue Patterns

| Issue Pattern | Count | Priority |
|--------------|-------|----------|
| missing_element:ProcessDataOut | 78 | High |
| extra_element:RecordItem@bitOffset | 64 | High |
| missing_element:Description | 62 | Medium |
| missing_element:ProcessDataRefCollection | 56 | High |
| incorrect_attribute:Name@textId | 54 | High |
| incorrect_attribute:SingleValue@value | 49 | Medium |
| incorrect_attribute:RecordItemInfo@subindex | 48 | Medium |
| incorrect_attribute:StdErrorTypeRef@additionalCode | 44 | Low |
| missing_element:SingleValue | 38 | Medium |
| missing_element:ErrorType | 31 | Medium |

### Worst Performing Device Analysis

**Device 18 (SL-x-TRIO IOLINK)** - 93.71% with 265+ issues:
- Primary cause: DatatypeCollection RecordItem ordering
- RecordItems reconstructed by `subindex` order, but original XML has different ordering
- Results in cascading mismatches: subindex, bitOffset, Name@textId, ValueRange values

### Planned Fixes (Priority Order)

#### Fix #31: ProcessDataRefCollection Reconstruction (56 issues)
**Complexity**: High
**Problem**: ProcessDataRefCollection element in UserInterface not implemented

**Implementation Required**:
1. ProcessDataRefCollection is child of UserInterface (after MenuCollection)
2. Contains ProcessDataRef elements with processDataId attribute
3. Each ProcessDataRef has ProcessDataRecordItemInfo children

#### Fix #32: RecordItem@bitOffset Conditional Output (64 issues) - COMMITTED

**Commit**: `3374140`

**Problem**: RecordItem bitOffset was output as "0" even when not present in original IODD.
Affected devices 35 and 36 (48 RecordItems each with no bitOffset in original).

**Root Cause**: Parser used `int(ri_elem.get('bitOffset', 0))` which converted missing
attribute to 0. Reconstruction then output `bitOffset="0"` for all RecordItems.

**Changes Made**:
1. `src/models/__init__.py` - Changed `bit_offset: int` to `bit_offset: Optional[int]`
2. `src/parsing/__init__.py` - Store None when bitOffset not present (3 locations)
3. `src/storage/parameter.py` - Use None as default for bit_offset

**Note**: Reconstruction already had correct logic: `if item['bit_offset'] is not None:`

**Expected Impact**: ~64 issues resolved (requires re-import)

**Status**: COMMITTED & PUSHED - Requires re-import to populate data

#### Fix #33a: Custom Datatype Child Table Deletion (165 issues) - COMMITTED

**Commit**: `6e5da61`

**Problem**: Device 18 had 9 record items per DT_Color datatype instead of 3 (3x duplication).
RecordItemInfo subindex and defaultValue were all mismatched due to this duplication.

**Root Cause**: FK cascade was disabled in SQLite (`PRAGMA foreign_keys = 0`), so deleting
from `custom_datatypes` didn't cascade to child tables. Duplicates accumulated on re-import.

**Changes Made**:
1. `src/storage/custom_datatype.py` - Explicitly delete from child tables before parent:
   - Get existing datatype IDs
   - Delete from custom_datatype_record_item_single_values
   - Delete from custom_datatype_record_items
   - Delete from custom_datatype_single_values
   - Delete from custom_datatypes

**Results for Device 18**:
- RecordItems per DT_Color: 9 → 3 (correct)
- Total diffs: 265 → 100 (165 fixed)
- Score: 93.71% → 94.26%

**Remaining Issues**: 100 diffs (RecordItemInfo ordering in VariableCollection - different issue)

**Status**: COMMITTED & PUSHED

---

#### Fix #33b: Parameter/ProcessData Child Table Deletion (182 issues) - COMMITTED

**Commit**: `f28a0da`

**Problem**: Same FK cascade issue as Fix #33a. Duplicate records in:
- `variable_record_item_info` (273 → 91 for device 18)
- `parameter_single_values`, `parameter_record_items`
- `process_data_*` child tables

**Changes Made**:
1. `src/storage/parameter.py` - Delete from variable_record_item_info, parameter_single_values,
   parameter_record_items before deleting from parameters
2. `src/storage/process_data.py` - Delete from process_data_single_values, process_data_ui_info,
   process_data_conditions, process_data_record_items before deleting from process_data

**Results for Device 18**:
- Score: 94.26% → 96.43% (3% improvement)
- Total diffs: 100 → 158 (mix of fixed and newly visible issues)

**Remaining Issues**: UserInterface menu element ordering (VariableRef, RecordItemRef, MenuRef)

**Status**: COMMITTED & PUSHED

#### Fix #34: ProcessDataOut Structure (78 issues)
**Complexity**: Medium
**Requires investigation**: Verify ProcessDataOut elements match expected wrapper structure

#### Fix #35: Missing Description Elements (62 issues)
**Complexity**: Low-Medium
**Requires investigation**: Identify missing Description contexts

---

## POST-REIMPORT RESULTS (HISTORICAL)

Re-import completed successfully with parser shadowing fix applied.

### Improvement Summary

| Metric | Before Reimport | After Reimport | Change |
|--------|-----------------|----------------|--------|
| **Average Score** | 89.43% | **96.58%** | +7.15% |
| **Min Score** | 80.21% | **86.26%** | +6.05% |
| **Max Score** | 96.84% | **99.76%** | +2.92% |
| **Devices Analyzed** | 149 | 161 | +12 |

### Score Distribution

| Range | Before | After |
|-------|--------|-------|
| 99-100% | 0 | **35** |
| 95-99% | 4 | **83** |
| 90-95% | 66 | 38 |
| 85-90% | 66 | **5** |
| 80-85% | 13 | **0** |

**73% of devices now score 95%+** (118 out of 161)

### Remaining Issues to Fix

| Priority | Category | Count | Status |
|----------|----------|-------|--------|
| 1 | ProcessDataIn/Out Name | 1,534 | TODO |
| 2 | Variable/Datatype missing element | 1,362 | TODO |
| 3 | Variable/Datatype extra element | 794 | TODO |
| 4 | Variable/Datatype incorrect attr | 623 | TODO |
| 5 | ErrorType issues | 343 | TODO |
| 6 | UserInterface issues | 256 | TODO |
| 7 | CommNetworkProfile (missing) | 128 | TODO |
| 8 | Stamp (missing) | 119 | TODO |

### Worst Performing Devices

| ID | Score | Product |
|----|-------|---------|
| 154 | 86.26% | VEGAPULS 42 IO-Link |
| 139 | 86.80% | TiM100 |
| 134 | 86.82% | DT50-2 |
| 136 | 88.10% | KTS/KTX |
| 130 | 88.94% | SL-x-TRIO IOLINK |

---

## PREVIOUS STATE (Before Reimport)

### Expected vs Actual Results

| Category | Expected After | Actual After | Notes |
|----------|---------------|--------------|-------|
| Boolean attributes | ~100 | Resolved | Migration 044 worked |
| StdVariableRef | ~0 | Resolved | Parser fix worked |
| textId issues | ~300 | Resolved | Parser fix worked |
| **Overall** | 50-55% reduction | **+7.15% avg score** | Exceeded expectations |

---

## FIX #1: Boolean Attribute Defaults (Migration 044)

**Problem**: Database columns `dynamic`, `excluded_from_data_storage`, `modifies_other_variables` had `DEFAULT 0`, causing NULL inserts to become 0.

**Root Cause**: When inserting `None` (for attributes not present in original IODD), SQLite used the default value `0`.

**Solution**: Created migration 044 to recreate columns without DEFAULT:
- `alembic/versions/044_fix_boolean_column_defaults.py`
- Removes DEFAULT 0 from parameters table
- Removes DEFAULT 0 from variable_record_item_info table
- Converts existing 0 values to NULL (since we can't distinguish which were explicit)

**Status**: COMPLETE - Migration applied, requires re-import.

---

## VERIFIED WORKING (Already Implemented)

### 1. Variable/Name textId Storage
- Parser extracts `name_text_id` from Variable/Name@textId ✓
- Storage saves to `parameters.name_text_id` column ✓
- Reconstruction uses stored textId ✓
- **Issue**: Data not populated (needs re-import)

### 2. DeviceVariant textId Storage
- Parser extracts `name_text_id` and `description_text_id` ✓
- Storage saves to `device_variants` table ✓
- Reconstruction uses stored textIds ✓
- **Issue**: Data not populated (needs re-import)

### 3. StdVariableRef Storage
- Parser extracts via `_extract_std_variable_refs()` ✓
- Storage saves to `std_variable_refs` table ✓
- Reconstruction generates StdVariableRef elements ✓
- **Issue**: Data not populated (needs re-import)

### 4. SingleValue textId Storage
- Parser extracts to `single_values` with `text_id` ✓
- Storage saves to `parameter_single_values.text_id` ✓
- Reconstruction uses stored textId ✓
- **Issue**: Data not populated (needs re-import)

### 5. RecordItem textId Storage
- Parser extracts `name_text_id` ✓
- Storage saves to `parameter_record_items.name_text_id` ✓
- Reconstruction uses stored textId ✓
- **Issue**: Data not populated (needs re-import)

---

## PREVIOUS SESSION RESULTS

### Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Issues | ~22,944 | 14,052 | -8,892 (38.8% reduction) |
| Average Score | ~85% | 89.43% | +4.4% |
| Min Score | - | 80.21% | - |
| Max Score | - | 96.84% | - |

### Score Distribution
- 95-100%: 4 devices
- 90-95%: 66 devices
- 85-90%: 66 devices
- 80-85%: 13 devices

---

## REMAINING ISSUES (Before This Session's Re-import)

| Priority | Category | Count | % | Status |
|----------|----------|-------|---|--------|
| 1 | Variable extra boolean attrs | 3,084 | 21.9% | FIXED (Mig 044) |
| 2 | Missing StdVariableRef | 2,278 | 16.2% | FIXED (re-import) |
| 3 | textId incorrect | 1,998 | 14.2% | FIXED (re-import) |
| 4 | Missing SingleValue | 1,190 | 8.5% | FIXED (re-import) |
| 5 | Missing RecordItem | 1,053 | 7.5% | FIXED (re-import) |
| 6 | Missing RecordItemInfo | 716 | 5.1% | FIXED (re-import) |
| 7 | Event Name/Description | 599 | 4.3% | Partial |
| 8 | Variable Description | 482 | 3.4% | Partial |
| 9 | Missing xsi:type | 413 | 2.9% | TBD |
| 10 | subindexAccessSupported | 295 | 2.1% | TBD |

---

## COMPLETED THIS SESSION (Continued)

### New Fixes Applied (Post-Reimport)

#### FIX #2: ProcessData Name and subindexAccessSupported (Migration 045)

**Problem**: ProcessDataIn/Out elements missing Name child element and subindexAccessSupported attribute.

**Changes Made**:
1. `src/models/__init__.py` - Added `name_text_id` and `subindex_access_supported` to ProcessData model
2. `src/parsing/__init__.py` - Extract name_text_id and subindexAccessSupported for both inputs and outputs
3. `src/storage/process_data.py` - Save both new fields
4. `src/utils/forensic_reconstruction_v2.py` - Generate Name element with textId and subindexAccessSupported attribute
5. `alembic/versions/045_add_process_data_name_text_id.py` - Add columns to process_data table

**Expected Impact**: ~1,700+ issues resolved (ProcessDataIn/Out Name + subindexAccessSupported)

#### FIX #3: StdErrorTypeRef code attribute

**Problem**: StdErrorTypeRef elements missing `code` attribute (always 128/0x80).

**Changes Made**:
- `src/utils/forensic_reconstruction_v2.py` - Add `code` attribute to StdErrorTypeRef output

**Expected Impact**: ~313 issues resolved

---

### Known Issues (Future Work)

These issues require more significant changes and are deferred:

| Issue | Count | Root Cause | Fix Required |
|-------|-------|------------|--------------|
| ValueRange in RecordItem | ~345 | Not stored for RecordItems | Add min/max columns, update parser/reconstruction |
| CommNetworkProfile missing | ~128 | Not reconstructed | Add reconstruction logic |
| Stamp missing | ~119 | Not reconstructed | Add reconstruction logic |
| Extra SimpleDatatype attrs | ~434 | Adding bitLength when not in original | Conditional attribute generation |
| UserInterface issues | ~256 | Complex nested structure | Further investigation needed |

---

## PREVIOUS SESSION FIXES

### Code Fixes
- [x] Migration 044: Fix boolean column defaults
- [x] Verified parser extracts name_text_id correctly
- [x] Verified storage saves name_text_id correctly
- [x] Verified reconstruction uses name_text_id correctly
- [x] Verified StdVariableRef full flow works
- [x] Verified DeviceVariant textId flow works

### Database Cleanup (Previous)
- [x] Fix FK violation cleanup - batch deletions (500 per batch)
- [x] Fix delete-all to include ALL tables (~65 tables)
- [x] Clean 152,571 orphaned records
- [x] Verify database clean before reimport

---

## ALL FILES CHANGED

### This Session
1. `alembic/versions/045_add_process_data_name_text_id.py` - NEW
   - Adds name_text_id and subindex_access_supported columns to process_data

2. `src/models/__init__.py` - UPDATED
   - Added name_text_id and subindex_access_supported to ProcessData

3. `src/parsing/__init__.py` - UPDATED
   - Extract ProcessData name_text_id and subindexAccessSupported

4. `src/storage/process_data.py` - UPDATED
   - Save name_text_id and subindex_access_supported

5. `src/utils/forensic_reconstruction_v2.py` - UPDATED
   - Generate Name element and subindexAccessSupported attribute for ProcessData

### Previous Session
1. `alembic/versions/044_fix_boolean_column_defaults.py` - NEW

2. `src/greenstack.py` - CRITICAL FIX
   - Parser shadowing fix

---

## NEXT STEPS

1. **RE-IMPORT DEVICES** to populate new ProcessData fields
   - Required for ProcessData Name and subindexAccessSupported

2. **Run PQA analysis** to verify improvement

3. **Future Improvements** (lower priority):
   - ValueRange for RecordItems
   - CommNetworkProfile reconstruction
   - Stamp reconstruction

---

## SESSION 2025-11-23 - PQA Improvements

### Summary
- **Starting State**: 27 devices at 100%, avg 99.67%, 878 diffs
- **Ending State**: 45 devices at 100%, avg 99.63%, 1139 diffs (ordering issues discovered)

### Fix #34: ProcessDataOut Wrapper Grouping
**Commits**: `66a6c9f`, `bd576dc`

**Problem**: ProcessDataIn and ProcessDataOut with same wrapper_id were output as separate ProcessData elements instead of being grouped.

**Changes**:
1. `src/utils/forensic_reconstruction_v2.py`:
   - Rewrote `_create_process_data_collection` to group rows by wrapper_id
   - Added `_add_process_data_direction_element` helper method
   - Used MIN(id) per wrapper to preserve original document order

**Impact**: Fixed 78 missing ProcessDataOut issues, improved ordering for 200+ issues

### Fix #31: ProcessDataRefCollection Reconstruction
**Commit**: `eb9f451`

**Problem**: ProcessDataRefCollection was missing entirely from UserInterface reconstruction.

**Changes**:
1. `src/utils/forensic_reconstruction_v2.py`:
   - Added ProcessDataRefCollection generation in `_create_user_interface`
   - Outputs ProcessDataRef with ProcessDataRecordItemInfo (gradient, offset, unitCode, displayFormat)
   - Fixed `_format_number` to preserve ".0" for float whole numbers (e.g., "0.0" not "0")

**Impact**: Fixed 56 missing ProcessDataRefCollection issues

### Outstanding Issues
1. **ProcessDataRefCollection ordering**: PDO/PDI order differs from original (313 issues)
2. **Description elements**: Connection/Description missing (62 issues) - requires schema change
3. **RecordItem@bitOffset**: Still present in some contexts (64 issues)
4. **SingleValue attributes**: DatatypeCollection issues (96 issues)

### All Commits This Session
1. `66a6c9f` feat(pqa): Fix #34 - group ProcessDataIn/Out by wrapper_id
2. `bd576dc` fix(pqa): Fix #34b - preserve ProcessData element order
3. `eb9f451` feat(pqa): Fix #31 - add ProcessDataRefCollection reconstruction

---

## SESSION 2025-11-23 (Continued) - PQA Complete Fix Pass

### Starting State
- **Average Score**: 99.71%
- **Perfect (100%)**: 45 devices
- **Near Perfect (99-99.99%)**: 99 devices
- **Below 99%**: 17 devices
- **Total Diffs**: 864

### Fixes Completed This Session

#### PQA Threshold API Fix
**Commit**: `1d9ec61`

**Problem**: PQA threshold UI not working - DELETE endpoint missing, model incomplete.

**Changes**:
1. `src/routes/pqa_routes.py`:
   - Added DELETE endpoint `/api/pqa/thresholds/{id}`
   - Updated ThresholdConfig model with all fields: id, description, min_value_score, allow_critical_data_loss, email_notifications, active
   - Fixed GET endpoint to return id and all fields with null safety
   - Fixed POST/PUT endpoints to include all fields
   - Protected default threshold from deletion

**Impact**: Unblocked PQA threshold UI

---

#### Fix #39: Connection/Description Missing (63 issues)
**Commit**: `c0844d5`

**Problem**: Connection elements in CommNetworkProfile have Description child element that was not being reconstructed.

**Changes**:
1. `src/models/__init__.py` - Added `connection_description_text_id` to CommunicationProfile
2. `src/parsing/__init__.py` - Extract Connection/Description@textId
3. `src/storage/communication.py` - Save connection_description_text_id
4. `src/utils/forensic_reconstruction_v2.py` - Output Description element inside Connection
5. `alembic/versions/072_add_connection_description_text_id.py` - Add column

**Expected Impact**: ~63 issues resolved (requires re-import)

---

#### Fix #36: ProcessDataRefCollection Ordering (313 issues)
**Commit**: `4b132f4`

**Problem**: ProcessDataRef elements in ProcessDataRefCollection ordered by pd.id instead of direction, causing PDI to appear before PDO.

**Changes**:
1. `src/utils/forensic_reconstruction_v2.py` - Changed ORDER BY from `pd.id` to `CASE pd.direction WHEN 'output' THEN 0 ELSE 1 END, pd.pd_id, pdui.subindex`

**Impact**: ~313 issues resolved (no re-import needed, just PQA re-run)

---

#### Fix #37: ErrorType vs StdErrorTypeRef (108 issues)
**Commit**: `cd7adde`

**Problem**: Three issues with ErrorTypeCollection:
- 16 extra StdErrorTypeRef elements (should be custom ErrorType)
- 52 incorrect attribute values (ordering)
- 40 missing ErrorType elements

**Root Cause**: Parser didn't distinguish between custom ErrorType (with Name/Description children) and StdErrorTypeRef (standard references).

**Changes**:
1. `src/models/__init__.py` - Added `is_custom`, `name_text_id`, `description_text_id` to ErrorType
2. `src/parsing/__init__.py` - Track custom vs standard errors, store textIds
3. `src/storage/event.py` - Save is_custom flag and textIds
4. `src/utils/forensic_reconstruction_v2.py` - Output ErrorType with Name/Description for custom, StdErrorTypeRef for standard
5. `alembic/versions/073_add_error_types_custom_fields.py` - Add 3 columns

**Expected Impact**: ~108 issues resolved (requires re-import)

---

#### Fix #38: DatatypeCollection/SingleValue Ordering (99 issues)
**Commit**: `8c4349b`

**Problem**: SingleValue elements inside custom datatypes ordered by value (alphabetically) instead of original XML order, causing "false" to appear before "true".

**Changes**:
1. `src/models/__init__.py` - Added `xml_order` to SingleValue
2. `src/parsing/__init__.py` - Track xml_order for SingleValue elements
3. `src/storage/custom_datatype.py` - Save xml_order to custom_datatype_single_values
4. `src/utils/forensic_reconstruction_v2.py` - Order by xml_order with fallback to value-based sort
5. `alembic/versions/074_add_single_value_xml_order.py` - Add xml_order column

**Expected Impact**: ~99 issues resolved (requires re-import)

---

#### Fix #40: DeviceVariant ProductName/ProductText (66 issues)
**Commit**: `d3cf3d2`

**Problem**: Some IODDs use ProductName/ProductText instead of Name/Description in DeviceVariant. Reconstruction always output Name/Description.

**Changes**:
1. `src/models/__init__.py` - Added `product_name_text_id`, `product_text_text_id`, `has_name`, `has_description`, `has_product_name`, `has_product_text` to DeviceVariant
2. `src/parsing/__init__.py` - Extract both element types, track which were present
3. `src/storage/document.py` - Save all new fields
4. `src/utils/forensic_reconstruction_v2.py` - Output correct element type based on what was present, with legacy fallback
5. `alembic/versions/075_add_device_variant_element_flags.py` - Add 6 columns

**Expected Impact**: ~66 issues resolved (requires re-import)

---

### All Commits This Session (Continued)
4. `1d9ec61` fix(api): Fix PQA threshold API - add DELETE, fix model
5. `c0844d5` feat(pqa): Fix #39 - add Connection/Description element reconstruction
6. `4b132f4` fix(pqa): Fix #36 - ProcessDataRefCollection ordering
7. `cd7adde` feat(pqa): Fix #37 - distinguish ErrorType vs StdErrorTypeRef
8. `8c4349b` fix(pqa): Fix #38 - DatatypeCollection/SingleValue ordering
9. `d3cf3d2` feat(pqa): Fix #40 - DeviceVariant ProductName/ProductText elements

### Expected Results After Re-import

| Issue Category | Before | After (Expected) | Reduction |
|----------------|--------|------------------|-----------|
| Connection/Description | 63 | 0 | -63 |
| ProcessDataRefCollection ordering | 313 | 0 | -313 |
| ErrorType issues | 108 | 0 | -108 |
| SingleValue ordering | 99 | 0 | -99 |
| DeviceVariant issues | 66 | 0 | -66 |
| **Total** | **649** | **0** | **-649** |

**Note**: Fix #36 (ProcessDataRefCollection) doesn't require re-import, just PQA re-run. All other fixes require re-import to populate new fields.

### Migrations Added
- 072: connection_description_text_id in communication_profile
- 073: is_custom, name_text_id, description_text_id in error_types
- 074: xml_order in custom_datatype_single_values
- 075: product_name_text_id, product_text_text_id, has_name, has_description, has_product_name, has_product_text in device_variants

---

### READY FOR RE-IMPORT

All fixes have been committed and pushed. Re-import required to:
1. Populate Connection/Description textId
2. Populate ErrorType is_custom and textIds
3. Populate SingleValue xml_order
4. Populate DeviceVariant element flags and textIds

After re-import, run PQA analysis to verify improvements.

---

## Session: 2025-11-23 (Fix #41-49 - PQA Final Push)

### Current IODD PQA Status (Before Session)
- **Total IODD Devices**: 161
- **Average Score**: 99.84%
- **Perfect (100%)**: 88 devices (54.7%)
- **Near Perfect (99-99.99%)**: 65 devices (40.4%)
- **Below 99%**: 8 devices (5.0%)
- **Total Remaining Diffs**: 521

### Fixes Completed

#### Fix #41: ProcessDataRecordItemInfo Ordering (233 issues)
**Commit**: `1bbd604` feat(pqa): Fix #41 - ProcessDataRecordItemInfo ordering

**Problem**: ProcessDataRecordItemInfo elements were reconstructed in wrong order (sorted by subindex) instead of original XML order.

**Changes**:
- Model: Add xml_order field to ProcessDataUIInfo
- Parser: Track element order when extracting ProcessDataRecordItemInfo
- Storage: Save xml_order to process_data_ui_info table
- Reconstruction: Order by COALESCE(xml_order, subindex)
- Migration 076: Add xml_order column

**Expected Impact**: ~233 issues resolved (requires re-import)

---

#### Fix #42: ProcessDataRef@processDataId (46 issues)
**Commit**: `b9b9b85` feat(pqa): Fix #42 - ProcessDataRef ordering

**Problem**: ProcessDataRef elements had Input/Output order hardcoded instead of preserving original XML order.

**Changes**:
- Model: Add pd_ref_order field to ProcessDataUIInfo
- Parser: Track ProcessDataRef element order
- Storage: Save pd_ref_order to process_data_ui_info table
- Reconstruction: Order by pd_ref_order first, with direction fallback
- Migration 077: Add pd_ref_order column

**Expected Impact**: ~46 issues resolved (requires re-import)

---

#### Fix #44: PhysicalLayer Attributes (26 issues)
**Commit**: `635f6be` feat(pqa): Fix #44 - PhysicalLayer physics and baudrate attributes

**Problem**: PhysicalLayer missing `physics` attribute. Also, parser looked for `bitrate` but IODD uses `baudrate`.

**Changes**:
- Model: Add physics field to CommunicationProfile
- Parser: Extract physics attribute, fix baudrate extraction
- Storage: Save physics to communication_profile table
- Reconstruction: Output physics attr, change bitrate to baudrate
- Migration 078: Add physics column

**Expected Impact**: ~26 issues resolved (requires re-import)

---

#### Fix #45: Datatype@subindexAccessSupported (21 issues)
**Commit**: `88926ba` fix(pqa): Fix #45 - Datatype@subindexAccessSupported for false values

**Problem**: DatatypeCollection/Datatype subindexAccessSupported only output when true, not when false.

**Changes**:
- Reconstruction: Check for `is not None` instead of truthy value

**Expected Impact**: ~21 issues resolved (no re-import needed)

---

#### Fix #46: Event@mode (18 issues)
**Commit**: `c5abfe2` feat(pqa): Fix #46 - Event@mode attribute

**Problem**: Event and StdEventRef missing `mode` attribute (e.g., "AppearDisappear").

**Changes**:
- Model: Add mode field to Event
- Parser: Extract mode from StdEventRef and Event elements
- Storage: Save mode to events table
- Reconstruction: Output mode attribute on both element types
- Migration 079: Add mode column

**Expected Impact**: ~18 issues resolved (requires re-import)

---

#### Fix #49: CommNetworkProfile@compatibleWith (11 issues)
**Commit**: `25ca568` fix(pqa): Fix #49 - CommNetworkProfile@compatibleWith attribute

**Problem**: CommNetworkProfile missing compatibleWith attribute (field was already extracted/stored, just not output).

**Changes**:
- Reconstruction: Output compatibleWith when present

**Expected Impact**: ~11 issues resolved (no re-import needed)

---

### Commits Summary (Session 2025-11-23)

1. `1bbd604` feat(pqa): Fix #41 - ProcessDataRecordItemInfo ordering
2. `b9b9b85` feat(pqa): Fix #42 - ProcessDataRef ordering
3. `635f6be` feat(pqa): Fix #44 - PhysicalLayer physics and baudrate attributes
4. `88926ba` fix(pqa): Fix #45 - Datatype@subindexAccessSupported for false values
5. `c5abfe2` feat(pqa): Fix #46 - Event@mode attribute
6. `25ca568` fix(pqa): Fix #49 - CommNetworkProfile@compatibleWith attribute

### Expected Results After Re-import

| Issue Category | Count | Status |
|----------------|-------|--------|
| ProcessDataRecordItemInfo ordering | 233 | Requires re-import |
| ProcessDataRef ordering | 46 | Requires re-import |
| PhysicalLayer attributes | 26 | Requires re-import |
| subindexAccessSupported | 21 | No re-import needed |
| Event@mode | 18 | Requires re-import |
| compatibleWith | 11 | No re-import needed |
| **Total Fixed** | **355** | |

### Deferred Issues (42 remaining)
- Fix #43: SingleValue in StdRecordItemRef (42 issues) - Complex nested structure, requires significant new tables/parsing

### Migrations Added This Session
- 076: xml_order in process_data_ui_info
- 077: pd_ref_order in process_data_ui_info
- 078: physics in communication_profile
- 079: mode in events

---

### READY FOR RE-IMPORT

Re-import required to populate new fields for Fixes #41, #42, #44, #46.

After re-import, run PQA analysis to verify improvements. Expected final score should be very close to 100% for most IODD devices.

---

## REGRESSION FIXES (Session 2025-11-23 continued)

### Post Re-import Analysis - REGRESSIONS DISCOVERED

After re-import, scores went DOWN instead of up:
- 0 devices at 100% (was 88)
- 1136 total diffs (was 521)

Two major regressions identified:

### Fix #45 Regression: subindexAccessSupported output when not present (593 issues)

**Problem**: Parser stored `False` (0 in SQLite) when attribute was not present.
Reconstruction checked `is not None` which returned True for 0.

**Root Cause**: The parser was storing:
```python
subindex_access = datatype_elem.get('subindexAccessSupported', 'false').lower() == 'true'
```
This stored `False` (0) when attribute not present, but reconstruction checked:
```python
if dt['subindex_access_supported'] is not None:  # True for 0!
```

**Fix**: Changed parser to only store when attribute is actually present:
```python
subindex_access_attr = datatype_elem.get('subindexAccessSupported')
subindex_access = subindex_access_attr.lower() == 'true' if subindex_access_attr is not None else None
```

### Fix #44 Regression: bitrate vs baudrate attribute naming (296 issues)

**Problem**: Assumed all IODDs use `baudrate` attribute name, but some use `bitrate`.
- 148 `missing_attribute:PhysicalLayer@bitrate`
- 148 `extra_element:PhysicalLayer@baudrate`

**Root Cause**: Changed reconstruction from `bitrate` to `baudrate` without tracking which
attribute name was used in the original IODD.

**Fix**: Track which attribute name was used:
1. Added `uses_baudrate` field to CommunicationProfile model
2. Parser tracks which attribute was present (baudrate or bitrate)
3. Storage saves uses_baudrate flag
4. Reconstruction uses correct attribute name based on flag
5. Migration 080 adds uses_baudrate column

**Commit**: `48869e3` fix(pqa): Fix regressions from Fix #44 and Fix #45

### Migrations Added
- 080: uses_baudrate in communication_profile

### READY FOR RE-IMPORT (2nd attempt)

Re-import required to fix regressions and apply regression fixes.

---

### Post Re-import #2 Analysis (2025-11-23)

After re-import with regression fixes:
- 41 devices at 100% (was 0 with regressions)
- 840 total diffs
- Average score: 99.74%

**Issue discovered**: subindexAccessSupported fix still not working (593 issues remain)

**Root cause**: Storage layer was converting `None` to `0`:
```python
1 if getattr(datatype, 'subindex_access_supported', False) else 0
```
This made `None` become `0`, so reconstruction still output the attribute.

**Fix**: Changed storage to preserve `None`:
```python
subindex_val = getattr(datatype, 'subindex_access_supported', None)
subindex_db_val = None if subindex_val is None else (1 if subindex_val else 0)
```

**Commit**: `0e7dce9` fix(pqa): Preserve NULL for subindex_access_supported in storage

### READY FOR RE-IMPORT (3rd attempt)

Re-import required to store NULL for missing subindexAccessSupported attributes.

---

### Post Re-import #3 Analysis (2025-11-23)

**Results:**
- 95 devices at 100% (was 41)
- 247 total diffs (was 840)
- Average score: 99.90%

**subindexAccessSupported fix confirmed working** - 593 issues resolved!

**Remaining issues (247 total):**

| Issue | Count | Description |
|-------|-------|-------------|
| ProcessDataRecordItemInfo@offset | 60 | Incorrect offset values |
| RecordItem/SimpleDatatype/SingleValue | 23 | Missing SingleValue in RecordItems |
| ProcessDataRecordItemInfo@gradient | 21 | Incorrect gradient values |
| ProcessDataIn Datatype vs DatatypeRef | 30 | Using inline Datatype instead of DatatypeRef |
| ProfileHeader values | 39 | ProfileIdentification/Name/Revision changes |
| DeviceName extras | 13 | Extra DeviceName elements |
| ErrorTypeCollection | 9 | Missing ErrorTypeCollection |
| Features@dataStorage | 7 | Missing dataStorage attribute |
| DeviceVariant revisions | 14 | Missing firmware/hardware revision |
| Various SingleValue | 17 | SingleValue in StdRecordItemRef etc |
| Datatype encoding/fixedLength | 10 | Missing encoding/fixedLength attrs |
| Other | 4 | deviceId, bitLength, etc |

---

### Fix #54: ProfileHeader Hardcoded Values (39 issues)
**Commit**: (pending)

**Problem**: ProfileHeader values (ProfileIdentification, ProfileRevision, ProfileName) were hardcoded in reconstruction instead of using the original values from the IODD.
- Original IODD might have different values like "IO Device Profile (1.1)" or custom identification strings
- Reconstruction always output "IO Device Profile", "1.1", "Device Profile for IO Devices"

**Changes Made**:
1. `src/models/__init__.py` - Added `profile_identification`, `profile_revision`, `profile_name` fields to DeviceProfile
2. `src/parsing/__init__.py` - Added `_extract_profile_header()` method to extract ProfileHeader values
3. `src/storage/iodd_file.py` - Save ProfileHeader values to iodd_files table
4. `src/utils/forensic_reconstruction_v2.py` - Updated `_create_profile_header()` to query stored values from database
5. `alembic/versions/082_add_profile_header_columns.py` - Add profile_identification, profile_revision, profile_name columns

**Expected Impact**: ~39 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #55: Extra DeviceName Elements (13 issues)
**Commit**: (pending)

**Problem**: DeviceName element was always output in DeviceIdentity reconstruction, even when the original IODD didn't have one. Some IODDs (like Murrelektronik 55518/55519 series) use ProductName/ProductText in DeviceVariant instead of DeviceName at DeviceIdentity level.

**Root Cause**: Reconstruction always created DeviceName and used lookup fallback when device_name_text_id was NULL. This caused extra DeviceName elements for 13 devices.

**Changes Made**:
1. `src/utils/forensic_reconstruction_v2.py` - Only output DeviceName when device_name_text_id is not NULL (indicating element was present in original)

**Expected Impact**: ~13 issues resolved (no re-import needed)

**Status**: COMMITTED

---

### Fix #56: ErrorTypeCollection Missing (9 issues)
**Commit**: (pending)

**Problem**: Some IODDs have an empty `<ErrorTypeCollection></ErrorTypeCollection>` element. The reconstruction was not outputting ErrorTypeCollection when there were no error types, causing 9 missing_element issues.

**Root Cause**: `_create_error_type_collection()` returned None when there were no error types in the database, without checking if the original IODD had an ErrorTypeCollection element.

**Changes Made**:
1. `src/models/__init__.py` - Added `has_error_type_collection` field to DeviceProfile
2. `src/parsing/__init__.py` - Added `_has_error_type_collection()` method to check if element exists
3. `src/storage/device.py` - Save has_error_type_collection flag to devices table
4. `src/utils/forensic_reconstruction_v2.py` - Output empty ErrorTypeCollection when flag is true but no error types exist
5. `alembic/versions/083_add_has_error_type_collection.py` - Add has_error_type_collection column

**Expected Impact**: ~9 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #57: Features@dataStorage Missing (7 issues)
**Commit**: (pending)

**Problem**: Features element `dataStorage` attribute was only output when value was "true", not when value was "false". Some IODDs have `dataStorage="false"` explicitly set.

**Root Cause**: Reconstruction checked `if features_row['data_storage']:` which evaluates to False for the boolean false value. Parser didn't track whether the attribute was present vs absent.

**Changes Made**:
1. `src/models/__init__.py` - Added `has_data_storage` field to DeviceFeatures
2. `src/parsing/__init__.py` - Track whether dataStorage attribute is present
3. `src/storage/document.py` - Save has_data_storage flag to device_features table
4. `src/utils/forensic_reconstruction_v2.py` - Output dataStorage only when has_data_storage is true
5. `alembic/versions/084_add_has_data_storage.py` - Add has_data_storage column

**Expected Impact**: ~7 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #58: DeviceVariant firmware/hardware revision (14 issues)
**Commit**: (pending)

**Problem**: DeviceVariant elements in some IODDs have `hardwareRevision` and `firmwareRevision` attributes that were not being extracted, stored, or reconstructed.

**Changes Made**:
1. `src/models/__init__.py` - Added `hardware_revision`, `firmware_revision` to DeviceVariant
2. `src/parsing/__init__.py` - Extract revision attributes from DeviceVariant elements
3. `src/storage/document.py` - Save revision attributes to device_variants table
4. `src/utils/forensic_reconstruction_v2.py` - Output revision attributes when present
5. `alembic/versions/085_add_device_variant_revisions.py` - Add revision columns

**Expected Impact**: ~14 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #59: Datatype encoding/fixedLength (10 issues)
**Commit**: (pending)

**Problem**: StringT and OctetStringT datatypes have `fixedLength` and `encoding` attributes that were not being extracted, stored, or reconstructed.

**Example**: `<Datatype xsi:type="StringT" fixedLength="16" encoding="UTF-8" />`

**Changes Made**:
1. `src/parsing/__init__.py` - Extract fixedLength and encoding from Datatype elements
2. `src/storage/custom_datatype.py` - Save string_fixed_length and string_encoding to custom_datatypes table
3. `src/utils/forensic_reconstruction_v2.py` - Output fixedLength and encoding attributes when present
4. `alembic/versions/086_add_datatype_encoding_fixedlength.py` - Add columns to custom_datatypes

**Expected Impact**: ~10 issues resolved (requires re-import)

**Status**: COMMITTED - Requires re-import to populate data

---

### Fix #60: ProcessDataRecordItemInfo gradient/offset decimal values (135 issues)
**Commit**: (pending)

**Problem**: Fix #50/#52 incorrectly converted gradient/offset to integers using `str(int(...))`. This truncated decimal values like `0.0007234` to `0`.

**Root Cause**: The original issues (#50/#52) were likely about different value formatting, but the fix overcorrected by forcing integer conversion on all gradient/offset values.

**Changes Made**:
1. `src/utils/forensic_reconstruction_v2.py` - Use `_format_number()` instead of `str(int(...))` for gradient/offset in two locations:
   - `_add_process_data_ui_info()` (line ~688)
   - `_create_user_interface()` ProcessDataRecordItemInfo (line ~1464)

**Expected Impact**: ~135 issues resolved (96 gradient + 39 offset)

**Status**: COMMITTED

---

## Session 2025-11-24 - Fixes #61-67

### Pre-session stats (247 files):
- Perfect (100%): 202
- Near perfect (99-100%): 45
- Total diffs: 210

---

### Fix #61: SingleValue xsi:type attribute (94 diffs)
**Commit**: `d355b2b`

**Problem**: SingleValue elements inside RecordItem/SimpleDatatype were missing xsi:type attribute (e.g., "BooleanValueT"). Affected both Variable and ProcessData collections.

**Changes Made**:
1. `src/parsing/__init__.py` - Extract xsi:type from SingleValue elements (2 locations)
2. `src/storage/process_data.py` - Save xsi_type to process_data_single_values
3. `src/storage/parameter.py` - Save xsi_type to record_item_single_values
4. `src/utils/forensic_reconstruction_v2.py` - Output xsi:type on SingleValue (2 locations)
5. `alembic/versions/088_add_single_value_xsi_type.py` - Add xsi_type columns

**Expected Impact**: ~94 issues resolved (requires re-import)

**Status**: COMMITTED

---

### Fix #62: deviceId leading zeros format (10 diffs)
**Commit**: `d7065f7`

**Problem**: deviceId values like "005" were being converted to integers, becoming "5" in reconstruction.

**Changes Made**:
1. `src/models/__init__.py` - Added device_id_str to DeviceInfo
2. `src/parsing/__init__.py` - Store original deviceId string
3. `src/storage/device.py` - Save device_id_str to devices table
4. `src/utils/forensic_reconstruction_v2.py` - Use device_id_str when available
5. `alembic/versions/089_add_device_id_str.py` - Add device_id_str column

**Expected Impact**: ~10 issues resolved (requires re-import)

**Status**: COMMITTED

---

### Fix #63: Extra bitLength on ProcessData/Datatype (7 diffs)
**Commit**: `fbec3ce`

**Problem**: bitLength was being output on both ProcessDataIn/Out element AND its child Datatype element, but original only had it on ProcessDataIn/Out.

**Changes Made**:
1. `src/utils/forensic_reconstruction_v2.py` - Removed bitLength output from Datatype element (it belongs on ProcessDataIn/Out)

**Expected Impact**: ~7 issues resolved (no re-import needed)

**Status**: COMMITTED

---

### Fix #65: RecordItem SimpleDatatype fixedLength/encoding (13+6 diffs)
**Commit**: `dc8f667`

**Problem**: fixedLength and encoding attributes on RecordItem/SimpleDatatype were not being extracted or stored for ProcessData RecordItems.

**Changes Made**:
1. `src/parsing/__init__.py` - Extract fixedLength and encoding from SimpleDatatype (2 locations)
2. `src/storage/process_data.py` - Save fixed_length and encoding to process_data_record_items

Note: Reconstruction already output these when present.

**Expected Impact**: ~19 issues resolved (~13 fixedLength + ~6 encoding) (requires re-import)

**Status**: COMMITTED

---

### Fix #66: Missing TextRedefine elements (12 diffs)
**Commit**: `a8f15bd`

**Problem**: TextRedefine elements (used to redefine standard text IDs like STD_TN_DeviceSpecific_*) were being output as Text elements.

**Changes Made**:
1. `src/models/__init__.py` - Added text_redefine_ids to DeviceProfile
2. `src/parsing/__init__.py` - Extract TextRedefine elements (marked with is_text_redefine)
3. `src/storage/text.py` - Save is_text_redefine to iodd_text table
4. `src/storage/__init__.py` - Pass text_redefine_ids to TextSaver
5. `src/utils/forensic_reconstruction_v2.py` - Output TextRedefine vs Text based on flag
6. `alembic/versions/090_add_is_text_redefine.py` - Add is_text_redefine column

**Expected Impact**: ~12 issues resolved (requires re-import)

**Status**: COMMITTED

---

### Fix #64: Missing SingleValue elements (14 diffs) - PENDING

**Problem**: Various SingleValue elements missing in reconstruction:
- StdRecordItemRef/SingleValue and StdSingleValueRef
- ProcessDataIn/Datatype/SingleValue
- DatatypeCollection/Datatype/SingleValue

**Note**: Requires additional model/parser/storage changes for StdRecordItemRef children. Deferred for now.

---

### Summary - Session 2025-11-24

| Fix | Issue | Count | Status |
|-----|-------|-------|--------|
| #61 | SingleValue xsi:type | 94 | COMMITTED |
| #62 | deviceId leading zeros | 10 | COMMITTED |
| #63 | Extra bitLength | 7 | COMMITTED |
| #65 | RecordItem fixedLength/encoding | 19 | COMMITTED |
| #66 | TextRedefine elements | 12 | COMMITTED |
| #64 | Missing SingleValue (StdRecordItemRef) | 14 | PENDING |

**Re-import required** to test fixes #61, #62, #65, #66
---

## Session 2025-11-24 (continued) - Fixes #68-69

### Post-reimport stats (247 files) after Fix #61-66:
- Perfect (100%): 216
- Near perfect (99-100%): 31
- Total diffs: 169

Note: Fix #63 caused a regression (210→691 diffs) and was reverted.

---

### Fix #63 Revert: bitLength needed on Datatype element
**Commit**: `d5c9f2e`

**Problem**: Fix #63 incorrectly removed bitLength from Datatype element, assuming it only belonged on ProcessDataIn/Out. Most IODDs actually have bitLength on BOTH elements.

**Impact**: Reverted. 691 diffs reduced back to ~169 diffs.

---

### Fix #68: Variable RecordItem SingleValue xsi:type (83 diffs)
**Commit**: `487e6ec`

**Problem**: Fix #61 added xsi:type extraction for ProcessData SingleValues but not for Variable RecordItem SingleValues. The storage and reconstruction code already handled xsi_type but the parser was missing extraction.

**Changes Made**:
1. `src/parsing/__init__.py` - Extract xsi:type from Variable RecordItem SingleValue elements in `_extract_variable_record_items()`

**Expected Impact**: ~83 issues resolved (requires re-import)

**Status**: COMMITTED

---

### Fix #69: DatatypeCollection RecordItem fixedLength/encoding (~11 diffs)
**Commit**: `da79dce`

**Problem**: fixedLength and encoding attributes on DatatypeCollection RecordItem/SimpleDatatype were not being extracted or stored.

**Changes Made**:
1. `src/parsing/__init__.py` - Extract fixedLength and encoding from SimpleDatatype in custom datatype RecordItems
2. `src/storage/custom_datatype.py` - Save fixed_length and encoding to custom_datatype_record_items
3. `src/utils/forensic_reconstruction_v2.py` - Output fixedLength and encoding when present

**Expected Impact**: ~11 issues resolved (requires re-import)

**Status**: COMMITTED

---

### Post-Fix #68 stats (247 files):
- Perfect (100%): 222
- Near perfect (99-100%): 25
- Total diffs: 86

---

### Remaining Issues Analysis (86 diffs):

| Issue | Count | Complexity |
|-------|-------|------------|
| Missing SingleValue in ProcessData/Datatype (direct children) | 6 | High - needs schema changes |
| Missing SingleValue in StdRecordItemRef | 5 | High - needs new model/storage |
| Missing StdSingleValueRef in StdRecordItemRef | 3 | High - same as above |
| Missing Name in Variable/Datatype | 4 | Medium |
| Extra bitLength on some ProcessData/Datatype | 5 | Medium - needs tracking |
| Missing SimpleDatatype in DatatypeCollection | 3 | Medium |
| Missing SingleValue in DatatypeCollection | 3 | Medium |
| Missing Name in ProcessData/Datatype | 3 | Medium |
| Extra VendorLogo elements | 2 | Low |
| mSequenceCapability format (01 vs 1) | 2 | Low - leading zeros |
| schemaLocation mismatch | 2 | Investigation needed |
| Missing Test element | 2 | Low |
| Missing ProductRef | 2 | Low |
| Various 1-off issues | ~11 | Low |

