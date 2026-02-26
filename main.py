# import os, sys
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# from utils.paths import app_dir
# from PyQt6.QtWidgets import QApplication
# from views.landing import LandingWindow


# def main():
#     app = QApplication(sys.argv)
#     base = app_dir()
#     os.makedirs(os.path.join(base, "uploads"), exist_ok=True)

#     win = LandingWindow()   # first screen
#     win.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()


import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMessageBox
from utils.paths import app_dir
from views.landing import LandingWindow

def check_required_files():
    base = app_dir()
    required_paths = [
        os.path.join(base, "ui"),
        os.path.join(base, "assets"),
        os.path.join(base, "config.json"),
    ]

    missing = [p for p in required_paths if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(
            "Missing required files/folders:\n\n" + "\n".join(missing) +
            f"\n\nApp folder detected as:\n{base}"
        )

def main():
    app = QApplication(sys.argv)

    try:
        check_required_files()
    except Exception as e:
        QMessageBox.critical(None, "EntrySafe Startup Error", str(e))
        sys.exit(1)

    win = LandingWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()