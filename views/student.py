import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "student.ui")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI into QMainWindow
        uic.loadUi(UI_FILE, self)

        # ----------------------------
        # Stacked widget navigation (ADDED)
        # ----------------------------
        # (these objectNames must match the ones in your .ui file)
        try:
            self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
            self.mainStudentPage = self.findChild(QtWidgets.QWidget, "mainStudentPage")
            self.enrollStudentPage = self.findChild(QtWidgets.QWidget, "enrollStudentPage")
            self.verificationPage = self.findChild(QtWidgets.QWidget, "verificationPage")
            self.confirmationPage = self.findChild(QtWidgets.QWidget, "confirmationPage")
            self.editStudenPage = self.findChild(QtWidgets.QWidget, "editStudenPage")

            # set initial page to mainStudentPage
            if self.stacked and self.mainStudentPage:
                self.stacked.setCurrentWidget(self.mainStudentPage)

            # find navigation buttons
            self.enrolStudBtn = self.findChild(QtWidgets.QPushButton, "enrollStudBtn")
            self.backToMainBtn = self.findChild(QtWidgets.QPushButton, "backToMainBtn")
            self.enrollBtn = self.findChild(QtWidgets.QPushButton, "enrollBtn")
            self.backToInputBtn = self.findChild(QtWidgets.QPushButton, "backToInputBtn")
            self.confirmBtn = self.findChild(QtWidgets.QPushButton, "confirmBtn")
            self.saveEditBtn = self.findChild(QtWidgets.QPushButton, "saveEditmBtn")
            # insert here a navigation button edit(this button is from the table actions column) that will jump to the editStudentPage

            # connect buttons (only if both button and target page exist)
            if self.enrolStudBtn and self.enrollStudentPage:
                self.enrolStudBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.enrollStudentPage))
            if self.backToMainBtn and self.mainStudentPage:
                self.backToMainBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.mainStudentPage))
            if self.enrollBtn and self.verificationPage:
                self.enrollBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.verificationPage))
            if self.backToInputBtn and self.enrollStudentPage:
                self.backToInputBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.enrollStudentPage))
            if self.confirmBtn and self.confirmationPage:
                self.confirmBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.confirmationPage))
            if self.saveEditBtn and self.mainStudentPage:
                self.saveEditBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.mainStudentPage))
        except Exception:
            # ignore if stacked-widget/pages/buttons are not present
            pass

        # --- Background image using QLabel (behind everything) ---
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # find table widget (try common names)
        self.table = (
            self.findChild(QtWidgets.QTableWidget, "studentTable")
            or self.findChild(QtWidgets.QTableWidget, "tableWidget")
            or self.findChild(QtWidgets.QTableWidget, "tableStudents")
            or self.findChild(QtWidgets.QTableWidget, "studentsTable")
        )

        if self.table is None:
            print("Warning: table widget not found. Check objectName in student.ui")
        else:
            # ensure columns: ID, Name, Actions
            if self.table.columnCount() < 3:
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["ID", "Name", "Actions"])

            # make table responsive and style it
            self.setup_table()

            # add sample rows so you can see how it looks
            sample = [
                {"id": "S001", "name": "Name of student 1"},
                {"id": "S002", "name": "Name of student 2"},
                {"id": "S003", "name": "Name of student 3"},
                {"id": "S004", "name": "Name of student 4"},
                {"id": "S005", "name": "Name of student 5"},
            ]
            for s in sample:
                self.add_row(s["id"], s["name"])


    # ----------------------------------------------------------------------------
    # Function to add a row (ID, Name, Actions column with 3 text-only buttons)
    def add_row(self, student_id, name):
        """
        Insert a new row into the table with:
          column 0: student_id (text)
          column 1: name (text)
          column 2: actions widget (Edit, Delete, View Guardian)
        """
        if self.table is None:
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        # ID cell (with padding)
        item_id = QTableWidgetItem(f"{student_id}")
        item_id.setFlags(item_id.flags() ^ Qt.ItemFlag.ItemIsEditable)  # read-only
        item_id.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 0, item_id)

        # Name cell (with left padding)
        item_name = QTableWidgetItem(f"{name}")
        item_name.setFlags(item_name.flags() ^ Qt.ItemFlag.ItemIsEditable)
        item_name.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 1, item_name)

        # Actions cell: create a widget with three text-only buttons
        action_cell = QWidget()
        h = QHBoxLayout(action_cell)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        h.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)


        # --- Buttons: Edit / Delete / View Guardian (underlined font) ---
        edit_btn = QPushButton("Edit")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setFixedHeight(30)

        delete_btn = QPushButton("Delete")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedHeight(30)

        view_btn = QPushButton("View Guardian")
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.setFixedHeight(30)

        # Set font size and underline
        btn_font = edit_btn.font()
        btn_font.setPointSize(13)
        btn_font.setUnderline(True)     # <--- underline the text
        edit_btn.setFont(btn_font)
        delete_btn.setFont(btn_font)
        view_btn.setFont(btn_font)

        # Style: remove borders / background (keeps underline from font)
        underline_style = """
        QPushButton {
            border: none;
            background: transparent;
            color: #333333;
        }
        QPushButton:hover {
            color: #8b2fdb;   /* optional hover color */
        }
        """
        edit_btn.setStyleSheet(underline_style)
        delete_btn.setStyleSheet(underline_style)
        view_btn.setStyleSheet(underline_style)

        # Connect signals
        edit_btn.clicked.connect(lambda checked=False, sid=student_id: self.edit_student(sid))
        delete_btn.clicked.connect(lambda checked=False, sid=student_id: self.delete_student(sid))
        view_btn.clicked.connect(lambda checked=False, sid=student_id: self.view_guardian(sid))

        # Add to layout
        h.addWidget(edit_btn)
        h.addWidget(delete_btn)
        h.addWidget(view_btn)


        # Optional: style buttons to match your UI (flat and subtle) — increased padding
        for btn in (edit_btn, delete_btn, view_btn):
            try:
                btn.setFlat(True)
                btn.setStyleSheet("""
                    QPushButton {
                        border-radius: 6px;
                        padding: 6px 10px;   /* increased horizontal padding */
                    }
                    QPushButton:hover { background: rgba(0,0,0,0.03); }
                """)
            except Exception:
                pass

        self.table.setCellWidget(row, 2, action_cell)

        # (Optional) if you want to auto-scroll to the newly added row:
        # self.table.scrollToItem(item_id)

    # ----------------------------------------------------------------------------
    # function to make the table responsive / stretch columns evenly
    def setup_table(self):
        if self.table is None:
            return

        # Make table adjust to contents policy (optional)
        try:
            self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        except Exception:
            pass

        # Increase font size for better readability
        try:
            font = self.table.font()
            font.setPointSize(13)  # increase main table font size
            self.table.setFont(font)
            # # also update header font
            # self.table.horizontalHeader().setFont(font)
        except Exception:
            pass

        header = self.table.horizontalHeader()
        # default: ID interactive so we can set a width, Name stretch, Actions Interactive
        try:
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Interactive)
        except Exception:
            # fallback: stretch all
            try:
                header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            except Exception:
                pass

        # Widen ID column (adjust value as desired)
        try:
            self.table.setColumnWidth(0, 150)   # make ID column wider
        except Exception:
            pass

        # Widen Actions column to fixed size (adjust value as desired)
        try:
            self.table.setColumnWidth(2, 300)   # ACTIONS column width (user-requested)
        except Exception:
            pass

        # Set row and header heights
        try:
            self.table.verticalHeader().setDefaultSectionSize(54)     # row height
        except Exception:
            pass
        try:
            self.table.horizontalHeader().setFixedHeight(48)          # header height
        except Exception:
            pass

        # Hide vertical row numbers
        try:
            self.table.verticalHeader().setVisible(False)
        except Exception:
            pass

        # # selection behavior: select whole rows
        # try:
        #     self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        # except Exception:
        #     pass

        # # optional alternating colors
        # try:
        #     self.table.setAlternatingRowColors(True)
        # except Exception:
        #     pass

        # Remove all borders/lines in table
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
        }
                                 
        QHeaderView::section {
            border: none;
            background: transparent;
            padding-left: 12px;   /* <--- Adjust this to match cell padding */
        }

        """)


    # ----------------------------------------------------------------------------
    # Example action handlers - replace with your real logic
    def edit_student(self, student_id):
        print("Edit student:", student_id)
        # TODO: open edit dialog or navigate to edit screen
        # e.g. self.stackedWidget.setCurrentIndex(2)

    def delete_student(self, student_id):
        print("Delete student:", student_id)
        # TODO: confirm then remove from DB and refresh table

    def view_guardian(self, student_id):
        print("View guardian for:", student_id)
        # TODO: open guardian view modal / page

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
    win = AdminWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
