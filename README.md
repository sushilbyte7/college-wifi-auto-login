# College WiFi Auto-Login System

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-brightgreen.svg)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, event-driven WiFi auto-login system for college networks that runs **only when needed** - no resource waste!

## ✨ Key Features

- 🎯 **Smart Event-Based**: Triggers only on WiFi connection changes
- ⚡ **One-Time Execution**: Runs once per connection, then exits
- 🔋 **Resource Efficient**: No continuous monitoring waste
- 🚀 **Auto-Startup**: Configurable Windows startup integration
- 📝 **Detailed Logging**: Separate logs for monitoring and login attempts
- ⚙️ **Easy Configuration**: Simple INI file configuration

## 🏗️ Architecture

```
┌─────────────────┐    WiFi Change    ┌──────────────────┐
│  WiFi Monitor   │ ──────────────────▶│   Auto-Login     │
│  (Background)   │                    │   (One-time)     │
└─────────────────┘                    └──────────────────┘
        │                                       │
        ▼                                       ▼
┌─────────────────┐                    ┌──────────────────┐
│ wifi_monitor.log│                    │  wifi_login.log  │
└─────────────────┘                    └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.6+
- College WiFi network access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/college-wifi-auto-login.git
   cd college-wifi-auto-login
   ```

2. **Configure your credentials**
   ```ini
   # Edit config.ini
   [CREDENTIALS]
   USERNAME = your_username
   PASSWORD = your_password
   ```

3. **Run setup**
   ```cmd
   # Run as Administrator
   setup.bat
   ```

4. **Choose your setup option**
   - Option 1: Add to Windows startup (recommended)
   - Option 2: Create desktop shortcut only
   - Option 3: Test the system first

## 📁 File Structure

```
├── wifi_auto_login.py      # Smart one-time login script
├── wifi_monitor.py         # WiFi connection change monitor
├── wifi_login.py           # Interactive testing script
├── config.ini              # Configuration file
├── setup.bat               # Windows setup wizard
├── README.md               # This file
├── LICENSE                 # MIT License
└── logs/
    ├── wifi_monitor.log    # Connection monitoring logs
    └── wifi_login.log      # Login attempt logs
```

## ⚙️ Configuration

Edit `config.ini` to customize settings:

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

## 🔄 How It Works

### Event-Driven Architecture

1. **WiFi Monitor** runs continuously in background (lightweight)
2. **Detects WiFi changes** every 10 seconds
3. **Triggers auto-login** only when connecting to college WiFi
4. **Auto-login script** runs once, completes login, then exits
5. **No repeated attempts** until next WiFi connection

### Trigger Scenarios

| Scenario | Action | Trigger |
|----------|--------|---------|
| Home WiFi → College WiFi | ✅ Login | Yes |
| No WiFi → College WiFi | ✅ Login | Yes |
| College WiFi → Home WiFi | ❌ None | No |
| WiFi Off/On (same network) | ❌ None | No |
| Already connected + working | ❌ None | No |

## 📊 Logging

### Monitor Log (`wifi_monitor.log`)
```log
[2025-08-05 10:00:00] 📶 WiFi changed: 'Home_WiFi' → 'PCU_Student'
[2025-08-05 10:00:01] 🎓 Connected to college WiFi: PCU_Student
[2025-08-05 10:00:01] 🔄 Triggering auto-login process...
[2025-08-05 10:00:05] ✅ Auto-login process completed successfully!
```

### Login Log (`wifi_login.log`)
```log
[2025-08-05 10:00:02] INFO - Attempting WiFi login...
[2025-08-05 10:00:03] INFO - Login successful!
[2025-08-05 10:00:08] INFO - Internet connectivity confirmed!
```

## 🛠️ Manual Usage

### Test auto-login
```cmd
python wifi_auto_login.py
```

### Start monitor manually
```cmd
python wifi_monitor.py
```

### Interactive testing
```cmd
python wifi_login.py
```

## 🔧 Troubleshooting

### Common Issues

1. **Script won't start**
   - Ensure Python is in PATH
   - Run `python --version` to verify installation

2. **Login fails**
   - Verify credentials in `config.ini`
   - Check portal URL accessibility
   - Review `wifi_login.log` for errors

3. **WiFi not detected**
   - Ensure WiFi name matches exactly (case-sensitive)
   - Test with `netsh wlan show interfaces`

### Debug Mode
```cmd
# Run with detailed output
python wifi_auto_login.py --debug
```

## 🔒 Security Notes

- Credentials are stored in plain text in `config.ini`
- Keep the configuration file secure
- Consider using environment variables for production

## 📈 Advantages

| Old Approach | This System |
|--------------|-------------|
| ❌ Continuous polling | ✅ Event-driven |
| ❌ Resource waste | ✅ Efficient |
| ❌ Repeated attempts | ✅ One-time execution |
| ❌ Always running | ✅ Auto-exit after success |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for educational institutions with captive portal authentication
- Designed with efficiency and resource conservation in mind
- Inspired by the need for seamless WiFi connectivity in college environments

---

<div align="center">
  <strong>Made with ❤️ for seamless college WiFi experience</strong>
</div>
