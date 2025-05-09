from hardware.stepper_motor import StepperMotor
from hardware.mock_controller import MockController
from utils.logger import get_logger

logger = get_logger(__name__)

class MotionController:
    def __init__(self):
        self.z_position = 0  # Initialize Z position
        self.setpoint = 0    # Initialize setpoint for feedback control
        self.kp = 0.0        # PID proportional gain
        self.ki = 0.0        # PID integral gain
        self.kd = 0.0        # PID derivative gain

    def move_z(self, position):
        """Move the Z-axis to the specified position."""
        if not isinstance(position, (int, float)):
            raise TypeError("Position must be a numeric value.")
        if position < 0 or position > 100:
            raise ValueError("Position out of range (0 to 100).")
        self.z_position = position
        logger.info(f"Z-axis moved to position {self.z_position}")

    def get_z_position(self):
        """Get the current Z-axis position."""
        if not isinstance(self.z_position, (int, float)):
            raise TypeError("Invalid Z position: Expected a numeric value.")
        return self.z_position

    def feedback_control(self):
        """Perform feedback control to adjust the Z-axis."""
        try:
            error = self.setpoint - self.get_z_position()
            logger.info(f"Feedback control error: {error}")
            # Adjust Z position based on error (simple proportional control for now)
            self.z_position += self.kp * error
            logger.info(f"Z-axis adjusted to position {self.z_position}")
        except Exception as e:
            logger.error(f"Feedback control failed: {e}")
            raise RuntimeError(f"Feedback control failed: {e}")

    def set_pid_parameters(self, kp, ki, kd):
        """Set PID parameters for feedback control."""
        if not all(isinstance(param, (int, float)) for param in [kp, ki, kd]):
            raise TypeError("PID parameters must be numeric values.")
        self.kp = kp
        self.ki = ki
        self.kd = kd
        logger.info(f"PID parameters set: kp={self.kp}, ki={self.ki}, kd={self.kd}")

    def emergency_retract(self):
        """Retract the Z-axis to a safe position."""
        safe_position = 0
        try:
            self.move_z(safe_position)
            logger.info("Emergency retract successful.")
        except Exception as e:
            logger.error(f"Emergency retract failed: {e}")
            raise RuntimeError(f"Emergency retract failed: {e}")