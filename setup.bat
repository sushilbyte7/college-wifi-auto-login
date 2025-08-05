@echo off
setlocal enabledelayedexpansion

echo College WiFi Auto-Login Setup
echo ==============================
echo.

set "SCRIPT_DIR=%~dp0"
set "MONITOR_SCRIPT=%SCRIPT_DIR%wifi_monitor.py"
set "BATCH_PATH=%SCRIPT_DIR%start_monitor_hidden.bat"

echo Creating startup files...

:: Create a hidden batch file that runs the monitor
echo @echo off > "%BATCH_PATH%"
echo cd /d "%SCRIPT_DIR%" >> "%BATCH_PATH%"
echo python wifi_monitor.py >> "%BATCH_PATH%"

:: Create VBS script to run batch file hidden
set "VBS_PATH=%SCRIPT_DIR%wifi_monitor_hidden.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%VBS_PATH%"
echo WshShell.Run chr(34) ^& "%BATCH_PATH%" ^& chr(34), 0 >> "%VBS_PATH%"
echo Set WshShell = Nothing >> "%VBS_PATH%"

echo.
echo Setup Options:
echo 1. Add to Windows Startup (runs automatically when Windows starts)
echo 2. Create desktop shortcut only  
echo 3. Test the system now
echo 4. Exit without setup
echo.

set /p choice="Choose an option (1-4): "

if "%choice%"=="1" (
    echo.
    echo Adding to Windows Startup...
    
    :: Add to startup folder
    set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
    copy "%VBS_PATH%" "!STARTUP_FOLDER!\WiFi Auto-Login Monitor.vbs" >nul
    
    if !errorlevel! equ 0 (
        echo ✅ Successfully added to Windows Startup
        echo The monitor will start automatically when Windows boots
    ) else (
        echo ❌ Failed to add to startup folder
    )
)

if "%choice%"=="1" goto create_shortcut
if "%choice%"=="2" goto create_shortcut  
if "%choice%"=="3" goto test_system
if "%choice%"=="4" goto end

:create_shortcut
echo.
echo Creating desktop shortcut...

:: Create desktop shortcut
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_PATH=%DESKTOP%\WiFi Auto-Login Monitor.lnk"

:: Use PowerShell to create shortcut
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%VBS_PATH%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'College WiFi Auto-Login Monitor'; $Shortcut.Save()"

if exist "%SHORTCUT_PATH%" (
    echo ✅ Desktop shortcut created
) else (
    echo ❌ Failed to create desktop shortcut
)

if "%choice%"=="2" goto end
goto test_system

:test_system
echo.
echo Testing the auto-login system...
echo.
python wifi_auto_login.py
echo.
echo Test completed!
goto end

:end
echo.
echo Setup completed!
echo.
echo 🎯 How the NEW system works:
echo ----------------------------------------
echo 1. Monitor runs in background continuously
echo 2. When you connect to PCU_Student WiFi:
echo    - Auto-login script runs ONCE
echo    - Attempts login if internet not working  
echo    - Exits after successful login
echo 3. No unnecessary repeated logins!
echo.
echo Files created:
echo - wifi_auto_login.py   (One-time login script)
echo - wifi_monitor.py      (Connection monitor)
echo - wifi_monitor.log     (Monitor activity log)
echo - wifi_login.log       (Login attempt log)
echo.
echo Usage:
echo - Monitor runs automatically at startup
echo - Check logs for activity details
echo - Edit config.ini to change settings
echo.

if "%choice%"=="1" (
    echo ✅ Monitor is now configured to start automatically with Windows
    echo.
)

pause
