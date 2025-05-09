# File: gui/panels/surface_info_panel.py

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel
import numpy as np
from utils.logger import get_logger
from simulation.simulation_backend import SimulationBackend

# Initialize logger
logger = get_logger(__name__)

class SurfaceInfoPanel(QGroupBox):
    """
    Panel for displaying Z-Scanner surface information parameters.
    """

    def __init__(self, parent=None):
        """
        Initialize the Surface Information Panel.
        """
        super().__init__("Surface Information", parent)
        self.layout = QVBoxLayout(self)

        # Initialize the SimulationBackend
        self.simulation_backend = SimulationBackend()

        # Add labels for surface parameters
        self.ra_label = QLabel("Ra (Arithmetic Mean Roughness): N/A")
        self.rq_label = QLabel("Rq (Root Mean Square Roughness): N/A")
        self.mean_label = QLabel("Mean Height: N/A")
        self.polyfit_label = QLabel("1st Order Polynomial Fit: N/A")
        self.rsk_label = QLabel("Rsk (Skewness): N/A")
        self.rku_label = QLabel("Rku (Kurtosis): N/A")
        self.rpv_label = QLabel("Rpv (Peak-to-Valley): N/A")

        # Add labels to the layout
        self.layout.addWidget(self.ra_label)
        self.layout.addWidget(self.rq_label)
        self.layout.addWidget(self.mean_label)
        self.layout.addWidget(self.polyfit_label)
        self.layout.addWidget(self.rsk_label)
        self.layout.addWidget(self.rku_label)
        self.layout.addWidget(self.rpv_label)

        # Update surface parameters with test data
        self.update_surface_parameters()

    def update_surface_parameters(self):
        """
        Update the surface information parameters based on simulated data.
        """
        try:
            # Get simulated data
            data = self.simulation_backend.generate_topography_data()

            # Calculate surface parameters
            parameters = self.calculate_surface_parameters(data)

            # Update labels
            self.ra_label.setText(f"Ra (Arithmetic Mean Roughness): {parameters['ra']:.2f}")
            self.rq_label.setText(f"Rq (Root Mean Square Roughness): {parameters['rq']:.2f}")
            self.mean_label.setText(f"Mean Height: {parameters['mean_height']:.2f}")
            self.polyfit_label.setText(f"1st Order Polynomial Fit: {parameters['polyfit']}")
            self.rsk_label.setText(f"Rsk (Skewness): {parameters['rsk']:.2f}")
            self.rku_label.setText(f"Rku (Kurtosis): {parameters['rku']:.2f}")
            self.rpv_label.setText(f"Rpv (Peak-to-Valley): {parameters['rpv']:.2f}")

            # Log the calculated parameters
            logger.debug(f"Surface Parameters: {parameters}")
        except Exception as e:
            logger.error(f"Error updating surface parameters: {e}")

    def calculate_surface_parameters(self, data):
        """
        Calculate surface parameters based on the provided data.
        :param data: 2D numpy array representing the topography data.
        :return: Dictionary containing calculated surface parameters.
        """
        try:
            # Flatten the data for calculations
            z = data.flatten()

            # Calculate Ra (Arithmetic Mean Roughness)
            mean_z = np.mean(z)
            ra = np.mean(np.abs(z - mean_z))

            # Calculate Rq (Root Mean Square Roughness)
            rq = np.sqrt(np.mean((z - mean_z) ** 2))

            # Calculate Mean Height
            mean_height = mean_z

            # Calculate 1st Order Polynomial Fit
            x = np.arange(data.shape[1])
            y = np.arange(data.shape[0])
            x, y = np.meshgrid(x, y)
            coeffs = np.polyfit(x.flatten(), z, 1)  # Linear fit
            polyfit = f"z = {coeffs[0]:.2f}x + {coeffs[1]:.2f}"

            # Calculate Skewness (Rsk)
            rsk = np.mean((z - mean_z) ** 3) / (rq ** 3)

            # Calculate Kurtosis (Rku)
            rku = np.mean((z - mean_z) ** 4) / (rq ** 4)

            # Calculate Peak-to-Valley Height (Rpv)
            rpv = np.max(z) - np.min(z)

            # Return all parameters as a dictionary
            return {
                "ra": ra,
                "rq": rq,
                "mean_height": mean_height,
                "polyfit": polyfit,
                "rsk": rsk,
                "rku": rku,
                "rpv": rpv,
            }
        except Exception as e:
            logger.error(f"Error calculating surface parameters: {e}")
            return {
                "ra": 0.0,
                "rq": 0.0,
                "mean_height": 0.0,
                "polyfit": "N/A",
                "rsk": 0.0,
                "rku": 0.0,
                "rpv": 0.0,
            }