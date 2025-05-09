import unittest
from run import add_project_root_to_path

# Add the project root to the Python path
project_root = add_project_root_to_path()
print(f"Project root added to Python path: {project_root}")

if __name__ == "__main__":
    # Discover and run all tests in the 'tests' directory
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    print(f"Discovered tests: {suite}")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)