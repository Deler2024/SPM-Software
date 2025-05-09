# File: gui/tabs/z_scanner_tab.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
from utils.logger import get_logger
from control.motion_controller import MotionController

# Initialize logger
logger = get_logger(__name__)

class ZScannerTab(QWidget):
    """
    Tab for configuring and controlling the Z-scanner.
    """

    def __init__(self, motion_controller: MotionController, parent=None):
        """
        Initialize the ZScannerTab.
        :param motion_controller: Instance of MotionController for Z-scanner control.
        """
        super().__init__(parent)
        self.motion_controller = motion_controller

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add Z-Scanner Configuration
        self.z_scanner_group = self.create_z_scanner_group()
        self.layout.addWidget(self.z_scanner_group)

        # Add Tip Approach Visualization
        self.tip_visualization = self.create_tip_visualization()
        self.layout.addWidget(self.tip_visualization)

        # Timer for real-time tip visualization updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tip_visualization)

    def create_z_scanner_group(self) -> QGroupBox:
        """
        Create the Z-scanner configuration group.
        :return: QGroupBox containing Z-scanner parameters.
        """
        group = QGroupBox("Z-Scanner Configuration")
        layout = QFormLayout()

        # Z-range (min and max)
        self.z_min_input = QLineEdit()
        self.z_min_input.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow values between 0.0 and 100.0
        self.z_min_input.setPlaceholderText("Enter Z-min (e.g., 0.0)")
        layout.addRow("Z-Min (nm):", self.z_min_input)

        self.z_max_input = QLineEdit()
        self.z_max_input.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow values between 0.0 and 100.0
        self.z_max_input.setPlaceholderText("Enter Z-max (e.g., 30.0)")
        layout.addRow("Z-Max (nm):", self.z_max_input)

        # Feedback settings
        self.feedback_gain_input = QLineEdit()
        self.feedback_gain_input.setValidator(QDoubleValidator(0.0, 10.0, 2))  # Allow values between 0.0 and 10.0
        self.feedback_gain_input.setPlaceholderText("Enter feedback gain (e.g., 1.0)")
        layout.addRow("Feedback Gain:", self.feedback_gain_input)

        self.feedback_setpoint_input = QLineEdit()
        self.feedback_setpoint_input.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow values between 0.0 and 100.0
        self.feedback_setpoint_input.setPlaceholderText("Enter setpoint (e.g., 50.0)")
        layout.addRow("Setpoint (nm):", self.feedback_setpoint_input)

        # Apply button
        self.apply_button = QPushButton("Apply Settings")
        self.apply_button.clicked.connect(self.apply_z_scanner_settings)
        layout.addRow(self.apply_button)

        group.setLayout(layout)
        return group

    def create_tip_visualization(self) -> QGroupBox:
        """
        Create a visualization for the tip approach.
        :return: QGroupBox containing the tip approach visualization.
        """
        group = QGroupBox("Tip Approach Visualization")
        layout = QVBoxLayout(group)

        # Create a PyQtGraph plot
        self.tip_plot = pg.PlotWidget(title="Tip Approach Visualization")
        self.tip_plot.setLabel('left', 'Z Position (nm)')
        self.tip_plot.setLabel('bottom', 'Time (s)')
        self.tip_plot.addLegend()

        # Simulate real-time data
        self.tip_curve = self.tip_plot.plot(pen='g', name="Tip Position")
        layout.addWidget(self.tip_plot)

        # Start/Stop button
        self.start_stop_button = QPushButton("Start Visualization")
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.toggled.connect(self.toggle_tip_visualization)
        layout.addWidget(self.start_stop_button)

        return group

    def apply_z_scanner_settings(self):
        """
        Apply the Z-scanner settings based on user input.
        """
        try:
            z_min = float(self.z_min_input.text())
            z_max = float(self.z_max_input.text())
            feedback_gain = float(self.feedback_gain_input.text())
            setpoint = float(self.feedback_setpoint_input.text())

            # Apply settings to the motion controller
            logger.info(f"Applying Z-scanner settings: Z-Min={z_min}, Z-Max={z_max}, Gain={feedback_gain}, Setpoint={setpoint}")
            # Here you would call methods on the motion_controller to apply these settings
            # For example:
            # self.motion_controller.set_z_range(z_min, z_max)
            # self.motion_controller.set_feedback_gain(feedback_gain)
            # self.motion_controller.set_setpoint(setpoint)

            logger.info("Z-scanner settings applied successfully.")
        except ValueError as e:
            logger.error(f"Invalid input for Z-scanner settings: {e}")

    def toggle_tip_visualization(self, checked):
        """
        Start or stop the tip approach visualization.
        :param checked: True to start, False to stop.
        """
        if checked:
            self.start_stop_button.setText("Stop Visualization")
            self.timer.start(100)  # Update every 100 ms
        else:
            self.start_stop_button.setText("Start Visualization")
            self.timer.stop()

    def update_tip_visualization(self):
        """
        Update the tip approach visualization with new data.
        """
        # Simulate new data (replace with real data if available)
        import random
        new_z_position = random.uniform(0, 30)  # Simulated Z-position
        current_time = self.tip_curve.xData[-1] + 0.1 if self.tip_curve.xData else 0

        # Update the plot
        self.tip_curve.setData(
            x=self.tip_curve.xData + [current_time] if self.tip_curve.xData else [0],
            y=self.tip_curve.yData + [new_z_position] if self.tip_curve.yData else [new_z_position]
        )