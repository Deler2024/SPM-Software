#  File: tests/test_simulation.py

import sys
import os
import numpy as np
from utils.logger import get_logger

# Add the parent directory to the system path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.simulation_manager import SimulationManager

# Initialize logger
logger = get_logger(__name__)

def test_stm_simulation():
    """
    Test the STM simulation mode.
    """
    logger.info("Testing STM Simulation")
    sim_manager = SimulationManager()
    sim_manager.select_simulation_mode("STM")
    parameters = {
        "resolution": 256,
        "scan_area": (1.0, 1.0),
        "bias_voltage": 0.1
    }
    sim_manager.configure_simulation_parameters(parameters)
    sim_manager.run_simulation()
    data = sim_manager.retrieve_simulated_data()
    logger.info(f"STM Simulation Data Shape: {data.shape}")
    assert data.shape == (256, 256), "STM Simulation data shape mismatch"

def test_afm_contact_simulation():
    """
    Test the AFM contact-mode simulation.
    """
    logger.info("Testing AFM Contact Simulation")
    sim_manager = SimulationManager()
    sim_manager.select_simulation_mode("AFM_contact")
    parameters = {
        "spring_constant": 0.5
    }
    sim_manager.configure_simulation_parameters(parameters)
    sim_manager.run_simulation()
    data = sim_manager.retrieve_simulated_data()
    logger.info(f"AFM Contact Simulation Data Shape: {data.shape}")
    assert data.shape[1] == 2, "AFM Contact Simulation data should have 2 columns (distance, force)"

def test_afm_noncontact_simulation():
    """
    Test the AFM non-contact simulation mode.
    """
    logger.info("Testing AFM Non-Contact Simulation")
    sim_manager = SimulationManager()
    sim_manager.select_simulation_mode("AFM_noncontact")
    parameters = {
        "tip_sample_distance": 1.0,
        "oscillation_amplitude": 0.1
    }
    sim_manager.configure_simulation_parameters(parameters)
    sim_manager.run_simulation()
    data = sim_manager.retrieve_simulated_data()
    logger.info(f"AFM Non-Contact Simulation Data Shape: {data.shape}")
    assert len(data.shape) == 1, "AFM Non-Contact Simulation data should be 1D"

if __name__ == "__main__":
    logger.info("Starting simulation tests...")
    test_stm_simulation()
    test_afm_contact_simulation()
    test_afm_noncontact_simulation()
    logger.info("✅ All simulation tests passed")