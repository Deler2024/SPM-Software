# File: gui/panels/control_panel.py

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import QTimer
from utils.logger import get_logger
from simulation.simulation_backend import SimulationBackend

# Initialize logger
logger = get_logger(__name__)

class ControlPanel(QGroupBox):
    """
    Control panel for managing the auto-approach and scanning process.
    """

    def __init__(self, surface_info_panel, parent=None):
        """
        Initialize the Control Panel.
        :param surface_info_panel: Reference to the SurfaceInfoPanel for updating parameters.
        """
        super().__init__("Control Panel", parent)
        self.layout = QVBoxLayout(self)

        # Reference to the SurfaceInfoPanel
        self.surface_info_panel = surface_info_panel

        # Initialize the SimulationBackend
        self.simulation_backend = SimulationBackend()

        # Add a label for status
        self.status_label = QLabel("Status: Idle")
        self.layout.addWidget(self.status_label)

        # Add a progress bar for auto-approach
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # Add a button to start auto-approach
        self.auto_approach_button = QPushButton("Start Auto-Approach")
        self.auto_approach_button.clicked.connect(self.start_auto_approach)
        self.layout.addWidget(self.auto_approach_button)

        # Add a button to start scanning
        self.start_scan_button = QPushButton("Start Scan")
        self.start_scan_button.setEnabled(False)  # Disabled until auto-approach is complete
        self.start_scan_button.clicked.connect(self.start_scan)
        self.layout.addWidget(self.start_scan_button)

        # Timer for simulating auto-approach
        self.auto_approach_timer = QTimer(self)
        self.auto_approach_timer.timeout.connect(self.update_auto_approach)

        # Timer for simulating scanning
        self.scan_timer = QTimer(self)
        self.scan_timer.timeout.connect(self.update_scan)

        # Internal state
        self.auto_approach_progress = 0
        self.scanning = False

    def start_auto_approach(self):
        """
        Start the auto-approach process.
        """
        try:
            logger.info("Starting auto-approach...")
            self.status_label.setText("Status: Auto-Approach in Progress")
            self.auto_approach_progress = 0
            self.progress_bar.setValue(0)
            self.auto_approach_button.setEnabled(False)
            self.auto_approach_timer.start(100)  # Update every 100 ms
        except Exception as e:
            logger.error(f"Error starting auto-approach: {e}")

    def update_auto_approach(self):
        """
        Update the auto-approach progress.
        """
        try:
            self.auto_approach_progress += 5
            self.progress_bar.setValue(self.auto_approach_progress)

            # Simulate Z-parameters during approach
            z_height = 100 - self.auto_approach_progress  # Simulated height
            feedback_signal = self.auto_approach_progress / 100  # Simulated feedback signal
            logger.info(f"Auto-Approach: Z-Height={z_height}, Feedback Signal={feedback_signal}")

            # Stop the timer when approach is complete
            if self.auto_approach_progress >= 100:
                self.auto_approach_timer.stop()
                self.status_label.setText("Status: Auto-Approach Complete")
                self.auto_approach_button.setEnabled(True)
                self.start_scan_button.setEnabled(True)
        except Exception as e:
            logger.error(f"Error updating auto-approach: {e}")

    def start_scan(self):
        """
        Start the scanning process.
        """
        try:
            logger.info("Starting scan...")
            self.status_label.setText("Status: Scanning in Progress")
            self.scanning = True
            self.scan_timer.start(500)  # Update every 500 ms
        except Exception as e:
            logger.error(f"Error starting scan: {e}")

    def update_scan(self):
        """
        Update the scanning process.
        """
        try:
            # Simulate surface data
            surface_data = self.simulation_backend.generate_topography_data()

            # Update the Surface Information Panel
            self.surface_info_panel.update_surface_parameters_with_data(surface_data)

            # Log the scanning process
            logger.info("Scanning: Updated surface information.")
        except Exception as e:
            logger.error(f"Error updating scan: {e}")