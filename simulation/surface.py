#  File: simulation/surface.py

import numpy as np
from utils.logger import get_logger

class Surface:
    """
    Models atomic surface topography for SPM simulations.
    Includes methods to generate synthetic surfaces, retrieve height data, and reset the surface.
    """

    def __init__(self):
        """
        Initialize the Surface class.
        """
        self.surface_data = None  # Placeholder for surface height data
        self.logger = get_logger(__name__)  # Logger for debugging

    def generate_sine_wave_surface(self, amplitude: float, frequency: float, size: int) -> None:
        """
        Generate a sine wave surface topography.
        :param amplitude: Amplitude of the sine wave.
        :param frequency: Frequency of the sine wave.
        :param size: Size of the surface (size x size).
        """
        self.logger.info(f"Generating sine wave surface with amplitude={amplitude}, frequency={frequency}, size={size}")
        try:
            if amplitude <= 0:
                raise ValueError("Amplitude must be positive.")
            if frequency <= 0:
                raise ValueError("Frequency must be positive.")
            if size <= 0:
                raise ValueError("Size must be a positive integer.")

            x = np.linspace(0, 2 * np.pi * frequency, size)
            y = np.linspace(0, 2 * np.pi * frequency, size)
            X, Y = np.meshgrid(x, y)
            self.surface_data = amplitude * np.sin(X) * np.sin(Y)
            self.logger.debug("Sine wave surface generated successfully.")
        except Exception as e:
            self.logger.error(f"Error generating sine wave surface: {e}")
            raise

    def generate_random_rough_surface(self, size: int, roughness: float) -> None:
        """
        Generate a random rough surface topography.
        :param size: Size of the surface (size x size).
        :param roughness: Standard deviation of the surface height variations.
        """
        self.logger.info(f"Generating random rough surface with size={size}, roughness={roughness}")
        try:
            if size <= 0:
                raise ValueError("Size must be a positive integer.")
            if roughness <= 0:
                raise ValueError("Roughness must be positive.")

            self.surface_data = np.random.normal(scale=roughness, size=(size, size))
            self.logger.debug("Random rough surface generated successfully.")
        except Exception as e:
            self.logger.error(f"Error generating random rough surface: {e}")
            raise

    def get_height_data(self) -> np.ndarray:
        """
        Retrieve the height data of the surface.
        :return: 2D NumPy array representing the surface height data.
        """
        self.logger.debug("Retrieving surface height data.")
        if self.surface_data is None:
            self.logger.warning("Surface data is not available. Returning None.")
        return self.surface_data

    def reset_surface(self) -> None:
        """
        Reset the surface data.
        """
        self.logger.info("Resetting surface data.")
        self.surface_data = None
        self.logger.info("Surface data reset successfully.")