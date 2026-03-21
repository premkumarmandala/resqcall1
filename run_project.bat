@echo off
echo ==========================================
echo   Starting ResQ Emergency App Support
echo ==========================================

:: 1. Database Check (Attempts to start standard MySQL service)
echo.
echo [1/3] Checking Database Service...
echo NOTE: If this fails, ensure your MySQL service is running via 'services.msc'.
net start MySQL80
if %ERRORLEVEL% NEQ 0 (
    echo (Service start command failed or service is already running. Continuing...)
)

:: 2. Start Backend
echo.
echo [2/3] Starting Backend Server...
start "ResQ Backend" /D "project" cmd /k "python -m backend.app"

:: 3. Start Frontend
echo.
echo [3/3] Starting Frontend Server...
start "ResQ Frontend" /D "project\frontend" cmd /k "python -m http.server 8080"

:: 4. Open Browser
echo.
echo Opening Application...
timeout /t 3 > nul
start http://localhost:8080/login.html

echo.
echo ==========================================
echo   System Running!
echo   backend: http://localhost:5000
echo   frontend: http://localhost:8080
echo ==========================================
pause
