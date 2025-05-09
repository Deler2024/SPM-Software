# File: gui/forward_backward_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt


class ForwardBackwardWindow(QDialog):
    """
    Window for managing forward and backward scan windows.
    """

    def __init__(self, parent=None):
        """
        Initialize the Forward/Backward Scan Windows dialog.
        """
        super().__init__(parent)
        self.setWindowTitle("Forward/Backward Scan Windows")
        self.setGeometry(200, 200, 1000, 600)

        # Main layout
        self.layout = QVBoxLayout(self)

        # Add a title label
        title_label = QLabel("Forward/Backward Scan Windows")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Add a spin box to select the number of windows
        self.layout.addWidget(QLabel("Number of Windows:"))
        self.window_count_spinbox = QSpinBox()
        self.window_count_spinbox.setRange(1, 10)  # Allow up to 10 windows
        self.window_count_spinbox.setValue(1)  # Default to 1 window
        self.window_count_spinbox.valueChanged.connect(self.update_windows)
        self.layout.addWidget(self.window_count_spinbox)

        # Add a reset button
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_to_default)
        self.layout.addWidget(self.reset_button)

        # Add a grid layout for the windows
        self.window_grid = QGridLayout()
        self.layout.addLayout(self.window_grid)

        # Initialize the windows
        self.windows = []
        self.update_windows(1)

    def update_windows(self, count):
        """
        Update the number of windows displayed in the grid.
        :param count: The number of windows to display.
        """
        try:
            # Clear the existing windows
            for i in reversed(range(self.window_grid.count())):
                widget = self.window_grid.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            # Add the new windows
            self.windows = []
            for i in range(count):
                frame = self.create_window_frame(i)
                self.window_grid.addWidget(frame, i // 5, i % 5)  # Arrange in a grid (5 columns max)
        except Exception as e:
            print(f"Error updating windows: {e}")

    def create_window_frame(self, index):
        """
        Create a frame for a single forward/backward scan window.
        :param index: Index of the window.
        :return: QFrame containing the dropdown and placeholder.
        """
        try:
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setFrameShadow(QFrame.Raised)
            frame.setStyleSheet("border: 1px solid gray; padding: 5px;")

            layout = QVBoxLayout(frame)

            # Add a dropdown for Line Mode/Topography Mode
            dropdown = QComboBox()
            dropdown.addItems(["Line Mode", "Topography Mode"])
            dropdown.setToolTip("Select the mode for this window.")
            dropdown.currentIndexChanged.connect(lambda idx, win=index: self.update_mode(win, idx))
            layout.addWidget(dropdown)

            # Add a placeholder label for the window
            placeholder = QLabel(f"Window {index + 1}")
            placeholder.setAlignment(Qt.AlignCenter)
            layout.addWidget(placeholder)

            self.windows.append((frame, dropdown, placeholder))
            return frame
        except Exception as e:
            print(f"Error creating window frame: {e}")
            return None

    def update_mode(self, window_index, mode_index):
        """
        Update the mode of a specific window.
        :param window_index: Index of the window.
        :param mode_index: Index of the selected mode.
        """
        try:
            mode = "Line Mode" if mode_index == 0 else "Topography Mode"
            self.windows[window_index][2].setText(f"Window {window_index + 1} - {mode}")
        except Exception as e:
            print(f"Error updating mode for window {window_index}: {e}")

    def reset_to_default(self):
        """
        Reset the configuration to the default state (1 window in Line Mode).
        """
        try:
            self.window_count_spinbox.setValue(1)  # Reset to 1 window
            self.update_windows(1)
        except Exception as e:
            print(f"Error resetting to default: {e}")