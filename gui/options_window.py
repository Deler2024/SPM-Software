# File: gui/options_window.py

import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class OptionsWindow(QDialog):
    """
    Options window for configuring measurement methods, scanner size, and hardware settings.
    """

    CONFIG_FILE = "config.json"  # File to save and load configuration
    DEFAULT_CONFIG = {
        "measurement_mode": "STM",
        "scanner_size": "Small",
        "hardware_settings": "Hardware A",
    }

    def __init__(self, parent=None):
        """
        Initialize the Options Window.
        """
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.setGeometry(200, 200, 600, 400)

        # Main layout
        layout = QVBoxLayout(self)

        # Measurement Mode
        layout.addWidget(QLabel("Measurement Mode:"))
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(["STM", "AFM", "Other"])
        layout.addWidget(self.method_dropdown)

        # Scanner Size
        layout.addWidget(QLabel("Scanner Size:"))
        self.scanner_size_dropdown = QComboBox()
        self.scanner_size_dropdown.addItems(["Small", "Large"])
        layout.addWidget(self.scanner_size_dropdown)

        # Hardware Settings
        layout.addWidget(QLabel("Hardware Settings:"))
        self.hardware_dropdown = QComboBox()
        self.hardware_dropdown.addItems(["Hardware A", "Hardware B", "Simulation"])
        layout.addWidget(self.hardware_dropdown)

        # Save Button
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_configuration)
        layout.addWidget(self.save_button)

        # Load Button
        self.load_button = QPushButton("Load Configuration")
        self.load_button.clicked.connect(self.load_configuration)
        layout.addWidget(self.load_button)

        # Reset Button
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_to_default)
        layout.addWidget(self.reset_button)

        # Load configuration on startup
        self.load_configuration()

    def save_configuration(self):
        """
        Save the selected configuration to a file.
        """
        try:
            config = {
                "measurement_mode": self.method_dropdown.currentText(),
                "scanner_size": self.scanner_size_dropdown.currentText(),
                "hardware_settings": self.hardware_dropdown.currentText(),
            }
            with open(self.CONFIG_FILE, "w") as file:
                json.dump(config, file)
            QMessageBox.information(self, "Save Configuration", "Configuration saved successfully!")
            logger.info("Configuration saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Save Configuration", f"Failed to save configuration: {e}")
            logger.error(f"Failed to save configuration: {e}")

    def load_configuration(self):
        """
        Load the configuration from a file.
        """
        try:
            with open(self.CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.method_dropdown.setCurrentText(config.get("measurement_mode", self.DEFAULT_CONFIG["measurement_mode"]))
                self.scanner_size_dropdown.setCurrentText(config.get("scanner_size", self.DEFAULT_CONFIG["scanner_size"]))
                self.hardware_dropdown.setCurrentText(config.get("hardware_settings", self.DEFAULT_CONFIG["hardware_settings"]))
                QMessageBox.information(self, "Load Configuration", "Configuration loaded successfully!")
                logger.info("Configuration loaded successfully.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Load Configuration", "No configuration file found. Using defaults.")
            logger.warning("No configuration file found. Using defaults.")
            self.reset_to_default()
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Load Configuration", f"Invalid configuration file format: {e}")
            logger.error(f"Invalid configuration file format: {e}")
            self.reset_to_default()
        except Exception as e:
            QMessageBox.critical(self, "Load Configuration", f"Failed to load configuration: {e}")
            logger.error(f"Failed to load configuration: {e}")
            self.reset_to_default()

    def reset_to_default(self):
        """
        Reset the configuration to default values.
        """
        self.method_dropdown.setCurrentText(self.DEFAULT_CONFIG["measurement_mode"])
        self.scanner_size_dropdown.setCurrentText(self.DEFAULT_CONFIG["scanner_size"])
        self.hardware_dropdown.setCurrentText(self.DEFAULT_CONFIG["hardware_settings"])
        QMessageBox.information(self, "Reset to Default", "Configuration reset to default values.")
        logger.info("Configuration reset to default values.")