import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Check if __file__ is defined
if '__file__' in globals():
    # Add the project root directory to sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
else:
    # Fallback for interactive environments
    sys.path.append(os.path.abspath('..'))

from simulation.simulation_manager import SimulationManager
from utils.logger import Logger  # Use the project's logger
from config.settings import simulation_parameters  # Centralized parameters

# Initialize simulation manager and logger
sim_manager = SimulationManager()
logger = Logger()

def visualize_stm_topography():
    sim_manager.select_simulation_mode("STM")
    parameters = {
        "resolution": 256,
        "scan_area": (1.0, 1.0),
        "bias_voltage": 0.1
    }
    sim_manager.configure_simulation_parameters(parameters)
    sim_manager.run_simulation()
    data = sim_manager.retrieve_simulated_data()

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.imshow(data, cmap='viridis', extent=[0, 1, 0, 1])
    fig.colorbar(cax, label='Height (a.u.)')
    ax.set_title('STM Topography')
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    plt.show()

    # Save the data and plot
    save_data_to_csv(data, "results/stm_topography.csv")
    save_plot_as_image(fig, "results/stm_topography.png")

def visualize_afm_contact():
    sim_manager.select_simulation_mode("AFM_contact")
    parameters = {
        "spring_constant": 0.5
    }
    sim_manager.configure_simulation_parameters(parameters)
    sim_manager.run_simulation()
    data = sim_manager.retrieve_simulated_data()

    distance = data[:, 0]
    force = data[:, 1]

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(distance, force, label='Force-Distance Curve')
    ax.set_title('AFM Contact Mode')
    ax.set_xlabel('Distance (nm)')
    ax.set_ylabel('Force (nN)')
    ax.legend()
    plt.show()

    # Save the data and plot
    save_data_to_csv({"Distance (nm)": distance, "Force (nN)": force}, "results/afm_contact.csv")
    save_plot_as_image(fig, "results/afm_contact.png")

def visualize_afm_noncontact():
    sim_manager.select_simulation_mode("AFM_noncontact")
    parameters = {
        "tip_sample_distance": 1.0,
        "oscillation_amplitude": 0.1
    }
    sim_manager.configure_simulation_parameters(parameters)
    sim_manager.run_simulation()
    data = sim_manager.retrieve_simulated_data()

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(data, label='Frequency Shift')
    ax.set_title('AFM Non-Contact Mode')
    ax.set_xlabel('Data Points')
    ax.set_ylabel('Frequency Shift (Hz)')
    ax.legend()
    plt.show()

    # Save the data and plot
    save_data_to_csv({"Frequency Shift (Hz)": data}, "results/afm_noncontact.csv")
    save_plot_as_image(fig, "results/afm_noncontact.png")
        
import pandas as pd

def save_data_to_csv(data, filename):
    """
    Save simulation data to a CSV file.
    :param data: 2D numpy array or dictionary.
    :param filename: Path to save the CSV file.
    """
    if isinstance(data, np.ndarray):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame(data)
    else:
        raise ValueError("Data must be a numpy array or dictionary.")
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_plot_as_image(fig, filename):
    """
    Save a matplotlib figure as an image file.
    :param fig: Matplotlib figure object.
    :param filename: Path to save the image.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {filename}")
    

# Run all visualizations
if __name__ == "__main__":
    visualize_stm_topography()
    visualize_afm_contact()
    visualize_afm_noncontact()