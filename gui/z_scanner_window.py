# File: gui/z_scanner_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSlider, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from pyqtgraph import PlotWidget, mkPen
from control.motion_controller import MotionController
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class ZScannerWindow(QDialog):
    """
    Window for controlling and monitoring the Z-scanner.
    """

    def __init__(self, motion_controller: MotionController, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Z-Scanner Control and Parameters")
        self.setGeometry(200, 200, 800, 600)

        self.motion_controller = motion_controller

        # Main layout
        layout = QVBoxLayout(self)

        # Add a title label
        title_label = QLabel("Z-Scanner Control and Parameters")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Add a label to display the current Z-position
        self.z_position_label = QLabel("Current Z-Position: 0.0")
        self.z_position_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.z_position_label)

        # Add a slider for Z-axis control
        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setMinimum(0)
        self.z_slider.setMaximum(300)  # Scale to match Z-axis limits (e.g., 0 to 30.0)
        self.z_slider.setValue(0)
        self.z_slider.setToolTip("Adjust the slider to set the target Z-position (0.0 - 30.0)")
        layout.addWidget(self.z_slider)

        # Add a button to move the Z-axis
        self.move_button = QPushButton("Move Z-Axis")
        self.move_button.setToolTip("Click to move the Z-axis to the selected position")
        layout.addWidget(self.move_button)

        # Add a reset button to reset the Z-position
        self.reset_button = QPushButton("Reset Z-Position")
        self.reset_button.setToolTip("Click to reset the Z-position to 0.0")
        layout.addWidget(self.reset_button)

        # Add a real-time graph for Z-position visualization
        self.z_position_graph = PlotWidget(title="Z-Position Over Time")
        self.z_position_graph.setLabel('left', 'Z Position (nm)')
        self.z_position_graph.setLabel('bottom', 'Time (s)')
        self.z_position_graph.addLegend()
        self.z_position_curve = self.z_position_graph.plot(pen=mkPen('b', width=2), name="Z-Position")
        layout.addWidget(self.z_position_graph)

        # Add a table for Z-scanner parameters
        self.parameter_table = QTableWidget(6, 2)  # 6 rows, 2 columns
        self.parameter_table.setHorizontalHeaderLabels(["Parameter", "Value"])
        self.parameter_table.setVerticalHeaderLabels(
            ["Ra (Roughness)", "Rq (RMS Roughness)", "Mean Height", "Rsk (Skewness)", "Rku (Kurtosis)", "Rpv (Peak-to-Valley)"]
        )
        layout.addWidget(self.parameter_table)

        # Populate the table with default values
        self.populate_table()

        # Connect signals
        self.move_button.clicked.connect(self.move_z_axis)
        self.reset_button.clicked.connect(self.reset_z_position)

        # Timer for real-time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_z_position)
        self.timer.start(100)  # Update every 100 ms

        # Internal state for graph
        self.time_data = []
        self.z_position_data = []

    def populate_table(self):
        """
        Populate the table with default Z-scanner parameter values.
        """
        parameters = [
            ("Ra (Roughness)", "N/A"),
            ("Rq (RMS Roughness)", "N/A"),
            ("Mean Height", "N/A"),
            ("Rsk (Skewness)", "N/A"),
            ("Rku (Kurtosis)", "N/A"),
            ("Rpv (Peak-to-Valley)", "N/A"),
        ]

        for row, (param, value) in enumerate(parameters):
            self.parameter_table.setItem(row, 0, QTableWidgetItem(param))
            self.parameter_table.setItem(row, 1, QTableWidgetItem(value))

    def update_parameters(self, data):
        """
        Update the Z-scanner parameters based on the provided data.
        :param data: Dictionary containing parameter names and values.
        """
        for row, (param, value) in enumerate(data.items()):
            self.parameter_table.setItem(row, 1, QTableWidgetItem(str(value)))

    def move_z_axis(self):
        """
        Move the Z-axis to the position specified by the slider.
        """
        target_position = self.z_slider.value() / 10.0  # Scale to 0.0 - 30.0
        try:
            self.motion_controller.move_z(target_position)
            logger.info(f"Moved Z-axis to position: {target_position}")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid Z-position: {e}")
            logger.error(f"Invalid Z-position: {e}")
        except ConnectionError as e:
            QMessageBox.critical(self, "Error", f"Connection error: {e}")
            logger.error(f"Connection error: {e}")

    def reset_z_position(self):
        """
        Reset the Z-position to 0.0.
        """
        try:
            self.motion_controller.move_z(0.0)
            self.z_slider.setValue(0)
            logger.info("Z-position reset to 0.0")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reset Z-position: {e}")
            logger.error(f"Failed to reset Z-position: {e}")

    def update_z_position(self):
        """
        Update the displayed Z-position in real-time and update the graph.
        """
        try:
            current_position = self.motion_controller.get_z_position()
            self.z_position_label.setText(f"Current Z-Position: {current_position:.2f}")

            # Update graph data
            if len(self.time_data) == 0:
                self.time_data.append(0)
            else:
                self.time_data.append(self.time_data[-1] + 0.1)  # Increment time by 0.1s
            self.z_position_data.append(current_position)

            self.z_position_curve.setData(self.time_data, self.z_position_data)
        except Exception as e:
            self.z_position_label.setText("Error: Unable to fetch Z-position")
            logger.error(f"Error updating Z-position: {e}")