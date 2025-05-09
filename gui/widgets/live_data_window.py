# File: D:/Documents/Project/SPM/copilot/SPM-Software/gui/widgets/live_data_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class LiveDataWindow(QWidget):
    """
    Window for displaying live data.
    """

    def __init__(self, parent=None):
        """
        Initialize the Live Data Window.
        """
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Add a matplotlib figure for visualization
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Add a label for debugging
        self.data_label = QLabel("No data")
        self.layout.addWidget(self.data_label)

    def update_data(self, data):
        """
        Update the visualization with new data.
        :param data: The data to display (e.g., 1D or 2D numpy array).
        """
        self.data_label.setText(f"Data shape: {data.shape}")

        # Clear the figure
        self.figure.clear()

        # Plot the data
        ax = self.figure.add_subplot(111)
        if data.ndim == 2:
            ax.imshow(data, cmap="viridis", origin="lower")
        elif data.ndim == 1:
            ax.plot(data)

        # Refresh the canvas
        self.canvas.draw()
            else:
                raise ValueError("Unsupported data dimensionality. Only 1D and 2D data are supported.")
        except Exception as e:
            logger.error(f"Error updating data: {e}")

    def _update_1d_data(self, data):
        """
        Update the visualization for 1D data.
        :param data: 1D numpy array to display.
        """
        if self.current_mode != "1D":
            self.image_view.setVisible(False)
            self.plot_widget.setVisible(True)
            self.current_mode = "1D"
            logger.info("Switched to 1D data visualization mode.")

        self.plot_widget.clear()
        self.plot_widget.plot(data, pen=pg.mkPen(color='b', width=2))
        logger.debug("1D data updated successfully.")

    def _update_2d_data(self, data):
        """
        Update the visualization for 2D data.
        :param data: 2D numpy array to display.
        """
        if self.current_mode != "2D":
            self.plot_widget.setVisible(False)
            self.image_view.setVisible(True)
            self.current_mode = "2D"
            logger.info("Switched to 2D data visualization mode.")

        self.image_view.setImage(data, autoLevels=True)
        logger.debug("2D data updated successfully.")

    def set_plot_labels(self, x_label="Index", y_label="Amplitude"):
        """
        Set custom labels for the 1D plot.
        :param x_label: Label for the x-axis.
        :param y_label: Label for the y-axis.
        """
        self.plot_widget.setLabel('bottom', x_label)
        self.plot_widget.setLabel('left', y_label)
        logger.info(f"Plot labels updated: X='{x_label}', Y='{y_label}'")

    def set_image_colormap(self, colormap="viridis"):
        """
        Set a custom colormap for the 2D image view.
        :param colormap: Name of the colormap to use (e.g., "viridis").
        """
        try:
            import matplotlib.pyplot as plt
            cmap = plt.get_cmap(colormap)
            lut = (cmap(np.linspace(0, 1, 256)) * 255).astype(np.uint8)
            self.image_view.setColorMap(pg.ColorMap(pos=np.linspace(0, 1, 256), color=lut))
            logger.info(f"Colormap updated to '{colormap}'.")
        except Exception as e:
            logger.error(f"Error setting colormap: {e}")

    def clear_data(self):
        """
        Clear the current visualization.
        """
        if self.current_mode == "1D":
            self.plot_widget.clear()
        elif self.current_mode == "2D":
            self.image_view.clear()
        logger.info("Visualization cleared.")