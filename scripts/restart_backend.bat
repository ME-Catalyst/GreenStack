@echo off
setlocal enabledelayedexpansion
REM ============================================================================
REM GreenStack Backend Restart Script
REM ============================================================================
REM This script:
REM 1. Stops the backend server (port 8000 only)
REM 2. Clears Python bytecode cache
REM 3. Starts the backend server fresh
REM ============================================================================

echo.
echo ============================================================================
echo  GreenStack Backend Restart
echo ============================================================================
echo.

REM Step 1: Stop backend server
echo [1/3] Stopping backend server...
call "%~dp0shutdown_server.bat"

REM Step 2: Clear Python cache
echo.
echo [2/3] Clearing Python bytecode cache...
set CACHE_COUNT=0

for /r "%~dp0..\src" %%d in (__pycache__) do (
    if exist "%%d" (
        rmdir /s /q "%%d" 2>nul
        if !ERRORLEVEL! EQU 0 (
            set /a CACHE_COUNT+=1
            echo     ✓ Cleared: %%d
        )
    )
)

echo     Total cache directories cleared: !CACHE_COUNT!

REM Step 3: Start backend server
echo.
echo [3/3] Starting backend server...
cd "%~dp0.."
start "GreenStack Backend" cmd /k "python -m src.api"

echo.
echo ============================================================================
echo  ✓ Backend Restart Complete
echo ============================================================================
echo.
echo Backend server is starting in a new window...
echo Wait for "Application startup complete" message before using.
echo.

pause
