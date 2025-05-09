import serial
from hardware.base_controller import BaseController

class ArduinoController(BaseController):
    """
    Controller for Arduino devices.
    """
    def __init__(self, port, baudrate=9600):
        super().__init__("Arduino")
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            self.connected = True
            print(f"Connected to Arduino on {self.port}")
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")
            self.connected = False

    def disconnect(self):
        if self.serial_connection:
            self.serial_connection.close()
            self.connected = False
            print("Disconnected from Arduino.")

    def send_command(self, command):
        if not self.connected:
            raise ConnectionError("Arduino is not connected.")
        self.serial_connection.write(command.encode())
        response = self.serial_connection.readline().decode().strip()
        return response