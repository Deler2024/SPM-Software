import time
from utils.logger import get_logger

logger = get_logger(__name__)

class StepperMotor:
    def __init__(self, step_size=1.0, max_position=100.0):
        """
        Initialize the StepperMotor with default parameters.
        :param step_size: The size of each step.
        :param max_position: The maximum position the motor can move to.
        """
        self.current_position = 0.0
        self.step_size = step_size
        self.max_position = max_position

    def move_to(self, target_position):
        """
        Move the stepper motor to the specified position.
        :param target_position: The target position to move to.
        """
        if target_position < 0 or target_position > self.max_position:
            raise ValueError(f"Target position {target_position} is out of range (0 to {self.max_position}).")
        
        logger.info(f"Moving stepper motor to position {target_position}...")
        time.sleep(abs(target_position - self.current_position) * 0.01)  # Simulate movement time
        self.current_position = target_position
        logger.info(f"Stepper motor moved to position {self.current_position}")

    def move_to_position(self, target_position):
        """
        Alias for move_to for backward compatibility.
        """
        self.move_to(target_position)

    def step(self, steps):
        """
        Step the motor by a specified number of steps.
        :param steps: The number of steps to move.
        """
        target_position = self.current_position + steps * self.step_size
        if target_position < 0 or target_position > self.max_position:
            raise ValueError(f"Step movement out of range. Current position: {self.current_position}, Target: {target_position}")
        
        logger.info(f"Stepping motor by {steps} steps...")
        time.sleep(abs(steps) * 0.01)  # Simulate movement time
        self.current_position = target_position
        logger.info(f"Stepper motor stepped to position {self.current_position}")

    def get_position(self):
        """
        Get the current position of the stepper motor.
        :return: The current position of the motor.
        """
        return self.current_position

    def reset(self):
        """
        Reset the stepper motor to its initial position (0.0).
        """
        logger.info("Resetting stepper motor to initial position...")
        self.move_to(0.0)
        logger.info("Stepper motor reset to position 0.0")