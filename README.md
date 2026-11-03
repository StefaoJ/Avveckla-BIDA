# Windows Application Diagnostics Tool

A Python-based diagnostic tool for inspecting and analyzing legacy Windows applications to determine automation capabilities. This tool is designed to be completely read-only and safe for use in production environments.

## :warning: IMPORTANT SECURITY NOTICES

- **READ-ONLY**: This tool does NOT perform any actions on your applications
- **NO AUTOMATIC CLICKS**: The tool will never automatically click buttons or modify data
- **LOCAL EXECUTION ONLY**: All diagnostics run locally on your machine
- **NO DATA COLLECTION**: Only technical identifiers are logged, never sensitive information
- **NO EXTERNAL COMMUNICATION**: The tool does not send any data to external services

## Overview

This project provides a comprehensive diagnostic toolkit for analyzing Windows applications to determine how they can be automated. The tools are specifically designed for legacy systems where the internal technology is unknown.

### Key Features

- **Window Inspection**: Identify all open application windows
- **Control Analysis**: Enumerate controls and their technical identifiers
- **Backend Detection**: Automatically detect Win32 vs UI Automation compatibility
- **Window Monitoring**: Detect when new windows or browsers open
- **Playwright Integration**: Ready for web-based application handling
- **Safe Logging**: Only technical identifiers are captured in logs

## Project Structure

```
project-root/
├── scripts/                           # Main execution scripts
│   └── inspect_windows_app.py         # Primary inspection script
├── src/
│   └── windows/
│       ├── __init__.py
│       ├── window_inspector.py        # Window identification and monitoring
│       └── control_inspector.py       # Control enumeration and analysis
├── tests/
│   ├── __init__.py
│   └── test_window_inspector.py       # Unit tests with mocked controls
├── docs/
│   └── windows-inspection.md          # Detailed usage guide
├── README.md                          # This file
├── AGENTS.md                          # Agent configuration
├── pyproject.toml                     # Project configuration
└── .gitignore                         # Git ignore patterns
```

## Quick Start

### Prerequisites

- **Windows OS** (These tools are Windows-specific)
- **Python 3.8 or higher**
- **pip** (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Install pywinauto with UI Automation support:
   ```bash
   pip install pywinauto[uiacom]
   ```

### Running the Diagnostic Tool

```bash
python scripts/inspect_windows_app.py
```

This will:
1. List all open windows
2. Enumerate controls for each window
3. Start monitoring for new windows

### Running Tests

```bash
python -m pytest tests/ -v
```

## Usage Examples

### Basic Window Inspection

```python
from src.windows.window_inspector import WindowInspector

inspector = WindowInspector()
windows = inspector.list_open_windows()

print(f"Found {len(windows)} open windows:")
for window in windows:
    print(f"  - {window['title']} (Handle: {window['handle']})")
```

### Control Analysis

```python
from src.windows.control_inspector import ControlInspector

inspector = ControlInspector()
window_handle = 12345  # Get from window inspection
controls = inspector.list_controls(window_handle)

print(f"Found {len(controls)} controls:")
for control in controls:
    print(f"  - {control['control_type']}: {control['name']}")
```

### Detecting Automation Backend

```python
from src.windows.window_inspector import WindowInspector

inspector = WindowInspector()
window_handle = 12345
backend = inspector.detect_automation_backend(window_handle)
print(f"Recommended backend: {backend}")
```

## Documentation

- [Detailed Usage Guide](docs/windows-inspection.md)
- [API Reference](docs/API.md) (Coming soon)
- [Security Guidelines](docs/security.md) (Coming soon)

## Testing on Non-Windows Systems

The unit tests use mocking to simulate Windows controls, allowing most tests to run on any platform. However, full integration testing requires a Windows environment.

### What Can Be Tested in Codex Cloud

- Mock-based unit tests
- Code structure validation
- Import and syntax checking
- Documentation generation

### What Must Be Tested on Windows

- Actual window detection
- Real control enumeration
- UI Automation backend functionality
- Win32 backend functionality
- Performance and stability

## Project Configuration

See [pyproject.toml](pyproject.toml) for project configuration details.

## Security Considerations

This tool implements the following security measures:

### Data Collection
- ✅ Only collects technical identifiers (handles, IDs, types)
- ❌ Never collects window titles that might contain sensitive info
- ❌ Never collects control text that might contain user data
- ❌ Never collects or transmits actual data from applications

### Actions
- ✅ Read-only access to controls
- ❌ No automatic clicking or interaction
- ❌ No database connections
- ❌ No modifications to application state

### Execution
- ✅ All processing happens locally
- ❌ No external service communication
- ❌ No data transmission to Codex Cloud or GitHub

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please open an issue in the repository.

---

**Note**: This tool is designed for diagnostic purposes only. It does not modify or interact with any applications.
