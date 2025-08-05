# Contributing to College WiFi Auto-Login System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/college-wifi-auto-login.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit: `git commit -m 'Add: brief description of changes'`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Use the GitHub Issues template
- Provide detailed steps to reproduce
- Include system information (Windows version, Python version)
- Attach relevant log files

### ✨ Feature Requests
- Check existing issues first
- Describe the use case clearly
- Explain why it would be beneficial
- Consider backward compatibility

### 🔧 Code Contributions
- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Include tests when applicable

## 📝 Development Setup

### Prerequisites
```bash
# Python 3.6+
python --version

# Git
git --version
```

### Setup Development Environment
```bash
# Clone your fork
git clone https://github.com/yourusername/college-wifi-auto-login.git
cd college-wifi-auto-login

# Create test configuration
cp config.ini config_test.ini
# Edit with test credentials
```

### Testing
```bash
# Test auto-login functionality
python wifi_auto_login.py

# Test monitoring
python wifi_monitor.py

# Test interactive mode
python wifi_login.py
```

## 🏗️ Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions
- Keep functions focused and small

### Example:
```python
def get_connected_wifi_name():
    """
    Get the name of currently connected WiFi network.
    
    Returns:
        str: WiFi network name or None if not connected
    """
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except Exception as e:
        logger.error(f"Error getting WiFi name: {e}")
        return None
```

### Configuration Changes
- Maintain backward compatibility
- Add new settings to `[ADVANCED]` section if experimental
- Update documentation

### Logging Standards
- Use appropriate log levels (INFO, WARNING, ERROR)
- Include context in log messages
- Don't log sensitive information (passwords)

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] Test with college WiFi connection
- [ ] Test with home WiFi (should not trigger)
- [ ] Test WiFi on/off scenarios
- [ ] Test startup integration
- [ ] Verify log file creation
- [ ] Test configuration changes

### Test Scenarios
1. **Fresh Installation**: Test complete setup process
2. **WiFi Changes**: Test various connection scenarios
3. **Error Handling**: Test with invalid credentials, network issues
4. **Resource Usage**: Monitor CPU/memory consumption

## 📚 Documentation

### Update Documentation For:
- New configuration options
- Changed behavior
- New files or dependencies
- Setup instructions

### Documentation Style
- Use clear, simple language
- Include code examples
- Add screenshots for GUI elements
- Keep README.md updated

## 🔒 Security Considerations

### Sensitive Data
- Never commit credentials in code
- Use placeholder values in examples
- Consider encryption for stored passwords
- Validate all user inputs

### Network Security
- Use HTTPS when possible
- Implement timeout mechanisms
- Handle network errors gracefully

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Test on fresh Windows installation
- [ ] Update documentation
- [ ] Add changelog entry
- [ ] Ensure no merge conflicts
- [ ] Write clear commit messages

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested on Windows 10/11
- [ ] Tested with college WiFi
- [ ] Tested startup integration
- [ ] No regression in existing functionality

## Screenshots/Logs
Include relevant screenshots or log snippets
```

## 🎯 Priority Areas

We especially welcome contributions in these areas:

1. **Multi-Platform Support**: Linux/macOS compatibility
2. **Security Enhancements**: Credential encryption
3. **GUI Interface**: Simple configuration tool
4. **Error Recovery**: Better failure handling
5. **Performance**: Further optimization
6. **Documentation**: More examples and tutorials

## 💬 Communication

- **Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

---

Thank you for making this project better! 🚀
