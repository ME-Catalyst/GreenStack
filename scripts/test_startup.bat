@echo off
echo Testing python -m src.start behavior...
echo.

echo [1] Checking if src.start module exists...
if exist "src\start.py" (
    echo    Found: src\start.py
) else (
    echo    ERROR: src\start.py not found!
    pause
    exit /b 1
)
echo.

echo [2] Testing import...
python -c "import src.start" 2>nul
if %errorlevel% equ 0 (
    echo    OK: Module imports successfully
) else (
    echo    ERROR: Module import failed
    python -c "import src.start"
    pause
    exit /b 1
)
echo.

echo [3] Launching python -m src.start...
echo    (This should run indefinitely until Ctrl+C)
echo    Press Ctrl+C to stop
echo.
python -m src.start
set EXIT_CODE=%errorlevel%

echo.
echo ================================================================
echo python -m src.start exited with code: %EXIT_CODE%
echo ================================================================
echo.

if %EXIT_CODE% equ 0 (
    echo This is NORMAL if you pressed Ctrl+C
) else (
    echo This is an ERROR - check messages above
)

echo.
pause
