# Window Exit Issue - Diagnostics & Solutions

## Problem

setup.bat window closes immediately after launch, even though `pause` command is present.

## Diagnostic Tests

### Test 1: Verify Pause Command Works

Run this simple test:
```cmd
test_pause.bat
```

**Expected**: Window shows message and "Press any key to continue..." and WAITS for keypress.

**If it closes immediately**: The `pause` command is not working in your environment.

### Test 2: Debug Setup.bat

Run the debug version:
```cmd
setup_debug.bat
```

This shows exactly where the script is failing or exiting.

### Test 3: Test Startup Only

Run minimal startup test:
```cmd
test_startup.bat
```

This tests if `python -m src.start` can launch at all.

## Potential Causes & Solutions

### Cause 1: Running Through Non-Interactive Shell

**Symptom**: Window closes without pause when run via `bash` or programmatically.

**Solution**: Double-click `setup.bat` directly in Windows Explorer instead of running via terminal.

### Cause 2: Error During Startup

**Symptom**: Application fails before reaching the main loop.

**Check**:
1. Run `setup_debug.bat` to see exact error
2. Check if Python dependencies are installed
3. Verify `src/start.py` exists

**Solution**: Fix the error shown in debug output.

### Cause 3: Want Window to Stay Open Permanently

**Symptom**: You want the window to stay open even after pressing a key.

**Solution**: Use the persistent version:
```cmd
scripts\setup_persistent.bat
```

This version:
- Runs all cleanup and launch steps
- **Never closes automatically**
- Opens a command prompt (`cmd /k`) after app stops
- You must type `exit` to close window

### Cause 4: Pause Requires Keypress

**Symptom**: Window pauses but closes when you press any key.

**Expected Behavior**: This is normal! The `pause` command waits for keypress, then exits.

**If you want it to stay open**: Use `setup_persistent.bat` instead.

## Current setup.bat Behavior

**Correct flow**:
1. Runs cleanup (kill backends, clear cache)
2. Checks Python
3. Installs dependencies
4. Launches `python -m src.start`
5. App runs until you press **Ctrl+C**
6. Shows status message
7. **Pauses** with "Press any key to continue..."
8. **Exits** when you press a key

## Alternative Versions

### 1. Original setup.bat (with pause)
```cmd
scripts\setup.bat
```
- Pauses after app stops
- Exits when you press any key

### 2. Persistent Window (NEVER exits)
```cmd
scripts\setup_persistent.bat
```
- Same cleanup and launch
- Opens command prompt after app stops
- Window stays open until you type `exit`
- **Recommended if you want window to stay open**

### 3. Debug Version (diagnostic output)
```cmd
setup_debug.bat
```
- Shows detailed execution steps
- Helps identify where failures occur

## Verification

After pulling latest changes, verify the pause is in the file:

```cmd
findstr /n "pause" scripts\setup.bat
```

Should show:
```
80:    pause
99:    pause
190:pause
```

Line 190 is the critical one at the end.

## If Issue Persists

If window still closes immediately even with `test_pause.bat`, please provide:

1. **How you're running it**:
   - [ ] Double-clicking in Windows Explorer
   - [ ] Running from CMD prompt
   - [ ] Running from PowerShell
   - [ ] Running from Git Bash
   - [ ] Other: _______________

2. **What you see**:
   - [ ] Window flashes and closes instantly
   - [ ] Window shows messages then closes without "Press any key..."
   - [ ] Window shows "Press any key..." but closes when I press a key (THIS IS EXPECTED)
   - [ ] Other: _______________

3. **Output of test_pause.bat**:
   - Does it pause? YES / NO

4. **Output of setup_debug.bat**:
   - What was the last message shown before window closed?

## Recommended Solution

**Use `setup_persistent.bat` if you want window to stay open permanently without requiring a keypress to exit.**

This version uses `cmd /k` at the end, which keeps the command prompt open indefinitely.
