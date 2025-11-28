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


class StudentWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI into QMainWindow
        uic.loadUi(UI_FILE, self)

        # ----------------------------
        # Stacked widget navigation
        # ----------------------------
        try:
            self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
            self.mainStudentPage = self.findChild(QtWidgets.QWidget, "mainStudentPage")
            self.enrollStudentPage = self.findChild(QtWidgets.QWidget, "enrollStudentPage")
            self.verificationPage = self.findChild(QtWidgets.QWidget, "verificationPage")
            self.confirmationPage = self.findChild(QtWidgets.QWidget, "confirmationPage")
            self.editStudentPage = self.findChild(QtWidgets.QWidget, "editStudentPage")
            self.viewGuardianPage = self.findChild(QtWidgets.QWidget, "viewGuardianPage")
            self.addGuardianPage = self.findChild(QtWidgets.QWidget, "addGuardianPage")
            self.editGuardianPage = self.findChild(QtWidgets.QWidget, "editGuardianPage")

            # set initial page to mainStudentPage
            if self.stacked and self.mainStudentPage:
                self.stacked.setCurrentWidget(self.mainStudentPage)

            # navigation buttons
            self.enrolStudBtn = self.findChild(QtWidgets.QPushButton, "enrollStudBtn")
            self.backToMainBtn = self.findChild(QtWidgets.QPushButton, "backToMainBtn")
            self.enrollBtn = self.findChild(QtWidgets.QPushButton, "enrollBtn")
            self.backToInputBtn = self.findChild(QtWidgets.QPushButton, "backToInputBtn")
            self.confirmBtn = self.findChild(QtWidgets.QPushButton, "confirmBtn")
            self.saveEditBtn = self.findChild(QtWidgets.QPushButton, "saveEditmBtn")
            self.backToMainBtn_3 = self.findChild(QtWidgets.QPushButton, "backToMainBtn_3")
            self.backToMainBtn_2 = self.findChild(QtWidgets.QPushButton, "backToMainBtn_2")
            self.backToViewGuardianBtn = self.findChild(QtWidgets.QPushButton, "backToViewGuardianBtn")
            self.backToViewGuardianBtn_2 = self.findChild(QtWidgets.QPushButton, "backToViewGuardianBtn_2")
            self.addBtn = self.findChild(QtWidgets.QPushButton, "addBtn")
            self.saveEditBtn_2 = self.findChild(QtWidgets.QPushButton, "saveEditmBtn_2")
            self.addGuardianBtn = self.findChild(QtWidgets.QPushButton, "addGuardianBtn")

            # connect buttons (only if both button and target page exist)
            if self.enrolStudBtn and self.enrollStudentPage:
                self.enrolStudBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.enrollStudentPage)
                )

            if self.backToMainBtn and self.mainStudentPage:
                self.backToMainBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
                )
            if self.backToMainBtn_2 and self.mainStudentPage:
                self.backToMainBtn_2.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
                )
            if self.backToMainBtn_3 and self.mainStudentPage:
                self.backToMainBtn_3.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
                )

            if self.enrollBtn and self.verificationPage:
                self.enrollBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.verificationPage)
                )

            if self.backToInputBtn and self.enrollStudentPage:
                self.backToInputBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.enrollStudentPage)
                )

            if self.confirmBtn and self.confirmationPage:
                self.confirmBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.confirmationPage)
                )

            if self.saveEditBtn and self.mainStudentPage:
                self.saveEditBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
                )

            # Guardian page navigation (best guess from names)
            if self.addBtn and self.addGuardianPage:
                self.addBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.addGuardianPage)
                )

            if self.backToViewGuardianBtn and self.viewGuardianPage:
                self.backToViewGuardianBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.viewGuardianPage)
                )

            if self.backToViewGuardianBtn_2 and self.viewGuardianPage:
                self.backToViewGuardianBtn_2.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.viewGuardianPage)
                )

            if self.saveEditBtn_2 and self.viewGuardianPage:
                self.saveEditBtn_2.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.viewGuardianPage)
                )

            if self.addGuardianBtn and self.addGuardianPage:
                self.addGuardianBtn.clicked.connect(
                    lambda: self.stacked.setCurrentWidget(self.addGuardianPage)
                )

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

        # STUDENT TABLE
        self.studentTable = self.findChild(QtWidgets.QTableWidget, "studentTable")

        if self.studentTable is None:
            print("Warning: studentTable not found")
        else:
            if self.studentTable.columnCount() < 3:
                self.studentTable.setColumnCount(3)
                self.studentTable.setHorizontalHeaderLabels(["ID", "Name", "Actions"])

            self.setup_table(self.studentTable)

            sample_students = [
                {"id": "S001", "name": "Name of student 1"},
                {"id": "S002", "name": "Name of student 2"},
                {"id": "S003", "name": "Name of student 3"},
                {"id": "S004", "name": "Name of student 4"},
                {"id": "S005", "name": "Name of student 5"},
            ]

            for s in sample_students:
                self.add_student_row(s["id"], s["name"])

        # GUARDIAN TABLE
        self.guardianTable = self.findChild(QtWidgets.QTableWidget, "guardianTable")

        if self.guardianTable is None:
            print("Warning: guardianTable not found")
        else:
            if self.guardianTable.columnCount() < 3:
                self.guardianTable.setColumnCount(3)
                self.guardianTable.setHorizontalHeaderLabels(["ID", "Name", "Actions"])

            self.setup_table(self.guardianTable)

            sample_guardians = [
                {"id": "G001", "name": "Guardian 1"},
                {"id": "G002", "name": "Guardian 2"},
                {"id": "G003", "name": "Guardian 3"},
                {"id": "G004", "name": "Guardian 4"},
                {"id": "G005", "name": "Guardian 5"},
            ]

            for g in sample_guardians:
                self.add_guardian_row(g["id"], g["name"])

    # ----------------------------------------------------------------------------
    # Row creators
    # ----------------------------------------------------------------------------
    def add_student_row(self, student_id, name):
        """
        Student table: Edit, Delete, View Guardian
        """
        self._add_row_common(
            table=self.studentTable,
            record_id=student_id,
            name=name,
            include_view_btn=True,
            is_guardian=False,
        )

    def add_guardian_row(self, guardian_id, name):
        """
        Guardian table: Edit, Delete
        """
        self._add_row_common(
            table=self.guardianTable,
            record_id=guardian_id,
            name=name,
            include_view_btn=False,
            is_guardian=True,
        )

    def _add_row_common(self, table, record_id, name, include_view_btn: bool, is_guardian: bool):
        """
        Internal helper to create a row with:
          column 0: ID
          column 1: Name
          column 2: Actions (buttons)
        """
        if table is None:
            return

        row = table.rowCount()
        table.insertRow(row)

        # ID cell
        item_id = QTableWidgetItem(f"{record_id}")
        item_id.setFlags(item_id.flags() ^ Qt.ItemFlag.ItemIsEditable)
        item_id.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        table.setItem(row, 0, item_id)

        # Name cell
        item_name = QTableWidgetItem(f"{name}")
        item_name.setFlags(item_name.flags() ^ Qt.ItemFlag.ItemIsEditable)
        item_name.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        table.setItem(row, 1, item_name)

        # Actions cell widget
        action_cell = QWidget()
        h = QHBoxLayout(action_cell)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        h.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Always Edit + Delete
        edit_btn = QPushButton("Edit")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setFixedHeight(30)

        delete_btn = QPushButton("Delete")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedHeight(30)

        buttons = [edit_btn, delete_btn]

        # Only for student table: View Guardian
        view_btn = None
        if include_view_btn:
            view_btn = QPushButton("View Guardian")
            view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            view_btn.setFixedHeight(30)
            buttons.append(view_btn)

        # Font + style
        btn_font = edit_btn.font()
        btn_font.setPointSize(13)
        btn_font.setUnderline(True)

        for btn in buttons:
            btn.setFont(btn_font)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    color: #333333;
                }
                QPushButton:hover {
                    color: #8b2fdb;
                }
            """)
            h.addWidget(btn)

        # Connect signals
        if is_guardian:
            edit_btn.clicked.connect(lambda checked=False, gid=record_id: self.edit_guardian(gid))
            delete_btn.clicked.connect(lambda checked=False, gid=record_id: self.delete_guardian(gid))
        else:
            edit_btn.clicked.connect(lambda checked=False, sid=record_id: self.edit_student(sid))
            delete_btn.clicked.connect(lambda checked=False, sid=record_id: self.delete_student(sid))

        if view_btn is not None:
            view_btn.clicked.connect(lambda checked=False, sid=record_id: self.view_guardian(sid))

        table.setCellWidget(row, 2, action_cell)

    # ----------------------------------------------------------------------------
    # function to make the table responsive / stretch columns evenly
    def setup_table(self, table):
        if table is None:
            return

        # Make table adjust to contents policy (optional)
        try:
            table.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
            )
        except Exception:
            pass

        # Increase font size for better readability
        try:
            font = table.font()
            font.setPointSize(13)
            table.setFont(font)
        except Exception:
            pass

        header = table.horizontalHeader()
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

        # Widen ID column
        try:
            table.setColumnWidth(0, 150)
        except Exception:
            pass

        # Widen Actions column
        try:
            table.setColumnWidth(2, 300)
        except Exception:
            pass

        # Set row and header heights
        try:
            table.verticalHeader().setDefaultSectionSize(54)
        except Exception:
            pass
        try:
            table.horizontalHeader().setFixedHeight(48)
        except Exception:
            pass

        # Hide vertical row numbers
        try:
            table.verticalHeader().setVisible(False)
        except Exception:
            pass

        # Remove all borders/lines in table
        table.setStyleSheet("""
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
    # Action handlers
    # ----------------------------------------------------------------------------
    def edit_student(self, student_id):
        print("Edit student:", student_id)
        try:
            if self.stacked and self.editStudentPage:
                self.stacked.setCurrentWidget(self.editStudentPage)
        except Exception:
            pass

    def delete_student(self, student_id):
        print("Delete student:", student_id)
        # TODO: confirm then remove from DB and refresh table

    def view_guardian(self, student_id):
        print("View guardian for student:", student_id)
        try:
            if self.stacked and self.viewGuardianPage:
                self.stacked.setCurrentWidget(self.viewGuardianPage)
        except Exception:
            pass

    def edit_guardian(self, guardian_id):
        print("Edit guardian:", guardian_id)
        try:
            if self.stacked and self.editGuardianPage:
                self.stacked.setCurrentWidget(self.editGuardianPage)
        except Exception:
            pass

    def delete_guardian(self, guardian_id):
        print("Delete guardian:", guardian_id)
        # TODO: confirm then remove from DB and refresh table

    # ----------------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize background to fill area
        try:
            cw = self.findChild(QtWidgets.QWidget, "centralwidget")
            scaled_bg = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._bg_label.setPixmap(scaled_bg)
            self._bg_label.resize(cw.size())
            self._bg_label.move(0, 0)
        except Exception:
            pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = StudentWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
