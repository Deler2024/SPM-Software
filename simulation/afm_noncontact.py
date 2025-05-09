# File: simulation/afm_noncontact.py
import numpy as np
from utils.logger import get_logger

class AFMNonContactSimulation:
    """
    Models non-contact AFM behavior. Generates synthetic frequency shift data.
    """

    def __init__(self):
        """
        Initialize the AFMNonContactSimulation class.
        """
        self.parameters = {}  # Dictionary to store simulation parameters
        self.simulation_data = None  # Placeholder for simulation results
        self.logger = get_logger(__name__)  # Logger for debugging

    def configure_parameters(self, parameters: dict) -> None:
        """
        Configure simulation parameters such as tip-sample distance, oscillation amplitude, etc.
        :param parameters: Dictionary of simulation parameters.
        """
        self.parameters = parameters
        self.logger.debug(f"Simulation parameters configured: {self.parameters}")

    def run_simulation(self) -> None:
        """
        Run the non-contact AFM simulation.
        """
        self.logger.info("Running non-contact AFM simulation.")
        self.simulation_data = self.generate_synthetic_data()
        self.logger.info("Non-contact AFM simulation completed.")

    def generate_synthetic_data(self) -> np.ndarray:
        """
        Generate synthetic frequency shift data based on the configured parameters.
        :return: A NumPy array containing the synthetic frequency shift data.
        """
        self.logger.debug("Generating synthetic frequency shift data.")
        try:
            # Example: Simple harmonic oscillator model
            tip_sample_distance = self.parameters.get("tip_sample_distance", 1.0)
            oscillation_amplitude = self.parameters.get("oscillation_amplitude", 0.1)

            if tip_sample_distance <= 0:
                raise ValueError("Tip-sample distance must be positive.")

            frequency_shift = (
                np.sin(np.linspace(0, 2 * np.pi, 100)) * oscillation_amplitude / tip_sample_distance
            )
            self.logger.debug(f"Synthetic frequency shift data generated: {frequency_shift}")
            return frequency_shift
        except Exception as e:
            self.logger.error(f"Error generating synthetic frequency shift data: {e}")
            raise

    def reset_simulation(self) -> None:
        """
        Reset the simulation state.
        """
        self.logger.info("Resetting non-contact AFM simulation.")
        self.parameters = {}
        self.simulation_data = None
        self.logger.info("Non-contact AFM simulation reset.")