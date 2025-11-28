# views/change_homepass.py
from PyQt6 import QtWidgets, uic, QtGui
from os import path
from database.connection import Database

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
UI_CHANGE_HOMEPASS = path.join(PROJECT_ROOT, "ui", "change_homepass.ui")


class ChangeHomepassDialog(QtWidgets.QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.db = Database()

        uic.loadUi(UI_CHANGE_HOMEPASS, self)
        
        self.setWindowTitle("Home Password - EntrySafe")

        icon_path = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")  
        self.setWindowIcon(QtGui.QIcon(icon_path))

        self.changeBtn.clicked.connect(self.change_homepass)
        self.cancelBtn.clicked.connect(self.reject)
        self.showPasswordBtn.clicked.connect(self.toggle_password)

    def toggle_password(self):
        fields = [
            self.currentHomepassLineEdit,
            self.newHomepassLineEdit
        ]
        for f in fields:
            if f.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
                f.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            else:
                f.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def change_homepass(self):
        current_hp = self.currentHomepassLineEdit.text().strip()
        new_hp = self.newHomepassLineEdit.text().strip()

        if not current_hp or not new_hp:
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if current_hp == new_hp:
            QtWidgets.QMessageBox.warning(self, "Error", "New home password cannot be the same as the current one.")
            return

        if not new_hp.isdigit() or len(new_hp) != 5:
            QtWidgets.QMessageBox.warning(self, "Error", "Home password must be exactly 5 digits.")
            return

        conn = self.db.connect()
        if not conn:
            QtWidgets.QMessageBox.critical(self, "Error", "Database connection failed.")
            return

        try:
            cur = conn.cursor()
            cur.execute("CALL change_user_homepass(%s, %s, %s)", (self.username, current_hp, new_hp))
            conn.commit()
            cur.close()

            QtWidgets.QMessageBox.information(self, "Success", "Home password successfully changed.")
            self.accept()

        except Exception as e:
            clean_message = str(e).splitlines()[0]
            QtWidgets.QMessageBox.critical(self, "Error", clean_message)
            if conn:
                conn.rollback()
