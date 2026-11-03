"""
Window Inspector Module

This module provides functionality to inspect open windows in a Windows environment
using both Win32 API and UI Automation technologies.
"""

import logging
import time
from typing import List, Dict, Any, Optional

try:
    import pywinauto
    from pywinauto import Application, Desktop
    try:
        from pywinauto.application import WindowSpecification
    except ImportError:
        WindowSpecification = None
    HAS_PYWINAUTO = True
except ImportError:
    HAS_PYWINAUTO = False
    WindowSpecification = None

logger = logging.getLogger(__name__)


class WindowInspector:
    """
    Inspector for identifying and analyzing open windows in Windows.
    
    Uses pywinauto to enumerate windows and their properties.
    Supports both Win32 and UI Automation backends.
    """

    def __init__(self, backend: str = "uia"):
        """
        Initialize the WindowInspector.
        
        Args:
            backend: Backend to use ('uia' for UI Automation, 'win32' for Win32 API)
        """
        if not HAS_PYWINAUTO:
            raise ImportError("pywinauto is required for window inspection. Install with: pip install pywinauto")
        
        self.backend = backend
        self._known_windows: Dict[int, Dict[str, Any]] = {}

    def list_open_windows(self) -> List[Dict[str, Any]]:
        """
        List all open windows with their technical identifiers.
        
        Returns:
            List of dictionaries containing window information:
            - title: Window title
            - class_name: Window class name
            - handle: Window handle (HWND)
            - process_id: Process ID
            - backend: Backend used to detect the window
        """
        windows = []
        
        try:
            # Use Desktop to get all windows
            desktop = Desktop(backend=self.backend)
            
            for window in desktop.windows():
                try:
                    window_info = {
                        "title": window.window_text(),
                        "class_name": window.get_properties()["class_name"],
                        "handle": window.handle,
                        "process_id": window.process_id(),
                        "backend": self.backend,
                    }
                    windows.append(window_info)
                except Exception as e:
                    logger.warning(f"Failed to get window info: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to enumerate windows: {e}")
            
        return windows

    def get_window_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific window by its title.
        
        Args:
            title: Window title to search for
            
        Returns:
            Dictionary with window information, or None if not found
        """
        windows = self.list_open_windows()
        for window in windows:
            if window["title"] == title:
                return window
        return None

    def get_window_by_handle(self, handle: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific window by its handle.
        
        Args:
            handle: Window handle (HWND)
            
        Returns:
            Dictionary with window information, or None if not found
        """
        try:
            app = Application(backend=self.backend)
            window = app.window(handle=handle)
            return {
                "title": window.window_text(),
                "class_name": window.get_properties()["class_name"],
                "handle": window.handle,
                "process_id": window.process_id(),
                "backend": self.backend,
            }
        except Exception as e:
            logger.warning(f"Failed to get window by handle {handle}: {e}")
            return None

    def monitor_new_windows(
        self, 
        callback=None, 
        interval: float = 1.0, 
        timeout: Optional[float] = None
    ) -> None:
        """
        Monitor for new windows opening on the system.
        
        Args:
            callback: Optional callback function to call when a new window is detected.
                     The callback receives the new window's information dictionary.
            interval: Time in seconds between checks
            timeout: Maximum time in seconds to monitor (None for indefinite)
        """
        start_time = time.time()
        
        # Initial snapshot
        initial_windows = {w["handle"]: w for w in self.list_open_windows()}
        self._known_windows = initial_windows.copy()
        
        while True:
            if timeout and (time.time() - start_time) > timeout:
                logger.info("Monitoring timeout reached.")
                break
                
            try:
                current_windows = {w["handle"]: w for w in self.list_open_windows()}
                
                # Find new windows
                new_handles = set(current_windows.keys()) - set(self._known_windows.keys())
                
                for handle in new_handles:
                    new_window = current_windows[handle]
                    logger.info(f"New window detected: {new_window['title']} (Handle: {handle})")
                    
                    if callback:
                        try:
                            callback(new_window)
                        except Exception as e:
                            logger.error(f"Error in callback: {e}")
                            
                # Update known windows
                self._known_windows = current_windows.copy()
                
            except Exception as e:
                logger.error(f"Error during window monitoring: {e}")
                
            time.sleep(interval)

    def detect_automation_backend(self, window_handle: int) -> Optional[str]:
        """
        Detect which automation backend (Win32 or UI Automation) works best for a window.
        
        Args:
            window_handle: Handle of the window to test
            
        Returns:
            'uia' if UI Automation works, 'win32' if Win32 works, None if neither works
        """
        try:
            # Try UI Automation first
            app_uia = Application(backend="uia")
            window_uia = app_uia.window(handle=window_handle)
            if window_uia.exists():
                return "uia"
        except Exception:
            pass
            
        try:
            # Try Win32
            app_win32 = Application(backend="win32")
            window_win32 = app_win32.window(handle=window_handle)
            if window_win32.exists():
                return "win32"
        except Exception:
            pass
            
        return None

    def get_window_hierarchy(self, window_handle: int) -> Optional[Dict[str, Any]]:
        """
        Get the complete hierarchy of a window and its children.
        
        Args:
            window_handle: Handle of the parent window
            
        Returns:
            Dictionary representing the window hierarchy
        """
        try:
            desktop = Desktop(backend=self.backend)
            parent = desktop.window(handle=window_handle)
            
            hierarchy = {
                "handle": parent.handle,
                "title": parent.window_text(),
                "class_name": parent.get_properties()["class_name"],
                "children": [],
            }
            
            # Recursively get children
            self._get_child_windows(parent, hierarchy["children"])
            
            return hierarchy
            
        except Exception as e:
            logger.error(f"Failed to get window hierarchy: {e}")
            return None

    def _get_child_windows(self, parent: WindowSpecification, children: List[Dict[str, Any]]) -> None:
        """Recursively gather child windows."""
        try:
            for child in parent.children():
                try:
                    child_info = {
                        "handle": child.handle,
                        "title": child.window_text(),
                        "class_name": child.get_properties()["class_name"],
                        "children": [],
                    }
                    children.append(child_info)
                    self._get_child_windows(child, child_info["children"])
                except Exception:
                    continue
        except Exception:
            pass
