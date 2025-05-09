# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/panels/z_scanner_panel.py

import sys
import os

# Dynamically add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QTimer
from control.motion_controller import MotionController

class ZScannerPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Z-Scanner Control")
        self.layout = QVBoxLayout(self)

        # Add widgets for Z-scanner control
        self.position_label = QLabel("Z Position: 0 µm")
        self.layout.addWidget(self.position_label)

        self.move_button = QPushButton("Move Z")
        self.layout.addWidget(self.move_button)

        self.move_button.clicked.connect(self.move_z)

        # Initialize MotionController
        self.motion_controller = MotionController()

        # Timer for updating the Z position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(1000)  # Update every second

    def move_z(self):
        # Example: Move Z to 50 µm
        self.motion_controller.move_z(50)

    def update_position(self):
        # Update the Z position label
        z_position = self.motion_controller.get_z_position()
        self.position_label.setText(f"Z Position: {z_position} µm")