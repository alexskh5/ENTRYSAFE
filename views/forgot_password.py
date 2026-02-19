# import sys
# from os import path
# from PyQt6 import QtWidgets, uic
# from controller.ForgotPasswordController import ForgotPasswordController
# from utils.password_validator import validate_password
# from views.login import LoginWindow

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "forgot_password.ui")


# class ForgotPasswordWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi(UI_FILE, self)

#         self.ctrl = ForgotPasswordController()

#         # Labels & inputs
#         self.q1Label = self.findChild(QtWidgets.QLabel, "q1Label")
#         self.q2Label = self.findChild(QtWidgets.QLabel, "q2Label")
#         self.ans1Input = self.findChild(QtWidgets.QLineEdit, "ans1Input")
#         self.ans2Input = self.findChild(QtWidgets.QLineEdit, "ans2Input")

#         self.submitBtn = self.findChild(QtWidgets.QPushButton, "submitBtn")

#         # Password reset section
#         self.newPassInput = self.findChild(QtWidgets.QLineEdit, "newPassInput")
#         self.confirmPassInput = self.findChild(QtWidgets.QLineEdit, "confirmPassInput")
#         self.updateBtn = self.findChild(QtWidgets.QPushButton, "updateBtn")
#         self.resetFrame = self.findChild(QtWidgets.QFrame, "resetFrame")

#         self.resetFrame.hide()

#         # Load questions
#         questions = self.ctrl.get_questions()
#         if questions:
#             self.q1Label.setText(questions[0])
#             self.q2Label.setText(questions[1])

#         # Connect buttons
#         self.submitBtn.clicked.connect(self.verify_answers)
#         self.updateBtn.clicked.connect(self.update_password)


#     def verify_answers(self):
#         a1 = self.ans1Input.text().strip()
#         a2 = self.ans2Input.text().strip()

#         if not a1 or not a2:
#             QtWidgets.QMessageBox.warning(self, "Missing", "Please answer both questions.")
#             return

#         if not self.ctrl.verify_answers(a1, a2):
#             QtWidgets.QMessageBox.warning(self, "Incorrect", "Your answers do not match.")
#             return

#         # correct → show new password fields
#         self.resetFrame.show()


#     def update_password(self):
#         new = self.newPassInput.text().strip()
#         conf = self.confirmPassInput.text().strip()

#         ok, msg = validate_password(new)
#         if not ok:
#             QtWidgets.QMessageBox.warning(self, "Invalid Password", msg)
#             return

#         if new != conf:
#             QtWidgets.QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
#             return

#         success, msg = self.ctrl.update_password(self.username, new)

#         if success:
#             QtWidgets.QMessageBox.information(self, "Success", msg)
#             self.go_login()
#         else:
#             QtWidgets.QMessageBox.warning(self, "Error", msg)

#     def go_login(self):
#         from views.login import LoginWindow
#         self.close()
#         self.l = LoginWindow()
#         self.l.show()

import os
from PyQt6 import QtWidgets, uic

from controller.ForgotPasswordController import ForgotPasswordController
from utils.password_validator import validate_password
from utils.paths import app_dir


BASE = app_dir()
UI_FILE = os.path.join(BASE, "ui", "forgot_password.ui")


class ForgotPasswordWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)

        self.ctrl = ForgotPasswordController()
        self.username = None  # will be set after asking user

        # Labels & inputs
        self.q1Label = self.findChild(QtWidgets.QLabel, "q1Label")
        self.q2Label = self.findChild(QtWidgets.QLabel, "q2Label")
        self.ans1Input = self.findChild(QtWidgets.QLineEdit, "ans1Input")
        self.ans2Input = self.findChild(QtWidgets.QLineEdit, "ans2Input")

        self.submitBtn = self.findChild(QtWidgets.QPushButton, "submitBtn")

        # Password reset section
        self.newPassInput = self.findChild(QtWidgets.QLineEdit, "newPassInput")
        self.confirmPassInput = self.findChild(QtWidgets.QLineEdit, "confirmPassInput")
        self.updateBtn = self.findChild(QtWidgets.QPushButton, "updateBtn")
        self.resetFrame = self.findChild(QtWidgets.QFrame, "resetFrame")

        if self.resetFrame:
            self.resetFrame.hide()

        # Connect buttons
        if self.submitBtn:
            self.submitBtn.clicked.connect(self.verify_answers)

        if self.updateBtn:
            self.updateBtn.clicked.connect(self.update_password)

        # ✅ Load questions (ask username first)
        self.load_questions()

    def load_questions(self):
        username, ok = QtWidgets.QInputDialog.getText(
            self, "Forgot Password", "Enter username:"
        )
        if not ok or not username.strip():
            self.go_login()
            return

        self.username = username.strip()

        ok, data = self.ctrl.get_questions(self.username)
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Error", data)
            self.go_login()
            return

        # expected dict: {"q1": "...", "q2": "..."}
        self.q1Label.setText(data["q1"])
        self.q2Label.setText(data["q2"])

    def verify_answers(self):
        if not self.username:
            QtWidgets.QMessageBox.warning(self, "Error", "No username set.")
            return

        a1 = self.ans1Input.text().strip() if self.ans1Input else ""
        a2 = self.ans2Input.text().strip() if self.ans2Input else ""

        if not a1 or not a2:
            QtWidgets.QMessageBox.warning(self, "Missing", "Please answer both questions.")
            return

        valid, msg = self.ctrl.verify_answers(self.username, a1, a2)
        if not valid:
            QtWidgets.QMessageBox.warning(self, "Incorrect", msg or "Your answers do not match.")
            return

        # correct → show new password fields
        if self.resetFrame:
            self.resetFrame.show()

    def update_password(self):
        if not self.username:
            QtWidgets.QMessageBox.warning(self, "Error", "No username set.")
            return

        new = self.newPassInput.text().strip() if self.newPassInput else ""
        conf = self.confirmPassInput.text().strip() if self.confirmPassInput else ""

        ok, msg = validate_password(new)
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Invalid Password", msg)
            return

        if new != conf:
            QtWidgets.QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return

        success, msg = self.ctrl.update_password(self.username, new)

        if success:
            QtWidgets.QMessageBox.information(self, "Success", msg)
            self.go_login()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", msg)

    def go_login(self):
        from views.login import LoginWindow
        self.close()
        self.l = LoginWindow()
        self.l.show()
