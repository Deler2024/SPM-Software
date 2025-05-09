import sys
sys.path.append("D:/Documents/Project/SPM/copilot/SPM-Software/")

import time
from hardware.base_controller import BaseController
from utils.logger import get_logger

class MockController:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.position = (0.0, 0.0, 0.0)
        self.connected = False
        self.status = "Idle"
        self.scanner_size = "Large"
        self.configure_scanner_size()

    def get_position(self):
        self.logger.debug(f"Current position: {self.position}")
        return self.position

    def get_z_position(self):
        z_position = self.position[2]
        self.logger.debug(f"Current Z-position: {z_position}")
        return z_position

    def move_to(self, x, y, z):
        if not self.connected:
            self.logger.error("Attempted to move while device is not connected.")
            raise ConnectionError("Mock device is not connected.")
        if not (0 <= x <= self.scanner_limits["x"] and 0 <= y <= self.scanner_limits["y"] and 0 <= z <= self.scanner_limits["z"]):
            self.logger.error(f"Target position ({x}, {y}, {z}) exceeds scanner limits: {self.scanner_limits}")
            raise ValueError(f"Target position ({x}, {y}, {z}) exceeds scanner limits: {self.scanner_limits}")
        self.status = "Moving"
        self.logger.info(f"Moving to position ({x}, {y}, {z})...")
        time.sleep(1)
        self.position = (x, y, z)
        self.status = "Idle"
        self.logger.info(f"Reached position: {self.position}")

    def move_z(self, z):
        if not self.connected:
            self.logger.error("Attempted to move Z-axis while device is not connected.")
            raise ConnectionError("Mock device is not connected.")
        if not (0 <= z <= self.scanner_limits["z"]):
            self.logger.error(f"Target Z-position ({z}) exceeds Z-axis limit: {self.scanner_limits['z']}")
            raise ValueError(f"Target Z-position ({z}) exceeds Z-axis limit: {self.scanner_limits['z']}")
        self.status = "Moving Z"
        self.logger.info(f"Moving Z-axis to {z}...")
        time.sleep(1)
        self.position = (self.position[0], self.position[1], z)
        self.status = "Idle"
        self.logger.info(f"Z-axis reached position: {z}")

    def get_status(self):
        self.logger.debug(f"Current status: {self.status}")
        return self.status

    def connect(self):
        self.connected = True
        self.logger.info("Mock device connected.")

    def disconnect(self):
        self.connected = False
        self.logger.info("Mock device disconnected.")

    def configure_scanner_size(self):
        if self.scanner_size == "Large":
            self.scanner_limits = {"x": 100.0, "y": 100.0, "z": 30.0}
            self.logger.info("Configured scanner size to Large: X=100cm, Y=100cm, Z=30cm")
        elif self.scanner_size == "Small":
            self.scanner_limits = {"x": 5.0, "y": 5.0, "z": 1.0}
            self.logger.info("Configured scanner size to Small: X=5cm, Y=5cm, Z=1cm")
        else:
            self.logger.error(f"Invalid scanner size: {self.scanner_size}")
            raise ValueError(f"Invalid scanner size: {self.scanner_size}")

    def reset(self):
        self.position = (0, 0, 0)
        self.status = "Idle"
        self.logger.info("Mock device reset to initial state.")
        
    def move_to(self, x, y, z):
        if not (0 <= z <= self.scanner_limits["z"]):
            self.logger.error(f"Target Z-position ({z}) exceeds Z-axis limit: {self.scanner_limits['z']}")
            raise ValueError(f"Target Z-position ({z}) exceeds Z-axis limit: {self.scanner_limits['z']}")
        self.logger.info(f"Moving to position ({x}, {y}, {z})...")
        self.position = (x, y, z)