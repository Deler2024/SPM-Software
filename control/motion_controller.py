# File: D:/Documents/Project/SPM/copilot/SPM-Software/control/motion_controller.py

from hardware.stepper_motor import StepperMotor
from hardware.mock_controller import MockController
from utils.logger import get_logger

class MotionController:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.stepper_motor = StepperMotor()
        self.mock_controller = MockController()
        self.z_position = 0.0
        self.setpoint = 0.0
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.0
        self.previous_error = 0.0
        self.integral = 0.0
        self.logger.info("MotionController initialized.")

    def move_z(self, position, fine_control=False):
        if position < 0 or position > 100:
            self.logger.error(f"Z position {position} out of range.")
            raise ValueError("Z position out of range.")
        if fine_control:
            self.logger.info(f"Using fine control to move Z-axis to {position} µm")
            self._fine_move(position)
        else:
            self.logger.info(f"Using coarse control to move Z-axis to {position} µm")
            self._coarse_move(position)
        self.z_position = position

    def _fine_move(self, position):
        self.stepper_motor.move_to(position)
        self.logger.info(f"Fine movement completed. Z-axis at {self.stepper_motor.get_position()} µm")

    def _coarse_move(self, position):
        self.stepper_motor.move_to(position)
        self.logger.info(f"Coarse movement completed. Z-axis at {self.stepper_motor.get_position()} µm")

    def get_z_position(self):
        self.z_position = self.mock_controller.get_position()
        if isinstance(self.z_position, (int, float)):
            return self.z_position
        else:
            self.logger.error("Invalid Z position: Expected a numeric value.")
            raise TypeError("Invalid Z position: Expected a numeric value.")

    def feedback_control(self):
        error = self.setpoint - self.get_z_position()
        proportional = self.kp * error
        self.integral += error
        integral = self.ki * self.integral
        derivative = self.kd * (error - self.previous_error)
        output = proportional + integral + derivative
        self.move_z(self.z_position + output, fine_control=True)
        self.previous_error = error
        self.logger.info(f"Feedback control: Setpoint={self.setpoint}, Current={self.z_position}, Error={error}")

    def set_pid_parameters(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.logger.info(f"PID parameters updated: Kp={kp}, Ki={ki}, Kd={kd}")

    def emergency_retract(self):
        safe_position = 0.0
        self.move_z(safe_position, fine_control=False)
        self.logger.info("Emergency retract completed. Z-axis moved to safe position.")

    def reset(self):
        self.z_position = 0.0
        self.previous_error = 0.0
        self.integral = 0.0
        self.logger.info("MotionController reset to initial state.")