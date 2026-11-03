"""
Control Inspector Module

This module provides functionality to inspect and analyze controls within Windows application windows.
Supports both Win32 and UI Automation technologies.
"""

import logging
from typing import List, Dict, Any, Optional

try:
    import pywinauto
    from pywinauto import Application
    try:
        from pywinauto.application import WindowSpecification
    except ImportError:
        WindowSpecification = None
    HAS_PYWINAUTO = True
except ImportError:
    HAS_PYWINAUTO = False
    WindowSpecification = None

logger = logging.getLogger(__name__)


class ControlInspector:
    """
    Inspector for identifying and analyzing controls within Windows application windows.
    
    Uses pywinauto to enumerate controls and their properties.
    Collects technical identifiers for automation purposes.
    """

    def __init__(self, backend: str = "uia"):
        """
        Initialize the ControlInspector.
        
        Args:
            backend: Backend to use ('uia' for UI Automation, 'win32' for Win32 API)
        """
        if not HAS_PYWINAUTO:
            raise ImportError("pywinauto is required for control inspection. Install with: pip install pywinauto")
        
        self.backend = backend

    def list_controls(self, window_handle: int) -> List[Dict[str, Any]]:
        """
        List all controls in a specified window.
        
        Args:
            window_handle: Handle of the window to inspect
            
        Returns:
            List of dictionaries containing control information:
            - control_type: Type of control (e.g., Button, Edit, TreeView)
            - name: Control name/text
            - control_id: Control ID
            - automation_id: Automation ID
            - rectangle: Control position and size
            - is_enabled: Whether the control is enabled
            - is_visible: Whether the control is visible
        """
        controls = []
        
        try:
            app = Application(backend=self.backend)
            window = app.window(handle=window_handle)
            
            if not window.exists():
                logger.warning(f"Window with handle {window_handle} does not exist")
                return controls
            
            # Iterate through all controls in the window
            for control in window.children():
                try:
                    props = control.get_properties()
                    
                    control_info = {
                        "control_type": props.get("control_type", "Unknown"),
                        "name": props.get("name", ""),
                        "control_id": props.get("control_id", -1),
                        "automation_id": props.get("automation_id", ""),
                        "rectangle": props.get("rectangle", {}),
                        "is_enabled": props.get("is_enabled", False),
                        "is_visible": props.get("is_visible", False),
                        "backend": self.backend,
                    }
                    controls.append(control_info)
                    
                except Exception as e:
                    logger.warning(f"Failed to inspect control: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to list controls for window {window_handle}: {e}")
            
        return controls

    def get_control_properties(self, window_handle: int, control_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed properties for a specific control.
        
        Args:
            window_handle: Handle of the parent window
            control_id: ID of the control to inspect
            
        Returns:
            Dictionary with all available properties, or None if not found
        """
        try:
            app = Application(backend=self.backend)
            window = app.window(handle=window_handle)
            
            # Find the control by ID
            for control in window.children():
                try:
                    props = control.get_properties()
                    if props.get("control_id") == control_id:
                        return props
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to get control properties: {e}")
            
        return None

    def find_controls_by_type(
        self, 
        window_handle: int, 
        control_type: str
    ) -> List[Dict[str, Any]]:
        """
        Find all controls of a specific type in a window.
        
        Args:
            window_handle: Handle of the parent window
            control_type: Type of control to find (e.g., "Button", "Edit")
            
        Returns:
            List of matching control information dictionaries
        """
        matching_controls = []
        
        try:
            app = Application(backend=self.backend)
            window = app.window(handle=window_handle)
            
            for control in window.children():
                try:
                    props = control.get_properties()
                    if props.get("control_type") == control_type:
                        control_info = {
                            "control_type": control_type,
                            "name": props.get("name", ""),
                            "control_id": props.get("control_id", -1),
                            "automation_id": props.get("automation_id", ""),
                            "rectangle": props.get("rectangle", {}),
                        }
                        matching_controls.append(control_info)
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to find controls by type: {e}")
            
        return matching_controls

    def find_controls_by_name(
        self, 
        window_handle: int, 
        name: str
    ) -> List[Dict[str, Any]]:
        """
        Find all controls with a specific name in a window.
        
        Args:
            window_handle: Handle of the parent window
            name: Name/text of the control to find
            
        Returns:
            List of matching control information dictionaries
        """
        matching_controls = []
        
        try:
            app = Application(backend=self.backend)
            window = app.window(handle=window_handle)
            
            for control in window.children():
                try:
                    props = control.get_properties()
                    if props.get("name") == name:
                        control_info = {
                            "control_type": props.get("control_type", "Unknown"),
                            "name": name,
                            "control_id": props.get("control_id", -1),
                            "automation_id": props.get("automation_id", ""),
                            "rectangle": props.get("rectangle", {}),
                        }
                        matching_controls.append(control_info)
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to find controls by name: {e}")
            
        return matching_controls

    def inspect_control_hierarchy(
        self, 
        window_handle: int
    ) -> Optional[Dict[str, Any]]:
        """
        Inspect the complete hierarchy of controls in a window.
        
        Args:
            window_handle: Handle of the parent window
            
        Returns:
            Dictionary representing the control hierarchy
        """
        try:
            app = Application(backend=self.backend)
            window = app.window(handle=window_handle)
            
            hierarchy = {
                "window_handle": window_handle,
                "controls": [],
            }
            
            for control in window.children():
                try:
                    control_info = self._get_control_with_children(control)
                    hierarchy["controls"].append(control_info)
                except Exception:
                    continue
                    
            return hierarchy
            
        except Exception as e:
            logger.error(f"Failed to inspect control hierarchy: {e}")
            return None

    def _get_control_with_children(self, control: WindowSpecification) -> Dict[str, Any]:
        """Recursively gather control and its children."""
        try:
            props = control.get_properties()
            
            result = {
                "control_type": props.get("control_type", "Unknown"),
                "name": props.get("name", ""),
                "control_id": props.get("control_id", -1),
                "automation_id": props.get("automation_id", ""),
                "rectangle": props.get("rectangle", {}),
                "is_enabled": props.get("is_enabled", False),
                "is_visible": props.get("is_visible", False),
                "children": [],
            }
            
            # Recursively get children
            for child in control.children():
                try:
                    child_info = self._get_control_with_children(child)
                    result["children"].append(child_info)
                except Exception:
                    continue
                    
            return result
            
        except Exception as e:
            logger.warning(f"Failed to get control info: {e}")
            return {"error": str(e)}

    def check_control_sensitivity(self, window_handle: int) -> Dict[str, Any]:
        """
        Check which controls are sensitive (enhanced/visible) in a window.
        
        Args:
            window_handle: Handle of the parent window
            
        Returns:
            Dictionary with sensitivity status for different control types
        """
        try:
            controls = self.list_controls(window_handle)
            
            sensitivity = {
                "total_controls": len(controls),
                "visible_controls": 0,
                "enabled_controls": 0,
                "by_type": {},
            }
            
            for control in controls:
                control_type = control["control_type"]
                
                if control_type not in sensitivity["by_type"]:
                    sensitivity["by_type"][control_type] = {
                        "count": 0,
                        "visible": 0,
                        "enabled": 0,
                    }
                
                sensitivity["by_type"][control_type]["count"] += 1
                
                if control.get("is_visible", False):
                    sensitivity["visible_controls"] += 1
                    sensitivity["by_type"][control_type]["visible"] += 1
                    
                if control.get("is_enabled", False):
                    sensitivity["enabled_controls"] += 1
                    sensitivity["by_type"][control_type]["enabled"] += 1
                    
            return sensitivity
            
        except Exception as e:
            logger.error(f"Failed to check control sensitivity: {e}")
            return {"error": str(e)}
