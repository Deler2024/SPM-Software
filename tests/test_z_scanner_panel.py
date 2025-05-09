import unittest
from PyQt5.QtWidgets import QApplication
from gui.panels.z_scanner_panel import ZScannerPanel

class TestZScannerPanel(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.panel = ZScannerPanel()

    def test_initial_position(self):
        self.assertEqual(self.panel.position_label.text(), "Z Position: 0 µm")

    def test_move_z(self):
        self.panel.move_z()
        self.assertEqual(self.panel.motion_controller.get_z_position(), 50)

    def tearDown(self):
        self.app.quit()

if __name__ == "__main__":
    unittest.main()