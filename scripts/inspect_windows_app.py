#!/usr/bin/env python3
"""
Script to inspect Windows applications for automation diagnostics.
This script uses pywinauto to identify and analyze open application windows and their controls.
"""

import logging
import sys
from pathlib import Path

# Ensure src is in the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from windows.window_inspector import WindowInspector
from windows.control_inspector import ControlInspector


def setup_logging():
    """Configure logging to only capture technical identifiers and status information."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("window_inspection.log"),
        ],
    )
    return logging.getLogger(__name__)


def main():
    """Main entry point for the Windows application inspection script."""
    logger = setup_logging()
    logger.info("Starting Windows application inspection...")

    try:
        # Initialize inspectors
        window_inspector = WindowInspector()
        control_inspector = ControlInspector()

        # Get all open windows
        windows = window_inspector.list_open_windows()
        logger.info(f"Found {len(windows)} open windows")

        for window in windows:
            logger.info(f"Window: {window['title']} (Class: {window['class_name']}, ID: {window['handle']})")

            # Inspect controls for each window
            try:
                controls = control_inspector.list_controls(window["handle"])
                logger.info(f"  Found {len(controls)} controls in window")

                for control in controls:
                    logger.info(
                        f"    Control: {control['control_type']} "
                        f"(ID: {control['control_id']}, Name: {control['name']}, "
                        f"AutomationID: {control['automation_id']})"
                    )
            except Exception as e:
                logger.warning(f"  Failed to inspect controls for window {window['handle']}: {e}")

        # Monitor for new windows
        logger.info("Starting window monitoring... (Press Ctrl+C to stop)")
        window_inspector.monitor_new_windows()

    except KeyboardInterrupt:
        logger.info("Inspection stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
