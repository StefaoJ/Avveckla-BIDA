"""
Tests for WindowInspector and ControlInspector modules.

Uses mocking to simulate Windows controls for testing in non-Windows environments.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

# Import the modules under test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Create a mock for pywinauto before importing
mock_pywinauto = MagicMock()
mock_application = MagicMock()
mock_desktop = MagicMock()

# Setup the mock module structure
mock_pywinauto.Application = mock_application
mock_pywinauto.Desktop = mock_desktop

# Patch pywinauto before any imports
sys.modules['pywinauto'] = mock_pywinauto
sys.modules['pywinauto.application'] = MagicMock()

from windows.window_inspector import WindowInspector
from windows.control_inspector import ControlInspector


# Now define our mock classes
class MockWindow:
    """Mock window for testing."""
    
    def __init__(self, handle, title, class_name, process_id):
        self.handle = handle
        self._title = title
        self._class_name = class_name
        self._process_id = process_id
        self._properties = {
            "class_name": class_name,
            "control_type": "Window",
        }
    
    def window_text(self):
        return self._title
    
    def get_properties(self):
        return self._properties
    
    def process_id(self):
        return self._process_id
    
    def exists(self):
        return True
    
    def children(self):
        # Return mock children for control inspection
        return [
            MockControl(1, "Button1", "Button", 1001, "btnOK"),
            MockControl(2, "Edit1", "Edit", 1002, "txtInput"),
            MockControl(3, "Static", "StaticText", 1003, "lblStatus"),
        ]


class MockControl:
    """Mock control for testing.""" 
    
    def __init__(self, handle, name, control_type, control_id, automation_id):
        self.handle = handle
        self._name = name
        self._control_type = control_type
        self._control_id = control_id
        self._automation_id = automation_id
        self._properties = {
            "name": name,
            "control_type": control_type,
            "control_id": control_id,
            "automation_id": automation_id,
            "rectangle": {"left": 0, "top": 0, "width": 100, "height": 25},
            "is_enabled": True,
            "is_visible": True,
            "class_name": control_type,
        }
    
    def window_text(self):
        return self._name
    
    def get_properties(self):
        return self._properties
    
    def children(self):
        return []


class MockDesktop:
    """Mock desktop for testing."""
    
    def __init__(self, backend=None):
        self.backend = backend
        self._windows = [
            MockWindow(100, "Application Window", "AppClass", 1000),
            MockWindow(200, "Dialog Box", "DialogClass", 1000),
        ]
    
    def windows(self):
        return self._windows


class MockApplication:
    """Mock application for testing."""
    
    def __init__(self, backend=None):
        self.backend = backend
        self._window = None
    
    def window(self, handle=None):
        if handle is not None:
            if handle == 300:
                return MockWindow(300, "Test Window", "TestClass", 2000)
            elif handle in [100, 200]:
                # Return windows from our mock desktop
                mock_desktop = MockDesktop()
                for w in mock_desktop.windows():
                    if w.handle == handle:
                        return w
            raise Exception(f"Window with handle {handle} not found")
        return MockWindow(999, "Default Window", "DefaultClass", 9999)


class TestWindowInspector(unittest.TestCase):
    """Tests for WindowInspector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.patchers = []
        
    def tearDown(self):
        """Clean up test fixtures."""
        for patcher in self.patchers:
            patcher.stop()

    def test_list_open_windows(self):
        """Test listing open windows."""
        # Setup mocks
        mock_desktop_instance = MockDesktop()
        
        # Patch Desktop to return our mock
        p1 = patch('windows.window_inspector.Desktop', return_value=mock_desktop_instance)
        self.patchers.append(p1)
        p1.start()
        
        inspector = WindowInspector()
        windows = inspector.list_open_windows()
        
        self.assertEqual(len(windows), 2)
        self.assertEqual(windows[0]['title'], "Application Window")
        self.assertEqual(windows[0]['class_name'], "AppClass")
        self.assertEqual(windows[0]['handle'], 100)
        self.assertEqual(windows[0]['backend'], "uia")

    def test_get_window_by_title(self):
        """Test getting a window by title."""
        mock_desktop_instance = MockDesktop()
        
        p1 = patch('windows.window_inspector.Desktop', return_value=mock_desktop_instance)
        self.patchers.append(p1)
        p1.start()
        
        inspector = WindowInspector()
        window = inspector.get_window_by_title("Application Window")
        
        self.assertIsNotNone(window)
        self.assertEqual(window['title'], "Application Window")
        
        # Test non-existent window
        window = inspector.get_window_by_title("Non-existent Window")
        self.assertIsNone(window)

    def test_get_window_by_handle(self):
        """Test getting a window by handle."""
        mock_app = MockApplication()
        
        p1 = patch('windows.window_inspector.Application', return_value=mock_app)
        self.patchers.append(p1)
        p1.start()
        
        inspector = WindowInspector()
        window = inspector.get_window_by_handle(300)
        
        self.assertIsNotNone(window)
        self.assertEqual(window['handle'], 300)
        
        # Test non-existent handle
        window = inspector.get_window_by_handle(9999)
        self.assertIsNone(window)

    def test_get_window_hierarchy(self):
        """Test getting window hierarchy."""
        # Create a desktop mock that can handle window(handle=...)
        mock_desktop_instance = MagicMock()
        mock_desktop_instance.windows.return_value = [
            MockWindow(100, "Application Window", "AppClass", 1000),
            MockWindow(200, "Dialog Box", "DialogClass", 1000),
        ]
        
        # Make the desktop itself callable to return windows
        # This handles the desktop.window(handle=100) call
        def get_window_by_handle(handle):
            for w in mock_desktop_instance.windows():
                if w.handle == handle:
                    return w
            raise Exception(f"Window with handle {handle} not found")
        
        mock_desktop_instance.window = get_window_by_handle
        
        p1 = patch('windows.window_inspector.Desktop', return_value=mock_desktop_instance)
        self.patchers.append(p1)
        p1.start()
        
        inspector = WindowInspector()
        hierarchy = inspector.get_window_hierarchy(100)
        
        self.assertIsNotNone(hierarchy)
        self.assertEqual(hierarchy['handle'], 100)
        self.assertEqual(hierarchy['title'], "Application Window")
        self.assertIn('children', hierarchy)

    def test_detect_automation_backend(self):
        """Test detecting automation backend."""
        # Mock the Application for both backends
        mock_app_uia = MagicMock()
        mock_app_win32 = MagicMock()
        
        # Create mock windows
        mock_window_uia = MockWindow(300, "Test Window", "TestClass", 2000)
        mock_window_win32 = MockWindow(300, "Test Window", "TestClass", 2000)
        
        mock_app_uia.window.return_value = mock_window_uia
        mock_app_win32.window.return_value = mock_window_win32
        
        # Patch Application to return our mocks
        def app_factory(backend):
            if backend == "uia":
                return mock_app_uia
            elif backend == "win32":
                return mock_app_win32
            return MagicMock()
        
        p1 = patch('windows.window_inspector.Application', side_effect=app_factory)
        self.patchers.append(p1)
        p1.start()
        
        inspector = WindowInspector()
        backend = inspector.detect_automation_backend(300)
        
        # Should return 'uia' if it works
        self.assertEqual(backend, "uia")


class TestControlInspector(unittest.TestCase):
    """Tests for ControlInspector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.patchers = []

    def tearDown(self):
        """Clean up test fixtures."""
        for patcher in self.patchers:
            patcher.stop()

    def test_list_controls(self):
        """Test listing controls in a window."""
        mock_app = MockApplication()
        
        p1 = patch('windows.control_inspector.Application', return_value=mock_app)
        self.patchers.append(p1)
        p1.start()
        
        inspector = ControlInspector()
        controls = inspector.list_controls(300)
        
        self.assertEqual(len(controls), 3)
        self.assertEqual(controls[0]['name'], "Button1")
        self.assertEqual(controls[0]['control_type'], "Button")
        self.assertEqual(controls[0]['control_id'], 1001)
        self.assertEqual(controls[0]['automation_id'], "btnOK")

    def test_find_controls_by_type(self):
        """Test finding controls by type."""
        mock_app = MockApplication()
        
        p1 = patch('windows.control_inspector.Application', return_value=mock_app)
        self.patchers.append(p1)
        p1.start()
        
        inspector = ControlInspector()
        buttons = inspector.find_controls_by_type(300, "Button")
        
        self.assertEqual(len(buttons), 1)
        self.assertEqual(buttons[0]['name'], "Button1")
        
        # Test non-existent type
        labels = inspector.find_controls_by_type(300, "Label")
        self.assertEqual(len(labels), 0)

    def test_find_controls_by_name(self):
        """Test finding controls by name."""
        mock_app = MockApplication()
        
        p1 = patch('windows.control_inspector.Application', return_value=mock_app)
        self.patchers.append(p1)
        p1.start()
        
        inspector = ControlInspector()
        controls = inspector.find_controls_by_name(300, "Button1")
        
        self.assertEqual(len(controls), 1)
        self.assertEqual(controls[0]['name'], "Button1")
        
        # Test non-existent name
        controls = inspector.find_controls_by_name(300, "Non-existent")
        self.assertEqual(len(controls), 0)

    def test_inspect_control_hierarchy(self):
        """Test inspecting control hierarchy."""
        mock_app = MockApplication()
        
        p1 = patch('windows.control_inspector.Application', return_value=mock_app)
        self.patchers.append(p1)
        p1.start()
        
        inspector = ControlInspector()
        hierarchy = inspector.inspect_control_hierarchy(300)
        
        self.assertIsNotNone(hierarchy)
        self.assertIn('window_handle', hierarchy)
        self.assertIn('controls', hierarchy)
        self.assertEqual(len(hierarchy['controls']), 3)

    def test_check_control_sensitivity(self):
        """Test checking control sensitivity."""
        mock_app = MockApplication()
        
        p1 = patch('windows.control_inspector.Application', return_value=mock_app)
        self.patchers.append(p1)
        p1.start()
        
        inspector = ControlInspector()
        sensitivity = inspector.check_control_sensitivity(300)
        
        self.assertIn('total_controls', sensitivity)
        self.assertEqual(sensitivity['total_controls'], 3)
        self.assertEqual(sensitivity['visible_controls'], 3)
        self.assertEqual(sensitivity['enabled_controls'], 3)
        self.assertIn('by_type', sensitivity)


class TestIntegration(unittest.TestCase):
    """Integration tests for window and control inspection."""

    def setUp(self):
        """Set up test fixtures."""
        self.patchers = []

    def tearDown(self):
        """Clean up test fixtures."""
        for patcher in self.patchers:
            patcher.stop()

    def test_full_inspection_workflow(self):
        """Test complete inspection workflow."""
        # Setup mocks
        mock_desktop_instance = MockDesktop()
        mock_app = MockApplication()
        
        p1 = patch('windows.window_inspector.Desktop', return_value=mock_desktop_instance)
        p2 = patch('windows.control_inspector.Application', return_value=mock_app)
        self.patchers.extend([p1, p2])
        p1.start()
        p2.start()
        
        # Create inspectors
        window_inspector = WindowInspector()
        control_inspector = ControlInspector()
        
        # List windows
        windows = window_inspector.list_open_windows()
        self.assertGreater(len(windows), 0)
        
        # Inspect first window's controls
        if windows:
            # Use a valid handle from our mock desktop
            valid_handle = windows[0]['handle']
            
            # For this test, we'll just verify the method can be called
            # The actual control listings are tested separately
            controls = control_inspector.list_controls(valid_handle)
            self.assertIsInstance(controls, list)
            
            # Check if any buttons exist
            buttons = control_inspector.find_controls_by_type(
                valid_handle, 
                "Button"
            )
            self.assertIsInstance(buttons, list)


if __name__ == '__main__':
    unittest.main()
