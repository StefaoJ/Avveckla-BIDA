# Windows Application Inspection Guide

This guide provides instructions for using the Windows application inspection tools to diagnose automation capabilities of legacy Windows applications.

## Overview

The diagnostic tools are designed to:
- Identify all open application windows
- Enumerate controls within windows
- Collect technical identifiers for automation
- Detect which automation backend (Win32 or UI Automation) works best
- Monitor for new windows opening
- Generate reports without capturing sensitive information

## Prerequisites

### Required Software
- **Windows OS**: These tools are designed for Windows and require Windows-specific libraries
- **Python**: Version 3.8 or higher
- **pywinauto**: The main library for Windows automation

### Installation

```bash
# Install required packages
pip install pywinauto==0.6.8
```

### Dependencies
- `pywinauto` with PyWin32 or pywinauto with UI Automation support
- Windows API access

## Usage Instructions

### Running the main inspection script

```bash
# Navigate to the project directory
cd /path/to/your/project

# Run the inspection script
python scripts/inspect_windows_app.py
```

### Command-line options

The script accepts the following options:

```
--backend BACKEND    Specify the automation backend: 'uia' (default) or 'win32'
--interval NUMBER    Set monitoring interval in seconds (default: 1.0)
--timeout NUMBER     Set monitoring timeout in seconds (default: None - indefinite)
--log-file FILE     Specify log file path (default: window_inspection.log)
--verbose           Enable verbose logging
```

### Example Usage Scenarios

#### Basic Window Inspection

```python
from src.windows.window_inspector import WindowInspector

# Create inspector with UI Automation backend
inspector = WindowInspector(backend='uia')

# List all open windows
windows = inspector.list_open_windows()

for window in windows:
    print(f"Window: {window['title']}")
    print(f"  Class: {window['class_name']}")
    print(f"  Handle: {window['handle']}")
    print(f"  Process ID: {window['process_id']}")
```

#### Control Inspection

```python
from src.windows.control_inspector import ControlInspector

# Create control inspector
control_inspector = ControlInspector(backend='uia')

# Get all controls in a window
window_handle = 12345  # Replace with actual window handle
controls = control_inspector.list_controls(window_handle)

for control in controls:
    print(f"Control: {control['control_type']}")
    print(f"  Name: {control['name']}")
    print(f"  Automation ID: {control['automation_id']}")
    print(f"  Control ID: {control['control_id']}")
```

#### Monitoring for New Windows

```python
from src.windows.window_inspector import WindowInspector

def on_new_window(window_info):
    print(f"New window detected: {window_info['title']}")

inspector = WindowInspector()

# Monitor for new windows with a callback
inspector.monitor_new_windows(
    callback=on_new_window,
    interval=0.5,
    timeout=60  # Monitor for 60 seconds
)
```

#### Detecting Automation Backend

```python
from src.windows.window_inspector import WindowInspector

inspector = WindowInspector()

# Check which backend works best for a window
window_handle = 12345
backend = inspector.detect_automation_backend(window_handle)

print(f"Recommended backend: {backend}")
```

#### Getting Window Hierarchy

```python
from src.windows.window_inspector import WindowInspector

inspector = WindowInspector()
hierarchy = inspector.get_window_hierarchy(window_handle)

# hierarchy contains nested information about parent-child relationships
```

#### Control Sensitivity Analysis

```python
from src.windows.control_inspector import ControlInspector

control_inspector = ControlInspector()
sensitivity = control_inspector.check_control_sensitivity(window_handle)

print(f"Total controls: {sensitivity['total_controls']}")
print(f"Visible controls: {sensitivity['visible_controls']}")
print(f"Enabled controls: {sensitivity['enabled_controls']}")
```

## Automation Backend Comparison

### UI Automation (uia)

**Pros:**
- Modern API designed for accessibility
- Better support for newer applications
- More consistent across different applications
- Supports Microsoft Active Accessibility (MSAA)

**Cons:**
- May not work with very old applications
- Slower for some operations
- Less control over low-level details

### Win32 API (win32)

**Pros:**
- Direct access to Windows API
- Works with older applications
- Faster for basic operations
- More control over window messages

**Cons:**
- Not all modern controls are properly exposed
- Requires understanding of Win32 API
- Less consistent across applications

## Security Guidelines

### Data Collection Restrictions
- **No sensitive information**: The tools are designed to only collect technical identifiers
- **No automatic actions**: The tools do not perform any automatic clicking or interaction
- **Read-only**: The tools have read-only access to controls
- **Local execution**: All inspections must be run locally on the target machine

### Logging Guidelines
- Only log technical identifiers (handles, IDs, types)
- Do not log window titles that might contain sensitive information
- Do not log control text that might contain user data
- All logs are stored locally and never transmitted

### Safe Usage
- Run the tools in a non-production environment first
- Verify the application is not in use before inspecting
- Do not leave monitoring tools running unattended
- Always review logs before sharing with others

## Verifying Installation

### Check pywinauto installation

```python
import pywinauto
print(f"pywinauto version: {pywinauto.__version__}")
```

### Verify Backend Support

```python
from pywinauto.application import Application

# Test UI Automation
try:
    app = Application(backend='uia')
    print("UI Automation backend: Available")
except Exception as e:
    print(f"UI Automation backend: Not available - {e}")

# Test Win32
try:
    app = Application(backend='win32')
    print("Win32 backend: Available")
except Exception as e:
    print(f"Win32 backend: Not available - {e}")
```

## Troubleshooting

### Common Issues

#### ImportError: pywinauto not found

**Solution:** Install pywinauto package
```bash
pip install pywinauto
```

#### Backend 'uia' failed to initialize

**Solution:** Install UI Automation support
```bash
# For Windows
pip install pywinauto[uiacom]
```

#### Backend 'win32' failed to initialize

**Solution:** Install PyWin32
```bash
pip install pywin32
```

#### Windows not detected

**Solution:** Ensure the script is running with appropriate permissions
- Run as administrator
- Ensure the application is actually open
- Try using the other backend

#### Controls not showing up

**Solution:** Try switching the backend
```python
# Switch from 'uia' to 'win32' or vice versa
inspector = WindowInspector(backend='win32')
```

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Testing

### Running Tests

The project includes unit tests that work with mocked Windows controls:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_window_inspector.py

# Run with verbose output
python -m pytest tests/ -v
```

Note: Some tests may require specific Python versions or environments.

## Limitations

### Platform Limitations
- These tools only work on Windows
- Some older applications may not be fully compatible
- Several modern applications (UWP, Windows Store apps) may not work

### Functionality Limitations
- Cannot access minimized windows reliably
- Cannot inspect password fields or secure controls
- Cannot access controls in elevated (admin) windows from non-elevated processes

## Future Enhancements

- Support for Playwright integration for web-based applications
- Enhanced reporting with HTML output
- Control interaction testing (read-only mode only)
- Performance metrics for control access
- Cross-platform support for testing on non-Windows systems

## References

- [pywinauto Documentation](https://pywinauto.readthedocs.io/)
- [UI Automation Overview](https://docs.microsoft.com/en-us/windows/win32/uiautomation/ui-automation-overview)
- [Win32 API Documentation](https://docs.microsoft.com/en-us/windows/win32/api/)
