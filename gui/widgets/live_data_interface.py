# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/widgets/live_data_interface.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from gui.panels.z_scanner_panel import ZScannerPanel
from gui.panels.surface_info_panel import SurfaceInfoPanel
from gui.panels.control_panel import ControlPanel
from gui.panels.xy_scanner_panel import XYScannerPanel
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class LiveDataInterface(QWidget):
    """
    Centralized interface for managing and displaying live data windows.
    """

    def __init__(self, parent=None):
        """
        Initialize the Live Data Interface.
        """
        super().__init__(parent)
        self.setWindowTitle("Live Data Interface")
        self.setGeometry(100, 100, 1200, 800)  # Set default size for the interface

        # Main layout for the Live Data Interface
        self.layout = QVBoxLayout(self)

        # Add a title label
        title_label = QLabel("Live Data Interface")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.layout.addWidget(title_label)

        # Add panels
        self._initialize_panels()

        # Timer for real-time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_live_data)

        logger.info("LiveDataInterface initialized successfully.")

    def _initialize_panels(self):
        """
        Initialize and add panels to the interface.
        """
        logger.debug("Initializing panels...")

        # Add Z-Scanner Panel
        self.z_scanner_panel = ZScannerPanel()
        self.layout.addWidget(self.z_scanner_panel)

        # Add Surface Information Panel
        self.surface_info_panel = SurfaceInfoPanel()
        self.layout.addWidget(self.surface_info_panel)

        # Add Control Panel
        self.control_panel = ControlPanel(self.surface_info_panel)
        self.layout.addWidget(self.control_panel)

        # Add XY Scanner Panel
        self.xy_scanner_panel = XYScannerPanel()
        self.layout.addWidget(self.xy_scanner_panel)

        logger.info("Panels added to LiveDataInterface.")

    def start_updates(self):
        """
        Start real-time updates for live data.
        """
        self.timer.start(100)  # Update every 100 ms
        logger.info("Started live data updates.")

    def stop_updates(self):
        """
        Stop real-time updates for live data.
        """
        self.timer.stop()
        logger.info("Stopped live data updates.")

    def update_live_data(self):
        """
        Update live data in real-time.
        """
        # Logic to fetch and update live data
        logger.debug("Updated live data.")

        # Example: Update panels with new data
        self.z_scanner_panel.update_data()
        self.surface_info_panel.update_data()
        self.xy_scanner_panel.update_data()