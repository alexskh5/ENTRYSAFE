# # import os
# # import sys

# # def app_dir():
# #     # If running as EXE (PyInstaller)
# #     if getattr(sys, "frozen", False):
# #         return os.path.dirname(sys.executable)
# #     # Normal python run
# #     return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# import os
# import sys

# def app_dir():
#     """
#     Returns the folder where resources (ui/assets/config) are expected.
#     Works for:
#     - python main.py
#     - PyInstaller --onedir
#     - when launched via shortcut / different working directory
#     """
#     if getattr(sys, "frozen", False):
#         # PyInstaller EXE: resources are beside the exe
#         base = os.path.dirname(sys.executable)
#     else:
#         # Dev: project root (ENTRYSAFE/)
#         base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#     # Fallback: if ui folder isn't found (because of nesting),
#     # try one level deeper (common when zipped/extracted)
#     if not os.path.exists(os.path.join(base, "ui")):
#         alt = os.path.join(base, "EntrySafe")
#         if os.path.exists(os.path.join(alt, "ui")):
#             base = alt

#     return base



import os
import sys

def app_dir():
    """
    Bundled resource directory.
    - Dev run: project root
    - PyInstaller macOS .app: .../EntrySafe.app/Contents/MacOS
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def app_bundle_path():
    """
    Returns the .app bundle path when frozen on macOS:
    .../EntrySafe.app
    Returns None if not running as a macOS .app.
    """
    if not getattr(sys, "frozen", False):
        return None

    # sys.executable: .../EntrySafe.app/Contents/MacOS/EntrySafe
    macos_dir = os.path.dirname(sys.executable)
    bundle = os.path.abspath(os.path.join(macos_dir, "..", "..", ".."))

    if bundle.endswith(".app") and os.path.isdir(bundle):
        return bundle
    return None


def install_dir():
    """
    Folder containing the .app bundle.
    Example:
      /Applications/EntrySafe-Intel
      /Applications/EntrySafe-ARM64
      or any folder the client chooses.
    """
    bundle = app_bundle_path()
    if bundle:
        return os.path.dirname(bundle)

    # Dev fallback: project root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def config_path():
    """
    Prefer external editable config.json in the same folder as EntrySafe.app.
    Fallback to bundled config.json inside Contents/MacOS if external not found.
    """
    external = os.path.join(install_dir(), "config.json")
    if os.path.exists(external):
        return external

    # fallback (inside bundle)
    return os.path.join(app_dir(), "config.json")