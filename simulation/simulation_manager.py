#  File: simulation/simulation_manager.py

from simulation.stm import STMSimulation
from simulation.afm_contact import AFMContactSimulation
from simulation.afm_noncontact import AFMNonContactSimulation
from utils.logger import get_logger

class SimulationManager:
    """
    Coordinates different simulation modes (STM, AFM contact, AFM non-contact).
    Supports Simulated and Hardware modes, as well as Large and Small scanner configurations.
    """

    def __init__(self):
        """
        Initialize the SimulationManager.
        """
        self.simulation_mode = None  # Current simulation mode
        self.simulation_instance = None  # Instance of the selected simulation
        self.scanner_size = "Large"  # Default scanner size ("Large" or "Small")
        self.operation_mode = "Simulated"  # Default operation mode ("Simulated" or "Hardware")
        self.logger = get_logger(__name__)  # Logger for debugging

    def set_operation_mode(self, mode: str) -> None:
        """
        Set the operation mode (Simulated or Hardware).
        :param mode: The operation mode to set ("Simulated" or "Hardware").
        """
        if mode not in ["Simulated", "Hardware"]:
            self.logger.error(f"Invalid operation mode selected: {mode}")
            raise ValueError(f"Invalid operation mode: {mode}")
        self.operation_mode = mode
        self.logger.info(f"Operation mode set to: {self.operation_mode}")

    def set_scanner_size(self, size: str) -> None:
        """
        Set the scanner size (Large or Small).
        :param size: The scanner size to set ("Large" or "Small").
        """
        if size not in ["Large", "Small"]:
            self.logger.error(f"Invalid scanner size selected: {size}")
            raise ValueError(f"Invalid scanner size: {size}")
        self.scanner_size = size
        self.logger.info(f"Scanner size set to: {self.scanner_size}")

    def select_simulation_mode(self, mode: str) -> None:
        """
        Select the simulation mode and initialize the corresponding simulation instance.
        :param mode: The simulation mode to select ("STM", "AFM_contact", "AFM_noncontact").
        """
        self.logger.debug(f"Selecting simulation mode: {mode}")
        if mode == "STM":
            self.simulation_instance = STMSimulation()
        elif mode == "AFM_contact":
            self.simulation_instance = AFMContactSimulation()
        elif mode == "AFM_noncontact":
            self.simulation_instance = AFMNonContactSimulation()
        else:
            self.logger.error(f"Invalid simulation mode selected: {mode}")
            raise ValueError(f"Invalid simulation mode: {mode}")
        self.simulation_mode = mode
        self.logger.info(f"Simulation mode selected: {self.simulation_mode}")

    def configure_simulation_parameters(self, parameters: dict) -> None:
        """
        Configure the parameters for the selected simulation mode.
        Automatically adjusts parameters based on the scanner size.
        :param parameters: Dictionary of parameters to configure the simulation.
        """
        if not self.simulation_instance:
            self.logger.error("Simulation mode not selected. Cannot configure simulation.")
            raise RuntimeError("Simulation mode not selected. Cannot configure simulation.")

        # Adjust parameters based on scanner size
        if self.scanner_size == "Large":
            parameters["x_range"] = 100.0
            parameters["y_range"] = 100.0
            parameters["z_range"] = 30.0
        elif self.scanner_size == "Small":
            parameters["x_range"] = 5.0
            parameters["y_range"] = 5.0
            parameters["z_range"] = 1.0

        # Validate parameters
        if not self._validate_parameters(parameters):
            self.logger.error(f"Invalid parameters: {parameters}")
            raise ValueError(f"Invalid parameters: {parameters}")

        self.logger.debug(f"Configuring simulation with parameters: {parameters}")
        self.simulation_instance.configure_parameters(parameters)

    def run_simulation(self) -> None:
        """
        Run the selected simulation.
        """
        if not self.simulation_instance:
            self.logger.error("Simulation mode not selected. Cannot run simulation.")
            raise RuntimeError("Simulation mode not selected. Cannot run simulation.")

        if self.operation_mode == "Hardware":
            self.logger.info("Running in Hardware mode. Delegating to hardware controller.")
            # Hardware mode logic would go here (e.g., interfacing with hardware controllers)
            raise NotImplementedError("Hardware mode is not yet implemented.")
        else:
            self.logger.info("Running simulation in Simulated mode.")
            self.simulation_instance.run_simulation()
            self.logger.info("Simulation completed.")

    def retrieve_simulated_data(self) -> dict:
        """
        Retrieve the simulated data from the selected simulation.
        :return: The simulated data as a dictionary or array.
        """
        if not self.simulation_instance:
            self.logger.error("Simulation mode not selected. Cannot retrieve simulated data.")
            raise RuntimeError("Simulation mode not selected. Cannot retrieve simulated data.")

        self.logger.debug("Retrieving simulated data.")
        return self.simulation_instance.generate_synthetic_data()

    def reset_simulation(self) -> None:
        """
        Reset the selected simulation to its initial state.
        """
        if not self.simulation_instance:
            self.logger.error("Simulation mode not selected. Cannot reset simulation.")
            raise RuntimeError("Simulation mode not selected. Cannot reset simulation.")

        self.logger.info("Resetting simulation.")
        self.simulation_instance.reset_simulation()
        self.logger.info("Simulation reset completed.")

    def _validate_parameters(self, parameters: dict) -> bool:
        """
        Validate the simulation parameters.
        :param parameters: Dictionary of parameters to validate.
        :return: True if parameters are valid, False otherwise.
        """
        try:
            x_range = parameters.get("x_range", 0)
            y_range = parameters.get("y_range", 0)
            z_range = parameters.get("z_range", 0)
            if x_range <= 0 or y_range <= 0 or z_range <= 0:
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating parameters: {e}")
            return False