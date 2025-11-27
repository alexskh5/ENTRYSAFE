import sys
from PyQt6.QtWidgets import QApplication
from views.landing import LandingWindow

def main():
    app = QApplication(sys.argv)
    win = LandingWindow()   # first screen
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
