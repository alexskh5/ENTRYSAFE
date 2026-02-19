import os
import sys

def app_dir():
    """
    Returns the root folder of the app.
    Works for:
    - python main.py
    - PyInstaller onedir exe
    """

    # If running as EXE (PyInstaller)
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    # Normal python run
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def resource_path(*paths):
    """
    Helper to safely get files like:
    ui files, assets, icons, uploads, etc.
    """

    return os.path.join(app_dir(), *paths)
