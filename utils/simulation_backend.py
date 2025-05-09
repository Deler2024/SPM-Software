import numpy as np

class SimulationBackend:
    """
    A flexible backend to simulate data streams for live data visualizations.
    """

    def __init__(self):
        # Independent time variables for each data stream
        self.xy_time = 0
        self.z_time = 0
        self.topography_time = 0
        self.line_profile_time = 0

    def generate_xy_data(self, amplitude=50, frequency=1, noise_level=0):
        """
        Simulate XY scanner data (e.g., a sinusoidal path).
        :param amplitude: Amplitude of the sinusoidal path.
        :param frequency: Frequency of the sinusoidal path.
        :param noise_level: Standard deviation of Gaussian noise to add.
        :return: Tuple of (x, y) data points.
        """
        self.xy_time += 0.1
        x = amplitude * np.sin(2 * np.pi * frequency * self.xy_time)
        y = amplitude * np.cos(2 * np.pi * frequency * self.xy_time)
        x += np.random.normal(0, noise_level)  # Add noise
        y += np.random.normal(0, noise_level)  # Add noise
        return x, y

    def generate_topography_data(self, size=100, amplitude=100, noise_level=0):
        """
        Simulate dynamic topography data (e.g., a 2D Gaussian surface with noise).
        :param size: Size of the grid (size x size).
        :param amplitude: Amplitude of the Gaussian surface.
        :param noise_level: Standard deviation of Gaussian noise to add.
        :return: 2D numpy array representing the surface.
        """
        self.topography_time += 0.1
        x = np.linspace(-50, 50, size)
        y = np.linspace(-50, 50, size)
        x, y = np.meshgrid(x, y)
        z = amplitude * np.exp(-(x**2 + y**2) / (2 * 20**2))  # Gaussian surface
        z += np.sin(self.topography_time) * 10  # Add dynamic changes
        z += np.random.normal(0, noise_level, z.shape)  # Add noise
        return z

    def generate_line_profile_data(self, length=100, amplitude=10, frequency=1, noise_level=0):
        """
        Simulate line profile data (e.g., a 1D sinusoidal wave with noise).
        :param length: Number of points in the line profile.
        :param amplitude: Amplitude of the sinusoidal wave.
        :param frequency: Frequency of the sinusoidal wave.
        :param noise_level: Standard deviation of Gaussian noise to add.
        :return: Tuple of (x, y) data points.
        """
        self.line_profile_time += 0.1
        x = np.linspace(0, length, length)
        y = amplitude * np.sin(2 * np.pi * frequency * x / length)
        y += np.random.normal(0, noise_level, y.shape)  # Add noise
        return x, y

    def generate_z_scanner_data(self, amplitude=100, damping=0.1, frequency=1, noise_level=0):
        """
        Simulate Z-scanner data (e.g., a damped oscillation with noise).
        :param amplitude: Amplitude of the oscillation.
        :param damping: Damping factor for the oscillation.
        :param frequency: Frequency of the oscillation.
        :param noise_level: Standard deviation of Gaussian noise to add.
        :return: Tuple of (time, z) data points.
        """
        self.z_time += 0.1
        z = amplitude * np.exp(-damping * self.z_time) * np.sin(2 * np.pi * frequency * self.z_time)
        z += np.random.normal(0, noise_level)  # Add noise
        return self.z_time, z