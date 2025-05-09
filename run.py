import sys
import os

def add_project_root_to_path():
    """
    Dynamically add the project root directory to the Python path.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(current_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return project_root

if __name__ == "__main__":
    project_root = add_project_root_to_path()
    print(f"Project root added to Python path: {project_root}")