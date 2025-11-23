# entrysafe/views/choose_mode.py 

import sys # Needed for sys.exit() and sys.argv
from os import path 
from PyQt6 import QtWidgets, uic, QtGui, QtCore 

BASE_DIR = path.dirname(path.abspath(__file__))         # .../entrysafe/views 
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))  # .../entrysafe 

UI_FILE = path.join(PROJECT_ROOT, "ui", "choose_mode.ui")
GATE_ICON = path.join(PROJECT_ROOT, "assets", "images", "gate.png")
HOME_ICON = path.join(PROJECT_ROOT, "assets", "images", "home.png")

class ChooseModeWindow(QtWidgets.QWidget):
    """
    Mode selector widget. Emits mode_selected(mode, payload) on selection.
    mode: 'gate' or 'home'
    payload: dict (e.g. {'home_pass': 'abcd'})
    """
    mode_selected = QtCore.pyqtSignal(str, dict)

    def __init__(self):
        super().__init__()
        
        # --- UI Loading ---
        if not path.exists(UI_FILE):
             print(f"FATAL ERROR: UI file not found at {UI_FILE}")
             # If the UI file is missing, we stop initialization here.
             return
        else:
            uic.loadUi(UI_FILE, self)

        # find widgets (names must match UI)
        self.gateBtn = self.findChild(QtWidgets.QPushButton, "gateBtn")
        self.homePassInput = self.findChild(QtWidgets.QLineEdit, "homePassInput")
        self.gateIcon = self.findChild(QtWidgets.QLabel, "gateIcon")
        self.homeIcon = self.findChild(QtWidgets.QLabel, "homeIcon")
        self.homeCard = self.findChild(QtWidgets.QFrame, "homeCard")
        self.homeExpandFrame = self.findChild(QtWidgets.QFrame, "homeExpandFrame")
        self.closeHomeBtn = self.findChild(QtWidgets.QPushButton, "closeHomeBtn") 
        self.forgotPassBtn = self.findChild(QtWidgets.QPushButton, "forgotPassBtn")


        # --- Defensive Checks ---
        if not all([self.gateBtn, self.homePassInput, self.homeExpandFrame, self.homeCard, self.closeHomeBtn]):
            print("WARNING: choose_mode UI missing crucial widgets. Check objectNames in UI file.")
            # We can't proceed if essential widgets for interaction/animation are missing
            return
        if not all([self.gateBtn, self.homePassInput, self.homeExpandFrame,
            self.homeCard, self.closeHomeBtn, self.forgotPassBtn]):
            return

        # --- Icon Setup ---
        # Define the desired icon size (Updated from 160 to 200 pixels)
        ICON_SIZE = 200 

        if path.exists(GATE_ICON) and self.gateIcon:
            pix = QtGui.QPixmap(GATE_ICON)
            if not pix.isNull():
                self.gateIcon.setPixmap(pix.scaled(ICON_SIZE, ICON_SIZE, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        if path.exists(HOME_ICON) and self.homeIcon:
            pix = QtGui.QPixmap(HOME_ICON)
            if not pix.isNull():
                self.homeIcon.setPixmap(pix.scaled(ICON_SIZE, ICON_SIZE, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

        # --- Connections ---
        self.gateBtn.clicked.connect(self._on_gate)
        self.homePassInput.returnPressed.connect(self._on_enter_home)
        self.forgotPassBtn.clicked.connect(self._on_forgot_pass)
        self.closeHomeBtn.clicked.connect(self._collapse_home_area) 
        self.homeCard.mousePressEvent = self._home_card_clicked

        # --- Animation and State Setup ---
        self._expanded_height = 180 
        self._anim_duration = 220    
        self._is_expanded = False

        # ensure homeExpandFrame starts collapsed (maxHeight 0) and hide the close button AND forgot pass button
        self.homeExpandFrame.setMaximumHeight(0)
        self.closeHomeBtn.hide()
        self.forgotPassBtn.hide()


    # ----- click handlers -----
    def _home_card_clicked(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self._is_expanded:
                self._collapse_home_area()
            else:
                self._expand_home_area()

    def _on_forgot_pass(self):
        QtWidgets.QMessageBox.information(
        self,
        "Forgot Home Pass",
        "Please contact your system administrator to reset your home pass."
    )


    def _expand_home_area(self):
        if not self.homeExpandFrame:
            return
        
        # Animate and show the close button AND forgot pass button
        start = self.homeExpandFrame.maximumHeight()
        end = self._expanded_height
        self._animate_home_expand(start, end)
        self._is_expanded = True
        self.closeHomeBtn.show()
        self.forgotPassBtn.show()

    def _collapse_home_area(self):
        if not self.homeExpandFrame:
            return
        
        # Animate and hide the close button AND forgot pass button
        start = self.homeExpandFrame.maximumHeight()
        end = 0
        self._animate_home_expand(start, end)
        self._is_expanded = False
        self.closeHomeBtn.hide()
        self.forgotPassBtn.hide()

    def _animate_home_expand(self, start, end):
        if not self.homeExpandFrame:
            return
        # stop existing animation if any
        try:
            if hasattr(self, "_expand_anim") and self._expand_anim and self._expand_anim.state() == QtCore.QAbstractAnimation.State.Running:
                self._expand_anim.stop()
        except Exception:
            pass
            
        self._expand_anim = QtCore.QPropertyAnimation(self.homeExpandFrame, b"maximumHeight")
        self._expand_anim.setDuration(self._anim_duration)
        self._expand_anim.setStartValue(start)
        self._expand_anim.setEndValue(end)
        self._expand_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self._expand_anim.start()

    def _on_gate(self):
        # user chose gate -> emit and let app handle
        self.mode_selected.emit('gate', {})

    def _on_enter_home(self):
        pass_text = ""
        if self.homePassInput:
            pass_text = self.homePassInput.text().strip()
            
        if not pass_text:
            # Using QMessageBox as per existing pattern; consider switching to a custom modal/inline error message
            QtWidgets.QMessageBox.warning(self, "Missing pass", "Please enter a home pass before continuing.")
            return
            
        self.mode_selected.emit('home', {'home_pass': pass_text})
        
        # clear field after emitting
        if self.homePassInput:
            self.homePassInput.clear()
            
        # collapse the area after submit
        self._collapse_home_area()
        self._is_expanded = False

if __name__ == '__main__':                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    # 1. Create the QApplication instance
    app = QtWidgets.QApplication(sys.argv)
    
    # 2. Create an instance of your custom widget/window
    main_window = ChooseModeWindow()
    
    # 3. Show the window
    main_window.show() 
    
    # 4. Start the application's event loop
    sys.exit(app.exec())