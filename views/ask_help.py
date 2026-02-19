# views/ask_help.py
from PyQt6 import QtWidgets, uic, QtGui
from os import path
import webbrowser
import os
from utils.paths import app_dir

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
# UI_ASK_HELP = path.join(PROJECT_ROOT, "ui", "ask_help.ui")
BASE = app_dir()
UI_ASK_HELP = os.path.join(BASE, "ui", "ask_help.ui")


class AskHelpDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_ASK_HELP, self)
        
        self.setWindowTitle("Ask Help - EntrySafe")

        icon_path = os.path.join(BASE, "assets", "images", "appLogo.png")  
        self.setWindowIcon(QtGui.QIcon(icon_path))

        # self.fbButton.clicked.connect(lambda: self.open_url("https://www.facebook.com/mckhenzyy"))
        # self.igButton.clicked.connect(lambda: self.open_url("https://www.instagram.com/khezmangubat"))
        self.closeBtn.clicked.connect(self.reject)

    def open_url(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to open URL: {url}\n{str(e)}")
# entrysafe2025