# File: gui/panels/xy_scanner_panel.py

from PyQt5.QtWidgets import (
    QGroupBox, QVBoxLayout, QComboBox, QLabel, QFrame, QDialog, QHBoxLayout
)
from gui.widgets.live_data_window import LiveDataWindow
from utils.logger import get_logger
import numpy as np

# Initialize logger
logger = get_logger(__name__)

class XYScannerPanel(QGroupBox):
    """
    Panel for managing XY scanner visualization.
    """

    def __init__(self, parent=None):
        """
        Initialize the XY Scanner Panel.
        """
        super().__init__("XY Scanner Panel", parent)
        self.layout = QVBoxLayout(self)

        # Add a dropdown for selecting Line Mode or Graph Mode
        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems(["Line Mode", "Graph Mode"])
        self.mode_dropdown.currentIndexChanged.connect(self.update_mode)
        self.layout.addWidget(self.mode_dropdown)

        # Add a label for displaying the selected mode
        self.mode_label = QLabel("Selected Mode: Line Mode")
        self.layout.addWidget(self.mode_label)

        # Add a live data window
        self.live_data_window = LiveDataWindow()
        self.layout.addWidget(self.live_data_window)

        # Initialize a list to store window frames
        self.windows = []

    def update_mode(self, index):
        """
        Update the visualization mode based on the dropdown selection.
        :param index: Index of the selected mode.
        """
        mode = self.mode_dropdown.itemText(index)
        self.mode_label.setText(f"Selected Mode: {mode}")
        logger.info(f"Updated XY Scanner mode to {mode}")

        # Update the live data window based on the selected mode
        try:
            if mode == "Line Mode":
                # Simulate line mode visualization
                self.live_data_window.update_data(self.generate_line_data())
            elif mode == "Graph Mode":
                # Simulate graph mode visualization
                self.live_data_window.update_data(self.generate_graph_data())
        except Exception as e:
            logger.error(f"Error updating mode to {mode}: {e}")

    def generate_line_data(self):
        """
        Generate simulated line data for Line Mode.
        :return: 1D numpy array representing the line data.
        """
        try:
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            return y
        except Exception as e:
            logger.error(f"Error generating line data: {e}")
            return np.array([])

    def generate_graph_data(self):
        """
        Generate simulated graph data for Graph Mode.
        :return: 2D numpy array representing the graph data.
        """
        try:
            x = np.linspace(-5, 5, 100)
            y = np.linspace(-5, 5, 100)
            x, y = np.meshgrid(x, y)
            z = np.sin(np.sqrt(x**2 + y**2))
            return z
        except Exception as e:
            logger.error(f"Error generating graph data: {e}")
            return np.array([[]])

    def create_window_frame(self, index):
        """
        Create a confined square frame for an XY scanner window.
        :param index: Index of the window.
        :return: QFrame containing the dropdowns and live data window.
        """
        try:
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setFrameShadow(QFrame.Raised)
            frame.setStyleSheet("border: 1px solid gray; padding: 5px;")

            layout = QVBoxLayout(frame)

            # Create a dropdown for Forward/Backward scan
            dropdown = QComboBox()
            dropdown.addItems(["Forward Scan", "Backward Scan"])
            layout.addWidget(dropdown)

            # Create a live data window
            live_data_window = LiveDataWindow()
            live_data_window.mousePressEvent = lambda event, win=index: self.enlarge_window(win)
            layout.addWidget(live_data_window)

            self.windows.append((frame, live_data_window))
            return frame
        except Exception as e:
            logger.error(f"Error creating window frame: {e}")
            return None

    def enlarge_window(self, index):
        """
        Enlarge the selected window in a separate dialog.
        :param index: Index of the window to enlarge.
        """
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Window {index + 1}")
            dialog.setLayout(QVBoxLayout())
            dialog.layout().addWidget(self.windows[index][1])  # Add the live data window
            dialog.setGeometry(100, 100, 800, 600)  # Set the size of the dialog
            dialog.exec_()
        except Exception as e:
            logger.error(f"Error enlarging window {index}: {e}")