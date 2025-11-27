import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "logs.ui")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


class LogsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI into QMainWindow
        uic.loadUi(UI_FILE, self)


        # --- Background image using QLabel (behind everything) ---
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # find table widget 
        self.table = (
            self.findChild(QtWidgets.QTableWidget, "logsTable")
        )

        if self.table is None:
            print("Warning: table widget not found. Check objectName in logs.ui")
        else:
            if self.table.columnCount() < 4:
                self.table.setColumnCount(4)
                self.table.setHorizontalHeaderLabels(["DATE", "STUDENT", "DROP OFF", "PICK UP"])

            # make table responsive and style it
            self.setup_table()

            # add sample rows so you can see how it looks
            sample = [
                {"date": "10-30-2025", "student": "Name of student 1", "drop_off": "Name of Guardian", "pick_up": "Name of Guardian"},
                {"date": "10-30-2025", "student": "Name of student 1", "drop_off": "Name of Guardian", "pick_up": "Name of Guardian"},
                {"date": "10-30-2025", "student": "Name of student 1", "drop_off": "Name of Guardian", "pick_up": "Name of Guardian"},
                {"date": "10-30-2025", "student": "Name of student 1", "drop_off": "Name of Guardian", "pick_up": "Name of Guardian"},
                {"date": "10-30-2025", "student": "Name of student 1", "drop_off": "Name of Guardian", "pick_up": "Name of Guardian"},
            ]
            for s in sample:
                self.add_row(s["date"], s["student"], s["drop_off"], s["pick_up"])


    # ----------------------------------------------------------------------------
    # Function to add a row 
    def add_row(self, date, student, drop_off, pick_up):
        if self.table is None:
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        # DATE
        date_item = QTableWidgetItem(date)
        date_item.setFlags(date_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        date_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 0, date_item)

        # STUDENT
        student_item = QTableWidgetItem(student)
        student_item.setFlags(student_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        student_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 1, student_item)

        # DROP OFF
        drop_item = QTableWidgetItem(drop_off)
        drop_item.setFlags(drop_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        drop_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 2, drop_item)

        # PICK UP
        pick_item = QTableWidgetItem(pick_up)
        pick_item.setFlags(pick_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        pick_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 3, pick_item)


    # ----------------------------------------------------------------------------
    # function to make the table responsive / stretch columns evenly
    def setup_table(self):
        if self.table is None:
            return

        try:
            body_font = self.table.font()
            body_font.setPointSize(13)
            self.table.setFont(body_font)
        except Exception:
            pass

        header = self.table.horizontalHeader()

        # ---- Header font ----
        try:
            header_font = header.font()
            header_font.setPointSize(13)   
            header_font.setBold(True)      
            header.setFont(header_font)
            header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        except Exception:
            pass

        # ---- 4 even columns ----
        try:
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception:
            pass

        # Row + header heights
        try:
            self.table.verticalHeader().setDefaultSectionSize(54)
        except Exception:
            pass
        try:
            self.table.horizontalHeader().setFixedHeight(48)
        except Exception:
            pass

        # Hide vertical row numbers
        try:
            self.table.verticalHeader().setVisible(False)
        except Exception:
            pass

        # table style
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



    # ----------------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize background to fill area
        try:
            cw = self.findChild(QtWidgets.QWidget, "centralwidget")
            scaled_bg = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._bg_label.setPixmap(scaled_bg)
            self._bg_label.resize(cw.size())
            self._bg_label.move(0, 0)
        except Exception:
            pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = LogsWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()