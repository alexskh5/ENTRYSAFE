# # entrysafe/views/choose_mode.py 

# import sys # Needed for sys.exit() and sys.argv
# from os import path 
# from PyQt6 import QtWidgets, uic, QtGui, QtCore 

# BASE_DIR = path.dirname(path.abspath(__file__))         # .../entrysafe/views 
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))  # .../entrysafe 

# UI_FILE = path.join(PROJECT_ROOT, "ui", "choose_mode.ui")
# GATE_ICON = path.join(PROJECT_ROOT, "assets", "images", "gate.png")
# HOME_ICON = path.join(PROJECT_ROOT, "assets", "images", "home.png")

# class ChooseModeWindow(QtWidgets.QWidget):
#     """
#     Mode selector widget. Emits mode_selected(mode, payload) on selection.
#     mode: 'gate' or 'home'
#     payload: dict (e.g. {'home_pass': 'abcd'})
#     """
#     mode_selected = QtCore.pyqtSignal(str, dict)

#     def __init__(self):
#         super().__init__()
        
#         # --- UI Loading ---
#         if not path.exists(UI_FILE):
#              print(f"FATAL ERROR: UI file not found at {UI_FILE}")
#              # If the UI file is missing, we stop initialization here.
#              return
#         else:
#             uic.loadUi(UI_FILE, self)

#         # find widgets (names must match UI)
#         self.gateBtn = self.findChild(QtWidgets.QPushButton, "gateBtn")
#         self.homePassInput = self.findChild(QtWidgets.QLineEdit, "homePassInput")
#         self.gateIcon = self.findChild(QtWidgets.QLabel, "gateIcon")
#         self.homeIcon = self.findChild(QtWidgets.QLabel, "homeIcon")
#         self.homeCard = self.findChild(QtWidgets.QFrame, "homeCard")
#         self.homeExpandFrame = self.findChild(QtWidgets.QFrame, "homeExpandFrame")
#         self.closeHomeBtn = self.findChild(QtWidgets.QPushButton, "closeHomeBtn") 
#         self.forgotPassBtn = self.findChild(QtWidgets.QPushButton, "forgotPassBtn")


#         # --- Defensive Checks ---
#         if not all([self.gateBtn, self.homePassInput, self.homeExpandFrame, self.homeCard, self.closeHomeBtn]):
#             print("WARNING: choose_mode UI missing crucial widgets. Check objectNames in UI file.")
#             # We can't proceed if essential widgets for interaction/animation are missing
#             return
#         if not all([self.gateBtn, self.homePassInput, self.homeExpandFrame,
#             self.homeCard, self.closeHomeBtn, self.forgotPassBtn]):
#             return

#         # --- Icon Setup ---
#         # Define the desired icon size (Updated from 160 to 200 pixels)
#         ICON_SIZE = 200 

#         if path.exists(GATE_ICON) and self.gateIcon:
#             pix = QtGui.QPixmap(GATE_ICON)
#             if not pix.isNull():
#                 self.gateIcon.setPixmap(pix.scaled(ICON_SIZE, ICON_SIZE, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
#         if path.exists(HOME_ICON) and self.homeIcon:
#             pix = QtGui.QPixmap(HOME_ICON)
#             if not pix.isNull():
#                 self.homeIcon.setPixmap(pix.scaled(ICON_SIZE, ICON_SIZE, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

#         # --- Connections ---
#         self.gateBtn.clicked.connect(self._on_gate)
#         self.homePassInput.returnPressed.connect(self._on_enter_home)
#         self.forgotPassBtn.clicked.connect(self._on_forgot_pass)
#         self.closeHomeBtn.clicked.connect(self._collapse_home_area) 
#         self.homeCard.mousePressEvent = self._home_card_clicked

#         # --- Animation and State Setup ---
#         self._expanded_height = 180 
#         self._anim_duration = 220    
#         self._is_expanded = False

#         # ensure homeExpandFrame starts collapsed (maxHeight 0) and hide the close button AND forgot pass button
#         self.homeExpandFrame.setMaximumHeight(0)
#         self.closeHomeBtn.hide()
#         self.forgotPassBtn.hide()


#     # ----- click handlers -----
#     def _home_card_clicked(self, event):
#         if event.button() == QtCore.Qt.MouseButton.LeftButton:
#             if self._is_expanded:
#                 self._collapse_home_area()
#             else:
#                 self._expand_home_area()

#     def _on_forgot_pass(self):
#         QtWidgets.QMessageBox.information(
#         self,
#         "Forgot Home Pass",
#         "Please contact your system administrator to reset your home pass."
#     )


#     def _expand_home_area(self):
#         if not self.homeExpandFrame:
#             return
        
#         # Animate and show the close button AND forgot pass button
#         start = self.homeExpandFrame.maximumHeight()
#         end = self._expanded_height
#         self._animate_home_expand(start, end)
#         self._is_expanded = True
#         self.closeHomeBtn.show()
#         self.forgotPassBtn.show()

#     def _collapse_home_area(self):
#         if not self.homeExpandFrame:
#             return
        
#         # Animate and hide the close button AND forgot pass button
#         start = self.homeExpandFrame.maximumHeight()
#         end = 0
#         self._animate_home_expand(start, end)
#         self._is_expanded = False
#         self.closeHomeBtn.hide()
#         self.forgotPassBtn.hide()

#     def _animate_home_expand(self, start, end):
#         if not self.homeExpandFrame:
#             return
#         # stop existing animation if any
#         try:
#             if hasattr(self, "_expand_anim") and self._expand_anim and self._expand_anim.state() == QtCore.QAbstractAnimation.State.Running:
#                 self._expand_anim.stop()
#         except Exception:
#             pass
            
#         self._expand_anim = QtCore.QPropertyAnimation(self.homeExpandFrame, b"maximumHeight")
#         self._expand_anim.setDuration(self._anim_duration)
#         self._expand_anim.setStartValue(start)
#         self._expand_anim.setEndValue(end)
#         self._expand_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
#         self._expand_anim.start()

#     def _on_gate(self):
#         # user chose gate -> emit and let app handle
#         self.mode_selected.emit('gate', {})

#     def _on_enter_home(self):
#         from controller.HomePassController import HomePassController
#         self.home_ctrl = HomePassController()

#         pass_text = self.homePassInput.text().strip()

#         if not pass_text:
#             QtWidgets.QMessageBox.warning(self, "Missing", "Enter a home pass.")
#             return

#         if not self.home_ctrl.validate_home_pass(pass_text):
#             QtWidgets.QMessageBox.warning(self, "Invalid", "Incorrect home pass.")
#             return

#         self.mode_selected.emit("home", {"home_pass": pass_text})

        
#         # clear field after emitting
#         if self.homePassInput:
#             self.homePassInput.clear()
            
#         # collapse the area after submit
#         self._collapse_home_area()
#         self._is_expanded = False

# if __name__ == '__main__':                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
#     # 1. Create the QApplication instance
#     app = QtWidgets.QApplication(sys.argv)
    
#     # 2. Create an instance of your custom widget/window
#     main_window = ChooseModeWindow()
    
#     # 3. Show the window
#     main_window.show() 
    
#     # 4. Start the application's event loop
#     sys.exit(app.exec())


# entrysafe/views/choose_mode.py

import sys  # needed for standalone test
from os import path
from PyQt6 import QtWidgets, uic, QtGui, QtCore

from controller.HomePassController import HomePassController
from controller.ForgotPasswordController import ForgotPasswordController

BASE_DIR = path.dirname(path.abspath(__file__))         # .../entrysafe/views
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))  # .../entrysafe

UI_FILE = path.join(PROJECT_ROOT, "ui", "choose_mode.ui")
GATE_ICON = path.join(PROJECT_ROOT, "assets", "images", "gate.png")
HOME_ICON = path.join(PROJECT_ROOT, "assets", "images", "home.png")


class ChooseModeWindow(QtWidgets.QWidget):
    """
    Mode selector window: Gate mode or Home mode.
    """
    mode_selected = QtCore.pyqtSignal(str, dict)  # kept from old code (not strictly needed now)

    def __init__(self, username):
        super().__init__()
        self.username = username

        # --- UI Loading ---
        if not path.exists(UI_FILE):
            print(f"FATAL ERROR: UI file not found at {UI_FILE}")
            return

        uic.loadUi(UI_FILE, self)

        # controllers
        self.home_ctrl = HomePassController()
        self.forgot_ctrl = ForgotPasswordController()

        # --- Find widgets (names must match UI) ---
        self.gateBtn = self.findChild(QtWidgets.QPushButton, "gateBtn")
        self.homePassInput = self.findChild(QtWidgets.QLineEdit, "homePassInput")
        self.gateIcon = self.findChild(QtWidgets.QLabel, "gateIcon")
        self.homeIcon = self.findChild(QtWidgets.QLabel, "homeIcon")
        self.homeCard = self.findChild(QtWidgets.QFrame, "homeCard")
        self.homeExpandFrame = self.findChild(QtWidgets.QFrame, "homeExpandFrame")
        self.closeHomeBtn = self.findChild(QtWidgets.QPushButton, "closeHomeBtn")
        self.forgotPassBtn = self.findChild(QtWidgets.QPushButton, "forgotPassBtn")

        # Defensive check (same as your old code)
        if not all([self.gateBtn, self.homePassInput, self.homeExpandFrame,
                    self.homeCard, self.closeHomeBtn, self.forgotPassBtn]):
            print("WARNING: choose_mode UI missing crucial widgets. Check objectNames in UI file.")
            return

        # --- Icon Setup (same visuals, PyQt6 enums fixed) ---
        ICON_SIZE = 200

        if path.exists(GATE_ICON) and self.gateIcon:
            pix = QtGui.QPixmap(GATE_ICON)
            if not pix.isNull():
                self.gateIcon.setPixmap(
                    pix.scaled(
                        ICON_SIZE,
                        ICON_SIZE,
                        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                        QtCore.Qt.TransformationMode.SmoothTransformation
                    )
                )

        if path.exists(HOME_ICON) and self.homeIcon:
            pix = QtGui.QPixmap(HOME_ICON)
            if not pix.isNull():
                self.homeIcon.setPixmap(
                    pix.scaled(
                        ICON_SIZE,
                        ICON_SIZE,
                        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                        QtCore.Qt.TransformationMode.SmoothTransformation
                    )
                )

        # --- Connections (kept your behavior, changed targets) ---
        self.gateBtn.clicked.connect(self._on_gate)
        self.homePassInput.returnPressed.connect(self._on_enter_home)  # ENTER still works
        self.forgotPassBtn.clicked.connect(self._on_forgot_pass)
        self.closeHomeBtn.clicked.connect(self._collapse_home_area)

        # clicking the homeCard expands/collapses input
        self.homeCard.mousePressEvent = self._home_card_clicked

        # --- Animation and State Setup (same as old) ---
        self._expanded_height = 180
        self._anim_duration = 220
        self._is_expanded = False

        # start collapsed, hide buttons initially (same as old)
        self.homeExpandFrame.setMaximumHeight(0)
        self.closeHomeBtn.hide()
        self.forgotPassBtn.hide()

    # ----- click handlers -----
    def _home_card_clicked(self, event):
        # PyQt6: MouseButton.LeftButton
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self._is_expanded:
                self._collapse_home_area()
            else:
                self._expand_home_area()

    def _on_forgot_pass(self):
        """
        Forgot home pass:
        - ask security questions using ForgotPasswordController
        - if OK, ask for new home pass and update via HomePassController
        """
        ok, data = self.forgot_ctrl.get_questions(self.username)
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Error", data)
            return

        q1, q2 = data["q1"], data["q2"]

        a1, ok = QtWidgets.QInputDialog.getText(self, "Security Check", q1)
        if not ok:
            return
        a2, ok = QtWidgets.QInputDialog.getText(self, "Security Check", q2)
        if not ok:
            return

        valid, msg = self.forgot_ctrl.verify_answers(self.username, a1, a2)
        if not valid:
            QtWidgets.QMessageBox.warning(self, "Error", "Incorrect answers.")
            return

        new_homepass, ok = QtWidgets.QInputDialog.getText(
            self, "New Home Pass", "Enter new home pass:"
        )
        if not ok or new_homepass.strip() == "":
            return

        if not self.home_ctrl.update_home_pass(self.username, new_homepass):
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to update home pass.")
            return

        QtWidgets.QMessageBox.information(self, "Success", "Home pass updated successfully.")

    def _expand_home_area(self):
        if not self.homeExpandFrame:
            return

        start = self.homeExpandFrame.maximumHeight()
        end = self._expanded_height
        self._animate_home_expand(start, end)
        self._is_expanded = True
        self.closeHomeBtn.show()
        self.forgotPassBtn.show()

    def _collapse_home_area(self):
        if not self.homeExpandFrame:
            return

        start = self.homeExpandFrame.maximumHeight()
        end = 0
        self._animate_home_expand(start, end)
        self._is_expanded = False
        self.closeHomeBtn.hide()
        self.forgotPassBtn.hide()

    def _animate_home_expand(self, start, end):
        if not self.homeExpandFrame:
            return

        try:
            if hasattr(self, "_expand_anim") and self._expand_anim and \
               self._expand_anim.state() == QtCore.QAbstractAnimation.State.Running:
                self._expand_anim.stop()
        except Exception:
            pass

        self._expand_anim = QtCore.QPropertyAnimation(self.homeExpandFrame, b"maximumHeight")
        self._expand_anim.setDuration(self._anim_duration)
        self._expand_anim.setStartValue(start)
        self._expand_anim.setEndValue(end)
        # PyQt6: QEasingCurve.Type.OutCubic
        self._expand_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self._expand_anim.start()

    # ----- Gate mode -----
    def _on_gate(self):
        """
        Old behavior: emit signal.
        New behavior: directly open ScanWindow and close self.
        """
        try:
            from views.scan import ScanWindow
            self.scan = ScanWindow()
            self.scan.show()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to open Gate view:\n{e}")

    # ----- Home pass -----
    def _on_enter_home(self):
        """
        Called when user presses Enter in homePassInput (same as before, but with backend):
        - validate home pass in DB
        - if OK, open dashboard
        """
        if not self.homePassInput:
            return

        pass_text = self.homePassInput.text().strip()

        if not pass_text:
            QtWidgets.QMessageBox.warning(self, "Missing", "Enter a home pass.")
            return

        # Use username-based validation
        if not self.home_ctrl.validate_home_pass(self.username, pass_text):
            QtWidgets.QMessageBox.warning(self, "Invalid", "Incorrect home pass.")
            return

        # SUCCESS → open dashboard
        try:
            from views.dashboard import AdminWindow
            self.dash = AdminWindow(self.username)
            self.dash.show()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to open dashboard:\n{e}")
            return

        # clear field after success
        self.homePassInput.clear()
        self._collapse_home_area()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ChooseModeWindow(username="demoUser")
    win.show()
    sys.exit(app.exec())
