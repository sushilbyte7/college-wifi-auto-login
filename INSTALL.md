# College WiFi Auto-Login System - Installation Guide

## 📋 System Requirements

- **Operating System**: Windows 10 or Windows 11
- **Python**: Version 3.6 or higher
- **Network**: Access to college WiFi with captive portal
- **Permissions**: Administrator access for startup configuration

## 🚀 Quick Installation

### Step 1: Download
```bash
git clone https://github.com/yourusername/college-wifi-auto-login.git
cd college-wifi-auto-login
```

### Step 2: Configure
```bash
# Copy example configuration
copy config.example.ini config.ini

# Edit with your credentials
notepad config.ini
```

### Step 3: Setup
```bash
# Run as Administrator
setup.bat
```

## 🔧 Detailed Installation

### 1. Python Installation

If Python is not installed:

1. Download from [python.org](https://python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:
   ```cmd
   python --version
   ```

### 2. Download Project

**Option A: Git Clone**
```bash
git clone https://github.com/yourusername/college-wifi-auto-login.git
```

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to desired location (e.g., `C:\WiFi-Auto-Login\`)

### 3. Configuration Setup

1. **Copy example config**:
   ```cmd
   copy config.example.ini config.ini
   ```

2. **Edit configuration**:
   ```ini
   [CREDENTIALS]
   USERNAME = your_college_username
   PASSWORD = your_college_password
   ```

3. **Verify WiFi name**:
   ```cmd
   netsh wlan show interfaces
   ```
   Update `COLLEGE_WIFI_NAME` if different.

### 4. Initial Testing

**Test auto-login**:
```cmd
python wifi_auto_login.py
```

**Expected output**:
```
INFO - Starting Smart WiFi Auto-Login Handler...
INFO - Current WiFi: PCU_Student
INFO - Internet is already working! No login needed.
```

### 5. Setup Windows Integration

**Run setup wizard**:
```cmd
# Right-click → "Run as Administrator"
setup.bat
```

**Choose setup option**:
- **Option 1**: Add to Windows startup (recommended)
- **Option 2**: Create desktop shortcut only
- **Option 3**: Test system first

## 🎯 Startup Configuration

### Automatic Startup (Recommended)

When you choose **Option 1** in setup:
1. Creates hidden VBS script
2. Adds to Windows startup folder
3. Starts automatically on boot
4. Runs silently in background

**Location**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

### Manual Startup

**Desktop shortcut**: Double-click to start monitoring
**Command line**: 
```cmd
cd path\to\wifi-auto-login
python wifi_monitor.py
```

## 🔍 Verification

### Check if Running
1. **Task Manager** → Look for `python.exe` process
2. **Log files**: Check for recent entries in `wifi_monitor.log`

### Test WiFi Connection
1. Disconnect from current WiFi
2. Connect to college WiFi
3. Check logs for auto-login activity

## 📁 File Structure After Installation

```
college-wifi-auto-login/
├── wifi_auto_login.py          # Main login script
├── wifi_monitor.py             # Background monitor
├── config.ini                  # Your configuration (created)
├── config.example.ini          # Example configuration
├── setup.bat                   # Setup wizard
├── logs/
│   ├── wifi_monitor.log        # Monitor activity
│   └── wifi_login.log          # Login attempts
└── generated_files/            # Created by setup
    ├── wifi_monitor_hidden.vbs
    └── start_monitor_hidden.bat
```

## 🛠️ Troubleshooting Installation

### Python Not Found
```
'python' is not recognized as an internal or external command
```

**Solution**: 
1. Reinstall Python with "Add to PATH" checked
2. OR use full path: `C:\Python39\python.exe`

### Permission Denied
```
Access is denied
```

**Solution**: Run Command Prompt as Administrator

### Config File Issues
```
Error reading configuration
```

**Solution**: 
1. Ensure `config.ini` exists
2. Check file format (use example as template)
3. Verify no special characters in credentials

### WiFi Not Detected
```
Current WiFi: None
```

**Solutions**:
1. Check WiFi adapter is enabled
2. Verify network name spelling (case-sensitive)
3. Test with: `netsh wlan show interfaces`

### Startup Not Working
1. **Check startup folder**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`
2. **Verify file exists**: `WiFi Auto-Login Monitor.vbs`
3. **Test manually**: Double-click the VBS file

## 🔄 Update Installation

### Git Update
```bash
git pull origin main
```

### Manual Update
1. Download new version
2. Replace all files EXCEPT `config.ini`
3. Re-run `setup.bat` if needed

## 🗑️ Uninstallation

### Remove from Startup
1. Delete file from startup folder:
   ```
   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\WiFi Auto-Login Monitor.vbs
   ```

### Complete Removal
1. Stop any running processes
2. Delete project folder
3. Remove startup entries
4. Delete desktop shortcuts

### Clean Uninstall Script
```cmd
@echo off
echo Removing WiFi Auto-Login...
taskkill /f /im python.exe 2>nul
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\WiFi Auto-Login Monitor.vbs" 2>nul
del "%USERPROFILE%\Desktop\WiFi Auto-Login Monitor.lnk" 2>nul
echo Uninstallation completed.
pause
```

## 📞 Support

If installation fails:
1. Check [Issues](https://github.com/yourusername/college-wifi-auto-login/issues)
2. Create new issue with:
   - Windows version
   - Python version
   - Error messages
   - Log files

---

**Installation complete!** The system will now automatically handle your college WiFi login. 🎉
