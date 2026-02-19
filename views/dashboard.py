import sys
# from os import path
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from views.change_username import ChangeUsernameDialog
from views.change_password import ChangePasswordDialog
from views.change_homepass import ChangeHomepassDialog
from views.about import AboutDialog
from views.ask_help import AskHelpDialog
from utils.paths import app_dir


# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "dashboard.ui")
# BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")
BASE = app_dir()
UI_FILE = os.path.join(BASE, "ui", "dashboard.ui")
BG_FILE = os.path.join(BASE, "assets", "images", "bg1.png")


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username   # store username

        uic.loadUi(UI_FILE, self)
        
        self.resize(1250, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())

        # Background setup
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # Sidebar
        self.menu_widget = self.findChild(QtWidgets.QWidget, "menuSubContainer")
        self.main_widget = self.findChild(QtWidgets.QWidget, "mainContainer")
        self.left_frame = self.findChild(QtWidgets.QFrame, "leftFrame")
        self._menu_expanded_width = 500

        if self.menu_widget:
            self._menu_animation = QPropertyAnimation(self.menu_widget, b"maximumWidth")
            self._menu_animation.setDuration(250)
            self._menu_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.menu_widget.setMaximumWidth(self._menu_expanded_width)
        else:
            self._menu_animation = None

        pic_btn = self.findChild(QtWidgets.QPushButton, "picBtn") or self.findChild(QtWidgets.QLabel, "picBtn")
        pic_btn_2 = self.findChild(QtWidgets.QPushButton, "picBtn_2") or self.findChild(QtWidgets.QLabel, "picBtn_2")

        if pic_btn:
            try:
                pic_btn.clicked.connect(self.collapse_menu)
            except:
                pic_btn.mousePressEvent = lambda ev: self.collapse_menu()

        if pic_btn_2:
            try:
                pic_btn_2.clicked.connect(self.expand_menu)
            except:
                pic_btn_2.mousePressEvent = lambda ev: self.expand_menu()

        # collapse initially
        if self.left_frame:
            self.left_frame.setVisible(True)

        if self.menu_widget:
            self.menu_widget.setMaximumWidth(0)
            try:
                self.menu_widget.resize(0, self.menu_widget.height())
            except:
                pass

        # --------------------------------
        # DISPLAY USERNAME
        # --------------------------------
        self.adminLabel = self.findChild(QtWidgets.QLabel, "adminLabel")
        if self.adminLabel:
            self.adminLabel.setText(self.username)

        # --------------------------------
        # CHANGE USERNAME BUTTON
        # --------------------------------
        self.userBtn = self.findChild(QtWidgets.QPushButton, "userBtn")
        if self.userBtn:
            self.userBtn.clicked.connect(self.open_change_username)
        
        # --------------------------------
        # CHANGE PASSWORD BUTTON
        # --------------------------------
        self.passBtn = self.findChild(QtWidgets.QPushButton, "passBtn")
        if self.passBtn:
            self.passBtn.clicked.connect(self.open_change_password)
        
        # --------------------------------
        # CHANGE HOME PASSWORD BUTTON
        # --------------------------------
        self.homePassBtn = self.findChild(QtWidgets.QPushButton, "homePassBtn")
        if self.homePassBtn:
            self.homePassBtn.clicked.connect(self.open_change_hpassword)
            
        # --------------------------------
        # ABOUT BUTTON
        # --------------------------------
        self.aboutBtn = self.findChild(QtWidgets.QPushButton, "aboutBtn")
        if self.aboutBtn:
            self.aboutBtn.clicked.connect(self.open_about)
            
        # --------------------------------
        # ASK HELP BUTTON
        # --------------------------------
        self.askBtn = self.findChild(QtWidgets.QPushButton, "askBtn")
        if self.askBtn:
            self.askBtn.clicked.connect(self.open_help)
        
        # --------------------------------
        # LOGOUT BUTTON
        # --------------------------------
        self.logOutBtn = self.findChild(QtWidgets.QPushButton, "logOutBtn")
        if self.logOutBtn:
            self.logOutBtn.clicked.connect(self.logout)

        # --------------------------------
        # ROUTE TO STUDENT PAGE
        # --------------------------------
        self.StudentBtn = self.findChild(QtWidgets.QPushButton, "StudentBtn")
        if self.StudentBtn:
            self.StudentBtn.clicked.connect(self.go_student_page)

        # --------------------------------
        # ROUTE TO ATTENDANCE PAGE
        # --------------------------------
        self.attendanceBtn = self.findChild(QtWidgets.QPushButton, "attendanceBtn")
        if self.attendanceBtn:
            self.attendanceBtn.clicked.connect(self.go_attendance_page)
        
        # --------------------------------
        # ROUTE TO LOGS PAGE
        # --------------------------------
        self.guardianBtn = self.findChild(QtWidgets.QPushButton, "guardianBtn")
        if self.guardianBtn:
            self.guardianBtn.clicked.connect(self.go_logs_page)
        
        
    # ---------------- Logout Function ----------------
    def logout(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to log out?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            from views.mode import ChooseModeWindow
            self.close()
            self.login = ChooseModeWindow(self.username)
            self.login.show()


    # ---------------- Route Student Page ----------------
    def go_student_page(self):
        from views.student import StudentWindow
        self.close()
        self.stud = StudentWindow(self.username)
        self.stud.show()
       
        
    
    # ---------------- COLLAPSE MENU ----------------
    def collapse_menu(self):
        if self.left_frame:
            self.left_frame.setVisible(True)

        if not self.menu_widget or not self._menu_animation:
            return

        current = self.menu_widget.width()

        self._menu_animation.stop()
        self._menu_animation.setStartValue(current)
        self._menu_animation.setEndValue(0)
        self._menu_animation.start()


    # ---------------- EXPAND MENU ----------------
    def expand_menu(self):
        if self.left_frame:
            self.left_frame.setVisible(False)

        if not self.menu_widget or not self._menu_animation:
            return

        current = self.menu_widget.width()
        target = self._menu_expanded_width

        self._menu_animation.stop()
        self._menu_animation.setStartValue(current)
        self._menu_animation.setEndValue(target)
        self._menu_animation.start()




    def resizeEvent(self, event):
        super().resizeEvent(event)

        cw = self.findChild(QtWidgets.QWidget, "centralwidget")

        if hasattr(self, "_bg_pix") and hasattr(self, "_bg_label"):
            scaled_bg = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._bg_label.setPixmap(scaled_bg)
            self._bg_label.resize(cw.size())




    # ---------------- Change Username Button ----------------
    def open_change_username(self):
        dialog = ChangeUsernameDialog(self.username)
        if dialog.exec():
            self.username = dialog.current_username
            if self.adminLabel:
                self.adminLabel.setText(self.username)
                
    # ---------------- Change Password Button ----------------
    def open_change_password(self):
        dialog = ChangePasswordDialog(self.username)
        if dialog.exec():
            return
        
    # ---------------- Change Home Password Button ----------------
    def open_change_hpassword(self):
        dialog = ChangeHomepassDialog(self.username)
        if dialog.exec():
            return
        
    # ---------------- About Button ----------------
    def open_about(self):
        dialog = AboutDialog()
        if dialog.exec():
            return
    
    # ---------------- Ask Help Button ----------------
    def open_help(self):
        dialog = AskHelpDialog()
        if dialog.exec():
            return
        
    # ---------------- Open Attendance ----------------
    def go_attendance_page(self):
        from views.attendance import AttendanceWindow
        self.close()
        self.stud = AttendanceWindow(self.username)
        self.stud.show()
    
    # ---------------- Open Logs ----------------
    def go_logs_page(self):
        from views.logs import LogsWindow
        self.close()
        self.stud = LogsWindow(self.username)
        self.stud.show()
        