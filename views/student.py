import cv2
import face_recognition
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt, QDate
import os
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem
from utils.paths import app_dir


from controller.StudentController import StudentController

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "student.ui")
# BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")
BASE = app_dir()
UI_FILE = os.path.join(BASE, "ui", "student.ui")
BG_FILE = os.path.join(BASE, "assets", "images", "bg1.png")
GUARDIAN_DIR_ABS = os.path.join(app_dir(), "uploads", "guardians")


class StudentWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.controller = StudentController()

        uic.loadUi(UI_FILE, self)
        self.resize(1250, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())

        # Background
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # Search bar
        self.searchStudent = self.findChild(QtWidgets.QLineEdit, "searchStudent")
        if self.searchStudent:
            self.searchStudent.textChanged.connect(self.apply_search)

        # Stacked pages
        self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.mainStudentPage = self.findChild(QtWidgets.QWidget, "mainStudentPage")
        self.enrollStudentPage = self.findChild(QtWidgets.QWidget, "enrollStudentPage")
        self.verificationPage = self.findChild(QtWidgets.QWidget, "verificationPage")
        self.confirmationPage = self.findChild(QtWidgets.QWidget, "confirmationPage")
        self.editStudentPage = self.findChild(QtWidgets.QWidget, "editStudentPage")
        self.viewGuardianPage = self.findChild(QtWidgets.QWidget, "viewGuardianPage")
        self.addGuardianPage = self.findChild(QtWidgets.QWidget, "addGuardianPage")
        self.editGuardianPage = self.findChild(QtWidgets.QWidget, "editGuardianPage")

        self.stacked.setCurrentWidget(self.mainStudentPage)

        # Buttons
        btn = self.findChild(QtWidgets.QPushButton, "enrollStudBtn")
        if btn:
            btn.clicked.connect(self.open_enroll_page)

        save_btn = self.findChild(QtWidgets.QPushButton, "saveEditBtn")
        if save_btn:
            save_btn.clicked.connect(self.save_student_changes)

        btn = self.findChild(QtWidgets.QPushButton, "backToDashboardBtn")
        if btn:
            btn.clicked.connect(self.go_to_dashboard)

        for name in ["backToMainBtn", "backToMainBtn_2", "backToMainBtn_3", "goBacktoDasboardBtn"]:
            btn = self.findChild(QtWidgets.QPushButton, name)
            if btn:
                btn.clicked.connect(lambda _, p=self.mainStudentPage: self.stacked.setCurrentWidget(p))

        btn = self.findChild(QtWidgets.QPushButton, "enrollBtn")
        if btn:
            btn.clicked.connect(self.validate_enroll_inputs)

        btn = self.findChild(QtWidgets.QPushButton, "backToInputBtn")
        if btn:
            btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.enrollStudentPage))

        btn = self.findChild(QtWidgets.QPushButton, "confirmBtn")
        if btn:
            btn.clicked.connect(self.finish_enrollment)

        delete_view_btn = self.findChild(QtWidgets.QPushButton, "deleteBtn_2")
        if delete_view_btn:
            delete_view_btn.clicked.connect(self.delete_guardian_view)

        back_view_btn = self.findChild(QtWidgets.QPushButton, "backToViewGuardianBtn")
        if back_view_btn:
            back_view_btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.viewGuardianPage))

        self.scanFaceBtn = self.findChild(QtWidgets.QPushButton, "scanFaceBtn")
        self.retakeBtn = self.findChild(QtWidgets.QPushButton, "retakeBtn")
        self.deleteBtn = self.findChild(QtWidgets.QPushButton, "deleteBtn")

        self.addGuardianBtn = self.findChild(QtWidgets.QPushButton, "addGuardianBtn")
        self.addSaveBtn = self.findChild(QtWidgets.QPushButton, "addSaveBtn")

        self.scanFaceBtn.clicked.connect(self.scan_guardian_face)
        self.retakeBtn.clicked.connect(self.retake_guardian_face)
        self.deleteBtn.clicked.connect(self.delete_scanned_face)
        self.addGuardianBtn.clicked.connect(self.open_add_guardian_page)
        self.addSaveBtn.clicked.connect(self.save_guardian)

        save_edit_btn = self.findChild(QtWidgets.QPushButton, "saveEditBtn_2")
        if save_edit_btn:
            save_edit_btn.clicked.connect(self.save_edit_guardian)

        guardian_routes = [
            ("addBtn", self.addGuardianPage),
            ("addGuardianBtn", self.addGuardianPage),
            ("backToViewGuardianBtn_2", self.viewGuardianPage),
        ]
        for name, page in guardian_routes:
            btn = self.findChild(QtWidgets.QPushButton, name)
            if btn:
                btn.clicked.connect(lambda _, p=page: self.stacked.setCurrentWidget(p))

        # Tables
        self.studentTable = self.findChild(QtWidgets.QTableWidget, "studentTable")
        self.setup_table(self.studentTable)

        self.guardianTable = self.findChild(QtWidgets.QTableWidget, "guardianTable")
        if self.guardianTable:
            self.setup_table(self.guardianTable)

        self.studentNameDisplay = self.findChild(QtWidgets.QLabel, "studentNameDisplay")

        # Inputs
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
        self.guardianDOBEdit.setSpecialValueText("")
        self.guardianDOBEdit.setDate(self.guardianDOBEdit.minimumDate())

        self.verifyCheck = self.findChild(QtWidgets.QCheckBox, "verifyCheck")
        self.confirmLabel = self.findChild(QtWidgets.QLabel, "confirmLabel")

        # Guardian fields
        self.newGuardianName = self.findChild(QtWidgets.QLineEdit, "newGuardianNameInput")
        self.newGuardianDOB = self.findChild(QtWidgets.QDateEdit, "newGuardianDOBInput")
        self.imgPlaceholder = self.findChild(QtWidgets.QLabel, "imgPlaceholder")

        self.current_student_for_guardian = None
        self.current_guardian_image_path = None
        self.current_guardian_encoding = None

        self.load_students()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "_bg_label") and hasattr(self, "_bg_pix"):
            cw = self.findChild(QtWidgets.QWidget, "centralwidget")
            scaled = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._bg_label.setPixmap(scaled)
            self._bg_label.resize(cw.size())

    def setup_table(self, table):
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Interactive)

        table.setColumnWidth(0, 150)
        table.setColumnWidth(2, 350)

        table.verticalHeader().setDefaultSectionSize(54)
        table.horizontalHeader().setFixedHeight(48)
        table.verticalHeader().setVisible(False)

        font = table.font()
        font.setPointSize(15)
        table.setFont(font)

        last_col = table.columnCount() - 1
        if last_col >= 0:
            item = table.horizontalHeaderItem(last_col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        table.setStyleSheet("""
        QTableWidget { gridline-color: transparent; border: none; }
        QTableWidget::item { border: none; padding: 8px; }
        QHeaderView::section { border: none; background: transparent; padding-left: 12px; }
        QHeaderView::section:last { padding-left: 0px; }
        """)

    def load_students(self):
        self.studentTable.setRowCount(0)
        students = self.controller.get_students(self.username)
        for s in students:
            fullname = f"{s['studlname']}, {s['studfname']} {s.get('studmname','')}"
            self.add_student_row(s["studid"], fullname)

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
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
                    font-size: 15px;
                }
                QPushButton:hover { color: #8b2fdb; }
            """)
            layout.addWidget(btn)

        edit_btn.clicked.connect(lambda _, sid=student_id: self.edit_student(sid))
        delete_btn.clicked.connect(lambda _, sid=student_id: self.delete_student(sid))
        view_btn.clicked.connect(lambda _, sid=student_id: self.view_guardian(sid))

        self.studentTable.setCellWidget(row, 2, action_cell)

    # def edit_student(self, studID):
    #     student = self.controller.get_student(studID)
    #     if not student:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Student not found.")
    #         return
    
    def edit_student(self, studID):
        student = self.controller.get_student(self.username, studID)
        if not student:
            QtWidgets.QMessageBox.warning(self, "Error", "Student not found.")
            return

        self.current_edit_id = studID


        self.findChild(QtWidgets.QLineEdit, "studFnameEdit").setText(student["studfname"])
        self.findChild(QtWidgets.QLineEdit, "studMnameEdit").setText(student["studmname"] or "")
        self.findChild(QtWidgets.QLineEdit, "studLnameEdit").setText(student["studlname"])
        self.findChild(QtWidgets.QLineEdit, "contactInputEdit").setText(student["studcontact"])
        self.findChild(QtWidgets.QComboBox, "studSexEdit").setCurrentText(student["studsex"])

        self.set_safe_date("studDOBEdit", student["studdob"])
        self.set_safe_date("motherDOBEdit", student["motherdob"])
        self.set_safe_date("fatherDOBEdit", student["fatherdob"])
        self.set_safe_date("guardianDOBEdit", student["guardiandob"])

        self.findChild(QtWidgets.QLineEdit, "motherNameEdit").setText(student["mothername"] or "")
        self.findChild(QtWidgets.QLineEdit, "fatherNameEdit").setText(student["fathername"] or "")
        self.findChild(QtWidgets.QLineEdit, "guardianNameEdit").setText(student["guardianname"] or "")

        self.stacked.setCurrentWidget(self.editStudentPage)

    def set_safe_date(self, name, value):
        widget = self.findChild(QtWidgets.QDateEdit, name)
        if widget is None:
            return
        if value is None:
            widget.setDate(widget.minimumDate())
        else:
            widget.setDate(value)

    def save_student_changes(self):
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

        if errors:
            QtWidgets.QMessageBox.warning(
                self,
                "Missing Required Fields",
                "Please complete:\n\n" + "\n".join(errors)
            )
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm",
            "Save changes?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        data = {
            "username": self.username,   # ✅ NEW
            "studID": self.current_edit_id,
            "studFname": fname,
            "studMname": self.findChild(QtWidgets.QLineEdit, "studMnameEdit").text(),
            "studLname": lname,
            "studDOB": self.get_safe_date("studDOBEdit"),
            "studSex": self.findChild(QtWidgets.QComboBox, "studSexEdit").currentText(),
            "studContact": contact,
            "motherName": self.findChild(QtWidgets.QLineEdit, "motherNameEdit").text(),
            "motherDOB": self.get_safe_date("motherDOBEdit"),
            "fatherName": self.findChild(QtWidgets.QLineEdit, "fatherNameEdit").text(),
            "fatherDOB": self.get_safe_date("fatherDOBEdit"),
            "guardianName": self.findChild(QtWidgets.QLineEdit, "guardianNameEdit").text(),
            "guardianDOB": self.get_safe_date("guardianDOBEdit"),
        }

        self.controller.update_student(data)
        QtWidgets.QMessageBox.information(self, "Success", "Student updated successfully!")
        self.load_students()
        self.stacked.setCurrentWidget(self.mainStudentPage)


    def get_safe_date(self, name):
        widget = self.findChild(QtWidgets.QDateEdit, name)
        if widget is None:
            return None

        date = widget.date()
        if date == widget.minimumDate():
            return None
        return date.toString("yyyy-MM-dd")
    
    def delete_student(self, student_code):
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete student {student_code}?\nThis also removes all guardians.",
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        from controller.GuardianController import GuardianController
        gc = GuardianController()

        # map studid code → studentid
        student = self.controller.get_student(self.username, student_code)
        if not student:
            QtWidgets.QMessageBox.warning(self, "Error", "Student not found.")
            return

        real_id = student["studentid"]
        guardians = gc.get_guardians_for_student(real_id)

        for g in guardians:
            # path = g["face_image_path"]
            # if path and os.path.exists(path):
            #     os.remove(path)
            # from controller.GuardianController import GuardianController
            # gc = GuardianController()

            db_path = g["face_image_path"]
            abs_path = gc.to_abs_path(db_path) if db_path else None

            if abs_path and os.path.exists(abs_path):
                os.remove(abs_path)

        self.controller.delete_student(self.username, student_code)

        QtWidgets.QMessageBox.information(self, "Deleted", "Student & guardians deleted.")
        self.load_students()


    def view_guardian(self, studid):
        from controller.GuardianController import GuardianController
        self.current_student_for_guardian = studid  # studid code (S001)

        student = self.controller.get_student(self.username, studid)
        full = f"{student['studlname']}, {student['studfname']} {student['studmname'] or ''}"
        self.studentNameDisplay.setText(full)

        self.load_guardians_table(studid)
        self.stacked.setCurrentWidget(self.viewGuardianPage)


    def open_enroll_page(self):
        self.clear_enroll_fields()
        new_id = self.controller.generate_student_id(self.username)
        self.studIDLabel.setText(new_id)
        self.stacked.setCurrentWidget(self.enrollStudentPage)

    def finish_enrollment(self):
        if not self.verifyCheck.isChecked():
            QtWidgets.QMessageBox.warning(self, "Error", "Please confirm verification.")
            return

        data = {
            "username": self.username,   # ✅ IMPORTANT
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

        self.controller.insert_student(data)

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

        errors = []
        if fname == "":
            errors.append("• First name is required.")
        if lname == "":
            errors.append("• Last name is required.")
        if contact == "":
            errors.append("• Contact / emergency contact is required.")

        if errors:
            QtWidgets.QMessageBox.warning(
                self,
                "Missing Required Fields",
                "Please fill in:\n\n" + "\n".join(errors)
            )
            return

        self.stacked.setCurrentWidget(self.verificationPage)

    def apply_search(self):
        search = self.searchStudent.text().strip().lower()
        self.studentTable.setRowCount(0)

        students = self.controller.search_students(self.username, search)
        for s in students:
            fullname = f"{s['studlname']}, {s['studfname']} {s.get('studmname','')}"
            self.add_student_row(s["studid"], fullname)

    def go_to_dashboard(self):
        from views.dashboard import AdminWindow
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

        self.studDOB.setDate(QDate.currentDate())
        self.motherDOB.setDate(QDate.currentDate())
        self.fatherDOB.setDate(QDate.currentDate())
        self.guardianDOB.setDate(QDate.currentDate())

        self.studSex.setCurrentIndex(0)
        self.verifyCheck.setChecked(False)


    def load_guardians_table(self, studid):
        from controller.GuardianController import GuardianController
        gc = GuardianController()

        # get real primary key (studentid int) using username + studid
        student = self.controller.get_student(self.username, studid)
        if not student:
            return

        real_id = student["studentid"]
        data = gc.get_guardians_for_student(real_id)

        table = self.guardianTable
        table.setRowCount(0)

        for g in data:
            row = table.rowCount()
            table.insertRow(row)

            # show STUDID code (S001, S002...) not numeric studentid
            table.setItem(row, 0, QTableWidgetItem(str(g["studid"])))
            table.setItem(row, 1, QTableWidgetItem(g["guardianname"]))

            action = QWidget()
            layout = QHBoxLayout(action)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            view_btn = QPushButton("View")
            view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            view_btn.setStyleSheet("""
                QPushButton { border: none; background: transparent; color: #333; font-size: 15px;}
                QPushButton:hover { color: #8b2fdb; }
            """)
            view_btn.clicked.connect(
                lambda _, guardian_id=g["guardianid"]: self.view_guardian_info(guardian_id)
            )
            layout.addWidget(view_btn)

            table.setCellWidget(row, 2, action)


    def open_add_guardian_page(self):
        self.newGuardianName.clear()
        self.newGuardianDOB.setDate(QDate.currentDate())
        self.newGuardianDOB.setCalendarPopup(True)

        self.imgPlaceholder.clear()
        self.current_guardian_image_path = None
        self.current_guardian_encoding = None

        self.stacked.setCurrentWidget(self.addGuardianPage)

    # def save_guardian(self):
    #     name = self.newGuardianName.text().strip()
    #     dob = self.newGuardianDOB.date().toString("yyyy-MM-dd")

    #     if name == "":
    #         QtWidgets.QMessageBox.warning(self, "Missing", "Guardian name is required.")
    #         return

    #     if self.current_guardian_encoding is None:
    #         QtWidgets.QMessageBox.warning(self, "Missing", "Please scan the guardian’s face.")
    #         return

    #     from controller.GuardianController import GuardianController
    #     gc = GuardianController()

    #     encoding = gc.encode_face(self.current_guardian_encoding)

    #     gc.insert_guardian(
    #         studid=self.current_student_for_guardian,
    #         name=name,
    #         dob=dob,
    #         image_path=self.current_guardian_image_path,
    #         encoding=encoding
    #     )

    #     QtWidgets.QMessageBox.information(self, "Success", "Guardian added successfully!")
    #     self.load_guardians_table(self.current_student_for_guardian)
    #     self.stacked.setCurrentWidget(self.viewGuardianPage)
    
    
    
    def save_guardian(self):
        name = self.newGuardianName.text().strip()
        dob = self.newGuardianDOB.date().toString("yyyy-MM-dd")

        if name == "":
            QtWidgets.QMessageBox.warning(self, "Missing", "Guardian name is required.")
            return

        if self.current_guardian_encoding is None:
            QtWidgets.QMessageBox.warning(self, "Missing", "Please scan the guardian’s face.")
            return

        from controller.GuardianController import GuardianController
        gc = GuardianController()

        encoding = gc.encode_face(self.current_guardian_encoding)

        # map current_student_for_guardian (studid code) → studentid
        student = self.controller.get_student(self.username, self.current_student_for_guardian)
        if not student:
            QtWidgets.QMessageBox.warning(self, "Error", "Student not found.")
            return

        real_id = student["studentid"]

        gc.insert_guardian(
            studentid=real_id,
            name=name,
            dob=dob,
            image_path=self.current_guardian_image_path,
            encoding=encoding
        )

        QtWidgets.QMessageBox.information(self, "Success", "Guardian added successfully!")
        self.load_guardians_table(self.current_student_for_guardian)
        self.stacked.setCurrentWidget(self.viewGuardianPage)


    def delete_guardian_record(self, guardianid):
        confirm = QtWidgets.QMessageBox.question(
            self, "Confirm", "Delete this guardian?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        from controller.GuardianController import GuardianController
        gc = GuardianController()
        gc.delete_guardian(guardianid)
        self.load_guardians_table(self.current_student_for_guardian)


    def scan_guardian_face(self):
        cam = CameraCapture()
        if cam.exec() == QtWidgets.QDialog.DialogCode.Accepted:

            from controller.GuardianController import GuardianController
            gc = GuardianController()
            # folder = "uploads/guardians"
            
            os.makedirs(GUARDIAN_DIR_ABS, exist_ok=True)

            safe_name = self.newGuardianName.text().strip().replace(" ", "_").lower()
            unique = str(QDate.currentDate().toJulianDay()) + "_" + str(os.getpid())
            filename = f"{self.current_student_for_guardian}_{safe_name}_{unique}.jpg"
            # filepath = os.path.join(folder, filename)

            # 1) ABS path for saving
            abs_path = os.path.join(GUARDIAN_DIR_ABS, filename)

            cv2.imwrite(abs_path, cam.captured_image)
            
            
            # 2) REL path for DB storing
            db_path = gc.to_db_path(abs_path)

            self.current_guardian_image_path = db_path
            self.current_guardian_encoding = cam.captured_encoding

            # 3) Display needs ABS path
            pixmap = QPixmap(abs_path)
            self.imgPlaceholder.setPixmap(
                pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            )

            # cv2.imwrite(filepath, cam.captured_image)
            # self.current_guardian_image_path = filepath
            # self.current_guardian_encoding = cam.captured_encoding

            # pixmap = QPixmap(filepath)
            # self.imgPlaceholder.setPixmap(
            #     pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            # )

            QtWidgets.QMessageBox.information(self, "Success", "Face scanned successfully!")

    def retake_guardian_face(self):
        self.current_guardian_encoding = None

        # if self.current_guardian_image_path and os.path.exists(self.current_guardian_image_path):
        #     os.remove(self.current_guardian_image_path)

        from controller.GuardianController import GuardianController
        gc = GuardianController()

        abs_path = gc.to_abs_path(self.current_guardian_image_path)

        if self.current_guardian_image_path and os.path.exists(abs_path):
            os.remove(abs_path)
        
        self.current_guardian_image_path = None
        self.imgPlaceholder.clear()

        self.scan_guardian_face()

    # def delete_scanned_face(self):
    #     self.current_guardian_encoding = None

    #     if self.current_guardian_image_path and os.path.exists(self.current_guardian_image_path):
    #         os.remove(self.current_guardian_image_path)

    #     self.current_guardian_image_path = None
    #     self.imgPlaceholder.clear()
    
    def delete_scanned_face(self):
        self.current_guardian_encoding = None

        if self.current_guardian_image_path:
            from controller.GuardianController import GuardianController
            gc = GuardianController()
            abs_path = gc.to_abs_path(self.current_guardian_image_path)

            if os.path.exists(abs_path):
                os.remove(abs_path)

        self.current_guardian_image_path = None
        self.imgPlaceholder.clear()


    def edit_guardian(self, guardian_id):
        from controller.GuardianController import GuardianController
        gc = GuardianController()

        guardian = gc.get_guardian_by_id(guardian_id)
        if guardian is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Guardian not found.")
            return

        self.current_edit_guardian_id = guardian_id
        page = self.editGuardianPage

        name_widget = page.findChild(QtWidgets.QLineEdit, "newGuardianNameInputEdit")
        name_widget.setText(guardian["guardianname"])

        dob_widget = page.findChild(QtWidgets.QDateEdit, "newGuardianDOBInputEdit")
        dob = guardian["guardiandob"]
        if dob:
            if isinstance(dob, str):
                dob_widget.setDate(QDate.fromString(dob, "yyyy-MM-dd"))
            else:
                dob_widget.setDate(QDate(dob.year, dob.month, dob.day))
        else:
            dob_widget.setDate(dob_widget.minimumDate())

        img_lbl = page.findChild(QtWidgets.QLabel, "imgPlaceholderEdit")
        db_path = guardian["face_image_path"]
        abs_path = gc.to_abs_path(db_path) if db_path else None

        self.current_guardian_encoding = guardian["face_encoding"]
        self.current_guardian_image_path = db_path

        if abs_path and os.path.exists(abs_path):
            pixmap = QPixmap(abs_path)
            img_lbl.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            img_lbl.clear()

        self.stacked.setCurrentWidget(self.editGuardianPage)

    def save_edit_guardian(self):
        from controller.GuardianController import GuardianController
        gc = GuardianController()

        guardian_id = self.current_edit_guardian_id
        page = self.editGuardianPage

        name_widget = page.findChild(QtWidgets.QLineEdit, "newGuardianNameInputEdit")
        dob_widget = page.findChild(QtWidgets.QDateEdit, "newGuardianDOBInputEdit")

        name = name_widget.text().strip()
        dob = dob_widget.date().toString("yyyy-MM-dd")

        if name == "":
            QtWidgets.QMessageBox.warning(self, "Missing", "Guardian name is required.")
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Update",
            "Save guardian changes?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        if self.current_guardian_encoding is not None:
            encoding = gc.encode_face(self.current_guardian_encoding)
        else:
            encoding = gc.get_guardian_by_id(guardian_id)["face_encoding"]

        new_image_path = self.current_guardian_image_path
        old_record = gc.get_guardian_by_id(guardian_id)
        # old_path = old_record["face_image_path"]

        # if old_path and new_image_path and old_path != new_image_path:
        #     if os.path.exists(old_path):
        #         os.remove(old_path)
        old_db_path = old_record["face_image_path"]

        if old_db_path and new_image_path and old_db_path != new_image_path:
            old_abs = gc.to_abs_path(old_db_path)
            if os.path.exists(old_abs):
                os.remove(old_abs)

        gc.update_guardian(
            guardianid=guardian_id,
            name=name,
            dob=dob,
            image_path=new_image_path,
            encoding=encoding
        )

        QtWidgets.QMessageBox.information(self, "Success", "Guardian updated successfully!")
        self.load_guardians_table(self.current_student_for_guardian)
        self.stacked.setCurrentWidget(self.viewGuardianPage)

    def view_guardian_info(self, guardian_id):
        from controller.GuardianController import GuardianController
        gc = GuardianController()

        guardian = gc.get_guardian_by_id(guardian_id)
        if guardian is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Guardian not found.")
            return

        self.current_view_guardian_id = guardian_id
        page = self.editGuardianPage

        name_lbl = page.findChild(QtWidgets.QLabel, "guardianNameDisplay")
        name_lbl.setText(guardian["guardianname"])

        dob_lbl = page.findChild(QtWidgets.QLabel, "guardianDOBDisplay")
        dob = guardian["guardiandob"]
        if dob:
            if isinstance(dob, str):
                dob_lbl.setText(dob)
            else:
                dob_lbl.setText(f"{dob.year}-{dob.month:02d}-{dob.day:02d}")
        else:
            dob_lbl.setText("No date available")

        img_lbl = page.findChild(QtWidgets.QLabel, "imgPlaceholderDisplay")
        # image_path = guardian["face_image_path"]
        # self.current_guardian_image_path = image_path

        from controller.GuardianController import GuardianController
        gc = GuardianController()
        
        db_path = guardian["face_image_path"]
        self.current_guardian_image_path = db_path
        abs_path = gc.to_abs_path(db_path) if db_path else None

        
        
        if abs_path and os.path.exists(abs_path):
            pixmap = QPixmap(abs_path)
            img_lbl.setPixmap(
                pixmap.scaled(220, 220, Qt.AspectRatioMode.KeepAspectRatio)
            )
        else:
            img_lbl.clear()

        self.stacked.setCurrentWidget(self.editGuardianPage)

    def delete_guardian_view(self):
        guardian_id = self.current_view_guardian_id

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this guardian?",
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        # if hasattr(self, "current_guardian_image_path") and \
        #     self.current_guardian_image_path and \
        #     os.path.exists(self.current_guardian_image_path):

        #     os.remove(self.current_guardian_image_path)
        from controller.GuardianController import GuardianController
        gc = GuardianController()

        gc.delete_guardian(guardian_id)
        
        if self.current_guardian_image_path:
            abs_path = gc.to_abs_path(self.current_guardian_image_path)
            if os.path.exists(abs_path):
                os.remove(abs_path)

        QtWidgets.QMessageBox.information(self, "Deleted", "Guardian deleted successfully.")

        self.load_guardians_table(self.current_student_for_guardian)
        self.stacked.setCurrentWidget(self.viewGuardianPage)


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

        self.cap = self.initialize_camera()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

        self.captured_encoding = None
        self.captured_image = None

    # def update_frame(self):
    #     ret, frame = self.cap.read()
    #     if not ret:
    #         return

    #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     h, w, ch = rgb.shape
    #     qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
    #     self.video_label.setPixmap(QPixmap.fromImage(qimg))
        # self.current_frame = frame
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        self.raw_frame = frame  # <-- ORIGINAL frame (not flipped)

        # Flip only for UI preview
        display = cv2.flip(frame, 1)
        self.display_frame = display

        rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

        

    # def capture_frame(self):
    #     frame = self.current_frame
    #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     locations = face_recognition.face_locations(rgb)

    #     if len(locations) == 0:
    #         QtWidgets.QMessageBox.warning(self, "No Face", "No face detected. Try again.")
    #         return

    #     encoding = face_recognition.face_encodings(rgb, locations)[0]
    #     self.captured_encoding = encoding
    #     self.captured_image = frame

    #     self.accept()
    def capture_frame(self):
        frame = self.raw_frame.copy()  # original feed (mirrored by Mac)
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)

        if not locations:
            QtWidgets.QMessageBox.warning(self, "No Face", "No face detected.")
            return

        self.captured_encoding = face_recognition.face_encodings(rgb, locations)[0]

        # 👇 Fix: unmirror the saved image
        self.captured_image = cv2.flip(frame, 1)

        self.accept()





    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()

    def initialize_camera(self):
        import platform
        system = platform.system()
        possible_indexes = [0, 1, 2, 3]

        for index in possible_indexes:
            if system == "Windows":
                cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            elif system == "Darwin":
                cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
            else:
                cap = cv2.VideoCapture(index)

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    return cap

            cap.release()

        raise RuntimeError("No working camera found")
