@echo off
setlocal enabledelayedexpansion
title GreenStack - Debug Setup

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 GREENSTACK - DEBUG SETUP                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [DEBUG] Current directory: %CD%
echo [DEBUG] Script location: %~dp0
echo.

echo Testing Python...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    goto :end_with_pause
)
echo [OK] Python found
echo.

echo Testing src.start import...
python -c "import src.start" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Cannot import src.start
    python -c "import src.start"
    goto :end_with_pause
)
echo [OK] src.start imports successfully
echo.

echo ══════════════════════════════════════════════════════════════
echo LAUNCHING APPLICATION
echo ══════════════════════════════════════════════════════════════
echo.
echo Starting: python -m src.start
echo.
echo [DEBUG] About to execute python -m src.start...
python -m src.start
set START_EXIT_CODE=%errorlevel%

echo.
echo ══════════════════════════════════════════════════════════════
echo [DEBUG] python -m src.start returned
echo [DEBUG] Exit code: %START_EXIT_CODE%
echo ══════════════════════════════════════════════════════════════
echo.

if %START_EXIT_CODE% equ 0 (
    echo   Application stopped gracefully
) else (
    echo   [ERROR] Application exited with error code: %START_EXIT_CODE%
    echo   Check the messages above for details
)

:end_with_pause
echo.
echo ══════════════════════════════════════════════════════════════
echo [DEBUG] About to pause...
echo ══════════════════════════════════════════════════════════════
pause
echo.
echo [DEBUG] After pause, about to exit...
exit /b
