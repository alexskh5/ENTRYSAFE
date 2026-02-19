import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.paths import app_dir
from PyQt6.QtWidgets import QApplication
from views.landing import LandingWindow


def main():
    app = QApplication(sys.argv)
    base = app_dir()
    os.makedirs(os.path.join(base, "uploads"), exist_ok=True)

    win = LandingWindow()   # first screen
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
