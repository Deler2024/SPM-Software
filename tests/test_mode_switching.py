# File: D:/Documents/Project/SPM/copilot/SPM-Software/tests/test_mode_switching.py

import sys
import os

# Dynamically add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from control.mode_switcher import ModeSwitcher  # Ensure this import is correct

class TestModeSwitching(unittest.TestCase):
    """
    Unit tests for the ModeSwitcher class.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a ModeSwitcher instance.
        """
        self.mode_switcher = ModeSwitcher()

    def test_switch_to_contact_mode(self):
        """
        Test switching to contact mode.
        """
        self.mode_switcher.switch_mode("contact")
        self.assertEqual(self.mode_switcher.current_mode, "contact")

    def test_switch_to_noncontact_mode(self):
        """
        Test switching to non-contact mode.
        """
        self.mode_switcher.switch_mode("noncontact")
        self.assertEqual(self.mode_switcher.current_mode, "noncontact")

    def test_invalid_mode(self):
        """
        Test switching to an invalid mode.
        """
        with self.assertRaises(ValueError):
            self.mode_switcher.switch_mode("invalid_mode")

if __name__ == "__main__":
    unittest.main()