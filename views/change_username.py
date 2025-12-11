# views/change_username.py
from PyQt6 import QtWidgets, uic, QtGui
from os import path
from database.connection import Database  

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
UI_CHANGE_USERNAME = path.join(PROJECT_ROOT, "ui", "change_username.ui")

class ChangeUsernameDialog(QtWidgets.QDialog):
    def __init__(self, current_username):
        super().__init__()
        self.current_username = current_username
        self.db = Database()  

        uic.loadUi(UI_CHANGE_USERNAME, self)
        
        self.setWindowTitle("Username - EntrySafe")

        icon_path = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")  
        self.setWindowIcon(QtGui.QIcon(icon_path))

        self.currentUsernameLineEdit.setText(self.current_username)

        self.changeBtn.clicked.connect(self.change_username)
        self.cancelBtn.clicked.connect(self.reject)

    def change_username(self):
        new_username = self.newUsernameLineEdit.text().strip()
        if not new_username:
            QtWidgets.QMessageBox.warning(self, "Error", "New username cannot be empty.")
            return

        conn = self.db.connect()
        if not conn:
            QtWidgets.QMessageBox.critical(self, "Error", "Database connection failed.")
            return

        try:
            cur = conn.cursor()
            cur.execute("CALL update_username(%s, %s)", (self.current_username, new_username))
            conn.commit()
            cur.close()
            QtWidgets.QMessageBox.information(self, "Success", f"Username changed to {new_username}")
            self.current_username = new_username
            self.accept()  
        except Exception as e:
            message = str(e).splitlines()[0]
            QtWidgets.QMessageBox.warning(self, "Error", message)
            if conn:
                conn.rollback()
