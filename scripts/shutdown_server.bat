@echo off
REM ============================================================================
REM GreenStack Backend Server Shutdown Script
REM ============================================================================
REM This script stops ONLY the GreenStack backend server (port 8000)
REM It will NOT kill other Python or Node applications
REM ============================================================================

echo.
echo ============================================================================
echo  GreenStack Backend Server Shutdown
echo ============================================================================
echo.

REM Find processes using port 8000 (GreenStack backend)
echo [1/1] Stopping GreenStack backend on port 8000...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    set PID=%%a
    if defined PID (
        taskkill /F /PID !PID! >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo     ✓ Stopped backend process (PID: !PID!)
        )
    )
)

REM Double-check by looking for python processes running src.api
echo     Checking for remaining src.api processes...
wmic process where "commandline like '%%src.api%%'" get processid,commandline 2>nul | findstr "src.api" >nul
if %ERRORLEVEL% EQU 0 (
    echo     Found src.api processes, stopping them...
    for /f "tokens=2" %%a in ('wmic process where "commandline like '%%src.api%%'" get processid ^| findstr /r "[0-9]"') do (
        taskkill /F /PID %%a >nul 2>&1
        echo     ✓ Stopped src.api process (PID: %%a)
    )
) else (
    echo     ✓ No src.api processes found
)

echo.
echo ============================================================================
echo  ✓ Backend Shutdown Complete
echo ============================================================================
echo.
echo GreenStack backend server stopped (port 8000).
echo Other Python applications were NOT affected.
echo.
echo To restart: scripts\restart_backend.bat
echo.

pause
