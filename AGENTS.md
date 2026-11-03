# AGENTS.md - Agent Configuration and Guidelines

This file provides configuration and guidelines for AI agents working with this Windows application diagnostics project.

## Project Overview

**Purpose**: Develop a Python-based diagnostic tool for inspecting legacy Windows applications to determine automation capabilities.

**Phase**: Uppdrag 1 - Diagnostic Tool Development (No data extraction or archiving yet)

**Security Level**: HIGH - Sensitive legacy system access

## Agent Environment Setup

### Required Tools
- Python 3.8+
- pywinauto 0.6.8+
- pytest for testing
- Git for version control

### Installation for Testing
```bash
# Install project dependencies
pip install pywinauto pytest

# Install with UI Automation support (Windows only)
pip install pywinauto[uiacom]
```

## Agent Workflow

### Development Guidelines

#### Code Standards
- Use type hints (Python 3.8+)
- Follow PEP 8 style guide
- Include docstrings for all public functions
- Use logging instead of print statements
- Implement proper error handling

#### Security Requirements
```python
# ALWAYS - Safe practices
- Use read-only operations
- Only collect technical identifiers
- Validate all inputs
- Log only non-sensitive information

# NEVER - Prohibited actions
- Do NOT perform automatic clicking
- Do NOT connect to production databases
- Do NOT collect customer information
- Do NOT transmit data externally
- Do NOT modify application state
```

#### Testing Approach
1. Use mocking for Windows API calls
2. Create synthetic test data
3. Test on non-Windows platforms with mocks
4. Document what requires Windows verification

### File Naming Conventions

**Modules**: `snake_case.py`
**Classes**: `PascalCase`
**Functions**: `snake_case`
**Variables**: `snake_case`
**Constants**: `UPPER_SNAKE_CASE`

### Directory Structure
```
project/
├── legacy-case-archive/      # For archived cases (future)
│   ├── testuttag/            # Extracted test data
│   ├── hela-ärenden/         # Complete case files
│   └── annat/                # Other materials
├── scripts/                   # Execution scripts
├── src/                      # Source code
│   └── windows/              # Windows-specific modules
├── tests/                    # Test files
└── docs/                     # Documentation
```

## Agent Tasks and Commands

### Available Commands

```bash
# Run the main inspection script
python scripts/inspect_windows_app.py

# Run tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_window_inspector.py -v

# Check imports and syntax
python -m py_compile scripts/inspect_windows_app.py
python -m py_compile src/windows/window_inspector.py
python -m py_compile src/windows/control_inspector.py

# Linting (if ruff available)
ruff check .

# Type checking (if mypy available)
mypy src/ tests/
```

### Common Development Tasks

#### Creating New Modules
1. Add file to appropriate directory
2. Include docstring with purpose
3. Add `__init__.py` if new package
4. Update imports as needed

#### Adding Tests
1. Create test file in `/tests/`
2. Use `unittest` or `pytest` framework
3. Mock Windows APIs for cross-platform compatibility
4. Document Windows-specific requirements

## Agent Capabilities and Limitations

### What Agents Can Do
✅ Create and modify Python files
✅ Run tests in mock environment
✅ Generate documentation
✅ Create project structure
✅ Analyze code for issues
✅ Suggest improvements

### What Agents Cannot Do
❌ Run actual Windows applications
❌ Access real Windows GUI elements
❌ Connect to production databases
❌ Execute on Windows OS directly
❌ Access customer data

### Required Manual Verification
The following must be verified on a real Windows machine:
- Actual window detection
- Real control enumeration
- UI Automation backend functionality
- Win32 backend functionality
- Performance characteristics
- Memory usage

## Testing Matrix

### Test Types

| Test Type | Environment | Mocking | Coverage |
|-----------|-------------|---------|----------|
| Unit Tests | Any OS | Yes | High |
| Integration Tests | Windows | Partial | Medium |
| System Tests | Windows | No | Low |

### Test Execution by Environment

#### Codex Cloud (Any OS)
- ✅ Unit tests with mocks
- ✅ Syntax validation
- ✅ Import checking
- ✅ Code style checking
- ❌ Real window inspection
- ❌ Actual automation

#### Windows Development Machine
- ✅ All unit tests
- ✅ Integration tests
- ✅ Real window inspection
- ✅ Backend compatibility tests
- ✅ Performance tests

## Code Review Checklist

### Before Committing
- [ ] All tests pass in mock environment
- [ ] Code follows PEP 8 guidelines
- [ ] Type hints are present
- [ ] Docstrings are complete
- [ ] Error handling is implemented
- [ ] Logging is used (not print)
- [ ] No sensitive data in logs
- [ ] No automatic actions
- [ ] Read-only operations only

### Before Merging
- [ ] Tests pass in Codex Cloud
- [ ] Code reviewed by another agent/developer
- [ ] Documentation updated
- [ ] Changes logged in CHANGELOG
- [ ] Version number updated if needed

## Project Phases

### Phase 1: Diagnostic Tool Development (Current)
**Status**: In Progress
**Goal**: Create tools to inspect and analyze Windows applications
**Deliverables**:
- [x] Project structure
- [x] Window inspector module
- [x] Control inspector module
- [x] Main inspection script
- [x] Unit tests with mocks
- [x] Documentation
- [ ] Manual Windows testing

### Phase 2: Data Extraction (Future)
**Status**: Not Started
**Goal**: Extract data from identified applications
**Requirements**:
- Diagnostic tools must be verified on target systems
- Security review of extraction methods
- Approval from system owners

### Phase 3: Archiving System (Future)
**Status**: Not Started
**Goal**: Archive extracted data to appropriate storage
**Requirements**:
- Phase 2 completion
- Storage system design
- Data retention policies

## Agent-Specific Notes

### For opencode Agent
- Use tools: Read, Write, Edit, Bash, Glob, Grep
- Prefer parallel tool calls when independent
- Minimize output tokens
- Follow project conventions
- Always verify before running destructive commands

### For Testing Agent
- Focus on mock-based testing
- Document Windows-specific requirements
- Create synthetic test data
- Verify code quality metrics

### For Documentation Agent
- Generate clear, concise documentation
- Include examples
- Document Windows-specific limitations
- Update README and docs/

## Common Issues and Solutions

### ImportError: pywinauto not found
```bash
pip install pywinauto
```

### Backend 'uia' failed to initialize
```bash
pip install pywinauto[uiacom]
```

### Backend 'win32' failed to initialize
```bash
pip install pywin32
```

### Test failures on non-Windows systems
- Tests use mocking - failures indicate mock issues
- Verify mock implementations
- Document Windows-specific functionality

## External Resources

- [pywinauto Documentation](https://pywinauto.readthedocs.io/)
- [UI Automation Overview](https://docs.microsoft.com/en-us/windows/win32/uiautomation/ui-automation-overview)
- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)

---

**Last Updated**: 2026-11-03
**Agent Configuration Version**: 1.0
