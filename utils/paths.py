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



# import os
# import sys

# APP_NAME = "EntrySafe"

# def _mac_bundle_dirs():
#     """
#     If running as a macOS .app bundle:
#     sys.executable -> .../EntrySafe.app/Contents/MacOS/EntrySafe
#     Resources -> .../EntrySafe.app/Contents/Resources
#     """
#     exe_dir = os.path.dirname(os.path.abspath(sys.executable))  # Contents/MacOS
#     contents_dir = os.path.abspath(os.path.join(exe_dir, "..")) # Contents
#     resources_dir = os.path.join(contents_dir, "Resources")
#     return exe_dir, contents_dir, resources_dir

# def app_dir():
#     """
#     Returns where bundled resources (ui/assets) live.
#     - Dev: project root
#     - Frozen macOS: Contents/Resources (preferred), fallback Contents/MacOS
#     """
#     if getattr(sys, "frozen", False):
#         exe_dir, _, resources_dir = _mac_bundle_dirs()
#         if os.path.exists(os.path.join(resources_dir, "ui")):
#             return resources_dir
#         return exe_dir  # fallback
#     return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# def config_path():
#     """
#     Config is editable, so we try EXTERNAL first, then fallback INTERNAL.

#     External search order:
#     1) Folder where the .app sits (recommended: keep release folder intact)
#        e.g. release/config.json beside EntrySafe.app
#     2) ~/Library/Application Support/EntrySafe/config.json (safe place on mac)

#     Internal fallback:
#     - Inside bundled resources (Contents/Resources/config.json)
#     """
#     # DEV mode
#     if not getattr(sys, "frozen", False):
#         p = os.path.join(app_dir(), "config.json")
#         return p

#     exe_dir, _, resources_dir = _mac_bundle_dirs()

#     # 1) beside the .app bundle (parent folder of EntrySafe.app)
#     # exe_dir = .../EntrySafe.app/Contents/MacOS
#     app_bundle = os.path.abspath(os.path.join(exe_dir, "..", ".."))   # .../EntrySafe.app
#     app_parent = os.path.dirname(app_bundle)                          # folder containing EntrySafe.app
#     external1 = os.path.join(app_parent, "config.json")
#     if os.path.exists(external1):
#         return external1

#     # 2) Application Support
#     external2_dir = os.path.join(
#         os.path.expanduser("~"),
#         "Library", "Application Support", APP_NAME
#     )
#     external2 = os.path.join(external2_dir, "config.json")
#     if os.path.exists(external2):
#         return external2

#     # Internal fallback (bundled)
#     internal = os.path.join(resources_dir, "config.json")
#     return internal



# def writable_data_dir():
#     """
#     A folder we can write to on mac/windows.
#     mac: ~/Library/Application Support/EntrySafe
#     """
#     if getattr(sys, "frozen", False) and sys.platform == "darwin":
#         base = os.path.join(
#             os.path.expanduser("~"),
#             "Library", "Application Support", APP_NAME
#         )
#     else:
#         # dev / windows fallback: project folder or beside exe
#         base = app_dir()

#     os.makedirs(base, exist_ok=True)
#     return base

# def uploads_dir():
#     """
#     Where scanned images are saved.
#     """
#     base = writable_data_dir()
#     p = os.path.join(base, "uploads", "guardians")
#     os.makedirs(p, exist_ok=True)
#     return 




import os
import sys

APP_NAME = "EntrySafe"

def _mac_bundle_dirs():
    """
    If running as a macOS .app bundle:
    sys.executable -> .../EntrySafe.app/Contents/MacOS/EntrySafe
    Resources -> .../EntrySafe.app/Contents/Resources
    """
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))          # .../Contents/MacOS
    contents_dir = os.path.abspath(os.path.join(exe_dir, ".."))         # .../Contents
    resources_dir = os.path.join(contents_dir, "Resources")             # .../Contents/Resources
    return exe_dir, contents_dir, resources_dir

def app_dir():
    """
    Where bundled read-only resources (ui/assets) live.
    - Dev: project root
    - Frozen macOS: Contents/Resources (preferred), fallback Contents/MacOS
    """
    if getattr(sys, "frozen", False) and sys.platform == "darwin":
        exe_dir, _, resources_dir = _mac_bundle_dirs()
        if os.path.exists(os.path.join(resources_dir, "ui")):
            return resources_dir
        return exe_dir
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def external_root_dir():
    """
    Folder where EntrySafe.app is located (release folder).
    Example:
      /Applications/EntrySafe-Intel/
        EntrySafe.app
        config.json
        uploads/
    """
    if getattr(sys, "frozen", False) and sys.platform == "darwin":
        exe_dir, _, _ = _mac_bundle_dirs()
        app_bundle = os.path.abspath(os.path.join(exe_dir, "..", ".."))  # .../EntrySafe.app
        return os.path.dirname(app_bundle)                               # folder containing EntrySafe.app
    # Dev: project root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def app_support_dir():
    """
    mac: ~/Library/Application Support/EntrySafe
    """
    base = os.path.join(
        os.path.expanduser("~"),
        "Library", "Application Support", APP_NAME
    )
    os.makedirs(base, exist_ok=True)
    return base

def config_path():
    """
    Config is editable, so we try EXTERNAL first, then Application Support,
    then internal fallback (bundled).
    """
    # Dev mode: use project config.json (if you want)
    if not getattr(sys, "frozen", False):
        return os.path.join(external_root_dir(), "config.json")

    # 1) beside the .app (same folder)
    p1 = os.path.join(external_root_dir(), "config.json")
    if os.path.exists(p1):
        return p1

    # 2) Application Support
    p2 = os.path.join(app_support_dir(), "config.json")
    if os.path.exists(p2):
        return p2

    # 3) Internal fallback (bundled)
    if sys.platform == "darwin":
        _, _, resources_dir = _mac_bundle_dirs()
        return os.path.join(resources_dir, "config.json")

    # fallback
    return os.path.join(app_dir(), "config.json")

def uploads_root_dir():
    """
    Prefer uploads beside the .app (so you can copy old uploads folder into new release).
    If not writable, fallback to Application Support.
    """
    # 1) external beside .app
    external = os.path.join(external_root_dir(), "uploads")
    try:
        os.makedirs(external, exist_ok=True)
        testfile = os.path.join(external, ".write_test")
        with open(testfile, "w") as f:
            f.write("ok")
        os.remove(testfile)
        return external
    except Exception:
        pass

    # 2) fallback Application Support
    fallback = os.path.join(app_support_dir(), "uploads")
    os.makedirs(fallback, exist_ok=True)
    return fallback

def uploads_guardians_dir():
    p = os.path.join(uploads_root_dir(), "guardians")
    os.makedirs(p, exist_ok=True)
    return p

def ensure_runtime_folders():
    """
    Call once at startup.
    """
    uploads_guardians_dir()