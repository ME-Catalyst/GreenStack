@echo off
setlocal enabledelayedexpansion
title Test Setup.bat Cleanup Functions

echo ============================================================================
echo Testing setup.bat Cleanup Functions
echo ============================================================================
echo.

:: Test 1: Check for processes on port 8000
echo [Test 1] Checking for processes on port 8000...
set "FOUND_8000=0"
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" 2^>nul') do (
    set FOUND_8000=1
    echo   Found process on port 8000 (PID: %%a)
)
if "%FOUND_8000%"=="0" (
    echo   No processes found on port 8000 [OK]
)
echo.

:: Test 2: Check for src.api processes
echo [Test 2] Checking for src.api processes...
set "FOUND_SRC_API=0"
wmic process where "commandline like '%%src.api%%'" get processid 2>nul | findstr /r "[0-9]" >nul
if %ERRORLEVEL% EQU 0 (
    echo   Found src.api processes:
    for /f "tokens=1" %%a in ('wmic process where "commandline like '%%src.api%%'" get processid ^| findstr /r "[0-9]"') do (
        echo     PID: %%a
        set FOUND_SRC_API=1
    )
) else (
    echo   No src.api processes found [OK]
)
echo.

:: Test 3: Check for __pycache__ directories
echo [Test 3] Checking for Python cache directories...
set CACHE_COUNT=0
for /r "%CD%\src" %%d in (__pycache__) do (
    if exist "%%d" (
        echo   Found: %%d
        set /a CACHE_COUNT+=1
    )
)
if %CACHE_COUNT% EQU 0 (
    echo   No cache directories found [OK]
) else (
    echo   Total cache directories: %CACHE_COUNT%
)
echo.

:: Test 4: Check Python installation
echo [Test 4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version') do echo   %%i [OK]
) else (
    echo   [ERROR] Python not found!
)
echo.

:: Test 5: Check database file
echo [Test 5] Checking database file...
if exist "greenstack.db" (
    for %%A in ("greenstack.db") do echo   Database exists: %%~zA bytes [OK]
) else (
    echo   [WARN] Database file not found
)
echo.

:: Test 6: Check requirements.txt
echo [Test 6] Checking requirements.txt...
if exist "requirements.txt" (
    for /f %%A in ('find /c /v "" ^< requirements.txt') do echo   Found %%A dependencies [OK]
) else (
    echo   [ERROR] requirements.txt not found!
)
echo.

echo ============================================================================
echo Test Complete
echo ============================================================================
echo.

:: Summary
echo Summary:
if "%FOUND_8000%"=="1" echo   - Backend processes on port 8000: YES (should be stopped)
if "%FOUND_SRC_API%"=="1" echo   - src.api processes running: YES (should be stopped)
if %CACHE_COUNT% GTR 0 echo   - Python cache directories: %CACHE_COUNT% (should be cleared)
echo.

pause
