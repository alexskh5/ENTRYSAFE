import sys
import cv2
import face_recognition
import numpy as np
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, QListWidgetItem, QInputDialog

from controller.StudentController import StudentController
from controller.GuardianController import GuardianController
from os import path


# -----------------------------------------
# PATHS
# -----------------------------------------
BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
UI_FILE = path.join(PROJECT_ROOT, "ui", "scan.ui")


class CameraCapture(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scanning...")
        self.resize(600, 500)

        self.video_label = QLabel()
        self.video_label.setFixedSize(560, 420)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        self.setLayout(layout)

        self.cap = self.initialize_camera()
        self.current_frame = None
        self.last_face_location = None
        self.motion_detected = False
        self.captured_encoding = None
        self.auto_captured = False

        # UI camera feed refresh
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.update_frame_fast)
        self.render_timer.start(30)

        # Motion + face detection loop
        self.detect_timer = QTimer()
        self.detect_timer.timeout.connect(self.detect_face_and_capture)
        self.detect_timer.start(500)

    def initialize_camera(self):
        import platform
        system = platform.system()

        for i in [0, 1, 2, 3]:
            if system == "Windows":
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            elif system == "Darwin":
                cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
            else:
                cap = cv2.VideoCapture(i)

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    return cap
            cap.release()

        raise RuntimeError("No working camera found")

    def update_frame_fast(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        self.current_frame = frame

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def detect_face_and_capture(self):
        if self.auto_captured or self.current_frame is None:
            return

        small = cv2.resize(self.current_frame, (0,0), fx=0.5, fy=0.5)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb_small, model="hog")
        if not faces:
            return

        top, right, bottom, left = faces[0]
        top *= 2; right *= 2; bottom *= 2; left *= 2

        if self.last_face_location:
            old_top, old_right, old_bottom, old_left = self.last_face_location
            movement = abs(top - old_top) + abs(left - old_left)
            if movement > 25:
                self.motion_detected = True

        self.last_face_location = (top, right, bottom, left)

        # Proceed automatically when face moves
        if self.motion_detected:
            self.auto_captured = True
            self.capture_frame()

    def capture_frame(self):
        rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb, model="hog")

        if not faces:
            QtWidgets.QMessageBox.warning(self, "Error", "Face lost, try again.")
            self.auto_captured = False
            return

        self.captured_encoding = face_recognition.face_encodings(
            rgb, faces, model="large"
        )[0]

        self.cleanup_camera()
        self.accept()

    def cleanup_camera(self):
        if hasattr(self, "render_timer"):
            self.render_timer.stop()
        if hasattr(self, "detect_timer"):
            self.detect_timer.stop()
        if self.cap:
            self.cap.release()

    def closeEvent(self, event):
        self.cleanup_camera()
        event.accept()



# --------------------------------------------------------
# MAIN SCAN WINDOW
# --------------------------------------------------------
class ScanWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.student_controller = StudentController()
        self.guardian_controller = GuardianController()

        # Load UI
        uic.loadUi(UI_FILE, self)
        
        
        
        self.resize(1400, 800)

        # --- center window ---
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        win = self.frameGeometry()
        win.moveCenter(screen.center())
        self.move(win.topLeft())
        
        self.studentList = self.findChild(QtWidgets.QListWidget)

        if self.studentList is None:
            print("ERROR: Could not find ANY QListWidget in UI.")
        else:
            print("LIST FOUND:", self.studentList.objectName())
            self.studentList.itemClicked.connect(self.handle_student_click)
    

        # ---------------------------
        # REQUIRED UI ELEMENTS
        # ---------------------------
        self.scanSearchField = self.findChild(QtWidgets.QLineEdit, "scanSearchField")
        self.studentList = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.backBtn = self.findChild(QtWidgets.QPushButton, "backBtn")
        
        
        
        # --------------------------------------
        # HOVER EFFECT FOR STUDENT LIST
        # --------------------------------------
        self.studentList.setMouseTracking(True)
        self.studentList.setStyleSheet("""
            QListWidget::item {
                padding: 10px;
                color: #333;
            }
            QListWidget::item:hover {
                background: #f0e6ff;
                color: #8b2fdb;
            }
            QListWidget::item:selected {
                background: #8b2fdb;
                color: white;
            }
        """)

        print("UI LOADED →", self.scanSearchField, self.studentList, self.backBtn)

        # ---------------------------
        # CONNECT EVENTS
        # ---------------------------
        if self.scanSearchField:
            self.scanSearchField.textChanged.connect(self.refresh_student_list)

        if self.studentList:
            self.studentList.itemClicked.connect(self.handle_student_click)

        if self.backBtn:
            self.backBtn.clicked.connect(self.go_back)

        self.all_students = []
        self.refresh_student_list()

    # ----------------------------------------------------
    # LOAD + SEARCH STUDENTS
    # ----------------------------------------------------
    def refresh_student_list(self):
        term = self.scanSearchField.text().strip() if self.scanSearchField else ""
        students = self.student_controller.search_students(self.username, term)

        print("DEBUG students from search:", students)

        self.all_students = students
        self.studentList.clear()

        for s in students:
            fullname = f"{s['studlname']}, {s['studfname']} {s['studmname'] or ''}".strip()
            item = QListWidgetItem(f"{fullname} ({s['studid']})")
            item.setData(Qt.ItemDataRole.UserRole, s["studid"])
            self.studentList.addItem(item)

    

    def handle_student_click(self, item: QListWidgetItem):
        if item is None:
            return

        # ----------------------------------------------------
        # GET STUDENT BY CODE (studid like "S001")
        # ----------------------------------------------------
        studid = item.data(Qt.ItemDataRole.UserRole)
        if not studid:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid student selected")
            return

        student = next((s for s in self.all_students if s["studid"] == studid), None)
        if student is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Student not found")
            return

        fullname = f"{student['studlname']}, {student['studfname']} {student['studmname'] or ''}".strip()

        # ----------------------------------------------------
        # OPEN CAMERA + CAPTURE FACE
        # ----------------------------------------------------
        cam = CameraCapture()
        result = cam.exec()

        if result != QtWidgets.QDialog.DialogCode.Accepted:
            return

        captured = cam.captured_encoding
        frame = cam.current_frame

        if captured is None:
            QtWidgets.QMessageBox.warning(self, "Error", "No face captured")
            return

        # ----------------------------------------------------
        # SECURITY CHECK: FACE SIZE MUST BE LARGE ENOUGH
        # ----------------------------------------------------
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)

        if not faces:
            QtWidgets.QMessageBox.warning(self, "Error", "No face detected")
            return

        top, right, bottom, left = faces[0]
        face_width = right - left
        face_height = bottom - top

        # Prevent scanning small printed photos or far faces
        if face_width < 150 or face_height < 150:
            QtWidgets.QMessageBox.warning(
                self,
                "Too Far",
                "Please move closer to the camera."
            )
            return

        # ----------------------------------------------------
        # GET REAL studentid (INT PK)
        # ----------------------------------------------------
        student_db = self.student_controller.get_student(self.username, studid)
        if not student_db:
            QtWidgets.QMessageBox.warning(self, "Error", "Student not found in DB")
            return

        real_id = student_db["studentid"]   # <--- correct primary key

        # ----------------------------------------------------
        # LOAD GUARDIANS (STUDENT-SPECIFIC)
        # ----------------------------------------------------
        guardians = self.guardian_controller.get_guardians_for_student(real_id)

        if not guardians:
            QtWidgets.QMessageBox.warning(self, "No Guardians", "No guardians registered")
            return

        # Convert bytea → numpy arrays
        known_encodings = []
        names = []

        for g in guardians:
            enc_bytes = g.get("face_encoding")
            if enc_bytes:
                try:
                    decoded = self.guardian_controller.decode_face(enc_bytes)
                    if decoded is not None:
                        known_encodings.append(decoded)
                        names.append(g["guardianname"])
                except Exception as e:
                    print("Decode error:", e)

        if not known_encodings:
            QtWidgets.QMessageBox.warning(self, "Error", "No stored face encodings")
            return

        
        distances = face_recognition.face_distance(known_encodings, captured)
        best_idx = int(np.argmin(distances))
        best_distance = float(distances[best_idx])

        THRESHOLD = 0.40  # strict + makeup-friendly

        if best_distance <= THRESHOLD:
            guardian_name = names[best_idx]
            status = self.guardian_controller.get_today_attendance(real_id)

            if status is None or status["dropoff_time"] is None:
                self.guardian_controller.call_dropoff(real_id, guardian_name, True)
                QtWidgets.QMessageBox.information(self, "Drop-off Recorded",
                    f"Student: {fullname}\nStudent Status: Attendance Recorded\nGuardian: {guardian_name}\nAction: DROP-OFF")
                return

            if status["pickup_time"] is None:
                self.guardian_controller.call_pickup(real_id, guardian_name, True)
                QtWidgets.QMessageBox.information(self, "Pick-up Recorded",
                    f"Student: {fullname}\nStudent Status: Attendance Recorded\nGuardian: {guardian_name}\nAction: PICK-UP")
                return

            QtWidgets.QMessageBox.warning(self, "Already Completed",
                f"Student: {fullname}\nBoth DROP-OFF and PICK-UP already recorded today.")
            return


        # ----------------------------------------------------
        # ========== UNVERIFIED BRANCH ==========
        # ----------------------------------------------------
        emergency_contact = student.get("studcontact") or "No contact number stored"

        status = self.guardian_controller.get_today_attendance(real_id)

        if status is None or status["dropoff_time"] is None:
            # First log → DROP-OFF
            self.guardian_controller.call_dropoff(real_id, "UNVERIFIED GUARDIAN", False)
            action = "DROP-OFF"
        elif status["pickup_time"] is None:
            # Follow-up log → PICK-UP
            self.guardian_controller.call_pickup(real_id, "UNVERIFIED GUARDIAN", False)
            action = "PICK-UP"
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Already Completed",
                f"Student: {fullname}\nBoth DROP-OFF and PICK-UP are already recorded today."
            )
            return


        # ----------------------------------------------------
        # MANUAL GUARDIAN OVERRIDE (Emergency)
        # ----------------------------------------------------
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Guardian NOT Recognized")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)

        msg.setTextFormat(Qt.TextFormat.RichText)

        msg.setText(
            f"""
            <div style="text-align:center;">

                <!-- Title -->
                <p style="font-size:18px; font-weight:700; margin-bottom:2px;">
                    Guardian NOT Recognized
                </p>

                <!-- Action -->
                <p style="font-size:14px; margin-top:0;">
                    for <b style="color:#8b2fdb;">{action}</b>
                </p>

                <!-- Big Spacer -->
                <div style="margin:18px 0;"></div>

                <!-- Contact -->
                <p style="font-size:14px; margin:4px 0;">
                    <b>You may add or contact guardian to verify:</b>
                </p>

                <p style="font-size:16px; font-weight:600; color:#8b2fdb; margin-top:2px;">
                    {emergency_contact}
                </p>

                <!-- Big Spacer -->
                <div style="margin:18px 0;"></div>

                <!-- Student Info -->
                <p style="text-align:left; margin-left:40px;">
                    <b>Student:</b> {fullname}<br>
                    <b>Status:</b> Attendance Recorded
                </p>

            </div>
            """
        )

        # Purple button design
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QLabel {
                color: #333;
                font-size: 13px;
            }
            QPushButton {
                min-width: 130px;
                padding: 7px 14px;
                border-radius: 8px;
                border: none;
                font-weight: 600;
                background-color: #8b2fdb;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #a35cff;
            }
        """)

        manual_btn = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        skip_btn   = msg.addButton("Skip For Now", QtWidgets.QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        # Optional: use your app logo as window icon
        # icon_path = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
        # msg.setWindowIcon(QtGui.QIcon(icon_path))



        if msg.clickedButton() == manual_btn:
            name, ok = QInputDialog.getText(
                self,
                "Manual Verification",
                "Enter Guardian Name:"
            )

            if ok and name.strip():
                manual_name = name.strip()

                # Only update pickup guardian
                # self.guardian_controller.update_pickup_guardian(real_id, manual_name)
                # self.guardian_controller.manual_pickup(real_id, manual_name)
                if action == "DROP-OFF":
                    # DO NOT update time again — only correct the guardian name
                    self.guardian_controller.update_dropoff_guardian(real_id, manual_name)
                else:
                    # PICKUP truly needs a timestamp
                    self.guardian_controller.manual_pickup(real_id, manual_name)



                QtWidgets.QMessageBox.information(
                    self,
                    "Guardian Updated",
                    f"Manual verification recorded:\nGuardian: {manual_name}"
                )


    # ----------------------------------------------------
    # BACK TO CHOOSE MODE
    # ----------------------------------------------------
    def go_back(self):
        from views.mode import ChooseModeWindow
        self.mode = ChooseModeWindow(self.username)
        self.mode.show()
        self.close()
