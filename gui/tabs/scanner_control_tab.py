#  File: gui/tabs/scanner_control_tab.py


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QFormLayout, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from utils.logger import get_logger
import json

# Initialize logger
logger = get_logger(__name__)

class ScannerControlTab(QWidget):
    """
    Tab for configuring and controlling the XY and Z scanners with mode and size options.
    """

    def __init__(self, parent=None):
        """
        Initialize the ScannerControlTab.
        """
        super().__init__(parent)
        logger.info("Initializing ScannerControlTab...")

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add Mode Selector
        self.mode_group = self.create_mode_selector()
        self.layout.addWidget(self.mode_group)

        # Add Scanner Size Selector
        self.size_group = self.create_size_selector()
        self.layout.addWidget(self.size_group)

        # Add XY Scanner Configuration
        self.xy_scanner_group = self.create_xy_scanner_group()
        self.layout.addWidget(self.xy_scanner_group)

        # Add Z Scanner Configuration
        self.z_scanner_group = self.create_z_scanner_group()
        self.layout.addWidget(self.z_scanner_group)

        # Add Save and Load Configuration Buttons
        self.save_load_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_configuration)
        self.save_load_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Configuration")
        self.load_button.clicked.connect(self.load_configuration)
        self.save_load_layout.addWidget(self.load_button)

        self.layout.addLayout(self.save_load_layout)

        logger.info("ScannerControlTab initialized successfully.")

    def create_mode_selector(self) -> QGroupBox:
        """
        Create the mode selector for Simulated and Hardware modes.
        :return: QGroupBox containing the mode selector.
        """
        group = QGroupBox("Mode Selector")
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
        group = QGroupBox("Scanner Size Selector")
        layout = QHBoxLayout()

        self.large_scanner = QRadioButton("Large (X=100cm, Y=100cm, Z=30cm)")
        self.large_scanner.setChecked(True)  # Default to Large scanner
        self.small_scanner = QRadioButton("Small (X=5cm, Y=5cm, Z=1cm)")

        self.size_button_group = QButtonGroup()
        self.size_button_group.addButton(self.large_scanner)
        self.size_button_group.addButton(self.small_scanner)

        self.large_scanner.toggled.connect(self.update_scanner_size)

        layout.addWidget(self.large_scanner)
        layout.addWidget(self.small_scanner)

        group.setLayout(layout)
        return group

    def create_xy_scanner_group(self) -> QGroupBox:
        """
        Create the XY scanner configuration group.
        :return: QGroupBox containing XY scanner parameters.
        """
        group = QGroupBox("XY Scanner Configuration")
        layout = QFormLayout()

        # Scan Range
        self.xy_width_input = QLineEdit()
        self.xy_width_input.setValidator(QDoubleValidator(0.1, 100.0, 2))
        self.xy_width_input.setPlaceholderText("Width (cm)")
        layout.addRow("Scan Width:", self.xy_width_input)

        self.xy_height_input = QLineEdit()
        self.xy_height_input.setValidator(QDoubleValidator(0.1, 100.0, 2))
        self.xy_height_input.setPlaceholderText("Height (cm)")
        layout.addRow("Scan Height:", self.xy_height_input)

        # Scan Resolution
        self.xy_resolution_x_input = QLineEdit()
        self.xy_resolution_x_input.setValidator(QIntValidator(1, 1000))
        self.xy_resolution_x_input.setPlaceholderText("Points in X")
        layout.addRow("Resolution (X):", self.xy_resolution_x_input)

        self.xy_resolution_y_input = QLineEdit()
        self.xy_resolution_y_input.setValidator(QIntValidator(1, 1000))
        self.xy_resolution_y_input.setPlaceholderText("Points in Y")
        layout.addRow("Resolution (Y):", self.xy_resolution_y_input)

        group.setLayout(layout)
        return group

    def create_z_scanner_group(self) -> QGroupBox:
        """
        Create the Z scanner configuration group.
        :return: QGroupBox containing Z scanner parameters.
        """
        group = QGroupBox("Z Scanner Configuration")
        layout = QFormLayout()

        # Z Range
        self.z_min_input = QLineEdit()
        self.z_min_input.setValidator(QDoubleValidator(0.0, 30.0, 2))
        self.z_min_input.setPlaceholderText("Min Height (cm)")
        layout.addRow("Min Height:", self.z_min_input)

        self.z_max_input = QLineEdit()
        self.z_max_input.setValidator(QDoubleValidator(0.0, 30.0, 2))
        self.z_max_input.setPlaceholderText("Max Height (cm)")
        layout.addRow("Max Height:", self.z_max_input)

        group.setLayout(layout)
        return group

    def update_scanner_size(self):
        """
        Update the scanner parameters based on the selected size.
        """
        if self.large_scanner.isChecked():
            logger.info("Large scanner selected.")
            self.xy_width_input.setText("100.0")
            self.xy_height_input.setText("100.0")
            self.z_min_input.setText("0.0")
            self.z_max_input.setText("30.0")
        elif self.small_scanner.isChecked():
            logger.info("Small scanner selected.")
            self.xy_width_input.setText("5.0")
            self.xy_height_input.setText("5.0")
            self.z_min_input.setText("0.0")
            self.z_max_input.setText("1.0")

    def save_configuration(self):
        """
        Save the current scanner configuration to a file.
        """
        try:
            config = {
                "mode": "Simulated" if self.simulated_mode.isChecked() else "Hardware",
                "scanner_size": "Large" if self.large_scanner.isChecked() else "Small",
                "xy_width": self.xy_width_input.text(),
                "xy_height": self.xy_height_input.text(),
                "xy_resolution_x": self.xy_resolution_x_input.text(),
                "xy_resolution_y": self.xy_resolution_y_input.text(),
                "z_min": self.z_min_input.text(),
                "z_max": self.z_max_input.text(),
            }
            with open("scanner_config.json", "w") as file:
                json.dump(config, file, indent=4)
            logger.info("Configuration saved successfully.")
            QMessageBox.information(self, "Success", "Configuration saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {e}")

    def load_configuration(self):
        """
        Load a scanner configuration from a file.
        """
        try:
            with open("scanner_config.json", "r") as file:
                config = json.load(file)
            self.simulated_mode.setChecked(config["mode"] == "Simulated")
            self.hardware_mode.setChecked(config["mode"] == "Hardware")
            self.large_scanner.setChecked(config["scanner_size"] == "Large")
            self.small_scanner.setChecked(config["scanner_size"] == "Small")
            self.xy_width_input.setText(config["xy_width"])
            self.xy_height_input.setText(str(config.get("xy_height", "0")))
            
            self.xy_resolution_x_input.setText(config["xy_resolution_x"])
            self.xy_resolution_y_input.setText(config["xy_resolution_y"])
            self.z_min_input.setText(config["z_min"])
            self.z_max_input.setText(config["z_max"])
            logger.info("Configuration loaded successfully.")
            QMessageBox.information(self, "Success", "Configuration loaded successfully.")
        except FileNotFoundError:
            logger.warning("Configuration file not found.")
            QMessageBox.warning(self, "Warning", "Configuration file not found.")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load configuration: {e}")