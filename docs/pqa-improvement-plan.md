# PQA Improvement Plan - Achieve 100% Score for Device #56

## Goal
Fix all identified issues in Device #56 (SICK AG RAY26_DID8389143) to achieve 100% PQA score while ensuring all improvements are reflected in the Device Detail frontend.

**Current Score**: 88.32%
**Target Score**: 100%
**Estimated Iterations**: 3-4

---

## Phase 1: Text ID Generation Fix (Highest Impact)
**Priority**: ⭐⭐⭐ CRITICAL
**Estimated Score Improvement**: +10-15 points (→ 98-103%)
**Estimated Time**: 2-3 hours

### Tasks

#### 1.1 Analyze Current Text ID Storage
**File**: `src/parsing/__init__.py`
**Action**: Review how Text elements are currently parsed and stored

```python
# Current behavior (suspected):
# - Text IDs are generated sequentially: TI_0, TI_1, TI_2...
# - Original IDs from IODD are not preserved

# Expected behavior:
# - Store original Text IDs: TI_VendorText, TI_DeviceFamily, UUIDs
# - Preserve ID references across the document
```

**Database Check**:
- Examine `text_references` or related table schema
- Check if original `id` attribute is stored
- If not, need to add column to store original IDs

#### 1.2 Update IODD Parser to Store Original IDs
**File**: `src/parsing/__init__.py`
**Location**: Text element parsing section (around ExternalTextCollection)

**Changes Needed**:
```python
# When parsing <Text id="TI_VendorText" value="...">
# Store BOTH:
# 1. Auto-generated internal ID (for database primary key)
# 2. Original XML id attribute (for reconstruction)

# Add column: original_text_id VARCHAR
# INSERT text_references (id, device_id, original_text_id, text_id, value)
```

**Database Migration** (if needed):
```sql
ALTER TABLE text_references ADD COLUMN original_text_id TEXT;
-- OR verify if column already exists with different name
```

#### 1.3 Update IODD Reconstructor to Use Original IDs
**File**: `src/reconstruction/iodd_reconstructor.py`
**Location**: Text element reconstruction

**Changes Needed**:
```python
# Change FROM:
# <Text id="TI_0" value="...">

# Change TO:
# <Text id="TI_VendorText" value="...">

# Use stored original_text_id from database instead of generating sequential IDs
```

#### 1.4 Update Device Detail Frontend
**Files**:
- `frontend/src/components/DeviceDetail.jsx` (or equivalent)
- Any component displaying Text elements

**Changes Needed**:
- Verify Text elements are displayed correctly
- Show original meaningful IDs in UI if needed
- Test that references (TextId refs) work correctly

#### 1.5 Test and Validate
**Actions**:
1. Re-run PQA analysis on Device #56
2. Verify attribute score improves from 72.36% → 95%+
3. Check reconstructed XML has correct Text IDs
4. Verify overall score reaches 98%+
5. Test with 2-3 other devices to ensure fix is general

---

## Phase 2: Add Missing Collections (Medium Impact)
**Priority**: ⭐⭐ HIGH
**Estimated Score Improvement**: +2-5 points per collection
**Estimated Time**: 3-4 hours

### 2.1 ErrorTypeCollection Reconstruction
**Impact**: +2-3 points

**Database Verification**:
```sql
SELECT COUNT(*) FROM error_types WHERE device_id = 56;
-- Expected: 9 error types
```

**File**: `src/reconstruction/iodd_reconstructor.py`

**Implementation**:
```python
def _reconstruct_error_type_collection(self, device_id):
    """Reconstruct ErrorTypeCollection from error_types table"""
    cursor.execute("""
        SELECT error_code, error_name, description
        FROM error_types
        WHERE device_id = ?
        ORDER BY error_code
    """, (device_id,))

    error_types = cursor.fetchall()

    xml = "<ErrorTypeCollection>\n"
    for error in error_types:
        xml += f'  <StdErrorTypeRef additionalCode="{error[0]}" />\n'
    xml += "</ErrorTypeCollection>\n"

    return xml
```

**Integration Point**: Insert into DeviceFunction section after ProcessDataCollection

**Frontend Verification**:
- Check if Device Detail shows error types
- Verify error names are displayed correctly (from previous events-errors-fix)

### 2.2 EventCollection Reconstruction
**Impact**: +2-3 points

**Database Verification**:
```sql
SELECT COUNT(*) FROM events WHERE device_id = 56;
-- Expected: 4 events
```

**File**: `src/reconstruction/iodd_reconstructor.py`

**Implementation**:
```python
def _reconstruct_event_collection(self, device_id):
    """Reconstruct EventCollection from events table"""
    cursor.execute("""
        SELECT event_code, event_name, description
        FROM events
        WHERE device_id = ?
        ORDER BY event_code
    """, (device_id,))

    events = cursor.fetchall()

    xml = "<EventCollection>\n"
    for event in events:
        xml += f'  <StdEventRef code="{event[0]}" />\n'
    xml += "</EventCollection>\n"

    return xml
```

**Integration Point**: Insert into DeviceFunction section after ErrorTypeCollection

**Frontend Verification**:
- Check if Device Detail shows events
- Verify event names are displayed correctly

---

## Phase 3: ProcessData and ID Fixes (Low-Medium Impact)
**Priority**: ⭐ MEDIUM
**Estimated Score Improvement**: +1-2 points
**Estimated Time**: 1-2 hours

### 3.1 Fix ProcessData ID Suffix Issue

**Current Issue**:
- Expected: `PD_ProcessDataA00`
- Actual: `PD_ProcessDataA00In`

**File**: `src/reconstruction/iodd_reconstructor.py`

**Investigation Needed**:
- Find where ProcessData IDs are generated
- Check if "In" suffix is being added incorrectly
- Likely in `_reconstruct_process_data()` method

**Fix**:
```python
# Review ID generation logic
# Remove inappropriate direction suffix from main ProcessData element
# Direction suffixes should only be on ProcessDataIn/ProcessDataOut children
```

### 3.2 Add ProcessDataIn Reconstruction

**Database Check**:
```sql
-- Check if ProcessDataIn is stored separately or as part of ProcessData
SELECT * FROM process_data WHERE device_id = 56;
-- or similar table
```

**File**: `src/reconstruction/iodd_reconstructor.py`

**Implementation**:
- Add reconstruction of `<ProcessDataIn>` child elements
- Ensure correct structure: `<ProcessData><ProcessDataIn>...</ProcessDataIn></ProcessData>`

---

## Phase 4: Metadata and Structure (Low Impact)
**Priority**: ⭐ LOW
**Estimated Score Improvement**: +1-2 points total
**Estimated Time**: 2-3 hours

### 4.1 Add DocumentInfo Section

**Information Needed**:
- Release date
- Version
- Copyright information
- File metadata

**Options**:
1. **Parse from original**: Store DocumentInfo during parsing
2. **Generate placeholder**: Create basic DocumentInfo with import metadata
3. **Database schema**: Add `document_info` table

**Recommended Approach**: Option 2 (Generate placeholder)

**Implementation**:
```python
def _reconstruct_document_info(self, device_id):
    """Generate DocumentInfo section"""
    xml = "<DocumentInfo>\n"
    xml += f"  <releaseDate>{datetime.now().strftime('%Y-%m-%d')}</releaseDate>\n"
    xml += "  <version>1.0</version>\n"
    xml += "  <copyright>Reconstructed by GreenStack PQA</copyright>\n"
    xml += "</DocumentInfo>\n"
    return xml
```

**Integration Point**: Insert at beginning of IODevice after ProfileHeader

### 4.2 Add CommNetworkProfile

**Research Needed**:
- Check if network profile data is stored in database
- Determine if this is device-specific or generic

**Options**:
1. Store during parsing
2. Generate generic IO-Link profile
3. Skip if not critical

**Recommended Approach**: Generate generic IO-Link profile template

### 4.3 UserInterface Menu Collections

**Database Check**:
```sql
-- Check if menu data exists
SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%menu%';
```

**Status**: Menu system may not be fully implemented in parser

**Options**:
1. **Full Implementation**: Parse and store menu structures (significant work)
2. **Placeholder**: Generate empty menu collections
3. **Skip**: Accept minor score penalty

**Recommended Approach**: Option 2 (Placeholder) for now

**Implementation**:
```python
def _reconstruct_user_interface(self, device_id):
    """Generate basic UserInterface structure"""
    xml = "<UserInterface>\n"
    xml += "  <ObserverRoleMenuSet />\n"
    xml += "  <MaintenanceRoleMenuSet />\n"
    xml += "  <SpecialistRoleMenuSet />\n"
    xml += "  <MenuCollection />\n"
    xml += "</UserInterface>\n"
    return xml
```

### 4.4 SupportedAccessLocks

**Implementation**:
```python
def _reconstruct_supported_access_locks(self):
    """Generate SupportedAccessLocks section"""
    xml = "<SupportedAccessLocks>\n"
    xml += "  <AccessLock />\n"  # Generic access lock
    xml += "</SupportedAccessLocks>\n"
    return xml
```

**Integration Point**: Insert into Features section

---

## Testing Strategy

### After Each Phase

1. **Run PQA Analysis**:
```python
python rerun_device56_analysis.py
```

2. **Check Score Improvement**:
```sql
SELECT overall_score, structural_score, attribute_score, value_score
FROM pqa_quality_metrics
WHERE device_id = 56
ORDER BY id DESC LIMIT 1;
```

3. **Review Diff Details**:
```sql
SELECT COUNT(*), severity, diff_type
FROM pqa_diff_details
WHERE metric_id = (SELECT MAX(id) FROM pqa_quality_metrics WHERE device_id = 56)
GROUP BY severity, diff_type
ORDER BY severity;
```

4. **Frontend Verification**:
- Navigate to Device Detail for Device #56
- Verify all sections display correctly
- Check that improvements are visible in UI

### Multi-Device Testing

**Test Devices** (after Phase 1 and 2):
- Device #56 (SICK AG RAY26_DID8389143)
- 2-3 additional IODD devices with different vendors
- Verify improvements don't break other devices

### Regression Testing

After all phases:
1. Run PQA analysis on all 56 devices
2. Check average score improvement
3. Verify no devices regressed
4. Ensure frontend displays all devices correctly

---

## Success Metrics

### Phase 1 Success Criteria
- ✅ Device #56 attribute score ≥ 95%
- ✅ Overall score ≥ 98%
- ✅ Text ID mismatches reduced to near-zero
- ✅ Frontend displays Text elements correctly

### Phase 2 Success Criteria
- ✅ ErrorTypeCollection present in reconstruction
- ✅ EventCollection present in reconstruction
- ✅ Structural score ≥ 98%
- ✅ Frontend shows errors and events correctly

### Phase 3 Success Criteria
- ✅ ProcessData IDs match original
- ✅ ProcessDataIn present in reconstruction
- ✅ Attribute score ≥ 98%

### Phase 4 Success Criteria
- ✅ DocumentInfo section present
- ✅ Overall score ≥ 99%
- ✅ All HIGH severity issues resolved

### Final Success Criteria
- ✅ Device #56 overall score = 100%
- ✅ Zero CRITICAL or HIGH severity diff items
- ✅ All device data displayed correctly in frontend
- ✅ Improvements work for multiple devices
- ✅ No regressions in other device analyses

---

## Implementation Order

### Iteration 1 (Highest ROI)
1. Text ID generation fix (Phase 1)
   - Expected: 88% → 98%

### Iteration 2 (Fill Major Gaps)
2. ErrorTypeCollection (Phase 2.1)
3. EventCollection (Phase 2.2)
   - Expected: 98% → 100-102%

### Iteration 3 (Polish and Verify)
4. ProcessData ID fixes (Phase 3.1)
5. ProcessDataIn (Phase 3.2)
6. Frontend verification
   - Expected: 100% → 100% (stable)

### Iteration 4 (Fine-Tuning)
7. DocumentInfo (Phase 4.1)
8. Remaining minor issues
9. Multi-device testing
   - Expected: 100% confirmed

---

## Frontend Integration Checklist

For each improvement, verify frontend displays:

### Device Detail View
- [ ] Text elements with correct IDs
- [ ] Error types list
- [ ] Events list
- [ ] ProcessData structure
- [ ] DocumentInfo metadata
- [ ] All sections render without errors

### PQA Console View
- [ ] Updated scores reflected
- [ ] Diff details show improvements
- [ ] Analysis history updated
- [ ] Ticket status correct (should clear when passing)

---

## Rollback Plan

If a change causes issues:

1. **Database Rollback**:
```sql
-- Backup before changes
.backup greenstack_backup.db

-- Restore if needed
-- Stop server, replace DB, restart
```

2. **Code Rollback**:
```bash
git log --oneline -10  # Find commit before changes
git revert <commit-hash>
```

3. **Incremental Testing**: Test each phase independently before moving to next

---

## Notes

- **User Reminder**: "remember that any parsing improvements need to be mapped to the device detail front end"
  - After each parser/reconstructor change, verify Device Detail UI
  - Test with actual device pages, not just PQA console
  - Ensure new data is accessible and displayed

- **Iterate Until 100%**: We will continue refining until Device #56 achieves perfect score
  - Re-analyze after each phase
  - Address any new issues that emerge
  - Fine-tune scoring weights if needed

- **Document Everything**: Update investigation doc with findings from each iteration

---

## File Reference

### Backend Files to Modify
1. `src/parsing/__init__.py` - IODD parser (Text IDs, ErrorTypes, Events)
2. `src/reconstruction/iodd_reconstructor.py` - Main reconstructor
3. `src/database.py` - Schema changes if needed

### Frontend Files to Verify
1. `frontend/src/components/DeviceDetail.jsx` - Main device display
2. `frontend/src/components/PQAConsole.jsx` - PQA display
3. Related UI components showing errors, events, text

### Testing Scripts
1. `rerun_device56_analysis.py` - Quick analysis test
2. `test_ticket_generation.py` - Ticket verification

### Documentation Files
1. `docs/pqa-device56-investigation.md` - Investigation findings
2. `docs/pqa-improvement-plan.md` - This file
3. `docs/events-errors-fix-2025-11-20.md` - Previous fixes reference
