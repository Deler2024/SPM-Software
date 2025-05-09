# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/widgets/surface_info_panel.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class SurfaceInfoPanel(QWidget):
    """
    Panel for displaying surface analysis information.
    """

    def __init__(self, parent=None):
        """
        Initialize the Surface Info Panel.
        """
        super().__init__(parent)
        self.setWindowTitle("Surface Analysis")
        self.setGeometry(200, 200, 400, 300)

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add a title label
        title_label = QLabel("Surface Analysis")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(title_label)

        # Add a table for surface parameters
        self.parameter_table = QTableWidget(6, 2)  # 6 rows, 2 columns
        self.parameter_table.setHorizontalHeaderLabels(["Parameter", "Value"])
        self.parameter_table.setVerticalHeaderLabels(
            ["Rq (RMS Roughness)", "Ra (Roughness)", "Rz (Max Height)", "Skewness", "Kurtosis", "Surface Area"]
        )
        self.layout.addWidget(self.parameter_table)

        # Populate the table with default values
        self.populate_table()

        logger.info("SurfaceInfoPanel initialized successfully.")

    def populate_table(self):
        """
        Populate the table with default surface parameter values.
        """
        parameters = [
            ("Rq (RMS Roughness)", "N/A"),
            ("Ra (Roughness)", "N/A"),
            ("Rz (Max Height)", "N/A"),
            ("Skewness", "N/A"),
            ("Kurtosis", "N/A"),
            ("Surface Area", "N/A"),
        ]

        for row, (param, value) in enumerate(parameters):
            self.parameter_table.setItem(row, 0, QTableWidgetItem(param))
            self.parameter_table.setItem(row, 1, QTableWidgetItem(value))

    def update_surface_parameters(self, data):
        """
        Update the surface parameters based on the provided data.
        :param data: Dictionary containing parameter names and values.
        """
        try:
            for row, (param, value) in enumerate(data.items()):
                self.parameter_table.setItem(row, 1, QTableWidgetItem(str(value)))
            logger.info("Surface parameters updated successfully.")
        except Exception as e:
            logger.error(f"Error updating surface parameters: {e}")