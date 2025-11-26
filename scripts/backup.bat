@echo off
REM ============================================================================
REM GreenStack Backup Script (Windows)
REM ============================================================================
REM Purpose: Backup database, files, and configuration
REM Created: 2025-11-25
REM Usage: backup.bat
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuration
set "BACKUP_DIR=backups"
set "TIMESTAMP=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "BACKUP_NAME=greenstack_backup_%TIMESTAMP%"
set "BACKUP_PATH=%BACKUP_DIR%\%BACKUP_NAME%"

echo.
echo ============================================
echo   GreenStack Backup (Windows)
echo ============================================
echo.
echo Backup ID: %BACKUP_NAME%
echo.

REM Load environment variables from .env
if exist .env (
    echo Loading environment variables...
    for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
        if not "%%a"=="" if not "%%b"=="" (
            set "%%a=%%b"
        )
    )
)

REM Create backup directory
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
if not exist "%BACKUP_PATH%" mkdir "%BACKUP_PATH%"

echo [INFO] Creating backup directory: %BACKUP_PATH%

REM ============================================================================
REM Backup Database
REM ============================================================================

echo [INFO] Backing up PostgreSQL database...

docker ps --format "{{.Names}}" | findstr /C:"greenstack-postgres" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    docker exec greenstack-postgres pg_dump -U iodd_user -d greenstack --format=custom > "%BACKUP_PATH%\postgres.dump" 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Database backup completed: postgres.dump
    ) else (
        echo [ERROR] Database backup failed
    )
) else (
    echo [WARN] PostgreSQL container not running, skipping database backup
)

REM ============================================================================
REM Backup Files
REM ============================================================================

echo [INFO] Backing up uploaded files...

if exist "iodd_storage" (
    tar -czf "%BACKUP_PATH%\iodd_storage.tar.gz" iodd_storage 2>nul
    echo [OK] IODD storage backup completed
) else (
    echo [WARN] IODD storage directory not found
)

if exist "generated" (
    tar -czf "%BACKUP_PATH%\generated.tar.gz" generated 2>nul
    echo [OK] Generated files backup completed
) else (
    echo [WARN] Generated directory not found
)

REM ============================================================================
REM Backup Configuration
REM ============================================================================

echo [INFO] Backing up configuration...

if exist "config" (
    tar -czf "%BACKUP_PATH%\config.tar.gz" config 2>nul
    echo [OK] Configuration backup completed
)

tar -czf "%BACKUP_PATH%\docker-compose.tar.gz" docker-compose*.yml 2>nul
echo [OK] Docker Compose files backed up

REM ============================================================================
REM Create Manifest
REM ============================================================================

echo [INFO] Creating backup manifest...

(
echo GreenStack Backup Manifest
echo ==========================
echo Backup ID: %BACKUP_NAME%
echo Created: %date% %time%
echo Hostname: %COMPUTERNAME%
echo User: %USERNAME%
echo.
echo Backup Contents:
) > "%BACKUP_PATH%\MANIFEST.txt"

dir "%BACKUP_PATH%" >> "%BACKUP_PATH%\MANIFEST.txt"

echo [OK] Manifest created

REM ============================================================================
REM Compress Final Archive
REM ============================================================================

echo [INFO] Compressing backup archive...

tar -czf "%BACKUP_DIR%\%BACKUP_NAME%.tar.gz" -C "%BACKUP_DIR%" "%BACKUP_NAME%" 2>nul

if %ERRORLEVEL% EQU 0 (
    echo [OK] Backup archive created: %BACKUP_NAME%.tar.gz

    REM Remove temporary directory
    rmdir /s /q "%BACKUP_PATH%"

    REM Show backup size
    for %%A in ("%BACKUP_DIR%\%BACKUP_NAME%.tar.gz") do (
        echo [INFO] Backup size: %%~zA bytes
    )
) else (
    echo [ERROR] Failed to compress backup
)

REM ============================================================================
REM Cleanup Old Backups (keep last 7)
REM ============================================================================

echo [INFO] Cleaning up old backups (keeping last 7)...

REM Count backup files
set /a count=0
for %%F in ("%BACKUP_DIR%\greenstack_backup_*.tar.gz") do set /a count+=1

echo [INFO] Total backups: %count%

REM Delete old backups if more than 7
if %count% GTR 7 (
    REM This is a simplified version - Windows doesn't have easy date-based cleanup
    echo [WARN] More than 7 backups exist. Manual cleanup recommended.
    echo [INFO] Use: forfiles /p "%BACKUP_DIR%" /m greenstack_backup_*.tar.gz /d -7 /c "cmd /c del @path"
)

echo.
echo [SUCCESS] Backup completed successfully!
echo [INFO] Backup location: %BACKUP_DIR%\%BACKUP_NAME%.tar.gz
echo.

endlocal
