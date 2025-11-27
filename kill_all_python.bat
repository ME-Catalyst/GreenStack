@echo off
echo Killing ALL Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo All Python processes killed.
echo.
echo Now run setup.bat to restart fresh
pause
