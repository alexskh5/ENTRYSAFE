import sys
from PyQt6.QtWidgets import QApplication
from views.login import LoginWindow

def main():
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
