# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/widgets/configuration_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QMessageBox
from utils.logger import get_logger
# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/widgets/configuration_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QMessageBox
)
from utils.logger import get_logger


# Initialize logger
logger = get_logger(__name__)

class ConfigurationWindow(QDialog):
    """
    Configuration window for setting up scan parameters, hardware settings, and data acquisition.
    """

    def __init__(self, parent=None):
        """
        Initialize the Configuration Window.
        """
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.setGeometry(200, 200, 600, 400)

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add sections for configuration
        self._initialize_mode_selection()
        self._initialize_scan_parameters()
        self._initialize_hardware_settings()
        self._initialize_data_acquisition_settings()

        # Add Save and Reset buttons
        self._initialize_buttons()

        logger.info("ConfigurationWindow initialized successfully.")

    def _initialize_mode_selection(self):
        """
        Initialize the mode selection section.
        """
        logger.debug("Initializing mode selection...")
        self.layout.addWidget(QLabel("Mode Selection:"))
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Contact", "Tapping", "Non-contact"])  # Example for AFM
        self.layout.addWidget(self.mode_selector)

    def _initialize_scan_parameters(self):
        """
        Initialize the scan parameters section.
        """
        logger.debug("Initializing scan parameters...")
        self.layout.addWidget(QLabel("Scan Parameters:"))
        grid = QGridLayout()

        # Scan size
        grid.addWidget(QLabel("Scan Size (X, Y):"), 0, 0)
        self.scan_size_x = QLineEdit()
        self.scan_size_x.setPlaceholderText("X (µm)")
        grid.addWidget(self.scan_size_x, 0, 1)
        self.scan_size_y = QLineEdit()
        self.scan_size_y.setPlaceholderText("Y (µm)")
        grid.addWidget(self.scan_size_y, 0, 2)

        # Resolution
        grid.addWidget(QLabel("Resolution (Points per Line, Lines):"), 1, 0)
        self.resolution_x = QLineEdit()
        self.resolution_x.setPlaceholderText("Points per Line")
        grid.addWidget(self.resolution_x, 1, 1)
        self.resolution_y = QLineEdit()
        self.resolution_y.setPlaceholderText("Number of Lines")
        grid.addWidget(self.resolution_y, 1, 2)

        # Scan speed
        grid.addWidget(QLabel("Scan Speed (µm/s):"), 2, 0)
        self.scan_speed = QLineEdit()
        self.scan_speed.setPlaceholderText("Speed")
        grid.addWidget(self.scan_speed, 2, 1)

        self.layout.addLayout(grid)

    def _initialize_hardware_settings(self):
        """
        Initialize the hardware settings section.
        """
        logger.debug("Initializing hardware settings...")
        self.layout.addWidget(QLabel("Hardware Settings:"))
        grid = QGridLayout()

        # Scanner calibration
        grid.addWidget(QLabel("Scanner Calibration:"), 0, 0)
        self.scanner_calibration = QLineEdit()
        self.scanner_calibration.setPlaceholderText("Calibration Factor")
        grid.addWidget(self.scanner_calibration, 0, 1)

        # Detector settings
        grid.addWidget(QLabel("Detector Settings:"), 1, 0)
        self.detector_settings = QLineEdit()
        self.detector_settings.setPlaceholderText("Detector Gain")
        grid.addWidget(self.detector_settings, 1, 1)

        self.layout.addLayout(grid)

    def _initialize_data_acquisition_settings(self):
        """
        Initialize the data acquisition settings section.
        """
        logger.debug("Initializing data acquisition settings...")
        self.layout.addWidget(QLabel("Data Acquisition Settings:"))
        grid = QGridLayout()

        # Sampling rate
        grid.addWidget(QLabel("Sampling Rate (Hz):"), 0, 0)
        self.sampling_rate = QLineEdit()
        self.sampling_rate.setPlaceholderText("Rate")
        grid.addWidget(self.sampling_rate, 0, 1)

        # Filter settings
        grid.addWidget(QLabel("Filter Settings:"), 1, 0)
        self.filter_settings = QLineEdit()
        self.filter_settings.setPlaceholderText("Filter Type")
        grid.addWidget(self.filter_settings, 1, 1)

        self.layout.addLayout(grid)

    def _initialize_buttons(self):
        """
        Initialize Save and Reset buttons.
        """
        logger.debug("Initializing buttons...")
        button_layout = QHBoxLayout()

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_configuration)
        button_layout.addWidget(self.save_button)

        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_button)

        self.layout.addLayout(button_layout)

    def save_configuration(self):
        """
        Save the current configuration.
        """
        logger.info("Saving configuration...")
        QMessageBox.information(self, "Save Configuration", "Configuration saved successfully!")

    def reset_to_defaults(self):
        """
        Reset all fields to their default values.
        """
        logger.info("Resetting configuration to defaults...")
        self.mode_selector.setCurrentIndex(0)
        self.scan_size_x.clear()
        self.scan_size_y.clear()
        self.resolution_x.clear()
        self.resolution_y.clear()
        self.scan_speed.clear()
        self.scanner_calibration.clear()
        self.detector_settings.clear()
        self.sampling_rate.clear()
        self.filter_settings.clear()
        QMessageBox.information(self, "Reset Configuration", "Configuration reset to default values.")