# File: D:/Documents/Project/SPM/copilot/SPM-Software/tests/test_stepper_motor.py

import sys
import os

# Import the centralized path manager
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from run import add_project_root_to_path

# Add the project root to the Python path
project_root = add_project_root_to_path()
print(f"Project root added to Python path: {project_root}")

import unittest
from hardware.stepper_motor import StepperMotor

class TestStepperMotor(unittest.TestCase):
    """
    Unit tests for the StepperMotor class.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a StepperMotor instance.
        """
        self.stepper_motor = StepperMotor(step_size=0.1, max_position=100.0)

    def test_move_to_valid_position(self):
        """
        Test moving the stepper motor to a valid position within the range.
        """
        self.stepper_motor.move_to(50.0)
        self.assertEqual(self.stepper_motor.get_position(), 50.0)

    def test_move_to_out_of_range_position(self):
        """
        Test moving the stepper motor to positions outside the valid range.
        """
        with self.assertRaises(ValueError):
            self.stepper_motor.move_to(-10.0)
        with self.assertRaises(ValueError):
            self.stepper_motor.move_to(150.0)

    def test_step_movement(self):
        """
        Test stepping the motor by a specific number of steps.
        """
        self.stepper_motor.move_to(20.0)
        self.stepper_motor.step(10)
        self.assertEqual(self.stepper_motor.get_position(), 21.0)
        self.stepper_motor.step(-5)
        self.assertEqual(self.stepper_motor.get_position(), 20.5)

    def test_step_out_of_range(self):
        """
        Test stepping the motor beyond the valid range.
        """
        self.stepper_motor.move_to(95.0)
        with self.assertRaises(ValueError):
            self.stepper_motor.step(60)
        self.stepper_motor.move_to(5.0)
        with self.assertRaises(ValueError):
            self.stepper_motor.step(-60)

    def test_reset(self):
        """
        Test resetting the stepper motor to its initial position.
        """
        self.stepper_motor.move_to(50.0)
        self.stepper_motor.reset()
        self.assertEqual(self.stepper_motor.get_position(), 0.0)

if __name__ == "__main__":
    unittest.main()