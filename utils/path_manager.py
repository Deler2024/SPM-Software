import sys
import os

def add_project_root_to_path():
    """
    Dynamically add the project root directory to the Python path.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../"))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return project_root