from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QTimer
from hardware.mock_controller import MockController
from hardware.arduino_controller import ArduinoController  # Replace with actual hardware controller

class HardwareTab(QWidget):
    """
    A tab for controlling hardware and monitoring its status in real time.
    """
    def __init__(self, get_mode_callback, parent=None):
        super().__init__(parent)

        # Store the callback to get the current mode
        self.get_mode = get_mode_callback

        # Initialize controllers
        self.simulation_controller = MockController()
        self.hardware_controller = ArduinoController(port="COM3")  # Replace with actual port
        self.current_controller = self.simulation_controller  # Default to simulation

        # Set up the layout
        self.layout = QVBoxLayout(self)

        # Add a label
        self.label = QLabel("Hardware Control Tab", self)
        self.layout.addWidget(self.label)

        # Add a button to connect to the hardware
        self.connect_button = QPushButton("Connect to Device", self)
        self.connect_button.clicked.connect(self.connect_device)
        self.layout.addWidget(self.connect_button)

        # Add a button to disconnect from the hardware
        self.disconnect_button = QPushButton("Disconnect from Device", self)
        self.disconnect_button.clicked.connect(self.disconnect_device)
        self.layout.addWidget(self.disconnect_button)

        # Add a text input for sending commands
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter command to send to device")
        self.layout.addWidget(self.command_input)

        # Add a button to send commands
        self.send_command_button = QPushButton("Send Command", self)
        self.send_command_button.clicked.connect(self.send_command)
        self.layout.addWidget(self.send_command_button)

        # Add a grid layout for real-time feedback
        self.status_grid = QGridLayout()
        self.layout.addLayout(self.status_grid)

        # Add labels for real-time feedback
        self.position_label = QLabel("Position (X, Y, Z):")
        self.position_value = QLabel("N/A")
        self.status_grid.addWidget(self.position_label, 0, 0)
        self.status_grid.addWidget(self.position_value, 0, 1)

        self.velocity_label = QLabel("Velocity:")
        self.velocity_value = QLabel("N/A")
        self.status_grid.addWidget(self.velocity_label, 1, 0)
        self.status_grid.addWidget(self.velocity_value, 1, 1)

        self.device_status_label = QLabel("Device Status:")
        self.device_status_value = QLabel("N/A")
        self.status_grid.addWidget(self.device_status_label, 2, 0)
        self.status_grid.addWidget(self.device_status_value, 2, 1)

        # Add a text area to display detailed logs
        self.status_display = QTextEdit(self)
        self.status_display.setReadOnly(True)
        self.layout.addWidget(self.status_display)

        # Add a timer for real-time monitoring
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.poll_device_status)

    def update_controller(self):
        """
        Update the current controller based on the selected mode.
        """
        mode = self.get_mode()
        if mode == "Simulation Mode":
            self.current_controller = self.simulation_controller
        elif mode == "Hardware Mode":
            self.current_controller = self.hardware_controller
        self.status_display.append(f"Switched to {mode}.")

    def connect_device(self):
        """
        Connect to the device and start monitoring.
        """
        self.update_controller()
        try:
            self.current_controller.connect()
            self.status_display.append("Connected to device.")
            self.monitor_timer.start(1000)  # Poll every 1 second
        except Exception as e:
            self.status_display.append(f"Error connecting to device: {e}")

    def disconnect_device(self):
        """
        Disconnect from the device and stop monitoring.
        """
        try:
            self.current_controller.disconnect()
            self.status_display.append("Disconnected from device.")
            self.monitor_timer.stop()
        except Exception as e:
            self.status_display.append(f"Error disconnecting from device: {e}")

    def send_command(self):
        """
        Send a command to the device.
        """
        command = self.command_input.text()
        if not command:
            self.status_display.append("Please enter a command.")
            return

        try:
            response = self.current_controller.send_command(command)
            self.status_display.append(f"Sent: {command}")
            self.status_display.append(f"Response: {response}")
        except Exception as e:
            self.status_display.append(f"Error sending command: {e}")

    def poll_device_status(self):
        """
        Poll the device for status updates.
        """
        try:
            # Simulate a status update (replace with actual hardware status polling)
            position = self.current_controller.send_command("GET_POSITION")
            velocity = self.current_controller.send_command("GET_VELOCITY")
            device_status = self.current_controller.send_command("GET_STATUS")

            # Update the labels with the fetched data
            self.position_value.setText(position)
            self.velocity_value.setText(velocity)
            self.device_status_value.setText(device_status)

            # Log the status updates
            self.status_display.append(f"Position: {position}")
            self.status_display.append(f"Velocity: {velocity}")
            self.status_display.append(f"Device Status: {device_status}")
        except Exception as e:
            self.status_display.append(f"Error polling device status: {e}")