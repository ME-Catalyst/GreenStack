# setup.bat Usage Guide

## Overview

`scripts/setup.bat` provides a **clean, automated launch** for GreenStack with built-in cleanup to ensure no stale code or processes interfere with operation.

## What It Does

### Phase 1-2: Clean Restart (NEW - Fix #86-92 Related)

**Step 1: Kill Existing Backends**
- Stops ALL processes on port 8000
- Kills ALL `src.api` Python processes
- Ensures no duplicate backend instances

**Step 2: Clear Python Cache**
- Removes all `__pycache__` directories in `src/`
- Ensures fresh code loads (no stale .pyc files)

### Phase 3-6: Environment Setup

**Step 3: Python Check**
- Verifies Python 3.8+ is installed
- Shows Python version

**Step 4: Install Dependencies**
- Runs `pip install -r requirements.txt`
- Ensures all required packages present

**Step 5: Redis Setup**
- Checks if Redis running on localhost:6379
- Starts Redis container via Docker if needed
- Falls back to in-memory mode if unavailable

**Step 6: Update Statistics**
- Refreshes codebase statistics cache

### Phase 7: Launch Application

**Launches `python -m src.start`** which:
- Starts backend API server (port 8000)
- Starts frontend dev server (port 6173+)
- Opens browser to web interface
- Runs until Ctrl+C pressed

**Exit Handling (FIXED)**:
- Window now stays open after app stops
- Shows "Application stopped gracefully" or error message
- Displays exit code
- Waits for keypress before closing

## How to Use

### Basic Launch

```cmd
scripts\setup.bat
```

This will:
1. Clean up any existing backend processes
2. Clear Python bytecode cache
3. Verify/install dependencies
4. Start Redis if needed
5. Launch GreenStack
6. Open browser to web interface

**Press Ctrl+C to stop** - window will stay open for review.

### What You Should See

```
╔══════════════════════════════════════════════════════════════╗
║                 GREENSTACK - QUICK SETUP                     ║
╚══════════════════════════════════════════════════════════════╝

[1/6] Cleaning up existing backend instances...
   Stopped backend process (PID: 12345)
   Existing backends stopped.

[2/6] Clearing Python bytecode cache...
   Cleared 42 cache directories.

[3/6] Checking Python installation...
   Found: Python 3.14.0

[4/6] Installing Python dependencies...
   Dependencies installed!

[5/6] Ensuring Redis (localhost:6379) is running...
   Redis already running.

[6/6] Updating codebase statistics...
   Statistics updated!

╔══════════════════════════════════════════════════════════════╗
║                 LAUNCHING GREENSTACK...                      ║
╚══════════════════════════════════════════════════════════════╝

   • API Server: http://localhost:8000
   • Web Interface: http://localhost:6173 (auto-detects next open port)
   • API Documentation: http://localhost:8000/docs

   Press Ctrl+C to stop the application

══════════════════════════════════════════════════════════════

[Application starts and runs...]

[User presses Ctrl+C]

══════════════════════════════════════════════════════════════
   Application stopped gracefully
══════════════════════════════════════════════════════════════

Press any key to continue . . .
```

## Troubleshooting

### Window Closes Immediately

**This is now FIXED** in commit `94f8220`.

If you still experience this:
1. Pull latest changes: `git pull`
2. Verify fix applied: `python verify_setup_functionality.py`
3. Check output shows: `[OK] Pause on exit`

### Port 8000 Already in Use

The script automatically kills processes on port 8000, but if it fails:

```cmd
scripts\shutdown_server.bat
```

Then try `setup.bat` again.

### Multiple Backend Instances

If you see duplicate uploads or inconsistent behavior:

```cmd
# Check for multiple backends
netstat -ano | findstr ":8000"

# Kill all backends
scripts\shutdown_server.bat

# Launch clean
scripts\setup.bat
```

### Python Cache Issues

If changes to code aren't reflected:

```cmd
# Clear cache manually
scripts\clear_cache.bat

# Or restart via setup.bat (clears automatically)
scripts\setup.bat
```

## Testing Fix #86-92

The clean restart in setup.bat is **critical** for testing Fix #86-92 (menu duplicates).

**Correct test procedure**:

1. **Close ALL backend instances**
   ```cmd
   scripts\shutdown_server.bat
   ```

2. **Launch via setup.bat** (ensures clean start)
   ```cmd
   scripts\setup.bat
   ```

3. **Wait for "Application startup complete"** in terminal

4. **Delete all devices** via GUI
   - Navigate to http://localhost:8000/admin
   - Click "Delete All Devices"
   - Verify "Deleted 247 devices" message

5. **Verify database empty**
   ```cmd
   python verify_delete.py
   ```

6. **Upload ALL IODD packages**
   - Navigate to http://localhost:8000/upload
   - Select all .zip files from `test-data/iodd-files/`
   - Click "Upload"
   - Wait for completion (watch backend terminal)

7. **Check results**
   ```cmd
   python check_import_results.py
   ```

**Expected results**:
- No menu duplicates
- ~159 total diffs (down from 299)
- ~235 perfect files (up from 229)

## Related Scripts

- `scripts/shutdown_server.bat` - Stop backend only (no restart)
- `scripts/restart_backend.bat` - Restart backend with cache clear
- `test_setup_cleanup.bat` - Test cleanup functions
- `verify_setup_functionality.py` - Validate setup.bat structure

## Verification

Run the verification script to check setup.bat health:

```cmd
python verify_setup_functionality.py
```

Should show:
```
[OK] Backend cleanup
[OK] Cache cleanup
[OK] Python check
[OK] Dependencies
[OK] Redis check
[OK] Stats update
[OK] Launch app
[OK] Error handling
[OK] Pause on exit
[OK] All checks passed
```

## Changes from Previous Version

**Commit `94f8220` - Fixed Window Exit Issue**

**Before**:
```batch
python -m src.start
if %errorlevel% neq 0 (
    echo [ERROR] Application failed to start!
    pause
    exit /b 1
)
goto :eof  # ← Window closes after Ctrl+C
```

**After**:
```batch
python -m src.start
set START_EXIT_CODE=%errorlevel%

echo ══════════════════════════════════════════════════════════════
if %START_EXIT_CODE% equ 0 (
    echo   Application stopped gracefully
) else (
    echo   [ERROR] Application exited with error code: %START_EXIT_CODE%
)
echo ══════════════════════════════════════════════════════════════

pause  # ← Window stays open
exit /b %START_EXIT_CODE%
```

**Result**: Window now **always** stays open with status message and waits for keypress.

---

**Ready for testing!** The setup.bat script is fully functional and will keep the window open after application stops.
