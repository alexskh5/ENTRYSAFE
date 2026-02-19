import os
import sys

def app_dir():
    # If running as EXE (PyInstaller)
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    # Normal python run
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
