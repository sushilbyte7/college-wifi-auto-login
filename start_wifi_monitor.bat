@echo off
title College WiFi Auto-Login
cd /d "%~dp0"

echo Starting College WiFi Auto-Login System...
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

:: Run the WiFi login script
python wifi_login.py

echo.
echo Script ended. Press any key to close...
pause >nul
