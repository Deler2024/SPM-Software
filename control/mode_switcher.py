# File: D:/Documents/Project/SPM/copilot/SPM-Software/control/mode_switcher.py

class ModeSwitcher:
    """
    A class to handle mode switching for the system.
    """

    def __init__(self):
        self.current_mode = None

    def switch_mode(self, mode):
        """
        Switch to the specified mode.
        """
        valid_modes = ["contact", "noncontact"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Valid modes are: {valid_modes}")
        self.current_mode = mode