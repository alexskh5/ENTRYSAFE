import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem

from controller.AttendanceController import AttendanceController

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "attendance.ui")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


class AttendanceWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username


        uic.loadUi(UI_FILE, self)
        
        self.resize(1250, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())

        # Controller
        self.attendance_controller = AttendanceController()

        # Background setup
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # Search bar
        self.searchStudent = self.findChild(QtWidgets.QLineEdit, "searchStudent")
        if self.searchStudent:
            self.searchStudent.textChanged.connect(self.load_attendance)

        # Table
        self.table = self.findChild(QtWidgets.QTableWidget, "attendanceTable")

        if self.table:
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["DATE", "STUDENT ID", "STUDENT NAME"])
            self.setup_table()

        # Load data initially
        self.load_attendance()

    
        btn = self.findChild(QtWidgets.QPushButton, "backToDashboardBtn")
        if btn:
            btn.clicked.connect(self.go_to_dashboard)
    
    # ------------------------------------------------------------------------
    # Load attendance records from DB
    # ------------------------------------------------------------------------
    def load_attendance(self):
        if self.table is None:
            return

        term = self.searchStudent.text().strip() if self.searchStudent else ""
        records = self.attendance_controller.search_attendance(self.username, term)


        self.table.setRowCount(0)

        for r in records:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # DATE (with time)
            item_date = QTableWidgetItem(str(r["date_display"]))
            item_date.setFlags(item_date.flags() ^ Qt.ItemFlag.ItemIsEditable)
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 0, item_date)

            # STUDENT ID
            item_id = QTableWidgetItem(r["studid"])
            item_id.setFlags(item_id.flags() ^ Qt.ItemFlag.ItemIsEditable)
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 1, item_id)

            # STUDENT NAME
            item_name = QTableWidgetItem(r["studentname"])
            item_name.setFlags(item_name.flags() ^ Qt.ItemFlag.ItemIsEditable)
            item_name.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 2, item_name)


    # ------------------------------------------------------------------------
    # Table design / responsive layout
    # ------------------------------------------------------------------------
    def setup_table(self):
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        body_font = self.table.font()
        body_font.setPointSize(15)
        self.table.setFont(body_font)

        header_font = header.font()
        header_font.setPointSize(13)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )


        self.table.verticalHeader().setDefaultSectionSize(54)
        self.table.horizontalHeader().setFixedHeight(48)
        self.table.verticalHeader().setVisible(False)

        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: transparent;
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
    
    
    def go_to_dashboard(self):
        from views.dashboard import AdminWindow  # safe import
        self.dashboard = AdminWindow(self.username)
        self.dashboard.show()
        self.close()

