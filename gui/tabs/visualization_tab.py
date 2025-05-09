#  File: gui/tabs/visualization_tab.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from simulation.simulation_manager import SimulationManager

class VisualizationTab(QWidget):
    """
    A tab for visualizing STM, AFM contact, and AFM non-contact simulations.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the simulation manager
        self.sim_manager = SimulationManager()

        # Set up the layout
        self.layout = QVBoxLayout(self)

        # Add a label
        self.label = QLabel("Visualization Tab", self)
        self.layout.addWidget(self.label)

        # Add buttons for each visualization
        self.stm_button = QPushButton("Visualize STM Topography", self)
        self.stm_button.clicked.connect(self.visualize_stm_topography)
        self.layout.addWidget(self.stm_button)

        self.afm_contact_button = QPushButton("Visualize AFM Contact Mode", self)
        self.afm_contact_button.clicked.connect(self.visualize_afm_contact)
        self.layout.addWidget(self.afm_contact_button)

        self.afm_noncontact_button = QPushButton("Visualize AFM Non-Contact Mode", self)
        self.afm_noncontact_button.clicked.connect(self.visualize_afm_noncontact)
        self.layout.addWidget(self.afm_noncontact_button)

        # Add a matplotlib canvas for displaying plots
        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.layout.addWidget(self.canvas)

    def visualize_stm_topography(self):
        """
        Visualize STM topography on the canvas.
        """
        try:
            self.sim_manager.select_simulation_mode("STM")
            parameters = {
                "resolution": 256,
                "scan_area": (1.0, 1.0),
                "bias_voltage": 0.1
            }
            self.sim_manager.configure_simulation_parameters(parameters)
            self.sim_manager.run_simulation()
            data = self.sim_manager.retrieve_simulated_data()

            if data is None:
                raise ValueError("No data returned from simulation.")

            # Plot the data on the canvas
            ax = self.canvas.figure.add_subplot(111)
            ax.clear()
            im = ax.imshow(data, cmap='viridis', extent=[0, 1, 0, 1])
            ax.set_title("STM Topography")
            ax.set_xlabel("X (µm)")
            ax.set_ylabel("Y (µm)")
            self.canvas.figure.colorbar(im, ax=ax, orientation='vertical', label="Height (nm)")
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to visualize STM topography: {e}")

    def visualize_afm_contact(self):
        """
        Visualize AFM contact mode on the canvas.
        """
        try:
            self.sim_manager.select_simulation_mode("AFM_contact")
            parameters = {
                "spring_constant": 0.5
            }
            self.sim_manager.configure_simulation_parameters(parameters)
            self.sim_manager.run_simulation()
            data = self.sim_manager.retrieve_simulated_data()

            if data is None or data.shape[1] != 2:
                raise ValueError("Invalid data returned from simulation.")

            distance = data[:, 0]
            force = data[:, 1]

            # Plot the data on the canvas
            ax = self.canvas.figure.add_subplot(111)
            ax.clear()
            ax.plot(distance, force, label="Force-Distance Curve")
            ax.set_title("AFM Contact Mode")
            ax.set_xlabel("Distance (nm)")
            ax.set_ylabel("Force (nN)")
            ax.legend()
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to visualize AFM contact mode: {e}")

    def visualize_afm_noncontact(self):
        """
        Visualize AFM non-contact mode on the canvas.
        """
        try:
            self.sim_manager.select_simulation_mode("AFM_noncontact")
            parameters = {
                "tip_sample_distance": 1.0,
                "oscillation_amplitude": 0.1
            }
            self.sim_manager.configure_simulation_parameters(parameters)
            self.sim_manager.run_simulation()
            data = self.sim_manager.retrieve_simulated_data()

            if data is None:
                raise ValueError("No data returned from simulation.")

            # Plot the data on the canvas
            ax = self.canvas.figure.add_subplot(111)
            ax.clear()
            ax.plot(data, label="Frequency Shift")
            ax.set_title("AFM Non-Contact Mode")
            ax.set_xlabel("Data Points")
            ax.set_ylabel("Frequency Shift (Hz)")
            ax.legend()
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to visualize AFM non-contact mode: {e}")