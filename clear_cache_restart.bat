@echo off
echo ================================================
echo  CLEARING PYTHON CACHE AND RESTARTING BACKEND
echo ================================================
echo.

echo [1/3] Clearing Python bytecode cache...
rd /s /q src\__pycache__ 2>nul
rd /s /q src\routes\__pycache__ 2>nul
rd /s /q src\storage\__pycache__ 2>nul
rd /s /q src\utils\__pycache__ 2>nul
echo Done.
echo.

echo [2/3] Testing if port 8000 is in use...
netstat -ano | findstr :8000 >nul
if %ERRORLEVEL% EQU 0 (
    echo WARNING: Port 8000 is in use!
    echo Please stop the existing backend server first.
    echo Press Ctrl+C in the terminal running it, or use Task Manager.
    pause
    exit /b 1
)
echo Port 8000 is available.
echo.

echo [3/3] Starting backend server...
echo Command: python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
echo.
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
