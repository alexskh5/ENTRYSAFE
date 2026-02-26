# import os
# import sys

# def app_dir():
#     # If running as EXE (PyInstaller)
#     if getattr(sys, "frozen", False):
#         return os.path.dirname(sys.executable)
#     # Normal python run
#     return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


import os
import sys

def app_dir():
    """
    Returns the folder where resources (ui/assets/config) are expected.
    Works for:
    - python main.py
    - PyInstaller --onedir
    - when launched via shortcut / different working directory
    """
    if getattr(sys, "frozen", False):
        # PyInstaller EXE: resources are beside the exe
        base = os.path.dirname(sys.executable)
    else:
        # Dev: project root (ENTRYSAFE/)
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Fallback: if ui folder isn't found (because of nesting),
    # try one level deeper (common when zipped/extracted)
    if not os.path.exists(os.path.join(base, "ui")):
        alt = os.path.join(base, "EntrySafe")
        if os.path.exists(os.path.join(alt, "ui")):
            base = alt

    return base