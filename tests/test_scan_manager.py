# File: D:/Documents/Project/SPM/copilot/SPM-Software/tests/test_scan_manager.py

import sys
import os

# Dynamically add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from scan_engine.scan_manager import ScanManager  # Ensure this import is correct

from control.motion_controller import MotionController

class TestScanManager(unittest.TestCase):
    def setUp(self):
        self.motion_controller = MotionController()
        self.scan_manager = ScanManager(motion_controller=self.motion_controller)

    def test_start_scan(self):
        """
        Test starting a scan.
        """
        self.scan_manager.start_scan()
        self.assertTrue(self.scan_manager.is_scanning)

    def test_stop_scan(self):
        """
        Test stopping a scan.
        """
        self.scan_manager.start_scan()
        self.scan_manager.stop_scan()
        self.assertFalse(self.scan_manager.is_scanning)

if __name__ == "__main__":
    unittest.main()