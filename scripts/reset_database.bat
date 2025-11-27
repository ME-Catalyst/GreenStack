@echo off
echo ========================================
echo GreenStack Database Reset Script
echo ========================================
echo.
echo This will:
echo   1. Delete the existing database
echo   2. Run all migrations to create fresh schema
echo.
echo WARNING: All data will be lost!
echo.
pause

echo.
echo [1/2] Deleting existing database...
if exist greenstack.db del /f greenstack.db
if exist greenstack.db-shm del /f greenstack.db-shm
if exist greenstack.db-wal del /f greenstack.db-wal
echo   Database deleted

echo.
echo [2/2] Running migrations...
python -m alembic upgrade head
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Migrations failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Database reset complete!
echo ========================================
echo.
echo You can now start the backend with setup.bat
pause
