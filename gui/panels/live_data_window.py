import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class LiveDataWindow(QWidget):
    """
    Widget for displaying live data.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Add a PyQtGraph plot widget
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Add an image view for 2D data
        self.image_view = pg.ImageView()
        self.layout.addWidget(self.image_view)
        self.image_view.setVisible(False)  # Initially hidden

    def update_data(self, data):
        """
        Update the live data visualization with new data.
        :param data: The data to display (e.g., 1D or 2D numpy array).
        """
        if data.ndim == 1:  # 1D data (e.g., line profile)
            self.image_view.setVisible(False)
            self.plot_widget.setVisible(True)
            self.plot_widget.clear()
            self.plot_widget.plot(data, pen='b')
        elif data.ndim == 2:  # 2D data (e.g., topography)
            self.plot_widget.setVisible(False)
            self.image_view.setVisible(True)
            self.image_view.setImage(data)