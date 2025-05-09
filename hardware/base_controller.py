class BaseController:
    """
    Abstract base class for hardware controllers.
    """

    def __init__(self, name):
        """
        Initialize the BaseController.
        :param name: Name of the hardware controller.
        """
        self.name = name
        self.connected = False
        self.scanner_size = "Large"  # Default scanner size ("Large" or "Small")

    def connect(self):
        """
        Connect to the hardware device.
        """
        raise NotImplementedError("The 'connect' method must be implemented by subclasses.")

    def disconnect(self):
        """
        Disconnect from the hardware device.
        """
        raise NotImplementedError("The 'disconnect' method must be implemented by subclasses.")

    def send_command(self, command):
        """
        Send a command to the hardware device.
        :param command: Command string to send.
        """
        raise NotImplementedError("The 'send_command' method must be implemented by subclasses.")

    def is_connected(self):
        """
        Check if the device is connected.
        :return: True if connected, False otherwise.
        """
        return self.connected

    def set_scanner_size(self, size: str):
        """
        Set the scanner size (Large or Small).
        :param size: The scanner size to set ("Large" or "Small").
        """
        if size not in ["Large", "Small"]:
            raise ValueError(f"Invalid scanner size: {size}")
        self.scanner_size = size
        self.configure_scanner_size()

    def configure_scanner_size(self):
        """
        Configure the hardware device based on the scanner size.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("The 'configure_scanner_size' method must be implemented by subclasses.")