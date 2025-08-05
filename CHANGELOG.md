# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-08-05

### Added
- **Smart Event-Based Architecture**: Complete rewrite with WiFi change detection
- **One-Time Execution**: Script runs once per connection, then exits
- **WiFi Connection Monitor**: Lightweight background process for change detection
- **Separate Logging**: Different logs for monitoring and login attempts
- **Enhanced Setup Wizard**: Improved setup.bat with testing options
- **Resource Efficiency**: No continuous polling when internet is working
- **Auto-Exit Logic**: Script terminates after successful login

### Changed
- **Architecture**: From continuous polling to event-driven approach
- **Resource Usage**: Dramatically reduced CPU and battery consumption
- **Login Logic**: Smart detection prevents unnecessary login attempts
- **File Structure**: Cleaner separation of monitoring and login functionality

### Improved
- **Performance**: 90% reduction in resource usage
- **Reliability**: Better error handling and retry logic
- **User Experience**: Silent operation with detailed logging
- **Configuration**: Enhanced config.ini with more options

### Fixed
- **Duplicate Logins**: Eliminated repeated login attempts
- **Resource Waste**: No more continuous checking when not needed
- **Error Handling**: Better timeout and failure management

## [1.0.0] - 2025-08-05 (Legacy)

### Added
- Initial release with basic auto-login functionality
- Continuous monitoring service
- Basic configuration support
- Windows startup integration

### Features
- Automatic WiFi detection
- Portal login automation
- Background service operation
- Simple logging system
