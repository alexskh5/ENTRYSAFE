from PyQt6 import QtWidgets, uic, QtGui
from os import path
import webbrowser
from views.ask_help import AskHelpDialog
import os
from utils.paths import app_dir

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
# UI_ASK_HELP = path.join(PROJECT_ROOT, "ui", "about.ui")
BASE = app_dir()
UI_ASK_HELP = os.path.join(BASE, "ui", "about.ui")



class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_ASK_HELP, self)
        
        self.setWindowTitle("About EntrySafe")

        icon_path = os.path.join(BASE, "assets", "images", "appLogo.png")  
        self.setWindowIcon(QtGui.QIcon(icon_path))

        self.helpBtn.clicked.connect(self.open_help_dialog)
        self.closeBtn.clicked.connect(self.reject)

    def open_help_dialog(self):
        self.reject()
        dialog = AskHelpDialog()
        dialog.exec()