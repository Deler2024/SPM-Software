from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from gui.tabs.control_tab import ControlTab
from gui.tabs.xy_scanner_tab import XYScannerTab
from gui.tabs.z_scanner_tab import ZScannerTab
import pyqtgraph as pg
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class MainTabbedInterface(QWidget):
    """
    Main tabbed interface for the application.
    """

    def __init__(self, parent=None):
        """
        Initialize the MainTabbedInterface.
        """
        super().__init__(parent)
        logger.info("Initializing MainTabbedInterface...")
        try:
            self.layout = QVBoxLayout(self)
            self.tab_widget = QTabWidget()

            # Add tabs
            self.control_tab = ControlTab()
            self.xy_scanner_tab = XYScannerTab()
            self.z_scanner_tab = ZScannerTab()

            self.tab_widget.addTab(self.control_tab, "Control")
            self.tab_widget.addTab(self.xy_scanner_tab, "XY Scanner")
            self.tab_widget.addTab(self.z_scanner_tab, "Z Scanner")

            self.layout.addWidget(self.tab_widget)
            logger.info("MainTabbedInterface initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize MainTabbedInterface: {e}")
            raise