# import sys
# from os import path
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt

# from controller.SignUpController import SignupController   # your controller file
# from utils.password_validator import validate_password     # password rules

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "signup.ui")
# LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
# BG_FILE   = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


# class SignupWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Load UI into QMainWindow
#         uic.loadUi(UI_FILE, self)

#         # ---------- STACKED WIDGET NAVIGATION (OLD BEHAVIOR) ----------
#         try:
#             self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
#             self.signUpPage = self.findChild(QtWidgets.QWidget, "signUpPage")
#             self.securityPage = self.findChild(QtWidgets.QWidget, "securityPage")

#             if self.stacked and self.signUpPage:
#                 self.stacked.setCurrentWidget(self.signUpPage)

#             self.nextBtn = self.findChild(QtWidgets.QPushButton, "nextBtn")
#             self.backToLoginBtn = self.findChild(QtWidgets.QPushButton, "backToLoginBtn")
#             self.backToSignupBtn = self.findChild(QtWidgets.QPushButton, "backToSignupBtn")
#             self.signupBtn = self.findChild(QtWidgets.QPushButton, "signupBtn")

#             if self.nextBtn and self.securityPage:
#                 self.nextBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.securityPage)
#                 )
#             if self.backToSignupBtn and self.signUpPage:
#                 self.backToSignupBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.signUpPage)
#                 )
#         except Exception:
#             # if stacked widget or buttons not found, silently ignore
#             pass

#         # ---------- BACKGROUND + FRAMES + LOGO (OLD UI LOOK) ----------
#         cw = self.findChild(QtWidgets.QWidget, "centralwidget")

#         self._bg_label = QtWidgets.QLabel(cw)
#         self._bg_pix = QPixmap(BG_FILE)
#         self._bg_label.setPixmap(self._bg_pix)
#         self._bg_label.setScaledContents(False)
#         self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
#         self._bg_label.lower()
#         self._bg_label.resize(cw.size())

#         right = self.findChild(QtWidgets.QFrame, "rightFrame")
#         if right:
#             right.setStyleSheet("background: transparent; border: none;")
#             right.setAutoFillBackground(False)

#         left = self.findChild(QtWidgets.QFrame, "leftFrame")
#         if left:
#             left.setStyleSheet("background: transparent; border: none;")
#             left.setAutoFillBackground(False)

#         self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
#         self._orig_logo_pix = QPixmap(LOGO_FILE)
#         if self.logo_label and not self._orig_logo_pix.isNull():
#             self.logo_label.setScaledContents(False)
#             self.logo_label.setStyleSheet("background: transparent;")
#             self.logo_label.setPixmap(self._orig_logo_pix)

#         self.setWindowTitle("EntrySafe - Sign Up")

#         # logo scaling settings
#         self.MAX_PROP = 0.40
#         self.ABS_MAX_W = 800
#         self.ABS_MIN_W = 120

#         # ---------- NEW BACKEND FIELDS ----------
#         self.userInput      = self.findChild(QtWidgets.QLineEdit, "userInput")
#         self.passInput      = self.findChild(QtWidgets.QLineEdit, "passInput")
#         self.homepassInput  = self.findChild(QtWidgets.QLineEdit, "homepassInput")

#         self.q1Input   = self.findChild(QtWidgets.QComboBox, "q1Input")
#         self.ans1Input = self.findChild(QtWidgets.QLineEdit, "ans1Input")
#         self.q2Input   = self.findChild(QtWidgets.QComboBox, "q2Input")
#         self.ans2Input = self.findChild(QtWidgets.QLineEdit, "ans2Input")

#         # backToLoginBtn & signupBtn were already found above
#         self.controller = SignupController()

#         if self.signupBtn:
#             self.signupBtn.clicked.connect(self.create_account)
#         if self.backToLoginBtn:
#             self.backToLoginBtn.clicked.connect(self.go_back)

#         # remove duplicate question in q2 when q1 changes
#         if self.q1Input:
#             self.q1Input.currentIndexChanged.connect(self.sync_questions)


#     # ---------- RESIZE BEHAVIOR (OLD) ----------
#     def resizeEvent(self, event):
#         super().resizeEvent(event)

#         cw = self.findChild(QtWidgets.QWidget, "centralwidget")
#         if cw and not self._bg_pix.isNull():
#             scaled_bg = self._bg_pix.scaled(
#                 cw.size(),
#                 Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#                 Qt.TransformationMode.SmoothTransformation
#             )
#             self._bg_label.setPixmap(scaled_bg)
#             self._bg_label.resize(cw.size())
#             self._bg_label.move(0, 0)

#         if not self._orig_logo_pix.isNull() and self.logo_label:
#             target_w = int(self.width() * self.MAX_PROP)
#             target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))

#             scaled_logo = self._orig_logo_pix.scaled(
#                 target_w, target_w,
#                 Qt.AspectRatioMode.KeepAspectRatio,
#                 Qt.TransformationMode.SmoothTransformation
#             )
#             self.logo_label.setPixmap(scaled_logo)

#     # ---------- SECURITY QUESTION LOGIC ----------
#     def sync_questions(self):
#         if not self.q1Input or not self.q2Input:
#             return

#         chosen = self.q1Input.currentText()
#         self.q2Input.clear()

#         all_questions = [
#             "What is your childhood nickname?",
#             "What is the name of your first pet?",
#             "What is the name of your first best friend?",
#             "What city were you born in?",
#             "What was the name of your first school?",
#             "What was the name of your favorite teacher?",
#             "What is your favorite food?",
#             "What is your favorite movie?"
#         ]

#         for q in all_questions:
#             if q != chosen:
#                 self.q2Input.addItem(q)

#     # ---------- SIGNUP BACKEND ----------
#     def create_account(self):
#         username = self.userInput.text().strip() if self.userInput else ""
#         password = self.passInput.text().strip() if self.passInput else ""
#         homepass = self.homepassInput.text().strip() if self.homepassInput else ""

#         q1 = self.q1Input.currentText() if self.q1Input else ""
#         a1 = self.ans1Input.text().strip() if self.ans1Input else ""
#         q2 = self.q2Input.currentText() if self.q2Input else ""
#         a2 = self.ans2Input.text().strip() if self.ans2Input else ""

#         if not username or not password or not a1 or not a2:
#             QtWidgets.QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
#             return

#         ok, msg = validate_password(password)
#         if not ok:
#             QtWidgets.QMessageBox.warning(self, "Invalid Password", msg)
#             return

#         success, message = self.controller.signup(
#             username, password, homepass, q1, a1, q2, a2
#         )

#         if not success:
#             QtWidgets.QMessageBox.warning(self, "Signup Failed", message)
#             return

#         QtWidgets.QMessageBox.information(self, "Success", message)
#         self.go_back()

#     def go_back(self):
#         from views.login import LoginWindow   # import here to avoid circular import
#         self.close()
#         self.login = LoginWindow()
#         self.login.show()


import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from controller.SignUpController import SignupController
from utils.password_validator import validate_password

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "signup.ui")
LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


class SignupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi(UI_FILE, self)

        # ------------ STACKED WIDGET (Next ↔ Back pages) ------------
        try:
            self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
            self.signUpPage = self.findChild(QtWidgets.QWidget, "signUpPage")
            self.securityPage = self.findChild(QtWidgets.QWidget, "securityPage")

            if self.stacked and self.signUpPage:
                self.stacked.setCurrentWidget(self.signUpPage)

            self.nextBtn = self.findChild(QtWidgets.QPushButton, "nextBtn")
            self.backToSignupBtn = self.findChild(QtWidgets.QPushButton, "backToSignupBtn")
            self.backToLoginBtn = self.findChild(QtWidgets.QPushButton, "backToLoginBtn")
            self.signupBtn = self.findChild(QtWidgets.QPushButton, "signupBtn")

            if self.nextBtn and self.securityPage:
                self.nextBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.securityPage))

            if self.backToSignupBtn and self.signUpPage:
                self.backToSignupBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.signUpPage))

        except Exception:
            pass  # ignore if no stacked widget


        # ------------ BACKGROUND + TRANSPARENCY + LOGO (OLD UI LOOK) ------------
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        right = self.findChild(QtWidgets.QFrame, "rightFrame")
        if right:
            right.setStyleSheet("background: transparent; border: none;")
            right.setAutoFillBackground(False)

        left = self.findChild(QtWidgets.QFrame, "leftFrame")
        if left:
            left.setStyleSheet("background: transparent; border: none;")
            left.setAutoFillBackground(False)

        self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
        self._orig_logo_pix = QPixmap(LOGO_FILE)
        if self.logo_label and not self._orig_logo_pix.isNull():
            self.logo_label.setScaledContents(False)
            self.logo_label.setStyleSheet("background: transparent;")
            self.logo_label.setPixmap(self._orig_logo_pix)

        self.setWindowTitle("EntrySafe - Sign Up")

        # Logo scaling limits
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 800
        self.ABS_MIN_W = 120


        # ------------ FIELD CONNECTIONS (NEW BACKEND) ------------
        self.userInput      = self.findChild(QtWidgets.QLineEdit, "userInput")
        self.passInput      = self.findChild(QtWidgets.QLineEdit, "passInput")
        self.homepassInput  = self.findChild(QtWidgets.QLineEdit, "homepassInput")

        self.q1Input        = self.findChild(QtWidgets.QComboBox, "q1Input")
        self.ans1Input      = self.findChild(QtWidgets.QLineEdit, "ans1Input")
        self.q2Input        = self.findChild(QtWidgets.QComboBox, "q2Input")
        self.ans2Input      = self.findChild(QtWidgets.QLineEdit, "ans2Input")

        self.controller = SignupController()

        if self.signupBtn:
            self.signupBtn.clicked.connect(self.create_account)
        if self.backToLoginBtn:
            self.backToLoginBtn.clicked.connect(self.go_back)

        # Connect question filtering
        if self.q1Input:
            self.q1Input.currentIndexChanged.connect(self.sync_questions)

        # Initialize q2 properly
        self.sync_questions()


    # ------------ RESIZE EVENT FOR PROPER SCALING ------------
    def resizeEvent(self, event):
        super().resizeEvent(event)

        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        if cw and not self._bg_pix.isNull():
            scaled_bg = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._bg_label.setPixmap(scaled_bg)
            self._bg_label.resize(cw.size())
            self._bg_label.move(0, 0)

        if not self._orig_logo_pix.isNull() and self.logo_label:
            target_w = int(self.width() * self.MAX_PROP)
            target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))

            scaled_logo = self._orig_logo_pix.scaled(
                target_w, target_w,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)


    # ------------ FIXED QUESTION FILTERING (NO DUPLICATES EVER) ------------
    def sync_questions(self):
        if not self.q1Input or not self.q2Input:
            return

        chosen = self.q1Input.currentText().strip().lower()

        all_questions = [
            "What is your childhood nickname?",
            "What is the name of your first pet?",
            "What is the name of your first best friend?",
            "What city were you born in?",
            "What was the name of your first school?",
            "What was the name of your favorite teacher?",
            "What is your favorite food?",
            "What is your favorite movie?"
        ]

        self.q2Input.clear()

        for q in all_questions:
            if q.strip().lower() != chosen:
                self.q2Input.addItem(q)

        if self.q2Input.count() > 0:
            self.q2Input.setCurrentIndex(0)


    # ------------ CREATE ACCOUNT (BACKEND) ------------
    def create_account(self):
        username = self.userInput.text().strip() if self.userInput else ""
        password = self.passInput.text().strip() if self.passInput else ""
        homepass = self.homepassInput.text().strip() if self.homepassInput else ""

        q1 = self.q1Input.currentText() if self.q1Input else ""
        a1 = self.ans1Input.text().strip() if self.ans1Input else ""
        q2 = self.q2Input.currentText() if self.q2Input else ""
        a2 = self.ans2Input.text().strip() if self.ans2Input else ""

        if not username or not password or not a1 or not a2:
            QtWidgets.QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
            return

        ok, msg = validate_password(password)
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Invalid Password", msg)
            return

        success, message = self.controller.signup(
            username, password, homepass, q1, a1, q2, a2
        )

        if not success:
            QtWidgets.QMessageBox.warning(self, "Signup Failed", message)
            return

        QtWidgets.QMessageBox.information(self, "Success", message)
        self.go_back()


    # ------------ GO BACK TO LOGIN (AVOID CIRCULAR IMPORT) ------------
    def go_back(self):
        from views.login import LoginWindow
        self.close()
        self.login = LoginWindow()
        self.login.show()
