@echo off
setlocal enabledelayedexpansion
title Kill All GreenStack Backends

echo ============================================================================
echo KILLING ALL GREENSTACK BACKEND PROCESSES
echo ============================================================================
echo.

set "KILLED_COUNT=0"

:: Method 1: Kill by port 8000
echo [1/3] Killing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8000"') do (
    set "PID=%%a"
    if defined PID (
        taskkill /F /PID %%a >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo   [X] Killed PID %%a (port 8000)
            set /a KILLED_COUNT+=1
        )
    )
)
echo.

:: Method 2: Kill by command line pattern - use DIRECT wmic output parsing
echo [2/3] Killing python processes with 'src.api' in command line...
for /f "skip=1" %%a in ('wmic process where "commandline like '%%src.api%%'" get processid 2^>nul') do (
    set "PID=%%a"
    :: Remove spaces and check if non-empty
    set "PID=!PID: =!"
    if not "!PID!"=="" (
        taskkill /F /PID !PID! >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo   [X] Killed PID !PID! (src.api process)
            set /a KILLED_COUNT+=1
        )
    )
)
echo.

:: Method 3: Kill by process name pattern
echo [3/3] Killing remaining python.exe processes running src module...
wmic process where "name='python.exe' and commandline like '%%src%%'" get processid 2>nul | find /i "src" >nul
if %ERRORLEVEL% EQU 0 (
    for /f "skip=1" %%a in ('wmic process where "name='python.exe' and commandline like '%%src%%'" get processid 2^>nul') do (
        set "PID=%%a"
        set "PID=!PID: =!"
        if not "!PID!"=="" (
            taskkill /F /PID !PID! >nul 2>&1
            if !ERRORLEVEL! EQU 0 (
                echo   [X] Killed PID !PID! (python src module)
                set /a KILLED_COUNT+=1
            )
        )
    )
)
echo.

:: Wait for processes to fully terminate
echo Waiting 3 seconds for processes to terminate...
timeout /t 3 /nobreak >nul
echo.

:: Verify all are dead
echo ============================================================================
echo VERIFICATION
echo ============================================================================
set "REMAINING=0"
for /f %%a in ('wmic process where "commandline like '%%src.api%%'" get processid 2^>nul ^| find /c /v ""') do set REMAINING=%%a
set /a REMAINING-=1

if %REMAINING% GTR 0 (
    echo [WARNING] %REMAINING% backend processes still running!
    echo.
    echo Remaining processes:
    wmic process where "commandline like '%%src.api%%'" get processid,commandline 2>nul
) else (
    echo [SUCCESS] All backend processes terminated
    echo   Total killed: %KILLED_COUNT%
)

echo ============================================================================
echo.
pause
