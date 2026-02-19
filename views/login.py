import sys
# from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from controller.LoginController import LoginController
import os
from utils.paths import app_dir



BASE = app_dir()

UI_FILE   = os.path.join(BASE, "ui", "login.ui")
LOGO_FILE = os.path.join(BASE, "assets", "images", "appLogo.png")
BG_FILE   = os.path.join(BASE, "assets", "images", "bg1.png")

# eye icons
EYE_ON  = os.path.join(BASE, "assets", "icons", "eye.svg")
EYE_OFF = os.path.join(BASE, "assets", "icons", "eye-off.svg")
# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "login.ui")
# LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
# BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")

# # eye icons
# EYE_ON = path.join(PROJECT_ROOT, "assets", "icons", "eye.svg")
# EYE_OFF = path.join(PROJECT_ROOT, "assets", "icons", "eye-off.svg")

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi(UI_FILE, self)
        
        self.resize(1250, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())

        # Background setup
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # Frames transparency
        right = self.findChild(QtWidgets.QFrame, "rightFrame")
        if right:
            right.setStyleSheet("background: transparent; border: none;")
            right.setAutoFillBackground(False)

        left = self.findChild(QtWidgets.QFrame, "leftFrame")
        if left:
            left.setStyleSheet("background: transparent; border: none;")
            left.setAutoFillBackground(False)

        # Logo
        self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
        self._orig_logo_pix = QPixmap(LOGO_FILE)
        if self.logo_label and not self._orig_logo_pix.isNull():
            self.logo_label.setStyleSheet("background: transparent;")
            self.logo_label.setPixmap(self._orig_logo_pix)

        # Inputs & Buttons
        self.userInput = self.findChild(QtWidgets.QLineEdit, "userInput")
        self.passInput = self.findChild(QtWidgets.QLineEdit, "passInput")
        self.loginBtn = self.findChild(QtWidgets.QPushButton, "loginBtn")
        self.createBtn = self.findChild(QtWidgets.QPushButton, "createBtn")
        self.forgotBtn = self.findChild(QtWidgets.QPushButton, "forgotBtn")

        self.controller = LoginController()

        # ----- PASSWORD TOGGLE SETUP -----
        self.passInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.togglePassBtn.setIcon(QIcon(EYE_OFF))
        self.togglePassBtn.setFlat(True)
        self.togglePassBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.togglePassBtn.clicked.connect(self.toggle_password)

        # Button Actions
        self.loginBtn.clicked.connect(self.handle_login)
        self.createBtn.clicked.connect(self.go_signup)
        self.forgotBtn.clicked.connect(self.go_forgot)

        # Logo scaling limits
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 800
        self.ABS_MIN_W = 120

    # ---------- SHOW / HIDE PASSWORD ----------
    def toggle_password(self):
        if self.passInput.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.passInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.togglePassBtn.setIcon(QIcon(EYE_ON))
        else:
            self.passInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.togglePassBtn.setIcon(QIcon(EYE_OFF))

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

        # Scale logo
        if not self._orig_logo_pix.isNull() and self.logo_label:
            target_w = int(self.width() * self.MAX_PROP)
            target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))

            scaled_logo = self._orig_logo_pix.scaled(
                target_w, target_w,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)


    def handle_login(self):
        username = self.userInput.text().strip()
        password = self.passInput.text().strip()

        ok, data = self.controller.login(username, password)

        if ok:
            from views.mode import ChooseModeWindow
            self.close()
            self.mode = ChooseModeWindow(username=username)
            self.mode.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", data)


    def go_signup(self):
        from views.signup import SignupWindow
        self.close()
        self.signup = SignupWindow()
        self.signup.show()


    def go_forgot(self):
        from controller.ForgotPasswordController import ForgotPasswordController
        ctrl = ForgotPasswordController()

        # username popup
        username, ok = QtWidgets.QInputDialog.getText(self, "Forgot Password", "Enter username:")
        if not ok or username.strip() == "":
            return

        # get security questions
        success, data = ctrl.get_questions(username)
        if not success:
            QtWidgets.QMessageBox.warning(self, "Error", data)
            return

        q1, q2 = data["q1"], data["q2"]

        # answer popup 1
        a1, ok = QtWidgets.QInputDialog.getText(self, "Security Question 1", q1)
        if not ok:
            return

        # answer popup 2
        a2, ok = QtWidgets.QInputDialog.getText(self, "Security Question 2", q2)
        if not ok:
            return

        # verify answers
        valid, msg = ctrl.verify_answers(username, a1, a2)
        if not valid:
            QtWidgets.QMessageBox.warning(self, "Error", msg)
            return

        # new password popup
        new_pass, ok = QtWidgets.QInputDialog.getText(self, "Reset Password", "Enter new password:")
        if not ok or new_pass.strip() == "":
            return

        from utils.password_validator import validate_password
        ok_pass, pass_msg = validate_password(new_pass)
        if not ok_pass:
            QtWidgets.QMessageBox.warning(self, "Invalid Password", pass_msg)
            return

        # update password
        success, msg = ctrl.update_password(username, new_pass)
        if not success:
            QtWidgets.QMessageBox.warning(self, "Error", msg)
            return

        QtWidgets.QMessageBox.information(self, "Success", "Password reset successfully!")
