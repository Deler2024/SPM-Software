# File: D:/Documents/Project/SPM/copilot/SPM-Software/simulation/simulation_backend.py

import numpy as np

class SimulationBackend:
    def __init__(self, resolution=(100, 100), amplitude=1.0, frequency=1.0):
        self.resolution = resolution
        self.amplitude = amplitude
        self.frequency = frequency

    def generate_topography_data(self):
        x = np.linspace(0, 10, self.resolution[0])
        y = np.linspace(0, 10, self.resolution[1])
        X, Y = np.meshgrid(x, y)
        Z = self.amplitude * np.sin(self.frequency * X) * np.cos(self.frequency * Y)
        return Z

    def generate_line_profile_data(self, length=10):
        x = np.linspace(0, length, self.resolution[0])
        Z = self.amplitude * np.sin(self.frequency * x)
        return Z

    def add_noise(self, data, noise_level=0.1):
        noise = noise_level * np.random.normal(size=data.shape)
        return data + noise

    def generate_noisy_topography_data(self, noise_level=0.1):
        data = self.generate_topography_data()
        return self.add_noise(data, noise_level)

    def generate_noisy_line_profile_data(self, length=10, noise_level=0.1):
        data = self.generate_line_profile_data(length)
        return self.add_noise(data, noise_level)