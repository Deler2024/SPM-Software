# File: gui/widgets/scan_parameter_widget.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QGridLayout, QMessageBox
)
from utils.logger import get_logger


class ScanParameterWidget(QWidget):
    """
    A widget for configuring scanner mode, scan range, and scan location.
    """

    def __init__(self, parent=None):
        """
        Initialize the Scan Parameter Widget.
        """
        super().__init__(parent)

        # Initialize logger
        self.logger = get_logger(__name__)

        # Set up the layout
        self.layout = QVBoxLayout(self)

        # SECTION: Scanner Mode Selection
        self.logger.debug("Initializing Scanner Mode Selection.")
        self.scanner_mode_layout = QHBoxLayout()
        self.scanner_mode_label = QLabel("Scanner Mode:", self)
        self.scanner_mode_layout.addWidget(self.scanner_mode_label)

        self.scanner_mode_selector = QComboBox(self)
        self.scanner_mode_selector.addItems(["Large Scanner", "Small Scanner"])
        self.scanner_mode_selector.setToolTip("Select the scanner mode (Large or Small).")
        self.scanner_mode_selector.currentIndexChanged.connect(self.update_max_range)
        self.scanner_mode_layout.addWidget(self.scanner_mode_selector)
        self.layout.addLayout(self.scanner_mode_layout)

        # SECTION: Input Fields for Scan Range and Location
        self.logger.debug("Initializing Input Fields for Scan Range and Location.")
        self.input_layout = QGridLayout()

        # Scan Range
        self.scan_range_label = QLabel("Scan Range (Width x Height):", self)
        self.input_layout.addWidget(self.scan_range_label, 0, 0)
        self.scan_range_width_input = QLineEdit(self)
        self.scan_range_width_input.setPlaceholderText("Width (cm)")
        self.scan_range_width_input.setToolTip("Enter the width of the scan range in cm.")
        self.input_layout.addWidget(self.scan_range_width_input, 0, 1)
        self.scan_range_height_input = QLineEdit(self)
        self.scan_range_height_input.setPlaceholderText("Height (cm)")
        self.scan_range_height_input.setToolTip("Enter the height of the scan range in cm.")
        self.input_layout.addWidget(self.scan_range_height_input, 0, 2)

        # Scan Location
        self.scan_location_label = QLabel("Scan Location (X Offset, Y Offset):", self)
        self.input_layout.addWidget(self.scan_location_label, 1, 0)
        self.scan_location_x_input = QLineEdit(self)
        self.scan_location_x_input.setPlaceholderText("X Offset (cm)")
        self.scan_location_x_input.setToolTip("Enter the X offset of the scan location in cm.")
        self.input_layout.addWidget(self.scan_location_x_input, 1, 1)
        self.scan_location_y_input = QLineEdit(self)
        self.scan_location_y_input.setPlaceholderText("Y Offset (cm)")
        self.scan_location_y_input.setToolTip("Enter the Y offset of the scan location in cm.")
        self.input_layout.addWidget(self.scan_location_y_input, 1, 2)

        self.layout.addLayout(self.input_layout)

        # SECTION: Initialize Maximum Ranges
        self.logger.debug("Initializing Maximum Ranges.")
        self.max_x_range = 100  # cm
        self.max_y_range = 100  # cm
        self.max_z_range = 30   # cm

    def update_max_range(self):
        """
        Update the maximum scan range based on the selected scanner mode.
        """
        self.logger.debug("Updating maximum scan range based on scanner mode.")
        mode = self.scanner_mode_selector.currentText()
        if mode == "Large Scanner":
            self.max_x_range = 100  # cm
            self.max_y_range = 100  # cm
            self.max_z_range = 30   # cm
        elif mode == "Small Scanner":
            self.max_x_range = 1  # cm
            self.max_y_range = 1  # cm
            self.max_z_range = 1  # cm
        self.logger.info(f"Updated max range: X={self.max_x_range} cm, Y={self.max_y_range} cm, Z={self.max_z_range} cm")

    def get_scan_parameters(self):
        """
        Get the scan parameters (range and location) entered by the user.
        :return: A dictionary with the scan parameters or None if validation fails.
        """
        self.logger.debug("Retrieving scan parameters.")
        try:
            width = float(self.scan_range_width_input.text())
            height = float(self.scan_range_height_input.text())
            x_offset = float(self.scan_location_x_input.text())
            y_offset = float(self.scan_location_y_input.text())

            # Validate the parameters
            self.validate_scan_parameters(width, height, x_offset, y_offset)

            self.logger.info(f"Scan parameters retrieved: Width={width}, Height={height}, X Offset={x_offset}, Y Offset={y_offset}")
            return {
                "width": width,
                "height": height,
                "x_offset": x_offset,
                "y_offset": y_offset,
            }
        except ValueError as e:
            self.logger.error(f"Error retrieving scan parameters: {e}")
            QMessageBox.critical(self, "Invalid Input", str(e))
            return None

    def validate_scan_parameters(self, width, height, x_offset, y_offset):
        """
        Validate the scan parameters.
        :param width: Width of the scan range.
        :param height: Height of the scan range.
        :param x_offset: X offset of the scan location.
        :param y_offset: Y offset of the scan location.
        :raises ValueError: If any parameter is invalid.
        """
        if width <= 0 or height <= 0:
            raise ValueError("Scan range must be positive.")
        if width > self.max_x_range or height > self.max_y_range:
            raise ValueError(f"Scan range exceeds maximum range ({self.max_x_range} cm x {self.max_y_range} cm).")
        if x_offset < 0 or y_offset < 0:
            raise ValueError("Scan location offsets must be non-negative.")
        if x_offset + width > self.max_x_range or y_offset + height > self.max_y_range:
            raise ValueError("Scan location exceeds maximum range.")