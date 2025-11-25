@echo off
setlocal enabledelayedexpansion
title GreenStack - Quick Setup (Persistent Window)

:: Change to project root directory
cd /d "%~dp0\.."

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 GREENSTACK - QUICK SETUP                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: ============================================================================
:: STEP 1: Clean Restart - Stop existing backends and clear cache
:: ============================================================================
echo [1/6] Cleaning up existing backend instances...

:: Find and kill processes using port 8000 (GreenStack backend)
set "BACKEND_KILLED=0"
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    set PID=%%a
    if defined PID (
        taskkill /F /PID !PID! >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo   Stopped backend process (PID: !PID!)
            set "BACKEND_KILLED=1"
        )
    )
)

:: Also check for python processes running src.api
wmic process where "commandline like '%%src.api%%'" get processid 2>nul | findstr /r "[0-9]" >nul
if %ERRORLEVEL% EQU 0 (
    echo   Stopping src.api processes...
    for /f "tokens=1" %%a in ('wmic process where "commandline like '%%src.api%%'" get processid ^| findstr /r "[0-9]"') do (
        taskkill /F /PID %%a >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo   Stopped src.api process (PID: %%a)
            set "BACKEND_KILLED=1"
        )
    )
)

if "%BACKEND_KILLED%"=="0" (
    echo   No existing backend processes found.
) else (
    echo   Existing backends stopped.
    timeout /t 2 /nobreak >nul
)
echo.

:: Clear Python bytecode cache
echo [2/6] Clearing Python bytecode cache...

:: Delete all __pycache__ directories in src
if exist "%CD%\src\__pycache__" (
    rmdir /s /q "%CD%\src\__pycache__" 2>nul
    echo   Cleared root __pycache__
)

:: Use Python to clear cache directories (more reliable)
python -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('src').rglob('__pycache__')]; print('   Python cache cleared')" 2>nul

echo.

:: ============================================================================
:: STEP 2: Check Python installation
:: ============================================================================
echo [3/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [ERROR] Python is not installed. Please install Python 3.8+ first.
    echo   Download from: https://www.python.org/downloads/
    goto :stay_open
)

for /f "tokens=*" %%i in ('python --version') do echo   Found: %%i
echo.

:: ============================================================================
:: STEP 3: Install dependencies
:: ============================================================================
echo [4/6] Installing Python dependencies...
python -m pip install -r requirements.txt >nul 2>&1
if %errorlevel% equ 0 (
    echo   Dependencies installed!
) else (
    echo   Installing dependencies with output...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo   [ERROR] Failed to install dependencies!
        goto :stay_open
    )
)
echo.

:: ============================================================================
:: STEP 4: Skip Redis and Stats for faster startup
:: ============================================================================
echo [5/6] Skipping Redis check (using in-memory mode)...
echo   Redis step skipped for faster startup.
echo.

echo [6/6] Skipping stats update (non-critical)...
echo   Stats will update on first API call.
echo.

:: ============================================================================
:: Launch the application
:: ============================================================================
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 LAUNCHING GREENSTACK...                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo   • API Server: http://localhost:8000
echo   • Web Interface: http://localhost:6173 (auto-detects next open port)
echo   • API Documentation: http://localhost:8000/docs
echo.
echo   Press Ctrl+C to stop the application
echo   (Window will remain open after stopping)
echo.
echo ══════════════════════════════════════════════════════════════
echo.

:: Start the application
python -m src.start
set START_EXIT_CODE=%errorlevel%

:: ALWAYS stay open after application stops
:stay_open
echo.
echo ══════════════════════════════════════════════════════════════

if defined START_EXIT_CODE (
    if %START_EXIT_CODE% equ 0 (
        echo   Application stopped gracefully (Ctrl+C pressed)
    ) else (
        echo   [ERROR] Application exited with error code: %START_EXIT_CODE%
        echo   Check the messages above for details
    )
) else (
    echo   Setup encountered an error - see messages above
)

echo ══════════════════════════════════════════════════════════════
echo.
echo This window will remain open. You can:
echo   - Review messages above
echo   - Run commands manually
echo   - Type 'exit' to close this window
echo.

:: Open a command prompt instead of exiting
cmd /k
