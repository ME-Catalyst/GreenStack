# Fix #86-92 Testing Plan - Clean Setup Method

## Objective
Verify that Fix #86-92 (Menu duplicate elimination) works correctly when launching via clean setup.bat

## Pre-Test Verification

### Current State
- ✅ Parser code has Fix #86-92 applied (verified in src/parsing/__init__.py)
- ✅ Parser test produces 0 duplicates (test_fix86_parser.py passes)
- ❌ Database has 6x duplicates (from stale backend code during upload)
- ✅ Database has 247 devices, IDs 1-247

### What Was Fixed in setup.bat
1. **Backend Cleanup** (NEW):
   - Kills all processes on port 8000
   - Kills all python processes running src.api
   - Ensures no stale backend instances

2. **Cache Cleanup** (NEW):
   - Clears all __pycache__ directories in src/
   - Ensures fresh Python code loads

3. **Clean Start**:
   - Launches ONE fresh backend instance
   - All code loaded from disk (not stale cache)

## Test Procedure

### Phase 1: Clean Shutdown
```bash
# Manually kill any existing backends
scripts\shutdown_server.bat

# Verify no backends running
netstat -ano | findstr ":8000"
# (Should return nothing)
```

### Phase 2: Launch via setup.bat
```bash
# This will:
# - Kill any existing backends
# - Clear Python cache
# - Start fresh backend
scripts\setup.bat
```

**Wait for**: "Application startup complete" in terminal

### Phase 3: Delete All Devices
1. Navigate to: http://localhost:8000/admin
2. Click "Database Management"
3. Click "Delete All Devices"
4. **Verify**: Message shows "Deleted 247 devices"

### Phase 4: Verify Clean Database
```bash
python verify_delete.py
```

**Expected Output**:
```
[OK]   IODD Devices                  :      0 rows
[OK]   UI Menus                      :      0 rows
[OK]   UI Menu Items                 :      0 rows
[SUCCESS] Database is completely empty - delete worked correctly!
```

### Phase 5: Upload IODD Packages
1. Navigate to: http://localhost:8000/upload
2. Select ALL .zip files from: `test-data/iodd-files/`
3. Click "Upload"
4. **Wait** for upload to complete (watch backend terminal)

**Expected Backend Logs**:
```
INFO:src.parsing:Extracted X menus
INFO:src.storage.device:Saved device: ... (ID: 1)
INFO:src.storage.device:Saved device: ... (ID: 2)
...
INFO:src.storage.device:Saved device: SL-x-TRIO IOLINK (ID: 186)
```

### Phase 6: Verify Fix #86-92
```bash
python check_import_results.py
```

**Expected Output** (SUCCESS):
```
[3] Menu Duplicate Check (Fix #86-92):
    Testing: SL-x-TRIO IOLINK (ID: 186)
    [PASS] NO duplicate variable_ids found!
    Status: Fix #86-92 WORKING CORRECTLY

[4] Total Diffs Across All Files: ~159

[5] Expected vs Actual:
    Before Fix #86-92: 299 diffs, 229 perfect files (92.7%)
    After Fix #86-92:  159 diffs, 235 perfect files (95.1%)
    Result: [SUCCESS] Reduced by 140 diffs - Fix #86-92 working!
```

## Success Criteria

### Must Pass (Critical)
- [ ] No duplicate variable_ids in SL-x-TRIO device (ID: 186)
- [ ] Total diffs reduced from 299 to ~159 (-140 diffs)
- [ ] Perfect files increased from 229 to ~235 (+6 files)

### Should Pass (Important)
- [ ] No duplicate menu items in ANY device
- [ ] Backend logs show "Extracted X menus" (not "Extracted 0 menus")
- [ ] PQA overall score improves to ~99.96% average

### Nice to Have
- [ ] Only ONE backend process running (no duplicates)
- [ ] Device IDs start at 1 and are sequential

## Failure Analysis

### If Fix #86-92 Still Shows Duplicates

**Check 1**: Verify backend is using new code
```bash
python check_parser_in_memory.py
```
Should show: `[PASS] Fix #86-92 IS loaded in memory!`

**Check 2**: Verify only ONE backend running
```bash
netstat -ano | findstr ":8000"
```
Should show only ONE PID

**Check 3**: Check backend startup logs
Look for:
```
INFO:     Started server process [XXXXX]
INFO:     Application startup complete.
```
Should appear ONCE (not multiple times)

### If Database Not Empty After Delete

**Check**: WAL checkpoint
```bash
python fix_wal_mode.py
```
Should show: `Device Count: 0`

### If Upload Doesn't Start at ID 1

**Cause**: Database wasn't empty
**Fix**: Manually run:
```bash
python verify_delete.py
```
Then re-upload.

## Rollback Plan

If testing fails:
1. Note exact failure point
2. Collect logs: backend terminal output
3. Run diagnostics: `check_import_results.py`, `check_parser_in_memory.py`
4. Report findings
5. Continue with current database (299 diffs) and work on other fixes

## Timeline

- **Phase 1-2**: 2 minutes (shutdown + setup.bat launch)
- **Phase 3-4**: 1 minute (delete + verify)
- **Phase 5**: 5-10 minutes (upload 247 files)
- **Phase 6**: 1 minute (verification)

**Total**: ~10-15 minutes

## Expected Outcome

**If Successful**:
- Menu duplicates eliminated (Fix #86-92 working)
- -140 diffs reduction (47% improvement)
- Ready to proceed with Phase 2 fixes (#93-98)

**If Failed**:
- Document exact failure mode
- Investigate root cause
- May need deeper investigation into Python module caching or process management

---

**Ready to test**: Awaiting user confirmation to proceed with test plan.
