# College WiFi Smart Auto-Login System

An intelligent automated WiFi login system for PCU_Student network that runs **only when needed** - no continuous monitoring waste!

## ✨ NEW Smart Features

- 🎯 **Runs Once Per Connection**: Only executes when you connect to college WiFi
- 🚀 **Event-Based**: Monitors WiFi changes, not continuous polling  
- ⚡ **Resource Efficient**: No unnecessary CPU/battery usage
- � **Auto-Exit**: Stops after successful login
- 📝 **Smart Logging**: Separate logs for monitoring and login attempts

## Files Description

- `wifi_auto_login.py` - Smart one-time login script (runs once per connection)
- `wifi_monitor.py` - WiFi connection change detector  
- `config.ini` - Configuration file for all settings
- `setup.bat` - Setup wizard to configure auto-startup
- `wifi_monitor.log` - WiFi connection monitoring log
- `wifi_login.log` - Login attempt details log

## Quick Start

1. **Test the login**: Run the auto-login script
   ```
   python wifi_auto_login.py
   ```

2. **Configure settings**: Edit `config.ini` with your credentials
   - Update USERNAME and PASSWORD
   - Modify other settings if needed

3. **Run setup**: Execute `setup.bat` as administrator
   - Choose option 1 to add to Windows startup
   - Choose option 3 to test the system first

4. **Manual start**: Use the desktop shortcut or run:
   ```
   python wifi_monitor.py
   ```

## How the NEW System Works

### 🎯 **Smart Event-Based Approach:**

1. **WiFi Monitor**: Runs in background, watches for WiFi changes
2. **Connection Detected**: When you connect to "PCU_Student"
3. **One-Time Login**: Auto-login script runs ONCE
4. **Success & Exit**: After successful login, script stops
5. **No Waste**: No continuous checking when internet is working

### 🔄 **Real Scenario:**
```
[10:00:00] 📶 WiFi changed: 'Home_WiFi' → 'PCU_Student'  
[10:00:01] 🎓 Connected to college WiFi: PCU_Student
[10:00:01] 🔄 Triggering auto-login process...
[10:00:02] 🔐 Attempting WiFi login...
[10:00:03] ✅ Login successful!
[10:00:08] ✅ Internet connectivity confirmed!
[10:00:08] ✅ Auto-login process completed successfully!
[10:00:08] Script execution completed.
```

## Configuration

Edit `config.ini` to customize:

```ini
[WIFI_SETTINGS]
COLLEGE_WIFI_NAME = PCU_Student
PORTAL_URL = http://10.11.200.1:8090/httpclient.html
LOGIN_URL = http://10.11.200.1:8090/login.xml

[CREDENTIALS]
USERNAME = your_username
PASSWORD = your_password

[MONITORING]
CHECK_INTERVAL = 30
MAX_LOGIN_ATTEMPTS = 3
```

## Logs

### `wifi_monitor.log` - Connection monitoring:
- WiFi connection changes
- Auto-login trigger events
- Monitor status and errors

### `wifi_login.log` - Login attempts:
- Login attempt details
- Success/failure status
- Portal communication logs

## Troubleshooting

### Monitor won't start
- Make sure Python is installed and in PATH
- Check if all files are in the same directory
- Run `python wifi_auto_login.py` first to test

### Login fails
- Verify credentials in `config.ini`
- Check if portal URL is correct
- Look at `wifi_login.log` for error details
- Try running `python wifi_auto_login.py` manually

### Not detecting WiFi changes
- Ensure WiFi name matches exactly (case-sensitive)
- Check Windows WiFi adapter is working
- Run `netsh wlan show interfaces` to see current connection

## Advantages Over Old System

| Old System | New Smart System |
|------------|------------------|
| ❌ Continuous monitoring | ✅ Event-based detection |
| ❌ Runs every 30 seconds | ✅ Runs only when needed |
| ❌ Resource waste | ✅ Resource efficient |
| ❌ Repeated login attempts | ✅ One-time login per connection |
| ❌ Always running | ✅ Auto-exit after success |

## Security Notes

- Credentials are stored in plain text in `config.ini`
- Keep the script directory secure
- Monitor logs are created for transparency

## Requirements

- Windows 10/11
- Python 3.6+
- Network access to college WiFi portal

## Advanced Usage

### Test auto-login manually
```batch
python wifi_auto_login.py
```

### Start monitor manually  
```batch
python wifi_monitor.py
```

### Check logs in real-time
```batch
powershell Get-Content wifi_monitor.log -Wait
powershell Get-Content wifi_login.log -Wait
```

### Remove from startup
Delete `WiFi Auto-Login Monitor.vbs` from:
`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

---

**🎯 Smart Design**: Runs only when you connect to college WiFi, completes login, then stops. No continuous resource usage!
