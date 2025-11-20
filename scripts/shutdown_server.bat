@echo off
REM ============================================================================
REM GreenStack Server Shutdown Script
REM ============================================================================
REM This script cleanly stops both the frontend and backend servers
REM ============================================================================

echo.
echo ============================================================================
echo  GreenStack Server Shutdown
echo ============================================================================
echo.

REM Kill Python processes (FastAPI backend)
echo [1/2] Stopping Python backend server...
taskkill /F /IM python.exe /T >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ Python backend stopped
) else (
    echo     ℹ No Python processes found
)

REM Kill Node processes (Vite frontend)
echo [2/2] Stopping Node.js frontend server...
taskkill /F /IM node.exe /T >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ Node.js frontend stopped
) else (
    echo     ℹ No Node.js processes found
)

echo.
echo ============================================================================
echo  ✓ Shutdown Complete
echo ============================================================================
echo.
echo All GreenStack servers have been stopped.
echo You can now restart using: scripts\setup.bat
echo.

pause
