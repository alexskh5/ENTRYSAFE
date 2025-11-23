# # entrysafe/views/login.py  (PyQt6-only, with background image layer)
# import sys
# from os import path
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt

# from controller.LoginController import LoginController
# from views.signup import SignupWindow
# from views.dashboard import DashboardWindow

# # Project paths (assumes this file is entrysafe/views/login.py)
# BASE_DIR = path.dirname(path.abspath(__file__))         # .../entrysafe/views
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))  # .../entrysafe

# UI_FILE = path.join(PROJECT_ROOT, "ui", "login.ui")
# LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
# BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")

# class LoginWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Load UI into QMainWindow
#         uic.loadUi(UI_FILE, self)

#         # --- Background image using QLabel (behind everything) ---
#         cw = self.findChild(QtWidgets.QWidget, "centralwidget")

#         self._bg_label = QtWidgets.QLabel(cw)
#         self._bg_pix = QPixmap(BG_FILE)
#         self._bg_label.setPixmap(self._bg_pix)
#         self._bg_label.setScaledContents(False)

#         # FIXED FOR PYQT6:
#         self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

#         self._bg_label.lower()      # send to back
#         self._bg_label.resize(cw.size())

#         # --- Make rightFrame transparent ---
#         right = self.findChild(QtWidgets.QFrame, "rightFrame")
#         if right:
#             right.setStyleSheet("background: transparent;")
#             right.setAutoFillBackground(False)

#         # --- Make leftFrame transparent ---
#         left = self.findChild(QtWidgets.QFrame, "leftFrame")
#         if left:
#             left.setStyleSheet("background: transparent;")
#             left.setAutoFillBackground(False)


#         # --- Logo Label ---
#         self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
#         self._orig_logo_pix = QPixmap(LOGO_FILE)
#         if self.logo_label and not self._orig_logo_pix.isNull():
#             self.logo_label.setScaledContents(False)
#             self.logo_label.setStyleSheet("background: transparent;")
#             self.logo_label.setPixmap(self._orig_logo_pix)

#         self.setWindowTitle("EntrySafe - Log In")

#         # Logo scaling settings
#         self.MAX_PROP = 0.40
#         self.ABS_MAX_W = 800
#         self.ABS_MIN_W = 120

#     def resizeEvent(self, event):
#         super().resizeEvent(event)

#         # --- Resize background to fill area ---
#         cw = self.findChild(QtWidgets.QWidget, "centralwidget")
#         scaled_bg = self._bg_pix.scaled(
#             cw.size(),
#             Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#             Qt.TransformationMode.SmoothTransformation
#         )
#         self._bg_label.setPixmap(scaled_bg)
#         self._bg_label.resize(cw.size())
#         self._bg_label.move(0, 0)

#         # --- Resize logo ---
#         if not self._orig_logo_pix.isNull() and self.logo_label:
#             target_w = int(self.width() * self.MAX_PROP)
#             target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))

#             scaled_logo = self._orig_logo_pix.scaled(
#                 target_w, target_w,
#                 Qt.AspectRatioMode.KeepAspectRatio,
#                 Qt.TransformationMode.SmoothTransformation
#             )
#             self.logo_label.setPixmap(scaled_logo)


#         self.loginBtn = self.findChild(QtWidgets.QPushButton, "loginBtn")
#         self.createBtn = self.findChild(QtWidgets.QPushButton, "createBtn")

#         self.loginBtn.clicked.connect(self.attempt_login)
#         self.createBtn.clicked.connect(self.open_signup)

#         self.controller = LoginController()
    
#     def attempt_login(self):
#         username = self.userInput.text()
#         password = self.passInput.text()

#         ok, result = self.controller.login(username, password)

#         if ok:
#             self.dashboard = DashboardWindow()
#             self.dashboard.show()
#             self.close()
#         else:
#             QtWidgets.QMessageBox.warning(self, "Login Error", result)

#     def open_signup(self):
#         self.signup = SignupWindow()
#         self.signup.show()
#         self.close()




import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from controller.LoginController import LoginController
# from views.signup import SignupWindow
# from views.dashboard import DashboardWindow

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "login.ui")
LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        # Background
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
            self.logo_label.setStyleSheet("background: transparent;")
            self.logo_label.setPixmap(self._orig_logo_pix)

        # Logo scaling setup
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 800
        self.ABS_MIN_W = 120

        # Buttons — MUST be in __init__
        self.loginBtn = self.findChild(QtWidgets.QPushButton, "loginBtn")
        self.createBtn = self.findChild(QtWidgets.QPushButton, "createBtn")

        self.loginBtn.clicked.connect(self.attempt_login)
        self.createBtn.clicked.connect(self.open_signup)

        # Controller
        self.controller = LoginController()

        self.setWindowTitle("EntrySafe - Login")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

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

    def attempt_login(self):
        username = self.userInput.text()
        password = self.passInput.text()

        from views.temp_dashboard import DashboardWindow
        ok, result = self.controller.login(username, password)

        if ok:
            self.dashboard = DashboardWindow()
            self.dashboard.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Login Error", result)

    def open_signup(self):
        from views.signup import SignupWindow 
        self.signup = SignupWindow()
        self.signup.show()
        self.close()
