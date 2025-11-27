# import sys
# from os import path
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "student.ui")
# BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


# class StudentWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Load UI into QMainWindow
#         uic.loadUi(UI_FILE, self)

#         # ----------------------------
#         # Stacked widget navigation
#         # ----------------------------
#         try:
#             self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
#             self.mainStudentPage = self.findChild(QtWidgets.QWidget, "mainStudentPage")
#             self.enrollStudentPage = self.findChild(QtWidgets.QWidget, "enrollStudentPage")
#             self.verificationPage = self.findChild(QtWidgets.QWidget, "verificationPage")
#             self.confirmationPage = self.findChild(QtWidgets.QWidget, "confirmationPage")
#             self.editStudentPage = self.findChild(QtWidgets.QWidget, "editStudentPage")
#             self.viewGuardianPage = self.findChild(QtWidgets.QWidget, "viewGuardianPage")
#             self.addGuardianPage = self.findChild(QtWidgets.QWidget, "addGuardianPage")
#             self.editGuardianPage = self.findChild(QtWidgets.QWidget, "editGuardianPage")

#             # set initial page to mainStudentPage
#             if self.stacked and self.mainStudentPage:
#                 self.stacked.setCurrentWidget(self.mainStudentPage)

#             # navigation buttons
#             self.enrolStudBtn = self.findChild(QtWidgets.QPushButton, "enrollStudBtn")
#             self.backToMainBtn = self.findChild(QtWidgets.QPushButton, "backToMainBtn")
#             self.enrollBtn = self.findChild(QtWidgets.QPushButton, "enrollBtn")
#             self.backToInputBtn = self.findChild(QtWidgets.QPushButton, "backToInputBtn")
#             self.confirmBtn = self.findChild(QtWidgets.QPushButton, "confirmBtn")
#             self.saveEditBtn = self.findChild(QtWidgets.QPushButton, "saveEditmBtn")
#             self.backToMainBtn_3 = self.findChild(QtWidgets.QPushButton, "backToMainBtn_3")
#             self.backToMainBtn_2 = self.findChild(QtWidgets.QPushButton, "backToMainBtn_2")
#             self.backToViewGuardianBtn = self.findChild(QtWidgets.QPushButton, "backToViewGuardianBtn")
#             self.backToViewGuardianBtn_2 = self.findChild(QtWidgets.QPushButton, "backToViewGuardianBtn_2")
#             self.addBtn = self.findChild(QtWidgets.QPushButton, "addBtn")
#             self.saveEditBtn_2 = self.findChild(QtWidgets.QPushButton, "saveEditmBtn_2")
#             self.addGuardianBtn = self.findChild(QtWidgets.QPushButton, "addGuardianBtn")

#             # connect buttons (only if both button and target page exist)
#             if self.enrolStudBtn and self.enrollStudentPage:
#                 self.enrolStudBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.enrollStudentPage)
#                 )

#             if self.backToMainBtn and self.mainStudentPage:
#                 self.backToMainBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
#                 )
#             if self.backToMainBtn_2 and self.mainStudentPage:
#                 self.backToMainBtn_2.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
#                 )
#             if self.backToMainBtn_3 and self.mainStudentPage:
#                 self.backToMainBtn_3.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
#                 )

#             if self.enrollBtn and self.verificationPage:
#                 self.enrollBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.verificationPage)
#                 )

#             if self.backToInputBtn and self.enrollStudentPage:
#                 self.backToInputBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.enrollStudentPage)
#                 )

#             if self.confirmBtn and self.confirmationPage:
#                 self.confirmBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.confirmationPage)
#                 )

#             if self.saveEditBtn and self.mainStudentPage:
#                 self.saveEditBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.mainStudentPage)
#                 )

#             # Guardian page navigation (best guess from names)
#             if self.addBtn and self.addGuardianPage:
#                 self.addBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.addGuardianPage)
#                 )

#             if self.backToViewGuardianBtn and self.viewGuardianPage:
#                 self.backToViewGuardianBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.viewGuardianPage)
#                 )

#             if self.backToViewGuardianBtn_2 and self.viewGuardianPage:
#                 self.backToViewGuardianBtn_2.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.viewGuardianPage)
#                 )

#             if self.saveEditBtn_2 and self.viewGuardianPage:
#                 self.saveEditBtn_2.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.viewGuardianPage)
#                 )

#             if self.addGuardianBtn and self.addGuardianPage:
#                 self.addGuardianBtn.clicked.connect(
#                     lambda: self.stacked.setCurrentWidget(self.addGuardianPage)
#                 )

#         except Exception:
#             # ignore if stacked-widget/pages/buttons are not present
#             pass

#         # --- Background image using QLabel (behind everything) ---
#         cw = self.findChild(QtWidgets.QWidget, "centralwidget")
#         self._bg_label = QtWidgets.QLabel(cw)
#         self._bg_pix = QPixmap(BG_FILE)
#         self._bg_label.setPixmap(self._bg_pix)
#         self._bg_label.setScaledContents(False)
#         self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
#         self._bg_label.lower()
#         self._bg_label.resize(cw.size())

#         # STUDENT TABLE
#         self.studentTable = self.findChild(QtWidgets.QTableWidget, "studentTable")

#         if self.studentTable is None:
#             print("Warning: studentTable not found")
#         else:
#             if self.studentTable.columnCount() < 3:
#                 self.studentTable.setColumnCount(3)
#                 self.studentTable.setHorizontalHeaderLabels(["ID", "Name", "Actions"])

#             self.setup_table(self.studentTable)

#             sample_students = [
#                 {"id": "S001", "name": "Name of student 1"},
#                 {"id": "S002", "name": "Name of student 2"},
#                 {"id": "S003", "name": "Name of student 3"},
#                 {"id": "S004", "name": "Name of student 4"},
#                 {"id": "S005", "name": "Name of student 5"},
#             ]

#             for s in sample_students:
#                 self.add_student_row(s["id"], s["name"])

#         # GUARDIAN TABLE
#         self.guardianTable = self.findChild(QtWidgets.QTableWidget, "guardianTable")

#         if self.guardianTable is None:
#             print("Warning: guardianTable not found")
#         else:
#             if self.guardianTable.columnCount() < 3:
#                 self.guardianTable.setColumnCount(3)
#                 self.guardianTable.setHorizontalHeaderLabels(["ID", "Name", "Actions"])

#             self.setup_table(self.guardianTable)

#             sample_guardians = [
#                 {"id": "G001", "name": "Guardian 1"},
#                 {"id": "G002", "name": "Guardian 2"},
#                 {"id": "G003", "name": "Guardian 3"},
#                 {"id": "G004", "name": "Guardian 4"},
#                 {"id": "G005", "name": "Guardian 5"},
#             ]

#             for g in sample_guardians:
#                 self.add_guardian_row(g["id"], g["name"])

#     # ----------------------------------------------------------------------------
#     # Row creators
#     # ----------------------------------------------------------------------------
#     def add_student_row(self, student_id, name):
#         """
#         Student table: Edit, Delete, View Guardian
#         """
#         self._add_row_common(
#             table=self.studentTable,
#             record_id=student_id,
#             name=name,
#             include_view_btn=True,
#             is_guardian=False,
#         )

#     def add_guardian_row(self, guardian_id, name):
#         """
#         Guardian table: Edit, Delete
#         """
#         self._add_row_common(
#             table=self.guardianTable,
#             record_id=guardian_id,
#             name=name,
#             include_view_btn=False,
#             is_guardian=True,
#         )

#     def _add_row_common(self, table, record_id, name, include_view_btn: bool, is_guardian: bool):
#         """
#         Internal helper to create a row with:
#           column 0: ID
#           column 1: Name
#           column 2: Actions (buttons)
#         """
#         if table is None:
#             return

#         row = table.rowCount()
#         table.insertRow(row)

#         # ID cell
#         item_id = QTableWidgetItem(f"{record_id}")
#         item_id.setFlags(item_id.flags() ^ Qt.ItemFlag.ItemIsEditable)
#         item_id.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
#         table.setItem(row, 0, item_id)

#         # Name cell
#         item_name = QTableWidgetItem(f"{name}")
#         item_name.setFlags(item_name.flags() ^ Qt.ItemFlag.ItemIsEditable)
#         item_name.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
#         table.setItem(row, 1, item_name)

#         # Actions cell widget
#         action_cell = QWidget()
#         h = QHBoxLayout(action_cell)
#         h.setContentsMargins(0, 0, 0, 0)
#         h.setSpacing(8)
#         h.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

#         # Always Edit + Delete
#         edit_btn = QPushButton("Edit")
#         edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
#         edit_btn.setFixedHeight(30)

#         delete_btn = QPushButton("Delete")
#         delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
#         delete_btn.setFixedHeight(30)

#         buttons = [edit_btn, delete_btn]

#         # Only for student table: View Guardian
#         view_btn = None
#         if include_view_btn:
#             view_btn = QPushButton("View Guardian")
#             view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
#             view_btn.setFixedHeight(30)
#             buttons.append(view_btn)

#         # Font + style
#         btn_font = edit_btn.font()
#         btn_font.setPointSize(13)
#         btn_font.setUnderline(True)

#         for btn in buttons:
#             btn.setFont(btn_font)
#             btn.setStyleSheet("""
#                 QPushButton {
#                     border: none;
#                     background: transparent;
#                     color: #333333;
#                 }
#                 QPushButton:hover {
#                     color: #8b2fdb;
#                 }
#             """)
#             h.addWidget(btn)

#         # Connect signals
#         if is_guardian:
#             edit_btn.clicked.connect(lambda checked=False, gid=record_id: self.edit_guardian(gid))
#             delete_btn.clicked.connect(lambda checked=False, gid=record_id: self.delete_guardian(gid))
#         else:
#             edit_btn.clicked.connect(lambda checked=False, sid=record_id: self.edit_student(sid))
#             delete_btn.clicked.connect(lambda checked=False, sid=record_id: self.delete_student(sid))

#         if view_btn is not None:
#             view_btn.clicked.connect(lambda checked=False, sid=record_id: self.view_guardian(sid))

#         table.setCellWidget(row, 2, action_cell)

#     # ----------------------------------------------------------------------------
#     # function to make the table responsive / stretch columns evenly
#     def setup_table(self, table):
#         if table is None:
#             return

#         # Make table adjust to contents policy (optional)
#         try:
#             table.setSizeAdjustPolicy(
#                 QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
#             )
#         except Exception:
#             pass

#         # Increase font size for better readability
#         try:
#             font = table.font()
#             font.setPointSize(13)
#             table.setFont(font)
#         except Exception:
#             pass

#         header = table.horizontalHeader()
#         # default: ID interactive so we can set a width, Name stretch, Actions Interactive
#         try:
#             header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Interactive)
#             header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
#             header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Interactive)
#         except Exception:
#             # fallback: stretch all
#             try:
#                 header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
#             except Exception:
#                 pass

#         # Widen ID column
#         try:
#             table.setColumnWidth(0, 150)
#         except Exception:
#             pass

#         # Widen Actions column
#         try:
#             table.setColumnWidth(2, 300)
#         except Exception:
#             pass

#         # Set row and header heights
#         try:
#             table.verticalHeader().setDefaultSectionSize(54)
#         except Exception:
#             pass
#         try:
#             table.horizontalHeader().setFixedHeight(48)
#         except Exception:
#             pass

#         # Hide vertical row numbers
#         try:
#             table.verticalHeader().setVisible(False)
#         except Exception:
#             pass

#         # Remove all borders/lines in table
#         table.setStyleSheet("""
#         QTableWidget {
#             gridline-color: transparent;
#             border: none;
#         }
#         QTableWidget::item {
#             border: none;
#             padding: 8px;
#         }
#         QHeaderView::section {
#             border: none;
#             background: transparent;
#             padding-left: 12px;
#         }
#         """)

#     # ----------------------------------------------------------------------------
#     # Action handlers
#     # ----------------------------------------------------------------------------
#     def edit_student(self, student_id):
#         print("Edit student:", student_id)
#         try:
#             if self.stacked and self.editStudentPage:
#                 self.stacked.setCurrentWidget(self.editStudentPage)
#         except Exception:
#             pass

#     def delete_student(self, student_id):
#         print("Delete student:", student_id)
#         # TODO: confirm then remove from DB and refresh table

#     def view_guardian(self, student_id):
#         print("View guardian for student:", student_id)
#         try:
#             if self.stacked and self.viewGuardianPage:
#                 self.stacked.setCurrentWidget(self.viewGuardianPage)
#         except Exception:
#             pass

#     def edit_guardian(self, guardian_id):
#         print("Edit guardian:", guardian_id)
#         try:
#             if self.stacked and self.editGuardianPage:
#                 self.stacked.setCurrentWidget(self.editGuardianPage)
#         except Exception:
#             pass

#     def delete_guardian(self, guardian_id):
#         print("Delete guardian:", guardian_id)
#         # TODO: confirm then remove from DB and refresh table

#     # ----------------------------------------------------------------------------
#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         # Resize background to fill area
#         try:
#             cw = self.findChild(QtWidgets.QWidget, "centralwidget")
#             scaled_bg = self._bg_pix.scaled(
#                 cw.size(),
#                 Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#                 Qt.TransformationMode.SmoothTransformation,
#             )
#             self._bg_label.setPixmap(scaled_bg)
#             self._bg_label.resize(cw.size())
#             self._bg_label.move(0, 0)
#         except Exception:
#             pass


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     win = StudentWindow()
#     win.show()
#     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()


import cv2
import face_recognition
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtGui import QImage
from PyQt6.QtCore import QTimer
import sys, os
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem

from controller.StudentController import StudentController

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "student.ui")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


class StudentWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.controller = StudentController()

        # Load UI
        uic.loadUi(UI_FILE, self)

        # SEARCH BAR
        self.searchStudent = self.findChild(QtWidgets.QLineEdit, "searchStudent")
        if self.searchStudent:
            self.searchStudent.textChanged.connect(self.apply_search)


        # STACKED PAGES
        self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.mainStudentPage = self.findChild(QtWidgets.QWidget, "mainStudentPage")
        self.enrollStudentPage = self.findChild(QtWidgets.QWidget, "enrollStudentPage")
        self.verificationPage = self.findChild(QtWidgets.QWidget, "verificationPage")
        self.confirmationPage = self.findChild(QtWidgets.QWidget, "confirmationPage")
        self.editStudentPage = self.findChild(QtWidgets.QWidget, "editStudentPage")
        self.viewGuardianPage = self.findChild(QtWidgets.QWidget, "viewGuardianPage")
        self.addGuardianPage = self.findChild(QtWidgets.QWidget, "addGuardianPage")
        self.editGuardianPage = self.findChild(QtWidgets.QWidget, "editGuardianPage")

        # DEFAULT PAGE
        self.stacked.setCurrentWidget(self.mainStudentPage)

        # ============= BUTTONS (old UI behavior) =============

        btn = self.findChild(QtWidgets.QPushButton, "enrollStudBtn")
        if btn:
            btn.clicked.connect(self.open_enroll_page)
            
        
        save_btn = self.findChild(QtWidgets.QPushButton, "saveEditBtn")
        if save_btn:
            save_btn.clicked.connect(self.save_student_changes)


        # All back buttons → mainStudentPage
        # True back to Dashboard
        btn = self.findChild(QtWidgets.QPushButton, "backToDashboardBtn")
        if btn:
            btn.clicked.connect(self.go_to_dashboard)

        # The rest go back to student main page
        for name in ["backToMainBtn", "backToMainBtn_2", "backToMainBtn_3", "goBacktoDasboardBtn"]:
            btn = self.findChild(QtWidgets.QPushButton, name)
            if btn:
                btn.clicked.connect(lambda _, p=self.mainStudentPage: self.stacked.setCurrentWidget(p))

        # Enrollment flow
        # btn = self.findChild(QtWidgets.QPushButton, "enrollBtn")
        # if btn:
        #     btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.verificationPage))

        btn = self.findChild(QtWidgets.QPushButton, "enrollBtn")
        if btn:
            btn.clicked.connect(self.validate_enroll_inputs)

        
        btn = self.findChild(QtWidgets.QPushButton, "backToInputBtn")
        if btn:
            btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.enrollStudentPage))

        btn = self.findChild(QtWidgets.QPushButton, "confirmBtn")
        if btn:
            btn.clicked.connect(self.finish_enrollment)

        self.addGuardianBtn.clicked.connect(self.open_add_guardian_page)
        self.addSaveBtn.clicked.connect(self.save_guardian)

        self.scanFaceBtn.clicked.connect(self.scan_guardian_face)
        self.retakeBtn.clicked.connect(self.retake_guardian_face)
        self.deleteBtn.clicked.connect(self.delete_scanned_face)

        
        # VIEW GUARDIAN PAGE
        self.guardianTable = self.findChild(QtWidgets.QTableWidget, "guardianTable")
        self.studentNameDisplay = self.findChild(QtWidgets.QLabel, "studentNameDisplay")

        self.newGuardianName = self.findChild(QtWidgets.QLineEdit, "newGuardianNameInput")
        self.newGuardianDOB = self.findChild(QtWidgets.QDateEdit, "newGuardianDOBInput")

        self.scanFaceBtn = self.findChild(QtWidgets.QPushButton, "scanFaceBtn")
        self.retakeBtn = self.findChild(QtWidgets.QPushButton, "retakeBtn")
        self.deleteBtn = self.findChild(QtWidgets.QPushButton, "deleteBtn")
        self.imgPlaceholder = self.findChild(QtWidgets.QLabel, "imgPlaceholder")

        self.addSaveBtn = self.findChild(QtWidgets.QPushButton, "addSaveBtn")
        self.addGuardianBtn = self.findChild(QtWidgets.QPushButton, "addGuardianBtn")


        # Tracks guardian data
        self.current_student_for_guardian = None
        self.current_guardian_image_path = None
        self.current_guardian_encoding = None

        
        # Guardian buttons
        guardian_routes = [
            ("addBtn", self.addGuardianPage),
            ("addGuardianBtn", self.addGuardianPage),
            ("backToViewGuardianBtn_2", self.viewGuardianPage),
        ]
        for name, page in guardian_routes:
            btn = self.findChild(QtWidgets.QPushButton, name)
            if btn:
                btn.clicked.connect(lambda _, p=page: self.stacked.setCurrentWidget(p))

        # ============= TABLE =============

        self.studentTable = self.findChild(QtWidgets.QTableWidget, "studentTable")
        self.setup_table(self.studentTable)
        self.load_students()

        # Background
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # ENROLL INPUTS
        self.studIDLabel = self.findChild(QtWidgets.QLabel, "studIDLabel")
        self.studFname = self.findChild(QtWidgets.QLineEdit, "studFnameInput")
        self.studMname = self.findChild(QtWidgets.QLineEdit, "studMnameInput")
        self.studLname = self.findChild(QtWidgets.QLineEdit, "studLnameInput")
        self.studDOB = self.findChild(QtWidgets.QDateEdit, "studDOBInput")
        self.studSex = self.findChild(QtWidgets.QComboBox, "studSexInput")
        self.contact = self.findChild(QtWidgets.QLineEdit, "contactInput")

        self.motherName = self.findChild(QtWidgets.QLineEdit, "motherNameInput")
        self.motherDOB = self.findChild(QtWidgets.QDateEdit, "motherDOBInput")
        self.fatherName = self.findChild(QtWidgets.QLineEdit, "fatherNameInput")
        self.fatherDOB = self.findChild(QtWidgets.QDateEdit, "fatherDOBInput")
        self.guardianName = self.findChild(QtWidgets.QLineEdit, "guardianNameInput")
        self.guardianDOB = self.findChild(QtWidgets.QDateEdit, "guardianDOBInput")

        self.guardianDOBEdit = self.findChild(QtWidgets.QDateEdit, "guardianDOBEdit")
        self.guardianDOBEdit.setSpecialValueText("")  # show blank if at minimum
        self.guardianDOBEdit.setDate(self.guardianDOBEdit.minimumDate())

        
        self.verifyCheck = self.findChild(QtWidgets.QCheckBox, "verifyCheck")
        self.confirmLabel = self.findChild(QtWidgets.QLabel, "confirmLabel")

    # =====================
    # TABLE SETTINGS
    # =====================
    def setup_table(self, table):
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Interactive)

        table.setColumnWidth(0, 150)
        table.setColumnWidth(2, 300)

        table.verticalHeader().setDefaultSectionSize(54)
        table.horizontalHeader().setFixedHeight(48)
        table.verticalHeader().setVisible(False)

        font = table.font()
        font.setPointSize(13)
        table.setFont(font)

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

    # =====================
    # LOAD STUDENTS
    # =====================
    def load_students(self):
        self.studentTable.setRowCount(0)
        students = self.controller.get_students(self.username)

        for s in students:
            fullname = f"{s['studlname']}, {s['studfname']} {s.get('studmname','')}"
            self.add_student_row(s["studid"], fullname)

    # =====================
    # ADD ROW + BUTTONS
    # =====================
    def add_student_row(self, student_id, name):
        row = self.studentTable.rowCount()
        self.studentTable.insertRow(row)

        id_item = QTableWidgetItem(student_id)
        id_item.setFlags(id_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.studentTable.setItem(row, 0, id_item)

        name_item = QTableWidgetItem(name)
        name_item.setFlags(name_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.studentTable.setItem(row, 1, name_item)

        action_cell = QWidget()
        layout = QHBoxLayout(action_cell)
        layout.setContentsMargins(0, 0, 0, 0)

        # Buttons
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        view_btn = QPushButton("View Guardian")

        for btn in (edit_btn, delete_btn, view_btn):
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    color: #333;
                }
                QPushButton:hover {
                    color: #8b2fdb;
                }
            """)
            layout.addWidget(btn)

        # CONNECTIONS (WORKING NOW)
        edit_btn.clicked.connect(lambda _, sid=student_id: self.edit_student(sid))
        delete_btn.clicked.connect(lambda _, sid=student_id: self.delete_student(sid))
        view_btn.clicked.connect(lambda _, sid=student_id: self.view_guardian(sid))

        self.studentTable.setCellWidget(row, 2, action_cell)

    # =====================
    # BUTTON HANDLERS
    # =====================
    def edit_student(self, studID):
        print("Editing student:", studID)

        # Fetch from DB
        student = self.controller.get_student(studID)
        if not student:
            QtWidgets.QMessageBox.warning(self, "Error", "Student not found.")
            return

        if student["guardiandob"] is None:
            self.guardianDOBEdit.setDate(self.guardianDOBEdit.minimumDate())
        else:
            self.guardianDOBEdit.setDate(student["guardiandob"])

        # Store current editing ID
        self.current_edit_id = studID

        # Populate fields
        self.findChild(QtWidgets.QLineEdit, "studFnameEdit").setText(student["studfname"])
        self.findChild(QtWidgets.QLineEdit, "studMnameEdit").setText(student["studmname"] or "")
        self.findChild(QtWidgets.QLineEdit, "studLnameEdit").setText(student["studlname"])
        self.findChild(QtWidgets.QDateEdit, "studDOBEdit").setDate(student["studdob"])
        self.findChild(QtWidgets.QComboBox, "studSexEdit").setCurrentText(student["studsex"])

        self.findChild(QtWidgets.QLineEdit, "motherNameEdit").setText(student["mothername"])
        self.findChild(QtWidgets.QDateEdit, "motherDOBEdit").setDate(student["motherdob"])

        self.findChild(QtWidgets.QLineEdit, "fatherNameEdit").setText(student["fathername"] or "")
        self.findChild(QtWidgets.QDateEdit, "fatherDOBEdit").setDate(student["fatherdob"])

        self.findChild(QtWidgets.QLineEdit, "guardianNameEdit").setText(student["guardianname"] or "")
        
        self.findChild(QtWidgets.QLineEdit, "contactInputEdit").setText(student["studcontact"])

        # Switch page
        self.stacked.setCurrentWidget(self.editStudentPage)

    def save_student_changes(self):
        # --- Required fields ---
        fname = self.findChild(QtWidgets.QLineEdit, "studFnameEdit").text().strip()
        lname = self.findChild(QtWidgets.QLineEdit, "studLnameEdit").text().strip()
        contact = self.findChild(QtWidgets.QLineEdit, "contactInputEdit").text().strip()

        errors = []
        if fname == "":
            errors.append("• First name is required.")
        if lname == "":
            errors.append("• Last name is required.")
        if contact == "":
            errors.append("• Emergency contact is required.")

        # If required fields missing → STOP & warn
        if errors:
            QtWidgets.QMessageBox.warning(
                self,
                "Missing Required Fields",
                "Please complete the following fields:\n\n" + "\n".join(errors)
            )
            return

        # --- Confirm saving ---
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm",
            "Are you sure you want to save the changes?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        # --- Prepare data ---
        data = {
            "studID": self.current_edit_id,
            "studFname": fname,
            "studMname": self.findChild(QtWidgets.QLineEdit, "studMnameEdit").text(),
            "studLname": lname,
            "studDOB": self.findChild(QtWidgets.QDateEdit, "studDOBEdit").text(),
            "studSex": self.findChild(QtWidgets.QComboBox, "studSexEdit").currentText(),
            "studContact": contact,
            "motherName": self.findChild(QtWidgets.QLineEdit, "motherNameEdit").text(),
            "motherDOB": (
                None 
                if self.findChild(QtWidgets.QLineEdit, "motherDOBEdit").text().strip() == "" 
                else self.findChild(QtWidgets.QDateEdit, "motherDOBEdit").text()
            ),
            "fatherName": self.findChild(QtWidgets.QLineEdit, "fatherNameEdit").text(),
            "fatherDOB": (
                None 
                if self.findChild(QtWidgets.QLineEdit, "fatherDOBEdit").text().strip() == "" 
                else self.findChild(QtWidgets.QDateEdit, "fatherDOBEdit").text()
            ),
            "guardianName": self.findChild(QtWidgets.QLineEdit, "guardianNameEdit").text(),
            "guardianDOB": (
                None 
                if self.findChild(QtWidgets.QLineEdit, "guardianNameEdit").text().strip() == "" 
                else self.findChild(QtWidgets.QDateEdit, "guardianDOBEdit").text()
            ),
        }

        # --- Save to DB ---
        self.controller.update_student(data)

        QtWidgets.QMessageBox.information(
            self,
            "Success",
            "Student information has been successfully updated!"
        )

        # Refresh table + go back
        self.load_students()
        self.stacked.setCurrentWidget(self.mainStudentPage)

    def delete_student(self, student_id):
        print("Deleting student:", student_id)
        # You will add deletion logic later

    def view_guardian(self, studid):
        from controller.GuardianController import GuardianController
        self.current_student_for_guardian = studid

        student = self.controller.get_student(studid)
        full = f"{student['studlname']}, {student['studfname']} {student['studmname'] or ''}"
        self.studentNameDisplay.setText(full)

        self.load_guardians_table(studid)
        self.stacked.setCurrentWidget(self.viewGuardianPage)



    # =====================
    # ENROLL
    # =====================
    def open_enroll_page(self):
        self.clear_enroll_fields()  # 🔥 CLEAR FIELDS FIRST

        new_id = self.controller.generate_student_id(self.username)
        self.studIDLabel.setText(new_id)

        self.stacked.setCurrentWidget(self.enrollStudentPage)

    def finish_enrollment(self):
        if not self.verifyCheck.isChecked():
            QtWidgets.QMessageBox.warning(self, "Error", "Please confirm verification.")
            return

        data = {
            "username": self.username,   # 🔥 REQUIRED FOR PROCEDURE
            "studID": self.studIDLabel.text(),
            "studLname": self.studLname.text(),
            "studFname": self.studFname.text(),
            "studMname": self.studMname.text(),
            "studDOB": self.studDOB.text(),
            "studSex": self.studSex.currentText(),
            "studContact": self.contact.text(),
            "motherName": self.motherName.text(),
            "motherDOB": None if self.motherName.text().strip() == "" else self.motherDOB.date().toString("yyyy-MM-dd"),
            "fatherName": self.fatherName.text(),
            "fatherDOB": None if self.fatherName.text().strip() == "" else self.fatherDOB.date().toString("yyyy-MM-dd"),
            "guardianName": self.guardianName.text(),
            "guardianDOB": None if self.guardianName.text().strip() == "" else self.guardianDOB.text(),
        }
        self.controller.insert_student(self.username, data)

        self.confirmLabel.setText(
            f"Student {data['studLname']}, {data['studFname']} {data['studMname']} "
            f"({data['studID']}) has been successfully enrolled."
        )

        self.stacked.setCurrentWidget(self.confirmationPage)
        self.load_students()
        
    
    def validate_enroll_inputs(self):
        fname = self.studFname.text().strip()
        lname = self.studLname.text().strip()
        contact = self.contact.text().strip()

        # Required field check
        errors = []

        if fname == "":
            errors.append("• First name is required.")
        if lname == "":
            errors.append("• Last name is required.")
        if contact == "":
            errors.append("• Contact / emergency contact is required.")

        # If ANY errors → show warning and STOP
        if errors:
            QtWidgets.QMessageBox.warning(
                self,
                "Missing Required Fields",
                "Please fill in the following:\n\n" + "\n".join(errors)
            )
            return

        # If all required fields are filled → continue normally
        self.stacked.setCurrentWidget(self.verificationPage)

        
    
    def apply_search(self):
        search = self.searchStudent.text().strip().lower()

        # Clear table
        self.studentTable.setRowCount(0)

        # Query DB
        students = self.controller.search_students(self.username, search)

        # Display
        for s in students:
            fullname = f"{s['studlname']}, {s['studfname']} {s.get('studmname','')}"
            self.add_student_row(s["studid"], fullname)

    def go_to_dashboard(self):
        from views.dashboard import AdminWindow  # safe import

        self.dashboard = AdminWindow(self.username)
        self.dashboard.show()
        self.close()

    def clear_enroll_fields(self):        
        self.studFname.clear()
        self.studMname.clear()
        self.studLname.clear()
        self.contact.clear()

        self.motherName.clear()
        self.fatherName.clear()
        self.guardianName.clear()

        # Reset dates to today (optional)
        self.studDOB.setDate(QDate.currentDate())
        self.motherDOB.setDate(QDate.currentDate())
        self.fatherDOB.setDate(QDate.currentDate())
        self.guardianDOB.setDate(QDate.currentDate())



        # Reset combo box (Male/Female)
        self.studSex.setCurrentIndex(0)

        # Uncheck verification
        self.verifyCheck.setChecked(False)



    def load_guardians_table(self, studid):
        from controller.GuardianController import GuardianController
        gc = GuardianController()

        data = gc.get_guardians_for_student(studid)
        table = self.guardianTable
        table.setRowCount(0)

        for g in data:
            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, 0, QTableWidgetItem(str(g["guardianid"])))
            table.setItem(row, 1, QTableWidgetItem(g["guardianname"]))

            # Actions
            action = QWidget()
            layout = QHBoxLayout(action)
            layout.setContentsMargins(0,0,0,0)

            edit_btn = QPushButton("Edit")
            delete_btn = QPushButton("Delete")

            edit_btn.clicked.connect(lambda _, id=g["guardianid"]: self.edit_guardian(id))
            delete_btn.clicked.connect(lambda _, id=g["guardianid"]: self.delete_guardian_record(id))

            layout.addWidget(edit_btn)
            layout.addWidget(delete_btn)
            table.setCellWidget(row, 2, action)



    def open_add_guardian_page(self):
        self.newGuardianName.clear()
        self.newGuardianDOB.setDate(QDate.currentDate())
        self.newGuardianDOB.setCalendarPopup(True)


        self.imgPlaceholder.clear()
        self.current_guardian_image_path = None
        self.current_guardian_encoding = None

        self.stacked.setCurrentWidget(self.addGuardianPage)

            
    
    def save_guardian(self):
        name = self.newGuardianName.text().strip()
        dob = self.newGuardianDOB.date().toString("yyyy-MM-dd")

        if name == "":
            QtWidgets.QMessageBox.warning(self, "Missing", "Guardian name is required.")
            return

        if not self.current_guardian_encoding:
            QtWidgets.QMessageBox.warning(self, "Missing", "Please scan the guardian’s face.")
            return

        from controller.GuardianController import GuardianController
        gc = GuardianController()

        encoded = gc.encode_face(self.current_guardian_encoding)

        gc.insert_guardian(
            studid=self.current_student_for_guardian,
            name=name,
            dob=dob,
            image_path=self.current_guardian_image_path,
            encoding=encoded
        )

        QtWidgets.QMessageBox.information(self, "Success", "Guardian added successfully!")

        self.load_guardians_table(self.current_student_for_guardian)
        self.stacked.setCurrentWidget(self.viewGuardianPage)



    def delete_guardian_record(self, guardianid):
        confirm = QtWidgets.QMessageBox.question(
            self, "Confirm", "Delete this guardian?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        from controller.GuardianController import GuardianController
        gc = GuardianController()
        gc.delete_guardian(guardianid)

        self.load_guardians_table(self.current_student_for_guardian)
    
    def scan_guardian_face(self):
        cam = CameraCapture()
        if cam.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # SAVE IMAGE
            folder = f"uploads/guardians"
            os.makedirs(folder, exist_ok=True)

            filename = f"{self.current_student_for_guardian}_{self.newGuardianName.text()}.jpg"
            filepath = os.path.join(folder, filename)

            cv2.imwrite(filepath, cam.captured_image)
            self.current_guardian_image_path = filepath

            # SAVE ENCODING
            self.current_guardian_encoding = cam.captured_encoding.tolist()

            # PREVIEW
            pixmap = QPixmap(filepath)
            self.imgPlaceholder.setPixmap(pixmap.scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

            QtWidgets.QMessageBox.information(self, "Success", "Face scanned successfully!")

    def retake_guardian_face(self):
        self.current_guardian_encoding = None

        if self.current_guardian_image_path and os.path.exists(self.current_guardian_image_path):
            os.remove(self.current_guardian_image_path)

        self.current_guardian_image_path = None
        self.imgPlaceholder.clear()

        self.scan_guardian_face()  # reopen webcam


    def delete_scanned_face(self):
        self.current_guardian_encoding = None

        if self.current_guardian_image_path and os.path.exists(self.current_guardian_image_path):
            os.remove(self.current_guardian_image_path)

        self.current_guardian_image_path = None
        self.imgPlaceholder.clear()




class CameraCapture(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan Guardian Face")
        self.resize(600, 500)

        self.video_label = QLabel()
        self.video_label.setFixedSize(560, 420)

        self.capture_btn = QPushButton("Capture")
        self.capture_btn.clicked.connect(self.capture_frame)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.capture_btn)
        self.setLayout(layout)

        self.cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

        self.captured_encoding = None
        self.captured_image = None

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

        self.current_frame = frame

    def capture_frame(self):
        frame = self.current_frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)

        if len(locations) == 0:
            QtWidgets.QMessageBox.warning(self, "No Face", "No face detected. Try again.")
            return

        encoding = face_recognition.face_encodings(rgb, locations)[0]
        self.captured_encoding = encoding
        self.captured_image = frame

        self.accept()

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()