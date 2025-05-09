# File: main.py

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStatusBar
from gui.main_gui import MainGUI  # Import the MainGUI class
from utils.logger import get_logger
from simulation.simulation_backend import SimulationBackend

# Initialize logger
logger = get_logger(__name__)

class MainWindow(QMainWindow):
    """
    Main application window that contains the MainGUI.
    """
    def __init__(self):
        """
        Initialize the main application window.
        """
        super().__init__()
        logger.info("Initializing MainWindow...")

        # Dynamically set the title based on system capabilities
        self.setWindowTitle("SPM Control and Acquisition")  # Default title
        self.setGeometry(100, 100, 1200, 800)  # Set the default window size and position

        try:
            # Set the main GUI as the central widget
            self.main_gui = MainGUI()
            self.setCentralWidget(self.main_gui)

            # Add a status bar
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)
            self.status_bar.showMessage("Ready")  # Default status message

            logger.info("MainWindow initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize MainWindow: {e}")
            self.show_error_message(f"An error occurred while initializing the MainWindow: {e}")

    def show_error_message(self, message):
        """
        Display an error message in a popup window.
        :param message: The error message to display.
        """
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Critical Error")
        error_box.setText("Initialization Error")
        error_box.setInformativeText(message)
        error_box.exec_()

    def update_status(self, message):
        """
        Update the status bar with a new message.
        :param message: The message to display in the status bar.
        """
        self.status_bar.showMessage(message)
        logger.info(f"Status updated: {message}")


if __name__ == "__main__":
    import sys
    logger.info("Starting SPM Control and Acquisition application...")
    try:
        # Create the application instance
        app = QApplication(sys.argv)

        # Create and show the main window
        window = MainWindow()
        window.show()

        # Start the application event loop
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"An error occurred while running the application: {e}")
        sys.exit(1)