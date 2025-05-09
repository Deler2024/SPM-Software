# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/widgets/z_scanner_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from control.motion_controller import MotionController
from utils.logger import get_logger


# Initialize logger
logger = get_logger(__name__)

class ZScannerWindow(QDialog):
    """
    Window for controlling and monitoring the Z-scanner.
    """

    def __init__(self, motion_controller: MotionController = None, parent=None):
        """
        Initialize the Z-Scanner Window.
        :param motion_controller: Instance of the MotionController for Z-axis control.
        """
        super().__init__(parent)
        self.setWindowTitle("Z-Scanner Control and Parameters")
        self.setGeometry(200, 200, 800, 600)

        self.motion_controller = motion_controller or MotionController()

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add a title label
        title_label = QLabel("Z-Scanner Control and Parameters")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Add a label to display the current Z-position
        self.z_position_label = QLabel("Current Z-Position: 0.0")
        self.z_position_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.z_position_label)

        # Add a slider for Z-axis control
        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setMinimum(0)
        self.z_slider.setMaximum(300)  # Scale to match Z-axis limits (e.g., 0 to 30.0)
        self.z_slider.setValue(0)
        self.layout.addWidget(self.z_slider)

        # Add a button to move the Z-axis
        self.move_button = QPushButton("Move Z-Axis")
        self.move_button.clicked.connect(self.move_z_axis)
        self.layout.addWidget(self.move_button)

        # Add a table for Z-scanner parameters
        self.parameter_table = QTableWidget(6, 2)  # 6 rows, 2 columns
        self.parameter_table.setHorizontalHeaderLabels(["Parameter", "Value"])
        self.parameter_table.setVerticalHeaderLabels(
            ["Ra (Roughness)", "Rq (RMS Roughness)", "Mean Height", "Rsk (Skewness)", "Rku (Kurtosis)", "Rpv (Peak-to-Valley)"]
        )
        self.layout.addWidget(self.parameter_table)

        # Populate the table with default values
        self.populate_table()

        # Timer for real-time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_z_position)
        self.timer.start(100)  # Update every 100 ms

        logger.info("ZScannerWindow initialized successfully.")

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

    def update_z_position(self):
        """
        Update the displayed Z-position in real-time.
        """
        try:
            current_position = self.motion_controller.get_z_position()
            self.z_position_label.setText(f"Current Z-Position: {current_position:.2f}")
            logger.debug(f"Updated Z-position: {current_position}")
        except Exception as e:
            self.z_position_label.setText("Error: Unable to fetch Z-position")
            logger.error(f"Error fetching Z-position: {e}")
            
            
# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/widgets/z_scanner_window.py

from PyQt5.QtCore import QTimer

class ZScannerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_z_position)

    def start_updates(self):
        """
        Start real-time updates for the Z-scanner.
        """
        self.timer.start(100)  # Update every 100 ms
        logger.info("Started Z-scanner updates.")

    def stop_updates(self):
        """
        Stop real-time updates for the Z-scanner.
        """
        self.timer.stop()
        logger.info("Stopped Z-scanner updates.")

    def update_z_position(self):
        """
        Update the Z-scanner position in real-time.
        """
        # Logic to fetch and update Z-position
        logger.debug("Updated Z-position.")