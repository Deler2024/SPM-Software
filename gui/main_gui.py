# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/main_gui.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from gui.widgets.configuration_window import ConfigurationWindow
from gui.widgets.z_scanner_window import ZScannerWindow
from gui.widgets.surface_info_panel import SurfaceInfoPanel
from gui.widgets.live_data_interface import LiveDataInterface
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class MainGUI(QWidget):
    """
    Main GUI class for the SPM Control and Acquisition application.
    """

    def __init__(self, parent=None):
        """
        Initialize the Main GUI.
        """
        super().__init__(parent)

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add a control panel with Connect/Disconnect button
        self._initialize_controls()

        # Add a tabbed interface
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Add tabs
        self._initialize_tabs()

        # Program state
        self.is_connected = False

        logger.info("MainGUI initialized successfully.")

    def _initialize_controls(self):
        """
        Initialize the control panel with Connect/Disconnect button.
        """
        control_layout = QHBoxLayout()

        # Connect/Disconnect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.connect_button.clicked.connect(self.toggle_connection)
        control_layout.addWidget(self.connect_button)

        self.layout.addLayout(control_layout)

    def _initialize_tabs(self):
        """
        Initialize and add tabs to the tabbed interface.
        """
        logger.debug("Initializing tabs...")

        # Configuration Tab
        self.configuration_window = ConfigurationWindow()
        self.tabs.addTab(self.configuration_window, "Configuration")

        # Z-Scanner Control Tab
        self.z_scanner_window = ZScannerWindow()
        self.tabs.addTab(self.z_scanner_window, "Z-Scanner Control")

        # Surface Analysis Tab
        self.surface_info_panel = SurfaceInfoPanel()
        self.tabs.addTab(self.surface_info_panel, "Surface Analysis")

        # Live Data Tab
        self.live_data_interface = LiveDataInterface()
        self.tabs.addTab(self.live_data_interface, "Live Data")

        logger.info("Tabs added to the MainGUI.")

    def toggle_connection(self):
        """
        Toggle the connection state between Connect and Disconnect.
        """
        if not self.is_connected:
            # Connect: Start the program
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
            self.start_program()
        else:
            # Disconnect: Stop the program
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            self.stop_program()

    def start_program(self):
        """
        Start the program and initialize all necessary components.
        """
        logger.info("Connecting to the system and starting the program...")
        self.is_connected = True

        # Start real-time updates in tabs
        self.z_scanner_window.start_updates()
        self.live_data_interface.start_updates()

        # Add logic to initialize and start the program
        # For example:
        # - Initialize hardware connections
        # - Start data acquisition

    def stop_program(self):
        """
        Stop the program and disconnect all components.
        """
        logger.info("Disconnecting from the system and stopping the program...")
        self.is_connected = False

        # Stop real-time updates in tabs
        self.z_scanner_window.stop_updates()
        self.live_data_interface.stop_updates()

        # Add logic to stop the program
        # For example:
        # - Stop data acquisition
        # - Disconnect hardware