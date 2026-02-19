import sys
# from os import path
from PyQt6 import QtWidgets, uic, QtGui, QtCore

from controller.HomePassController import HomePassController
from controller.ForgotPasswordController import ForgotPasswordController

import os
from utils.paths import app_dir

BASE = app_dir()
UI_FILE = os.path.join(BASE, "ui", "mode.ui")

# eye icons
EYE_ON = os.path.join(BASE, "assets", "icons", "eye.svg")
EYE_OFF = os.path.join(BASE, "assets", "icons", "eye-off.svg")

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
# UI_FILE = path.join(PROJECT_ROOT, "ui", "mode.ui")

# # eye icons
# EYE_ON = path.join(PROJECT_ROOT, "assets", "icons", "eye.svg")
# EYE_OFF = path.join(PROJECT_ROOT, "assets", "icons", "eye-off.svg")

class ChooseModeWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username

        uic.loadUi(UI_FILE, self)
        
        
        self.resize(1250, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())

        # ============= CONTROLLERS =============
        self.home_ctrl = HomePassController()
        self.forgot_ctrl = ForgotPasswordController()

        # ============= UI WIDGETS =============
        self.gateFrame = self.findChild(QtWidgets.QFrame, "gateFrame")
        self.homeFrame = self.findChild(QtWidgets.QFrame, "homeFrame")
        self.homeTopFrame = self.findChild(QtWidgets.QFrame, "frame_5")
        self.homeExtraFrame = self.findChild(QtWidgets.QFrame, "frame_4")

        self.gateBtn = self.findChild(QtWidgets.QPushButton, "gateBtn")
        self.gateIconBtn = self.findChild(QtWidgets.QPushButton, "gateIconBtn")

        self.homeBtn = self.findChild(QtWidgets.QPushButton, "homeBtn")
        self.homeIconBtn = self.findChild(QtWidgets.QPushButton, "homeIconBtn")

        self.exitBtn = self.findChild(QtWidgets.QPushButton, "exitBtn")
        self.backBtn = self.findChild(QtWidgets.QPushButton, "backBtn")

        self.homePassInput = self.findChild(QtWidgets.QLineEdit, "homePassInput")
        self.forgotPassBtn = self.findChild(QtWidgets.QPushButton, "forgotPassBtn")
        
        # ============= PASSWORD TOGGLE SETUP =============
        if self.homePassInput and self.toggleHomePassBtn:
            self.homePassInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.toggleHomePassBtn.setIcon(QtGui.QIcon(EYE_OFF))
            self.toggleHomePassBtn.setFlat(True)
            self.toggleHomePassBtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            self.toggleHomePassBtn.clicked.connect(self.toggle_home_pass)

        # ============= STATES =============
        self.home_expanded = False

        # Start frames at 400px height
        for frame in (self.gateFrame, self.homeFrame):
            if frame:
                frame.setMinimumHeight(400)
                frame.setMaximumHeight(400)

        # ================= SIGNALS =================
        # HOME expand
        if self.homeBtn:
            self.homeBtn.clicked.connect(self.expand_home_card)

        if self.homeIconBtn:
            self.homeIconBtn.clicked.connect(self.expand_home_card)

        # HOME collapse
        if self.exitBtn:
            self.exitBtn.clicked.connect(self.collapse_home_card)

        self.backBtn.clicked.connect(self._on_back)


        # HOME PASS ENTER
        if self.homePassInput:
            self.homePassInput.returnPressed.connect(self._on_enter_home)

        # FORGOT PASS FLOW
        if self.forgotPassBtn:
            self.forgotPassBtn.clicked.connect(self._on_forgot_pass)

        # GATE MODE
        if self.gateBtn:
            self.gateBtn.clicked.connect(self._on_gate)

        if self.gateIconBtn:
            self.gateIconBtn.clicked.connect(self._on_gate)

        # Start collapsed
        self.collapse_home_card()

    # ------------------------------------------------------
    # SHOW / HIDE HOME PASS
    # ------------------------------------------------------
    def toggle_home_pass(self):
        if self.homePassInput.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.homePassInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.toggleHomePassBtn.setIcon(QtGui.QIcon(EYE_ON))
        else:
            self.homePassInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.toggleHomePassBtn.setIcon(QtGui.QIcon(EYE_OFF))

    # ------------------------------------------------------
    # HOME CARD SIZES
    # ------------------------------------------------------
    def set_home_expanded(self, expanded: bool):
        """Show/hide home pass input + forgot pass."""
        self.home_expanded = expanded

        if self.homeExtraFrame:
            self.homeExtraFrame.setVisible(expanded)

        if self.exitBtn:
            self.exitBtn.setVisible(expanded)

        if self.homeFrame:
            if expanded:
                self.homeFrame.setMinimumHeight(400)
                self.homeFrame.setMaximumHeight(9999)
            else:
                self.homeFrame.setMinimumHeight(400)
                self.homeFrame.setMaximumHeight(400)

        # gate stays constant
        if self.gateFrame:
            self.gateFrame.setMinimumHeight(400)
            self.gateFrame.setMaximumHeight(400)

    def expand_home_card(self):
        self.set_home_expanded(True)

    def collapse_home_card(self):
        self.set_home_expanded(False)

    # ------------------------------------------------------
    # HOME PASS LOGIC
    # ------------------------------------------------------
    def _on_enter_home(self):
        """Enter key in homePassInput → validate → dashboard."""
        if not self.homePassInput:
            return

        pass_text = self.homePassInput.text().strip()

        if pass_text == "":
            QtWidgets.QMessageBox.warning(self, "Missing", "Enter a home pass.")
            return

        if not self.home_ctrl.validate_home_pass(self.username, pass_text):
            QtWidgets.QMessageBox.warning(self, "Invalid", "Incorrect home pass.")
            return

        # SUCCESS → Open dashboard
        try:
            from views.dashboard import AdminWindow
            self.dash = AdminWindow(self.username)
            self.dash.show()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to open dashboard:\n{e}")
            return

        self.homePassInput.clear()
        self.collapse_home_card()

    # ------------------------------------------------------
    # FORGOT PASS LOGIC
    # ------------------------------------------------------
    def _on_forgot_pass(self):
        # 1. get questions
        ok, data = self.forgot_ctrl.get_questions(self.username)
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Error", data)
            return

        q1, q2 = data["q1"], data["q2"]

        # 2. ask answers
        a1, ok = QtWidgets.QInputDialog.getText(self, "Security Check", q1)
        if not ok:
            return
        a2, ok = QtWidgets.QInputDialog.getText(self, "Security Check", q2)
        if not ok:
            return

        # 3. verify
        valid, _ = self.forgot_ctrl.verify_answers(self.username, a1, a2)
        if not valid:
            QtWidgets.QMessageBox.warning(self, "Error", "Incorrect answers.")
            return

        # 4. ask new homepass
        new_hp, ok = QtWidgets.QInputDialog.getText(self, "New Home Pass", "Enter new 5-digit home pass:")
        if not ok:
            return

        new_hp = new_hp.strip()

        # VALIDATION RULES (merged with profile)
        if not new_hp.isdigit() or len(new_hp) != 5:
            QtWidgets.QMessageBox.warning(self, "Error", "Home pass must be exactly 5 digits.")
            return

        # 5. disallow same as current homepass
        # (validate_home_pass is true if same)
        if self.home_ctrl.validate_home_pass(self.username, new_hp):
            QtWidgets.QMessageBox.warning(self, "Error", "New home pass cannot match the current one.")
            return

        # 6. update using SECURITY METHOD
        ok, msg = self.home_ctrl.change_homepass_with_security(self.username, new_hp)

        if not ok:
            QtWidgets.QMessageBox.warning(self, "Error", msg)
            return

        QtWidgets.QMessageBox.information(self, "Success", "Home pass updated successfully.")

    # ------------------------------------------------------
    # GATE MODE LOGIC
    # ------------------------------------------------------
    def _on_gate(self):
        """Same logic as old choose_mode: open scan window."""
        try:
            from views.scan import ScanWindow
            self.scan = ScanWindow(self.username)
            self.scan.show()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to open Gate view:\n{e}")

    def _on_back(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit and return to the login page?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            from views.login import LoginWindow
            self.login = LoginWindow()
            self.login.show()
            self.close()

    