from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt
from utils.logger import get_logger
import pyqtgraph as pg

# Initialize logger
logger = get_logger(__name__)

class XYScannerTab(QWidget):
    """
    Tab for configuring and controlling the XY scanner.
    """

    def __init__(self, parent=None):
        """
        Initialize the XYScannerTab.
        """
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Add XY Scanner Configuration
        self.xy_scanner_group = self.create_xy_scanner_group()
        self.layout.addWidget(self.xy_scanner_group)

    def create_xy_scanner_group(self) -> QGroupBox:
        """
        Create the XY scanner configuration group.
        :return: QGroupBox containing XY scanner parameters.
        """
        group = QGroupBox("XY Scanner Configuration")
        layout = QFormLayout()

        # X Range
        self.xy_width_input = QLineEdit()
        self.xy_width_input.setValidator(QDoubleValidator(0.1, 100.0, 2))
        self.xy_width_input.setPlaceholderText("Width (cm)")
        layout.addRow("Scan Width (X):", self.xy_width_input)

        # Y Range
        self.xy_height_input = QLineEdit()
        self.xy_height_input.setValidator(QDoubleValidator(0.1, 100.0, 2))
        self.xy_height_input.setPlaceholderText("Height (cm)")
        layout.addRow("Scan Height (Y):", self.xy_height_input)

        # X Resolution
        self.xy_resolution_x_input = QLineEdit()
        self.xy_resolution_x_input.setValidator(QIntValidator(1, 1000))
        self.xy_resolution_x_input.setPlaceholderText("Points in X")
        layout.addRow("Resolution (X):", self.xy_resolution_x_input)

        # Y Resolution
        self.xy_resolution_y_input = QLineEdit()
        self.xy_resolution_y_input.setValidator(QIntValidator(1, 1000))
        self.xy_resolution_y_input.setPlaceholderText("Points in Y")
        layout.addRow("Resolution (Y):", self.xy_resolution_y_input)

        group.setLayout(layout)
        return group

    def create_scan_direction_group(self) -> QGroupBox:
        """
        Create the scan direction controls group.
        :return: QGroupBox containing scan direction controls.
        """
        group = QGroupBox("Scan Direction")
        layout = QFormLayout()

        # Add a dropdown to select the scan direction
        self.scan_direction_dropdown = QComboBox()
        self.scan_direction_dropdown.addItems(["Forward Only", "Backward Only", "Both"])
        self.scan_direction_dropdown.currentIndexChanged.connect(self.update_scan_direction)
        layout.addRow("Scan Direction:", self.scan_direction_dropdown)

        # Add a label to display the current scanning direction
        self.current_direction_label = QLabel("Scanning Forward")
        layout.addRow("Current Direction:", self.current_direction_label)

        group.setLayout(layout)
        return group

    def update_scan_direction(self, index):
        """
        Update the scan direction based on the selected option.
        :param index: Index of the selected scan direction.
        """
        direction = self.scan_direction_dropdown.itemText(index)
        logger.info(f"Updated scan direction to {direction}")
        self.current_direction_label.setText(f"Scanning {direction}")