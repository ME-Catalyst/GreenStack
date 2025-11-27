@echo off
echo ========================================
echo GreenStack Backend Restart Script
echo ========================================
echo.

echo Step 1: Killing backend process on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing PID: %%a
    taskkill /PID %%a /F
)

echo.
echo Step 2: Clearing Python cache...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo Cache cleared!

echo.
echo Step 3: Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo.
echo Step 4: Starting backend server...
start "GreenStack Backend" python src/api.py

echo.
echo ========================================
echo Backend restart complete!
echo ========================================
echo.
echo Backend should now be running on http://localhost:8000
echo Check the new window for server logs
pause
