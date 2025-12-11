# views/change_password.py
from PyQt6 import QtWidgets, uic, QtGui
from os import path
from database.connection import Database
import re

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
UI_CHANGE_PASSWORD = path.join(PROJECT_ROOT, "ui", "change_password.ui")


class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.db = Database()

        uic.loadUi(UI_CHANGE_PASSWORD, self)
        
        self.setWindowTitle("User Password - EntrySafe")

        icon_path = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")  
        self.setWindowIcon(QtGui.QIcon(icon_path))

        self.changeBtn.clicked.connect(self.change_password)
        self.cancelBtn.clicked.connect(self.reject)

        self.showPasswordBtn.clicked.connect(self.toggle_password)

    def toggle_password(self):
        fields = [
            self.currentPasswordLineEdit,
            self.newPasswordLineEdit
        ]

        for f in fields:
            if f.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
                f.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            else:
                f.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def change_password(self):
        current_pwd = self.currentPasswordLineEdit.text().strip()
        new_pwd = self.newPasswordLineEdit.text().strip()

        if not current_pwd or not new_pwd:
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return
        
        if new_pwd == current_pwd:
            QtWidgets.QMessageBox.warning(self, "Error", "New password cannot be the same as the current password.")
            return

        if len(new_pwd) < 8 or \
           not re.search(r"[A-Z]", new_pwd) or \
           not re.search(r"[a-z]", new_pwd) or \
           not re.search(r"\d", new_pwd):
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "Password must be at least 8 characters long and include:\n"
                "- One uppercase letter\n"
                "- One lowercase letter\n"
                "- One number"
            )
            return

        conn = self.db.connect()
        if not conn:
            QtWidgets.QMessageBox.critical(self, "Error", "Database connection failed.")
            return

        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM login_user(%s, %s)", (self.username, current_pwd))
            result = cur.fetchall()

            if not result:
                QtWidgets.QMessageBox.warning(self, "Error", "Current password is incorrect.")
                return

            cur.execute("CALL update_user_password(%s, %s)", (self.username, new_pwd))
            conn.commit()
            cur.close()

            QtWidgets.QMessageBox.information(self, "Success", "Password successfully changed.")
            self.accept()

        except Exception as e:
            clean_message = str(e).splitlines()[0]
            QtWidgets.QMessageBox.critical(self, "Error", clean_message)

            if conn:
                conn.rollback()
