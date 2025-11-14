# entrysafe/views/login.py  (PyQt6-only, with background image layer)
import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Project paths (assumes this file is entrysafe/views/login.py)
BASE_DIR = path.dirname(path.abspath(__file__))         # .../entrysafe/views
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))  # .../entrysafe

UI_FILE = path.join(PROJECT_ROOT, "ui", "login.ui")
LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI into QMainWindow
        uic.loadUi(UI_FILE, self)

        # --- Background image using QLabel (behind everything) ---
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)

        # FIXED FOR PYQT6:
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self._bg_label.lower()      # send to back
        self._bg_label.resize(cw.size())

        # --- Make rightFrame transparent ---
        right = self.findChild(QtWidgets.QFrame, "rightFrame")
        if right:
            right.setStyleSheet("background: transparent;")
            right.setAutoFillBackground(False)

        # --- Make leftFrame transparent ---
        left = self.findChild(QtWidgets.QFrame, "leftFrame")
        if left:
            left.setStyleSheet("background: transparent;")
            left.setAutoFillBackground(False)


        # --- Logo Label ---
        self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
        self._orig_logo_pix = QPixmap(LOGO_FILE)
        if self.logo_label and not self._orig_logo_pix.isNull():
            self.logo_label.setScaledContents(False)
            self.logo_label.setStyleSheet("background: transparent;")
            self.logo_label.setPixmap(self._orig_logo_pix)

        self.setWindowTitle("EntrySafe - Login")

        # Logo scaling settings
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 800
        self.ABS_MIN_W = 120

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # --- Resize background to fill area ---
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        scaled_bg = self._bg_pix.scaled(
            cw.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self._bg_label.setPixmap(scaled_bg)
        self._bg_label.resize(cw.size())
        self._bg_label.move(0, 0)

        # --- Resize logo ---
        if not self._orig_logo_pix.isNull() and self.logo_label:
            target_w = int(self.width() * self.MAX_PROP)
            target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))

            scaled_logo = self._orig_logo_pix.scaled(
                target_w, target_w,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
