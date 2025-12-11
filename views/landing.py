# entrysafe/views/landing.py
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

BASE_DIR = path.dirname(path.abspath(__file__))
UI_FILE = path.join(PROJECT_ROOT, "ui", "landing.ui")

LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")    # replace if different
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "landing bg.png")  # your provided bg

class LandingWindow(QtWidgets.QMainWindow):
    """
    Splash / Landing screen:
    shows background image, logo, tagline, footer then transitions to LoginWindow.
    """
    def __init__(self, auto_next=True, delay_ms=3500):
        super().__init__()
        uic.loadUi(UI_FILE, self)

        
        self.resize(1250, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())
        
        
        # central widget & background pattern same as other views
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        # background label
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        if not self._bg_pix.isNull():
            self._bg_label.setPixmap(self._bg_pix)
            self._bg_label.setScaledContents(False)
        # allow clicks to pass through
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # logo label (will be scaled in resizeEvent to match app pattern)
        self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
        self._orig_logo_pix = QPixmap(LOGO_FILE)

        # title/subtitle/footer are set in the UI; we only ensure transparent backgrounds
        for name in ("logoLabel", "taglineLabel", "footerLabel"):
            lbl = self.findChild(QtWidgets.QLabel, name)
            if lbl:
                lbl.setStyleSheet("background: transparent;")

        self.setWindowTitle("EntrySafe")

        # scaling settings (copy pattern from other views)
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 900
        self.ABS_MIN_W = 120

        # auto transition
        self._timer = None
        if auto_next:
            self._timer = QTimer(self)
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._go_to_login)
            self._timer.start(delay_ms)

    def _go_to_login(self):
        # Import here to avoid circular imports at module load time
        try:
            from views.login import LoginWindow
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Import Error",
                f"Failed to import LoginWindow:\n\n{str(e)}"
            )
            return

        try:
            self.login_win = LoginWindow()
            self.login_win.show()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "LoginWindow Error",
                f"Failed to create LoginWindow:\n\n{str(e)}"
            )
            return

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # resize background to cover central widget
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        if getattr(self, "_bg_pix", None) and not self._bg_pix.isNull():
            scaled_bg = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._bg_label.setPixmap(scaled_bg)
            self._bg_label.resize(cw.size())
            self._bg_label.move(0, 0)

        # scale logo similarly to other views
        if getattr(self, "_orig_logo_pix", None) and self.logo_label:
            target_w = int(self.width() * self.MAX_PROP)
            target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))
            scaled_logo = self._orig_logo_pix.scaled(
                target_w, target_w,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)

