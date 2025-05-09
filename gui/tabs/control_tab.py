from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QGroupBox, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtCore import Qt
import json
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class ControlTab(QWidget):
    """
    Tab for controlling the scanner's mode, size, and scanning mode.
    """

    def __init__(self, parent=None):
        """
        Initialize the ControlTab.
        """
        super().__init__(parent)
        logger.info("Initializing ControlTab...")

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add Mode Selector
        self.mode_group = self.create_mode_selector()
        self.layout.addWidget(self.mode_group)

        # Add Scanner Size Selector
        self.size_group = self.create_size_selector()
        self.layout.addWidget(self.size_group)

        # Add Scanning Mode Selector
        self.scanning_mode_group = self.create_scanning_mode_selector()
        self.layout.addWidget(self.scanning_mode_group)

        # Add Save and Load Configuration Buttons
        self.save_load_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_configuration)
        self.save_load_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Configuration")
        self.load_button.clicked.connect(self.load_configuration)
        self.save_load_layout.addWidget(self.load_button)

        self.layout.addLayout(self.save_load_layout)

        logger.info("ControlTab initialized successfully.")

    def create_mode_selector(self) -> QGroupBox:
        """
        Create the mode selector for Simulated and Hardware modes.
        :return: QGroupBox containing the mode selector.
        """
        group = QGroupBox("Operation Mode")
        layout = QHBoxLayout()

        self.simulated_mode = QRadioButton("Simulated")
        self.simulated_mode.setChecked(True)  # Default to Simulated mode
        self.hardware_mode = QRadioButton("Hardware")

        self.mode_button_group = QButtonGroup()
        self.mode_button_group.addButton(self.simulated_mode)
        self.mode_button_group.addButton(self.hardware_mode)

        layout.addWidget(self.simulated_mode)
        layout.addWidget(self.hardware_mode)

        group.setLayout(layout)
        return group

    def create_size_selector(self) -> QGroupBox:
        """
        Create the scanner size selector for Large and Small scanners.
        :return: QGroupBox containing the size selector.
        """
        group = QGroupBox("Scanner Size")
        layout = QHBoxLayout()

        self.large_scanner = QRadioButton("Large (X=100cm, Y=100cm, Z=30cm)")
        self.large_scanner.setChecked(True)  # Default to Large scanner
        self.small_scanner = QRadioButton("Small (X=5cm, Y=5cm, Z=1cm)")

        self.size_button_group = QButtonGroup()
        self.size_button_group.addButton(self.large_scanner)
        self.size_button_group.addButton(self.small_scanner)

        layout.addWidget(self.large_scanner)
        layout.addWidget(self.small_scanner)

        group.setLayout(layout)
        return group

    def create_scanning_mode_selector(self) -> QGroupBox:
        """
        Create the scanning mode selector for STM, AFM, contact, and non-contact modes.
        :return: QGroupBox containing the scanning mode selector.
        """
        group = QGroupBox("Scanning Mode")
        layout = QHBoxLayout()

        self.scanning_mode_dropdown = QComboBox()
        self.scanning_mode_dropdown.addItems(["STM", "AFM (Contact)", "AFM (Non-Contact)"])
        self.scanning_mode_dropdown.setCurrentIndex(0)  # Default to STM

        layout.addWidget(QLabel("Select Scanning Mode:"))
        layout.addWidget(self.scanning_mode_dropdown)

        group.setLayout(layout)
        return group

    def save_configuration(self):
        """
        Save the current control configuration to a file.
        """
        try:
            config = {
                "mode": "Simulated" if self.simulated_mode.isChecked() else "Hardware",
                "scanner_size": "Large" if self.large_scanner.isChecked() else "Small",
                "scanning_mode": self.scanning_mode_dropdown.currentText(),
            }
            with open("control_config.json", "w") as file:
                json.dump(config, file, indent=4)
            logger.info("Configuration saved successfully.")
            QMessageBox.information(self, "Success", "Configuration saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {e}")

    def load_configuration(self):
        """
        Load a control configuration from a file.
        """
        try:
            with open("control_config.json", "r") as file:
                config = json.load(file)
            self.simulated_mode.setChecked(config["mode"] == "Simulated")
            self.hardware_mode.setChecked(config["mode"] == "Hardware")
            self.large_scanner.setChecked(config["scanner_size"] == "Large")
            self.small_scanner.setChecked(config["scanner_size"] == "Small")
            self.scanning_mode_dropdown.setCurrentText(config["scanning_mode"])
            logger.info("Configuration loaded successfully.")
            QMessageBox.information(self, "Success", "Configuration loaded successfully.")
        except FileNotFoundError:
            logger.warning("Configuration file not found.")
            QMessageBox.warning(self, "Warning", "Configuration file not found.")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load configuration: {e}")