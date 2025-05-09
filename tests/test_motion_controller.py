import sys
sys.path.append("D:/Documents/Project/SPM/copilot/SPM-Software/")

import unittest
from control.motion_controller import MotionController
from hardware.mock_controller import MockController
from utils.logger import get_logger

logger = get_logger(__name__)

class TestMotionController(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up TestMotionController...")
        self.mock_controller = MockController()
        self.motion_controller = MotionController()

    def test_move_z(self):
        logger.info("Testing move_z...")
        try:
            self.motion_controller.move_z(50)
            self.assertEqual(self.motion_controller.get_z_position(), 50)
            logger.info("move_z test passed.")
        except Exception as e:
            logger.error(f"move_z test failed: {e}")
            self.fail(f"move_z test raised an exception: {e}")

    def test_move_z_out_of_range(self):
        logger.info("Testing move_z_out_of_range...")
        with self.assertRaises(ValueError):
            self.motion_controller.move_z(-10)
        with self.assertRaises(ValueError):
            self.motion_controller.move_z(150)
        logger.info("move_z_out_of_range test passed.")

    def test_feedback_control(self):
        logger.info("Testing feedback_control...")
        try:
            self.motion_controller.set_pid_parameters(kp=1.0, ki=0.1, kd=0.05)
            self.motion_controller.setpoint = 75
            self.motion_controller.feedback_control()
            self.assertAlmostEqual(self.motion_controller.get_z_position(), 75, delta=0.1)
            logger.info("feedback_control test passed.")
        except Exception as e:
            logger.error(f"feedback_control test failed: {e}")
            self.fail(f"feedback_control test raised an exception: {e}")

    def test_emergency_retract(self):
        logger.info("Testing emergency_retract...")
        try:
            self.motion_controller.move_z(50)
            self.motion_controller.emergency_retract()
            self.assertEqual(self.motion_controller.get_z_position(), 0.0)
            logger.info("emergency_retract test passed.")
        except Exception as e:
            logger.error(f"emergency_retract test failed: {e}")
            self.fail(f"emergency_retract test raised an exception: {e}")

    def test_set_pid_parameters(self):
        logger.info("Testing set_pid_parameters...")
        try:
            self.motion_controller.set_pid_parameters(kp=2.0, ki=0.5, kd=0.1)
            self.assertEqual(self.motion_controller.kp, 2.0)
            self.assertEqual(self.motion_controller.ki, 0.5)
            self.assertEqual(self.motion_controller.kd, 0.1)
            logger.info("set_pid_parameters test passed.")
        except Exception as e:
            logger.error(f"set_pid_parameters test failed: {e}")
            self.fail(f"set_pid_parameters test raised an exception: {e}")

    def test_move_z_valid(self):
        logger.info("Testing move_z_valid...")
        self.motion_controller.move_z(50.0)
        self.assertEqual(self.motion_controller.get_z_position(), 50.0)
        logger.info("move_z_valid test passed.")
    
    def test_move_z_invalid(self):
        logger.info("Testing move_z_invalid...")
        with self.assertRaises(TypeError):
            self.motion_controller.move_z("invalid")  # Invalid input
        with self.assertRaises(TypeError):
            self.motion_controller.move_z(None)  # Invalid input
        logger.info("move_z_invalid test passed.")


if __name__ == "__main__":
    unittest.main()