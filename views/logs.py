import sys
# from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem


import os
from utils.paths import app_dir

BASE = app_dir()
UI_FILE = os.path.join(BASE, "ui", "logs.ui")
BG_FILE = os.path.join(BASE, "assets", "images", "bg1.png")
# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "logs.ui")
# BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


from controller.LogsController import LogsController

class LogsWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()

        self.username = username

        
        self.resize(1200, 800)
        # Load UI
        uic.loadUi(UI_FILE, self)
        
        self.resize(1250, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())

        # --- background ---
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # --- UI widgets ---
        self.table = self.findChild(QtWidgets.QTableWidget, "logsTable")
        self.searchInput = self.findChild(QtWidgets.QLineEdit, "searchInput")
        self.backBtn = self.findChild(QtWidgets.QPushButton, "backToDashboardBtn")

        # --- Keep your exact table setup (DO NOT CHANGE) ---
        self.setup_table()

        # Controller
        self.logs_controller = LogsController()

        # Search
        self.searchInput.textChanged.connect(self.load_logs)

        # Back
        # self.backBtn.clicked.connect(self.go_back)
        btn = self.findChild(QtWidgets.QPushButton, "backToDashboardBtn")
        if btn:
            btn.clicked.connect(self.go_to_dashboard)

        # Load data
        self.load_logs()

    def load_logs(self):
        if self.table is None:
            return

        term = self.searchInput.text().strip()
        records = self.logs_controller.search_logs(self.username, term)

        self.table.setRowCount(0)

        for r in records:
            self.add_row(
                r["date_display"],
                r["studentname"],
                r["dropoff_by"],
                r["pickup_by"],
                r["dropoff_time"],
                r["pickup_time"]
            )


    def add_row(self, date, student, drop_by, pick_by, drop_time, pick_time):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # DATE
        item_date = QTableWidgetItem(date)
        item_date.setFlags(item_date.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 0, item_date)

        # STUDENT NAME
        item_student = QTableWidgetItem(student)
        item_student.setFlags(item_student.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 1, item_student)

        # FORMAT DROP-OFF
        if drop_by:
            drop_txt = f"{drop_by}\n{drop_time.strftime('%I:%M %p') if drop_time else ''}"
        else:
            drop_txt = "—"

        drop_item = QTableWidgetItem(drop_txt)
        drop_item.setFlags(drop_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 2, drop_item)

        # FORMAT PICK-UP
        if pick_by:
            pick_txt = f"{pick_by}\n{pick_time.strftime('%I:%M %p') if pick_time else ''}"
        else:
            pick_txt = "—"

        pick_item = QTableWidgetItem(pick_txt)
        pick_item.setFlags(pick_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 3, pick_item)

        # Adjust row height for multiline
        self.table.setRowHeight(row, 55)

    # ------------------------------------------------------
    # KEEPING YOUR EXACT STYLE — NO CHANGES
    def setup_table(self):
        if self.table is None:
            return
        try:
            body_font = self.table.font()
            body_font.setPointSize(20)
            self.table.setFont(body_font)
        except: pass

        header = self.table.horizontalHeader()
        try:
            header_font = header.font()
            header_font.setPointSize(18)
            header_font.setBold(True)
            header.setFont(header_font)
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        except: pass

        try:
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except: pass

        try:
            self.table.verticalHeader().setDefaultSectionSize(54)
            self.table.horizontalHeader().setFixedHeight(48)
            self.table.verticalHeader().setVisible(False)
        except: pass

        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: transparent;
                border: none;
            }
            QTableWidget::item {
                border: none;
                padding: 8px;
            }
            QHeaderView::section {
                border: none;
                background: transparent;
                padding-left: 12px;
            }
        """)

    # ------------------------------------------------------
    def go_to_dashboard(self):
        from views.dashboard import AdminWindow  # safe import
        self.dashboard = AdminWindow(self.username)
        self.dashboard.show()
        self.close()

    # ------------------------------------------------------------------------
    # Background scaling
    # ------------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        try:
            cw = self.findChild(QtWidgets.QWidget, "centralwidget")
            scaled_bg = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._bg_label.setPixmap(scaled_bg)
            self._bg_label.resize(cw.size())
        except:
            pass