import csv
import json
import math
from utils.logger import get_logger


class ScanManager:
    def __init__(self, motion_controller):
        """
        Initialize the ScanManager with a MotionController instance.
        :param motion_controller: An instance of MotionController to control the scan.
        """
        self.motion_controller = motion_controller
        self.is_scanning = False
        self.logger = get_logger(__name__)
        self.scan_data = []

    def start_scan(self):
        """Start a scan."""
        self.is_scanning = True
        self.logger.info("Scan started.")

    def stop_scan(self):
        """Stop a scan."""
        self.is_scanning = False
        self.logger.info("Scan stopped.")

    def clear_scan_data(self):
        """Clear the scan data before starting a new scan."""
        self.logger.debug("Clearing scan data.")
        self.scan_data = []

    def log_scan_position(self, x, y, z):
        """
        Log the current scan position.
        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param z: Z-coordinate.
        """
        self.logger.info(f"Scanning position: ({x:.2f}, {y:.2f}, {z:.2f})")
        self.scan_data.append({"x": round(x, 2), "y": round(y, 2), "z": round(z, 2)})

    def raster_scan(self, x_start, x_end, y_start, y_end, step_size, progress_callback=None, data_logger=None):
        """
        Perform a raster scan over the specified area.
        """
        self.logger.info("Starting raster scan...")
        self.clear_scan_data()  # Clear previous scan data

        # Calculate the total number of steps
        total_steps = ((x_end - x_start) // step_size + 1) * ((y_end - y_start) // step_size + 1)
        current_step = 0

        y = y_start
        while y <= y_end:
            x_positions = range(x_start, x_end + 1, step_size)
            if (y - y_start) // step_size % 2 == 1:
                x_positions = reversed(x_positions)  # Zigzag pattern

            for x in x_positions:
                # Fetch real-time Z-data from the MotionController
                z = self.motion_controller.get_z_position()
                self.motion_controller.move(x, y, z)
                self.log_scan_position(x, y, z)

                # Log data to the Data Logging Tab
                if data_logger:
                    data_logger(x, y, z)

                # Update progress
                current_step += 1
                if progress_callback:
                    progress_callback(
                        int((current_step / total_steps) * 100),
                        current_position={"x": x, "y": y, "z": z}
                    )

            y += step_size
        self.logger.info("Raster scan complete.")

    def spiral_scan(self, center_x, center_y, radius, step_size, progress_callback=None):
        """
        Perform a spiral scan around a center point.
        """
        self.logger.info("Starting spiral scan...")
        self.clear_scan_data()  # Clear previous scan data

        # Estimate the total number of steps (approximation)
        total_steps = int((2 * math.pi * radius) / step_size)
        current_step = 0

        theta = 0
        r = 0
        while r <= radius:
            x = center_x + r * math.cos(theta)
            y = center_y + r * math.sin(theta)
            z = self.motion_controller.get_z_position()  # Fetch Z-data
            self.motion_controller.move(x, y, z)
            self.log_scan_position(x, y, z)

            # Update progress
            current_step += 1
            if progress_callback:
                progress_callback(
                    int((current_step / total_steps) * 100),
                    current_position={"x": x, "y": y, "z": z}
                )

            theta += step_size / r if r != 0 else step_size
            r += step_size / (2 * math.pi)
        self.logger.info("Spiral scan complete.")

    def grid_scan(self, x_start, x_end, y_start, y_end, rows, cols, progress_callback=None):
        """
        Perform a grid scan over the specified area.
        """
        self.logger.info("Starting grid scan...")
        self.clear_scan_data()  # Clear previous scan data

        # Calculate step sizes
        x_step = (x_end - x_start) / (cols - 1)
        y_step = (y_end - y_start) / (rows - 1)

        # Calculate total steps
        total_steps = rows * cols
        current_step = 0

        for i in range(rows):
            for j in range(cols):
                x = x_start + j * x_step
                y = y_start + i * y_step
                z = self.motion_controller.get_z_position()  # Fetch Z-data
                self.motion_controller.move(x, y, z)
                self.log_scan_position(x, y, z)

                # Update progress
                current_step += 1
                if progress_callback:
                    progress_callback(
                        int((current_step / total_steps) * 100),
                        current_position={"x": x, "y": y, "z": z}
                    )

        self.logger.info("Grid scan complete.")

    def circular_scan(self, center_x, center_y, radius, num_points, progress_callback=None):
        """
        Perform a circular scan around a center point.
        """
        self.logger.info("Starting circular scan...")
        self.clear_scan_data()  # Clear previous scan data

        # Calculate total steps
        total_steps = num_points
        current_step = 0

        for i in range(num_points):
            theta = 2 * math.pi * i / num_points
            x = center_x + radius * math.cos(theta)
            y = center_y + radius * math.sin(theta)
            z = self.motion_controller.get_z_position()  # Fetch Z-data
            self.motion_controller.move(x, y, z)
            self.log_scan_position(x, y, z)

            # Update progress
            current_step += 1
            if progress_callback:
                progress_callback(
                    int((current_step / total_steps) * 100),
                    current_position={"x": x, "y": y, "z": z}
                )

        self.logger.info("Circular scan complete.")