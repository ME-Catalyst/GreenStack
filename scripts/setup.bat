@echo off
setlocal enabledelayedexpansion
title GreenStack - Quick Setup

:: Change to project root directory
cd /d "%~dp0\.."

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 GREENSTACK - QUICK SETUP                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: ============================================================================
:: STEP 1: Clean Restart - Kill ALL Python processes for clean slate
:: ============================================================================
echo [1/6] Ensuring clean Python environment...

:: Kill ALL python.exe processes to ensure no stale code is running
:: This is CRITICAL - old Python processes can serve stale cached code
taskkill /F /IM python.exe /T >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo   Killed all Python processes for clean restart
    :: Wait for processes to fully terminate
    timeout /t 2 /nobreak >nul
) else (
    echo   No Python processes were running
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
    pause
    exit /b 1
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
        pause
        exit /b 1
    )
)
echo.

:: ============================================================================
:: STEP 4: Ensure Redis is running
:: ============================================================================
echo [5/6] Ensuring Redis (localhost:6379) is running...
set "REDIS_READY=0"
call :check_redis_ready
if %errorlevel% equ 0 goto :redis_already_running

call :ensure_docker_ready
if %errorlevel% neq 0 goto :redis_unavailable

call :start_redis_with_docker
if %errorlevel% equ 0 goto :redis_started
echo   Warning: Unable to launch Redis container (see messages above).
goto :after_redis_check

:redis_already_running
echo   Redis already running.
set "REDIS_READY=1"
goto :after_redis_check

:redis_started
set "REDIS_READY=1"
goto :after_redis_check

:redis_unavailable
echo   Warning: Docker Desktop is not available. Redis will not be started automatically.
goto :after_redis_check

:after_redis_check
if "%REDIS_READY%"=="1" goto :redis_ready_message
echo   Continuing without Redis (caching/rate-limits will use in-memory mode).
goto :redis_message_end

:redis_ready_message
echo   Redis is ready.

:redis_message_end
echo.

:: ============================================================================
:: STEP 5: Update codebase statistics
:: ============================================================================
echo [6/6] Updating codebase statistics...
python -m src.utils.codebase_stats >nul 2>&1
if %errorlevel% equ 0 (
    echo   Statistics updated!
) else (
    echo   Warning: Could not update statistics (non-critical)
)
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
echo.
echo ══════════════════════════════════════════════════════════════
echo.

:: Start the application with fresh, clean backend
python -m src.start
set START_EXIT_CODE=%errorlevel%

:: Show final status
echo.
echo ══════════════════════════════════════════════════════════════

if %START_EXIT_CODE% equ 0 (
    echo   Application stopped gracefully
) else (
    echo   [ERROR] Application exited with error code: %START_EXIT_CODE%
    echo   Check the messages above for details
)

echo ══════════════════════════════════════════════════════════════
echo.
pause
exit /b %START_EXIT_CODE%

:: ============================================================================
:: Helper Functions
:: ============================================================================

:ensure_docker_ready
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo   Docker CLI not found on PATH.
    exit /b 1
)
docker info >nul 2>&1
if %errorlevel% equ 0 (
    exit /b 0
)
echo   Docker Desktop is not running. Attempting to start it...
set "DOCKER_APP=%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
if not exist "%DOCKER_APP%" (
    set "DOCKER_APP=%ProgramFiles% (x86)%\Docker\Docker\Docker Desktop.exe"
)
if exist "%DOCKER_APP%" (
    start "" "%DOCKER_APP%"
) else (
    echo   Unable to locate Docker Desktop executable. Please start Docker manually.
    exit /b 1
)
echo   Waiting for Docker daemon to be ready...
for /l %%i in (1,1,60) do (
    timeout /t 2 >nul
    docker info >nul 2>&1
    if %errorlevel% equ 0 (
        echo   Docker is ready.
        exit /b 0
    )
)
echo   Docker daemon did not become ready in time.
exit /b 1

:start_redis_with_docker
call :detect_compose_cmd
if errorlevel 1 (
    echo   docker compose command not available.
    exit /b 1
)
echo   Starting Redis container using %DOCKER_COMPOSE_CMD%...
%DOCKER_COMPOSE_CMD% -f docker-compose.yml up -d redis
if %errorlevel% neq 0 (
    echo   Failed to run Redis container.
    exit /b 1
)
echo   Waiting for Redis service to become ready...
for /l %%i in (1,1,30) do (
    timeout /t 1 >nul
    call :check_redis_ready
    if %errorlevel% equ 0 (
        echo   Redis container is online!
        exit /b 0
    )
)
echo   Redis container failed to respond in time.
exit /b 1

:detect_compose_cmd
set "DOCKER_COMPOSE_CMD=docker compose"
docker compose version >nul 2>&1
if %errorlevel% equ 0 (
    exit /b 0
)
where docker-compose >nul 2>&1
if %errorlevel% equ 0 (
    set "DOCKER_COMPOSE_CMD=docker-compose"
    docker-compose version >nul 2>&1
    exit /b %errorlevel%
)
exit /b 1

:check_redis_ready
set "POWERSHELL_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%POWERSHELL_EXE%" (
    set "POWERSHELL_EXE=powershell"
)
"%POWERSHELL_EXE%" -NoLogo -NoProfile -Command "try { $client = New-Object Net.Sockets.TcpClient('localhost',6379); $client.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
exit /b %errorlevel%
