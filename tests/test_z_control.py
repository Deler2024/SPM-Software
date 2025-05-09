# File: tests/test_z_control.py

import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from hardware.mock_controller import MockController


def test_z_scanner():
    """
    Test the Z-scanner functionality using the MockController.
    """
    print("Starting Z-Scanner Tests...")

    # Initialize the mock controller
    z_scanner = MockController()

    # Test 1: Connect the device
    print("Test 1: Connecting the device...")
    z_scanner.connect()
    assert z_scanner.connected, "Failed to connect the mock device."
    print("Device connected successfully.")

    # Test 2: Move Z-axis to a valid position
    print("Test 2: Moving Z-axis to position 10.0...")
    z_scanner.move_z(10.0)
    current_z = z_scanner.get_z_position()
    assert abs(current_z - 10.0) < 0.1, f"Z-position mismatch! Expected: 10.0, Got: {current_z}"
    print(f"Z-axis moved successfully to {current_z}.")

    # Test 3: Move Z-axis to another valid position
    print("Test 3: Moving Z-axis to position 5.0...")
    z_scanner.move_z(5.0)
    current_z = z_scanner.get_z_position()
    assert abs(current_z - 5.0) < 0.1, f"Z-position mismatch! Expected: 5.0, Got: {current_z}"
    print(f"Z-axis moved successfully to {current_z}.")

    # Test 4: Attempt to move Z-axis beyond limits
    print("Test 4: Attempting to move Z-axis beyond limits...")
    try:
        z_scanner.move_z(50.0)  # Exceeds Z-axis limit
    except ValueError as e:
        print(f"Expected error caught: {e}")
    else:
        raise AssertionError("Expected ValueError for exceeding Z-axis limits, but no error was raised.")

    # Test 5: Disconnect the device and attempt to move
    print("Test 5: Disconnecting the device and attempting to move...")
    z_scanner.disconnect()
    try:
        z_scanner.move_z(5.0)
    except ConnectionError as e:
        print(f"Expected error caught: {e}")
    else:
        raise AssertionError("Expected ConnectionError for moving while disconnected, but no error was raised.")

    print("All Z-Scanner tests passed!")


if __name__ == "__main__":
    test_z_scanner()