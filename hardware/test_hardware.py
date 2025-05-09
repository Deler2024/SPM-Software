import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware.mock_controller import MockController

def test_mock_controller():
    mock = MockController()

    # Test connection
    mock.connect()
    assert mock.is_connected() == True

    # Test sending a command
    response = mock.send_command("TEST_COMMAND")
    assert response == "Mock response to 'TEST_COMMAND'"

    # Test disconnection
    mock.disconnect()
    assert mock.is_connected() == False

if __name__ == "__main__":
    test_mock_controller()
    print("All tests passed!")