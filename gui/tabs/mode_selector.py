#gui/tabs/mode_selector.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox

class ModeSelector(QWidget):
    """
    A widget for selecting the current mode (Simulation or Hardware).
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the layout
        self.layout = QHBoxLayout(self)

        # Add a label
        self.label = QLabel("Mode:")
        self.layout.addWidget(self.label)

        # Add a combo box for mode selection
        self.mode_combo = QComboBox(self)
        self.mode_combo.addItems(["Simulation Mode", "Hardware Mode"])
        self.layout.addWidget(self.mode_combo)

    @property
    def current_mode(self):
        """
        Get the currently selected mode.
        """
        return self.mode_combo.currentText()