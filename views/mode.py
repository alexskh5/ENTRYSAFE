import sys
from os import path

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt


BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "mode.ui")


class ChooseModeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        # ----------------------------
        # Get widgets from UI
        # ----------------------------
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

        self.home_expanded = False

        # ----------------------------
        # INITIAL CARD HEIGHTS
        # ----------------------------
        # 👉 both cards start at 400px height
        for frame in (self.gateFrame, self.homeFrame):
            if frame is not None:
                frame.setMinimumHeight(400)
                frame.setMaximumHeight(400)

        # ----------------------------
        # Connect signals
        # ----------------------------

        if self.homeBtn is not None:
            self.homeBtn.clicked.connect(self.expand_home_card)

        if self.homeIconBtn is not None:
            self.homeIconBtn.clicked.connect(self.expand_home_card)

        if self.exitBtn is not None:
            self.exitBtn.clicked.connect(self.collapse_home_card)

        if self.backBtn is not None:
            self.backBtn.clicked.connect(self.close)

        # Start collapsed
        self.collapse_home_card()

    # ------------------------------------------------------------------
    def set_home_expanded(self, expanded: bool):
        """Show/hide the extra Home widgets (pass input, forgot btn, etc.)."""
        self.home_expanded = expanded

        if self.homeExtraFrame is not None:
            self.homeExtraFrame.setVisible(expanded)

        if self.exitBtn is not None:
            self.exitBtn.setVisible(expanded)

        # HEIGHT LOGIC
        if self.homeFrame is not None:
            if expanded:
                # expanded: allow home card to grow taller than 400
                self.homeFrame.setMinimumHeight(400)    # base size
                self.homeFrame.setMaximumHeight(9999)   # no real limit
            else:
                # collapsed: fixed 400 height
                self.homeFrame.setMinimumHeight(400)
                self.homeFrame.setMaximumHeight(400)

        # gateFrame stays 400 all the time
        if self.gateFrame is not None:
            self.gateFrame.setMinimumHeight(400)
            self.gateFrame.setMaximumHeight(400)

    def expand_home_card(self):
        self.set_home_expanded(True)

    def collapse_home_card(self):
        self.set_home_expanded(False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = ChooseModeWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
