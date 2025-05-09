# SPM Software Project

## Overview

This project is a professional-grade, modular, and extensible Scanning Probe Microscopy (SPM) software suite designed to control custom-built hardware (Arduino, Raspberry Pi, stepper motors, actuators, etc.). It is built with the precision, reliability, and modularity expected from leading scientific instrumentation platforms.

## Folder Structure

- **`config/`**: Centralized configuration management.
- **`hardware/`**: Hardware abstraction layer for microcontrollers and actuators.
- **`control/`**: Low-level control logic for motion, feedback, and signal generation.
- **`scan_engine/`**: Scan logic for each SPM mode (STM, AFM, etc.).
- **`simulation/`**: Physics-based simulation models for virtual scanning.
- **`gui/`**: GUI logic and interface components.
- **`data/`**: Data storage, processing, and visualization.
- **`utils/`**: Utility functions and helpers.
- **`static/`**: Web assets (CSS, JS, images) for the GUI.
- **`template/`**: HTML templates for the GUI.
- **`tests/`**: Unit and integration tests.
- **`docs/`**: Developer and user documentation.

## Setup Instructions

To initialize the folder and file structure:

1. Ensure Python is installed on your system.
2. Save the `setup_structure.py` script in your project directory.
3. Open a terminal or command prompt.
4. Navigate to the directory containing the script.
5. Run the script:

```bash
python setup_structure.py
