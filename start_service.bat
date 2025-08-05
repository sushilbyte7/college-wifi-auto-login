@echo off
title College WiFi Auto-Login Service
cd /d "%~dp0"

echo Starting College WiFi Auto-Login Service...
echo This will run in the background and automatically login when needed.
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

:: Run the service
echo Service is starting...
echo Check wifi_login.log for detailed logs
echo Press Ctrl+C to stop the service
echo.

python wifi_service.py --service
