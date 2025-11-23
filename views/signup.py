import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


from controller.SignUpController import SignupController
# from views.login import LoginWindow
# from views.dashboard import DashboardWindow

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))




UI_FILE = path.join(PROJECT_ROOT, "ui", "signup.ui")
LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")

class SignupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        # --- Background ---
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # Transparent frames
        for frame_name in ["rightFrame", "leftFrame"]:
            frame = self.findChild(QtWidgets.QFrame, frame_name)
            if frame:
                frame.setStyleSheet("background: transparent;")
                frame.setAutoFillBackground(False)

        # Logo
        self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
        self._orig_logo_pix = QPixmap(LOGO_FILE)
        if self.logo_label and not self._orig_logo_pix.isNull():
            self.logo_label.setScaledContents(False)
            self.logo_label.setStyleSheet("background: transparent;")
            self.logo_label.setPixmap(self._orig_logo_pix)

        # Logo scaling limits
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 800
        self.ABS_MIN_W = 120

        # Buttons — MUST be initialized here
        self.signupBtn = self.findChild(QtWidgets.QPushButton, "signupBtn")
        self.backBtn = self.findChild(QtWidgets.QPushButton, "backBtn")

        self.signupBtn.clicked.connect(self.attempt_signup)
        self.backBtn.clicked.connect(self.go_back)

        # Controller
        self.controller = SignupController()

        self.setWindowTitle("EntrySafe - Sign Up")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        # Resize background
        scaled_bg = self._bg_pix.scaled(
            cw.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self._bg_label.setPixmap(scaled_bg)
        self._bg_label.resize(cw.size())

        # Resize logo
        if not self._orig_logo_pix.isNull() and self.logo_label:
            target_w = int(self.width() * self.MAX_PROP)
            target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))

            scaled_logo = self._orig_logo_pix.scaled(
                target_w,
                target_w,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)

    def attempt_signup(self):
        username = self.userInput.text()
        password = self.passInput.text()
        homepass = self.homepassInput.text()

        from views.temp_dashboard import DashboardWindow 
        ok, msg = self.controller.signup(username, password, homepass)

        if ok:
            self.dashboard = DashboardWindow()
            self.dashboard.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Signup Error", msg)

    def go_back(self):
        from views.login import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()
