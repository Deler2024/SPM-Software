# File: D:/Documents/Project/SPM/copilot/SPM-Software/hardware/stepper_motor.py

import time
from utils.logger import get_logger

class StepperMotor:
    def __init__(self, driver_pins=None, step_size=0.01, max_position=100.0):
        self.logger = get_logger(__name__)
        self.driver_pins = driver_pins
        self.position = 0.0
        self.step_size = step_size
        self.max_position = max_position
        self.status = "Idle"

    def move_to(self, position):
        if position < 0 or position > self.max_position:
            self.logger.error(f"Target position {position} is out of range (0 to {self.max_position}).")
            raise ValueError(f"Target position {position} is out of range (0 to {self.max_position}).")
        self.status = "Moving"
        self.logger.info(f"Moving stepper motor to position {position}...")
        steps = int(abs(position - self.position) / self.step_size)
        for _ in range(steps):
            time.sleep(0.01)
        self.position = position
        self.status = "Idle"
        self.logger.info(f"Stepper motor reached position {self.position}.")

    def step(self, steps):
        target_position = self.position + steps * self.step_size
        if target_position < 0 or target_position > self.max_position:
            self.logger.error(f"Step movement out of range. Current position: {self.position}, Target: {target_position}")
            raise ValueError(f"Step movement out of range. Current position: {self.position}, Target: {target_position}")
        self.status = "Stepping"
        self.logger.info(f"Stepping motor by {steps} steps...")
        time.sleep(abs(steps) * 0.01)
        self.position = target_position
        self.status = "Idle"
        self.logger.info(f"Stepper motor stepped to position {self.position}.")

    def get_position(self):
        self.logger.debug(f"Current position: {self.position}")
        return self.position

    def get_status(self):
        self.logger.debug(f"Current status: {self.status}")
        return self.status

    def reset(self):
        self.logger.info("Resetting stepper motor to initial position.")
        self.position = 0.0
        self.status = "Idle"