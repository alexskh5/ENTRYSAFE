import sys
import cv2
import face_recognition
import numpy as np
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, QListWidgetItem, QInputDialog
from PyQt6.QtWidgets import QPushButton, QMessageBox

from controller.StudentController import StudentController
from controller.GuardianController import GuardianController
# from os import path
import os
from utils.paths import app_dir

# -----------------------------------------
# PATHS
# -----------------------------------------
# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))
# UI_FILE = path.join(PROJECT_ROOT, "ui", "scan.ui")
BASE = app_dir()
UI_FILE = os.path.join(BASE, "ui", "scan.ui")

# class CameraCapture(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Scanning...")
#         self.resize(600, 500)
        
#         self.stable_frames = 0
#         self.auto_captured = False

#         self.video_label = QLabel()
#         self.video_label.setFixedSize(560, 420)

#         layout = QVBoxLayout()
#         layout.addWidget(self.video_label)
#         self.setLayout(layout)

        
#         # Initialize camera
#         try:
#             self.cap = self.initialize_camera()
#         except RuntimeError as e:
#             QtWidgets.QMessageBox.critical(self, "Camera Error", str(e))
#             self.reject()
#             return

        
#         # self.cap = self.initialize_camera()
#         self.current_frame = None
#         self.last_face_location = None
#         self.motion_detected = False
#         self.captured_encoding = None
#         # self.auto_captured = False

#         # UI camera feed refresh
#         self.render_timer = QTimer()
#         self.render_timer.timeout.connect(self.update_frame_fast)
#         self.render_timer.start(30)

#         # Motion + face detection loop
#         self.detect_timer = QTimer()
#         # self.detect_timer.timeout.connect(self.detect_face_and_capture)
#         self.detect_timer.timeout.connect(self.detect_and_validate_face)
#         self.detect_timer.start(500)
        
#         # =========================
#         # TIMEOUT FOR SCAN ERROR
#         # =========================
#         self.timeout_timer = QTimer()
#         self.timeout_timer.setSingleShot(True)
#         self.timeout_timer.timeout.connect(self.face_timeout_error)
#         self.timeout_timer.start(10000)  # 10 seconds to detect a face

#     def face_timeout_error(self):
#         if not self.auto_captured:
#             QtWidgets.QMessageBox.warning(
#                 self,
#                 "Scan Timeout",
#                 "Unable to detect a face. Please ensure your face is visible and try again."
#             )
#             self.cleanup_camera()
#             self.reject()

#     def initialize_camera(self):
#         import platform
#         system = platform.system()

#         for i in [0, 1, 2, 3]:
#             if system == "Windows":
#                 cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
#             elif system == "Darwin":
#                 cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
#             else:
#                 cap = cv2.VideoCapture(i)

#             cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#             cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#             if cap.isOpened():
#                 ret, frame = cap.read()
#                 if ret:
#                     return cap
#             cap.release()

#         raise RuntimeError("No working camera found")

#     def update_frame_fast(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return
        
#         frame = cv2.flip(frame, 1)
#         self.current_frame = frame

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb.shape
#         qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
#         self.video_label.setPixmap(QPixmap.fromImage(qimg))
        
    
#     # -------------------------------------
#     # SECURITY HELPERS
#     # -------------------------------------
#     def face_centered(self, face, frame_width):
#         top, right, bottom, left = face
#         face_center = (left + right) // 2
#         return abs(face_center - frame_width // 2) < 70

#     def forehead_visible(self, face):
#         top, right, bottom, left = face
#         return (bottom - top) > 180

#     def eyes_clear(self, frame, face):
#         top, right, bottom, left = face
#         face_img = frame[top:bottom, left:right]
#         gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
#         edges = cv2.Canny(gray, 60, 120)
#         edge_ratio = np.sum(edges > 0) / edges.size
#         return edge_ratio < 0.13
    
    

#     # def detect_face_and_capture(self):
#     #     if self.auto_captured or self.current_frame is None:
#     #         return

#     #     small = cv2.resize(self.current_frame, (0,0), fx=0.5, fy=0.5)
#     #     rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

#     #     faces = face_recognition.face_locations(rgb_small, model="cnn")
#     #     if not faces:
#     #         return

#     #     top, right, bottom, left = faces[0]
#     #     top *= 2; right *= 2; bottom *= 2; left *= 2

#     #     if self.last_face_location:
#     #         old_top, old_right, old_bottom, old_left = self.last_face_location
#     #         movement = abs(top - old_top) + abs(left - old_left)
#     #         if movement > 25:
#     #             self.motion_detected = True

#     #     self.last_face_location = (top, right, bottom, left)
        
#     #     # Proceed automatically when face moves
#     #     if self.motion_detected:
#     #         self.auto_captured = True
#     #         self.capture_frame()
    
#     # -------------------------------------
#     # DETECT + VALIDATE
#     # -------------------------------------
#     def detect_and_validate_face(self):
#         if self.auto_captured or self.current_frame is None:
#             return

#         # Resize to 1/4 for faster processing
#         small = cv2.resize(self.current_frame, (0, 0), fx=0.25, fy=0.25)
#         rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

#         # Detect faces
#         faces = face_recognition.face_locations(rgb_small, model="hog")
#         if not faces:
#             self.stable_frames = 0
#             return

#         # Scale coordinates back to original frame
#         top, right, bottom, left = faces[0]
#         top *= 4
#         right *= 4
#         bottom *= 4
#         left *= 4
#         face = (top, right, bottom, left)

#         h, w, _ = self.current_frame.shape

#         # Check if face is centered (optional: widen threshold if needed)
#         if not self.face_centered(face, w):
#             self.stable_frames = 0
#             return

#         # Optional: skip forehead/eyes checks for now to ensure detection works
#         # if not self.forehead_visible(face):
#         #     self.stable_frames = 0
#         #     return

#         # if not self.eyes_clear(self.current_frame, face):
#         #     self.stable_frames = 0
#         #     return

#         # Check if face is stable (relax movement threshold to 15 pixels)
#         if self.last_face_location:
#             ot, or_, ob, ol = self.last_face_location
#             movement = abs(top - ot) + abs(left - ol)
#             if movement < 15:  # relaxed from 5 → more tolerant
#                 self.stable_frames += 1
#             else:
#                 self.stable_frames = 0

#         self.last_face_location = face

#         # If face stable for 3 consecutive frames → capture
#         if self.stable_frames >= 3:
#             self.capture_frame()

#     def capture_frame(self):
#         # rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
#         # faces = face_recognition.face_locations(rgb, model="cnn")

#         # if not faces:
#         #     QtWidgets.QMessageBox.warning(self, "Error", "Face lost, try again.")
#         #     self.auto_captured = False
#         #     return

#         # self.captured_encoding = face_recognition.face_encodings(
#         #     rgb, faces, model="large"
#         # )[0]

#         # self.cleanup_camera()
#         # self.accept()
#         rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
#         faces = face_recognition.face_locations(rgb, model="hog")

#         if not faces:
#             return

#         encodings = face_recognition.face_encodings(rgb, faces, model="large")
#         if not encodings:
#             return

#         self.captured_encoding = np.mean(encodings, axis=0)
#         self.auto_captured = True

#         # Stop timeout timer — face was captured
#         self.timeout_timer.stop()

#         self.cleanup_camera()
#         self.accept()

#     # def cleanup_camera(self):
#     #     if hasattr(self, "render_timer"):
#     #         self.render_timer.stop()
#     #     if hasattr(self, "detect_timer"):
#     #         self.detect_timer.stop()
#     #     if self.cap:
#     #         self.cap.release()
    
#     def cleanup_camera(self):
#         self.render_timer.stop()
#         self.detect_timer.stop()
#         self.cap.release()

#     def closeEvent(self, event):
#         self.cleanup_camera()
#         event.accept()

import cv2
import face_recognition
import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton


class CameraCapture(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan Guardian Face")
        self.resize(600, 560)

        self.video_label = QLabel()
        self.video_label.setFixedSize(560, 420)
        self.video_label.setStyleSheet("background:#111;border-radius:12px;")

        # Live status text
        self.status_label = QLabel("🟡 Initializing camera...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                border-radius: 10px;
                background: #f4f4f6;
                color: #333;
                font-weight: 600;
            }
        """)

        # Capture button
        self.capture_btn = QPushButton("Capture")
        self.capture_btn.setFixedHeight(42)
        self.capture_btn.setEnabled(False)
        self.capture_btn.clicked.connect(self.capture_frame)
        self.capture_btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                font-weight: 700;
                background: #8b2fdb;
                color: white;
            }
            QPushButton:disabled {
                background: #cfc4dd;
                color: #ffffff;
            }
            QPushButton:hover:!disabled {
                background: #a35cff;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.capture_btn)
        self.setLayout(layout)

        # Camera init
        try:
            self.cap = self.initialize_camera()
        except RuntimeError as e:
            QtWidgets.QMessageBox.critical(self, "Camera Error", str(e))
            self.reject()
            return

        self.current_frame = None
        self.captured_encoding = None

        # validation state
        self.last_validation = {
            "ok": False,
            "msg": "🟡 Looking for face...",
            "face_box": None
        }

        # Smooth preview
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.update_frame_fast)
        self.render_timer.start(30)

        # Lightweight validation (5x/sec)
        self.validate_timer = QTimer()
        self.validate_timer.timeout.connect(self.validate_frame)
        self.validate_timer.start(200)

        self.status_label.setText("🟡 Looking for face...")

    # -----------------------------
    # CAMERA SETUP
    # -----------------------------
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
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    return cap
            cap.release()

        raise RuntimeError("No working camera found")

    # -----------------------------
    # PREVIEW
    # -----------------------------
    def update_frame_fast(self):
        if not self.cap:
            return

        # reduce "laggy" feel
        self.cap.grab()
        ret, frame = self.cap.retrieve()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        self.current_frame = frame

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

    # -----------------------------
    # VALIDATION (FAST CHECKS)
    # -----------------------------
    def validate_frame(self):
        if self.current_frame is None:
            return

        frame = self.current_frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(gray.mean())

        # downscale for faster detection
        small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        faces_small = face_recognition.face_locations(rgb_small, model="hog")

        # No face
        if len(faces_small) == 0:
            self.set_status(False, "🟡 No face detected. Please look at the camera.", None)
            return

        # Multiple faces
        if len(faces_small) > 1:
            self.set_status(False, "🔴 Multiple faces detected. Only ONE person please.", None)
            return

        # Scale back coordinates
        top, right, bottom, left = faces_small[0]
        top *= 2; right *= 2; bottom *= 2; left *= 2

        face_w = right - left
        face_h = bottom - top

        # Too far
        if face_w < 150 or face_h < 150:
            self.set_status(False, "🔴 Face too far. Please move closer.", (top, right, bottom, left))
            return

        # Not centered
        h, w = gray.shape
        face_center_x = (left + right) // 2
        if abs(face_center_x - w // 2) > 90:
            self.set_status(False, "🔴 Please center your face.", (top, right, bottom, left))
            return

        # Too dark
        if brightness < 60:
            self.set_status(False, "🔴 Too dark. Move to a brighter area.", (top, right, bottom, left))
            return

        # Blurry (Laplacian variance)
        face_img = gray[max(0, top):min(h, bottom), max(0, left):min(w, right)]
        if face_img.size == 0:
            self.set_status(False, "🔴 Adjust your position and try again.", (top, right, bottom, left))
            return

        blur_score = float(cv2.Laplacian(face_img, cv2.CV_64F).var())
        if blur_score < 40:
            self.set_status(False, "🔴 Face not clear. Stay still for a second.", (top, right, bottom, left))
            return

        # ✅ Ready
        self.set_status(True, "🟢 Face detected. Ready to capture.", (top, right, bottom, left))

    def set_status(self, ok: bool, msg: str, face_box):
        # avoid updating UI too often if same message
        if self.last_validation["ok"] == ok and self.last_validation["msg"] == msg:
            return

        self.last_validation = {"ok": ok, "msg": msg, "face_box": face_box}
        self.status_label.setText(msg)
        self.capture_btn.setEnabled(ok)

    # -----------------------------
    # CAPTURE (ONE ENCODE)
    # -----------------------------
    def capture_frame(self):
        if not self.last_validation["ok"] or self.current_frame is None:
            return

        self.capture_btn.setEnabled(False)
        self.capture_btn.setText("Processing...")

        frame = self.current_frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_box = self.last_validation["face_box"]
        if not face_box:
            # safety fallback
            self.capture_btn.setText("Capture")
            return

        # Fast encode for scanning (use "small")
        enc = face_recognition.face_encodings(rgb, [face_box], model="small")
        if not enc:
            self.status_label.setText("🔴 Could not process face. Try again.")
            self.capture_btn.setEnabled(False)
            self.capture_btn.setText("Capture")
            return

        self.captured_encoding = enc[0]

        self.cleanup_camera()
        self.accept()

    # -----------------------------
    # CLEANUP
    # -----------------------------
    def cleanup_camera(self):
        if hasattr(self, "render_timer"):
            self.render_timer.stop()
        if hasattr(self, "validate_timer"):
            self.validate_timer.stop()
        if hasattr(self, "cap") and self.cap:
            self.cap.release()
            self.cap = None

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
        
        self.guardian_cache = {} 
        
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

    

    # def handle_student_click(self, item: QListWidgetItem):
    #     if item is None:
    #         return

    #     # ----------------------------------------------------
    #     # GET STUDENT BY CODE (studid like "S001")
    #     # ----------------------------------------------------
    #     studid = item.data(Qt.ItemDataRole.UserRole)
    #     if not studid:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Invalid student selected")
    #         return

    #     student = next((s for s in self.all_students if s["studid"] == studid), None)
    #     if student is None:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Student not found")
    #         return

    #     fullname = f"{student['studlname']}, {student['studfname']} {student['studmname'] or ''}".strip()

    #     # ----------------------------------------------------
    #     # OPEN CAMERA + CAPTURE FACE
    #     # ----------------------------------------------------
    #     cam = CameraCapture()
    #     result = cam.exec()

    #     if result != QtWidgets.QDialog.DialogCode.Accepted:
    #         return

    #     captured = cam.captured_encoding
    #     frame = cam.current_frame

    #     if captured is None:
    #         QtWidgets.QMessageBox.warning(self, "Error", "No face captured")
    #         return

    #     # ----------------------------------------------------
    #     # SECURITY CHECK: FACE SIZE MUST BE LARGE ENOUGH
    #     # ----------------------------------------------------
    #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     faces = face_recognition.face_locations(rgb)

    #     if not faces:
    #         QtWidgets.QMessageBox.warning(self, "Error", "No face detected")
    #         return

    #     top, right, bottom, left = faces[0]
    #     face_width = right - left
    #     face_height = bottom - top

    #     # Prevent scanning small printed photos or far faces
    #     if face_width < 150 or face_height < 150:
    #         QtWidgets.QMessageBox.warning(
    #             self,
    #             "Too Far",
    #             "Please move closer to the camera."
    #         )
    #         return

    #     # ----------------------------------------------------
    #     # GET REAL studentid (INT PK)
    #     # ----------------------------------------------------
    #     student_db = self.student_controller.get_student(self.username, studid)
    #     if not student_db:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Student not found in DB")
    #         return

    #     real_id = student_db["studentid"]   # <--- correct primary key

    #     # ----------------------------------------------------
    #     # LOAD GUARDIANS (STUDENT-SPECIFIC)
    #     # ----------------------------------------------------
    #     guardians = self.guardian_controller.get_guardians_for_student(real_id)

    #     if not guardians:
    #         QtWidgets.QMessageBox.warning(self, "No Guardians", "No guardians registered")
    #         return

    #     # Convert bytea → numpy arrays
    #     known_encodings = []
    #     names = []

    #     for g in guardians:
    #         enc_bytes = g.get("face_encoding")
    #         if enc_bytes:
    #             try:
    #                 decoded = self.guardian_controller.decode_face(enc_bytes)
    #                 if decoded is not None:
    #                     known_encodings.append(decoded)
    #                     names.append(g["guardianname"])
    #             except Exception as e:
    #                 print("Decode error:", e)

    #     if not known_encodings:
    #         QtWidgets.QMessageBox.warning(self, "Error", "No stored face encodings")
    #         return

        
    #     distances = face_recognition.face_distance(known_encodings, captured)
    #     best_idx = int(np.argmin(distances))
    #     best_distance = float(distances[best_idx])

    #     THRESHOLD = 0.40  # strict + makeup-friendly

    #     if best_distance <= THRESHOLD:
    #         guardian_name = names[best_idx]
    #         status = self.guardian_controller.get_today_attendance(real_id)

    #         if status is None or status["dropoff_time"] is None:
    #             self.guardian_controller.call_dropoff(real_id, guardian_name, True)
    #             QtWidgets.QMessageBox.information(self, "Drop-off Recorded",
    #                 f"Student: {fullname}\nStudent Status: Attendance Recorded\nGuardian: {guardian_name}\nAction: DROP-OFF")
    #             return

    #         if status["pickup_time"] is None:
    #             self.guardian_controller.call_pickup(real_id, guardian_name, True)
    #             QtWidgets.QMessageBox.information(self, "Pick-up Recorded",
    #                 f"Student: {fullname}\nStudent Status: Attendance Recorded\nGuardian: {guardian_name}\nAction: PICK-UP")
    #             return

    #         QtWidgets.QMessageBox.warning(self, "Already Completed",
    #             f"Student: {fullname}\nBoth DROP-OFF and PICK-UP already recorded today.")
    #         return


    #     # ----------------------------------------------------
    #     # ========== UNVERIFIED BRANCH ==========
    #     # ----------------------------------------------------
    #     emergency_contact = student.get("studcontact") or "No contact number stored"

    #     status = self.guardian_controller.get_today_attendance(real_id)

    #     if status is None or status["dropoff_time"] is None:
    #         # First log → DROP-OFF
    #         self.guardian_controller.call_dropoff(real_id, "UNVERIFIED GUARDIAN", False)
    #         action = "DROP-OFF"
    #     elif status["pickup_time"] is None:
    #         # Follow-up log → PICK-UP
    #         self.guardian_controller.call_pickup(real_id, "UNVERIFIED GUARDIAN", False)
    #         action = "PICK-UP"
    #     else:
    #         QtWidgets.QMessageBox.warning(
    #             self,
    #             "Already Completed",
    #             f"Student: {fullname}\nBoth DROP-OFF and PICK-UP are already recorded today."
    #         )
    #         return


    #     # ----------------------------------------------------
    #     # MANUAL GUARDIAN OVERRIDE (Emergency)
    #     # ----------------------------------------------------
    #     msg = QtWidgets.QMessageBox(self)
    #     msg.setWindowTitle("Guardian NOT Recognized")
    #     msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)

    #     msg.setTextFormat(Qt.TextFormat.RichText)

    #     msg.setText(
    #         f"""
    #         <div style="text-align:center;">

    #             <!-- Title -->
    #             <p style="font-size:18px; font-weight:700; margin-bottom:2px;">
    #                 Guardian NOT Recognized
    #             </p>

    #             <!-- Action -->
    #             <p style="font-size:14px; margin-top:0;">
    #                 for <b style="color:#8b2fdb;">{action}</b>
    #             </p>

    #             <!-- Big Spacer -->
    #             <div style="margin:18px 0;"></div>

    #             <!-- Contact -->
    #             <p style="font-size:14px; margin:4px 0;">
    #                 <b>You may add or contact guardian to verify:</b>
    #             </p>

    #             <p style="font-size:16px; font-weight:600; color:#8b2fdb; margin-top:2px;">
    #                 {emergency_contact}
    #             </p>

    #             <!-- Big Spacer -->
    #             <div style="margin:18px 0;"></div>

    #             <!-- Student Info -->
    #             <p style="text-align:left; margin-left:40px;">
    #                 <b>Student:</b> {fullname}<br>
    #                 <b>Status:</b> Attendance Recorded
    #             </p>

    #         </div>
    #         """
    #     )

    #     # Purple button design
    #     msg.setStyleSheet("""
    #         QMessageBox {
    #             background-color: #ffffff;
    #         }
    #         QLabel {
    #             color: #333;
    #             font-size: 13px;
    #         }
    #         QPushButton {
    #             min-width: 130px;
    #             padding: 7px 14px;
    #             border-radius: 8px;
    #             border: none;
    #             font-weight: 600;
    #             background-color: #8b2fdb;
    #             color: #ffffff;
    #         }
    #         QPushButton:hover {
    #             background-color: #a35cff;
    #         }
    #     """)

    #     manual_btn = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
    #     skip_btn   = msg.addButton("Skip For Now", QtWidgets.QMessageBox.ButtonRole.RejectRole)

    #     msg.exec()

    #     # Optional: use your app logo as window icon
    #     # icon_path = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
    #     # msg.setWindowIcon(QtGui.QIcon(icon_path))



    #     if msg.clickedButton() == manual_btn:
    #         name, ok = QInputDialog.getText(
    #             self,
    #             "Manual Verification",
    #             "Enter Guardian Name:"
    #         )

    #         if ok and name.strip():
    #             manual_name = name.strip()

    #             # Only update pickup guardian
    #             # self.guardian_controller.update_pickup_guardian(real_id, manual_name)
    #             # self.guardian_controller.manual_pickup(real_id, manual_name)
    #             if action == "DROP-OFF":
    #                 # DO NOT update time again — only correct the guardian name
    #                 self.guardian_controller.update_dropoff_guardian(real_id, manual_name)
    #             else:
    #                 # PICKUP truly needs a timestamp
    #                 self.guardian_controller.manual_pickup(real_id, manual_name)



    #             QtWidgets.QMessageBox.information(
    #                 self,
    #                 "Guardian Updated",
    #                 f"Manual verification recorded:\nGuardian: {manual_name}"
    #             )

    # def handle_student_click(self, item: QListWidgetItem):
    #     if item is None:
    #         return

    #     studid = item.data(Qt.ItemDataRole.UserRole)
    #     student = next((s for s in self.all_students if s["studid"] == studid), None)
    #     if not student:
    #         return

    #     fullname = f"{student['studlname']}, {student['studfname']} {student['studmname'] or ''}".strip()
    #     emergency_contact = student.get("studcontact") or "No emergency contact on record"

    #     student_db = self.student_controller.get_student(self.username, studid)
    #     real_id = student_db["studentid"]

    #     status = self.guardian_controller.get_today_attendance(real_id)

    #     # ---------------- EARLY RETURN IF BOTH LOGGED ----------------
    #     if status and status["dropoff_time"] is not None and status["pickup_time"] is not None:
    #         QtWidgets.QMessageBox.information(
    #             self,
    #             "Already Completed",
    #             f"Student: {fullname}\nBoth DROP-OFF and PICK-UP already recorded today."
    #         )
    #         return

    #     # ---------------- CAMERA ----------------
    #     cam = CameraCapture()
    #     if cam.exec() != QDialog.DialogCode.Accepted:
    #         return

    #     captured = cam.captured_encoding
    #     frame = cam.current_frame
    #     if captured is None:
    #         return

    #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     faces = face_recognition.face_locations(rgb)
    #     if not faces:
    #         return

    #     top, right, bottom, left = faces[0]
    #     if (right - left) < 150 or (bottom - top) < 150:
    #         QtWidgets.QMessageBox.warning(self, "Too Far", "Please move closer.")
    #         return

    #     # ---------------- MATCH ----------------
    #     guardians = self.guardian_controller.get_guardians_for_student(real_id)
    #     known_encodings, names = [], []

    #     for g in guardians:
    #         decoded = self.guardian_controller.decode_face(g["face_encoding"])
    #         if decoded is not None:
    #             known_encodings.append(decoded)
    #             names.append(g["guardianname"])

    #     recognized = False
    #     guardian_name = None

    #     if known_encodings:
    #         distances = face_recognition.face_distance(known_encodings, captured)
    #         best = np.argmin(distances)
    #         if distances[best] <= 0.40:
    #             recognized = True
    #             guardian_name = names[best]


    #     # ==================================================
    #     # ✅ RECOGNIZED — NO CHANGES
    #     # ==================================================
    #     if recognized:
    #         if status is None or status["dropoff_time"] is None:
    #             self.guardian_controller.call_dropoff(real_id, guardian_name, True)
    #             QtWidgets.QMessageBox.information(self, "Drop-off Recorded", guardian_name)
    #             return

    #         if status["pickup_time"] is None:
    #             self.guardian_controller.call_pickup(real_id, guardian_name, True)
    #             self.guardian_controller.clear_verification(real_id)
    #             QtWidgets.QMessageBox.information(self, "Pick-up Recorded", guardian_name)
    #             return

    #         return

    #     # ==================================================
    #     # ❌ UNRECOGNIZED — DROP-OFF
    #     # ==================================================
    #     if status is None or status["dropoff_time"] is None:
    #         msg = QtWidgets.QMessageBox(self)
    #         msg.setWindowTitle("Guardian Not Recognized")
    #         msg.setTextFormat(Qt.TextFormat.RichText)
    #         msg.setText(f"""
    #         <div style="text-align:center;">
    #             <p><b>Guardian NOT Recognized</b></p>
    #             <p>Action: DROP-OFF</p>
    #             <hr>
    #             <p><b>Emergency Contact</b></p>
    #             <p style="color:#8b2fdb;">{emergency_contact}</p>
    #             <hr>
    #             <p>{fullname}</p>
    #         </div>
    #         """)

    #         add_btn = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
    #         # msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
    #         msg.exec()

    #         if msg.clickedButton() != add_btn:
    #             return  # ❌ cancel = NO SAVE

    #         name, ok = QInputDialog.getText(self, "Add Guardian", "Guardian Name:")
    #         if ok and name.strip():
    #             self.guardian_controller.call_dropoff(real_id, name.strip(), True)
    #         return

    #     # ==================================================
    #     # 🔐 PICK-UP — FIRST FAILURE
    #     # ==================================================
    #     if status["pickup_time"] is None and not self.guardian_controller.is_waiting_verification(real_id):
    #         self.guardian_controller.set_waiting_verification(real_id)

    #         msg = QtWidgets.QMessageBox(self)
    #         msg.setTextFormat(Qt.TextFormat.RichText)
    #         msg.setText(f"""
    #         <div style="text-align:center;">
    #             <p><b>Guardian NOT Recognized</b></p>
    #             <p>Action: PICK-UP</p>
    #             <hr>
    #             <p><b>Emergency Contact</b></p>
    #             <p style="color:#8b2fdb;">{emergency_contact}</p>
    #             <p>Status: Waiting for parent verification</p>
    #         </div>
    #         """)

    #         msg.addButton("Verify Parent", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
    #         # msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
    #         msg.exec()
    #         return

    #     # ==================================================
    #     # 🔁 PICK-UP — AFTER VERIFY
    #     # ==================================================
    #     msg = QtWidgets.QMessageBox(self)
    #     msg.setTextFormat(Qt.TextFormat.RichText)
    #     msg.setText(f"""
    #     <div style="text-align:center;">
    #         <p><b>Verification Pending</b></p>
    #         <hr>
    #         <p><b>Emergency Contact</b></p>
    #         <p style="color:#8b2fdb;">{emergency_contact}</p>
    #         <p>{fullname}</p>
    #     </div>
    #     """)

    #     scan_btn = msg.addButton("Scan Again", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
    #     add_btn = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.ActionRole)
    #     # msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
    #     msg.exec()

    #     if msg.clickedButton() == scan_btn:
    #         self.handle_student_click(item)

    #     if msg.clickedButton() == add_btn:
    #         name, ok = QInputDialog.getText(self, "Manual Pick-up", "Guardian Name:")
    #         if ok and name.strip():
    #             self.guardian_controller.manual_pickup(real_id, name.strip())
    #             self.guardian_controller.clear_verification(real_id)


    def handle_student_click(self, item: QListWidgetItem):
        if item is None:
            return

        student = self.get_student_from_item(item)
        if not student:
            return

        fullname = f"{student['studlname']}, {student['studfname']} {student['studmname'] or ''}".strip()
        emergency_contact = student.get("studcontact") or "No emergency contact"

        student_db = self.student_controller.get_student(self.username, student["studid"])
        real_id = student_db["studentid"]

        status = self.guardian_controller.get_today_attendance(real_id)

        # ✅ ALREADY COMPLETED
        if status and status["dropoff_time"] and status["pickup_time"]:
            QtWidgets.QMessageBox.information(
                self, "Already Completed",
                f"{fullname}\nDrop-off and Pick-up already recorded."
            )
            return

        # ==================================================
        # 🔐 PICK-UP — WAITING VERIFICATION (NO CAMERA)
        # ==================================================
        if status and status["dropoff_time"] and status["pickup_time"] is None:
            if self.guardian_controller.is_waiting_verification(real_id):
                # Let handle_unrecognized_guardian decide what to show
                self.handle_unrecognized_guardian(
                    real_id, fullname, emergency_contact, status, item
                )
                return


        # ---------------- CAMERA OPENS ONLY HERE ----------------
        captured, frame = self.capture_student_face()
        if captured is None:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        if not faces:
            return

        top, right, bottom, left = faces[0]
        if (right - left) < 150 or (bottom - top) < 150:
            QtWidgets.QMessageBox.warning(self, "Too Far", "Please move closer.")
            return

        recognized, guardian_name = self.match_guardian(real_id, captured)

        if recognized:
            self.handle_recognized_guardian(real_id, fullname, guardian_name, status)
        else:
            self.handle_unrecognized_guardian(real_id, fullname, emergency_contact, status, item)




    # ---------------- Helper Methods ----------------

    def get_student_from_item(self, item: QListWidgetItem):
        studid = item.data(Qt.ItemDataRole.UserRole)
        return next((s for s in self.all_students if s["studid"] == studid), None)

    # def capture_student_face(self):
    #     cam = CameraCapture()
    #     if cam.exec() != QDialog.DialogCode.Accepted:
    #         return None, None
    #     return cam.captured_encoding, cam.current_frame

    # def capture_student_face(self):
    #     cam = CameraCapture()
    #     if cam.exec() != QDialog.DialogCode.Accepted:
    #         return None, None

    #     frames_to_average = 5
    #     encodings_list = []

    #     for i in range(frames_to_average):
    #         rgb = cv2.cvtColor(cam.current_frame, cv2.COLOR_BGR2RGB)
    #         faces = face_recognition.face_locations(rgb)
    #         if faces:
    #             encs = face_recognition.face_encodings(rgb, faces)
    #             if encs:
    #                 encodings_list.append(encs[0])
    #         # wait ~100ms between frames for movement
    #         QtWidgets.QApplication.processEvents()
        
    #     if not encodings_list:
    #         return None, None
        
    #     # Average encoding
    #     avg_encoding = np.mean(encodings_list, axis=0)
    #     return avg_encoding, cam.current_frame

    def capture_student_face(self):
        cam = CameraCapture()
        if cam.exec() != QDialog.DialogCode.Accepted:
            return None, None
        return cam.captured_encoding, cam.current_frame

    # def match_guardian(self, student_id, captured_encoding):
    #     guardians = self.guardian_controller.get_guardians_for_student(student_id)
    #     known_encodings, names = [], []

    #     for g in guardians:
    #         decoded = self.guardian_controller.decode_face(g["face_encoding"])
    #         if decoded is not None:
    #             known_encodings.append(decoded)
    #             names.append(g["guardianname"])

    #     if not known_encodings:
    #         return False, None

    #     distances = face_recognition.face_distance(known_encodings, captured_encoding)
    #     best_idx = np.argmin(distances)
    #     if distances[best_idx] <= 0.40:
    #         return True, names[best_idx]
    #     return False, None

    # def match_guardian(self, student_id, captured_encoding):
    #     guardians = self.guardian_controller.get_guardians_for_student(student_id)
    #     known_encodings, names = [], []

    #     for g in guardians:
    #         decoded = self.guardian_controller.decode_face(g["face_encoding"])
    #         if decoded is not None:
    #             known_encodings.append(decoded)
    #             names.append(g["guardianname"])

    #     if not known_encodings:
    #         return False, None

    #     distances = face_recognition.face_distance(known_encodings, captured_encoding)
    #     best_idx = np.argmin(distances)
        
    #     # Increased threshold for more reliable detection
    #     THRESHOLD = 0.40
    #     if distances[best_idx] <= THRESHOLD:
    #         return True, names[best_idx]
    #     return False, None
    def get_guardian_templates(self, student_id):
        if student_id in self.guardian_cache:
            return self.guardian_cache[student_id]

        guardians = self.guardian_controller.get_guardians_for_student(student_id)
        known_encodings, names = [], []

        for g in guardians:
            decoded = self.guardian_controller.decode_face(g.get("face_encoding"))
            if decoded is not None:
                known_encodings.append(decoded)
                names.append(g["guardianname"])

        self.guardian_cache[student_id] = (known_encodings, names)
        return known_encodings, names


    def match_guardian(self, student_id, captured_encoding):
        known_encodings, names = self.get_guardian_templates(student_id)

        if not known_encodings:
            return False, None

        distances = face_recognition.face_distance(known_encodings, captured_encoding)
        best_idx = int(np.argmin(distances))
        best_distance = float(distances[best_idx])

        THRESHOLD = 0.40
        return (best_distance <= THRESHOLD), (names[best_idx] if best_distance <= THRESHOLD else None)

    
    def handle_recognized_guardian(self, student_id, fullname, guardian_name, status):
        # DROP-OFF
        if status is None or status["dropoff_time"] is None:
            self.guardian_controller.call_dropoff(student_id, guardian_name, True)
            QtWidgets.QMessageBox.information(
                self,
                "Drop-off Recorded",
                f"Drop-off by Guardian: \n{guardian_name}"
            )
            return

        # PICK-UP
        if status["pickup_time"] is None:
            self.guardian_controller.call_pickup(student_id, guardian_name, True)
            self.guardian_controller.clear_verification(student_id)
            QtWidgets.QMessageBox.information(
                self,
                "Pick-up Recorded",
                f"Pick-up by Guardian: \n{guardian_name}"
            )
            return

    # def handle_recognized_guardian(self, student_id, fullname, guardian_name, status):
    #     # DROP-OFF
    #     if status is None or status["dropoff_time"] is None:
    #         self.guardian_controller.call_dropoff(student_id, guardian_name, True)
    #         QtWidgets.QMessageBox.information(self, "Drop-off Recorded", guardian_name)
    #         return

    #     # PICK-UP
    #     if status["pickup_time"] is None:
    #         self.guardian_controller.call_pickup(student_id, guardian_name, True)
    #         self.guardian_controller.clear_verification(student_id)
    #         QtWidgets.QMessageBox.information(self, "Pick-up Recorded", guardian_name)
    #         return

    def handle_unrecognized_guardian(self, student_id, fullname, emergency_contact, status, item):
        """
        Handles situations where the guardian is not recognized.
        Properly manages DROP-OFF and PICK-UP flows, including X button handling
        and Scan Again functionality.
        """

        # ==================================================
        # ❌ DROP-OFF — UNRECOGNIZED
        # ==================================================
        if status is None or status["dropoff_time"] is None:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("Guardian Not Recognized")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(f"""
            <div style="text-align:center;">
                <p><b>Guardian NOT Recognized</b></p>
                <p>Action: DROP-OFF</p>
                <hr>
                <p><b>Emergency Contact</b></p>
                <p style="color:#8b2fdb;">{emergency_contact}</p>
                <p>{fullname}</p>
            </div>
            """)

            add_btn = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
            msg.exec()
            clicked = msg.clickedButton()

            # ❌ X or cancel → do nothing
            if clicked != add_btn:
                return

            # ✅ Add Guardian manually
            name, ok = QInputDialog.getText(self, "Add Guardian", "Guardian Name:")
            if ok and name.strip():
                self.guardian_controller.call_dropoff(student_id, name.strip(), True)
            return

        # ==================================================
        # 🔐 PICK-UP — FIRST UNRECOGNIZED (NO WAITING YET)
        # ==================================================
        if status["pickup_time"] is None and not self.guardian_controller.is_waiting_verification(student_id):
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("Guardian Not Recognized")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(f"""
            <div style="text-align:center;">
                <p><b>Guardian NOT Recognized</b></p>
                <p>Action: PICK-UP</p>
                <hr>
                <p><b>Emergency Contact</b></p>
                <p style="color:#8b2fdb;">{emergency_contact}</p>
                <p>Status: Waiting for parent verification</p>
            </div>
            """)

            verify_btn = msg.addButton("Verify Parent", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
            msg.exec()
            clicked = msg.clickedButton()

            # ❌ X → clear waiting flag, exit
            if clicked != verify_btn:
                self.guardian_controller.clear_verification(student_id)
                return

            # ✅ User clicked "Verify Parent" → set waiting flag
            self.guardian_controller.set_waiting_verification(student_id)
            return

        # ==================================================
        # 🔁 PICK-UP — VERIFICATION PENDING
        # ==================================================
        while True:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("Verification Pending")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(f"""
            <div style="text-align:center;">
                <p><b>Verification Pending</b></p>
                <hr>
                <p><b>Emergency Contact</b></p>
                <p style="color:#8b2fdb;">{emergency_contact}</p>
                <p>{fullname}</p>
            </div>
            """)

            # Add custom buttons
            scan_btn = msg.addButton("Scan Again", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
            add_btn  = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.ActionRole)

            # Add standard Cancel button (this gives the X a role)
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)

            result = msg.exec()  # returns Accepted, Rejected, etc

            # Check what happened
            clicked = msg.clickedButton()

            if result == QtWidgets.QMessageBox.StandardButton.Cancel or clicked not in [scan_btn, add_btn]:
                # User pressed X or Cancel
                # self.guardian_controller.clear_verification(student_id)
                return

            # ---------------- Scan Again ----------------
            clicked = msg.clickedButton()
            if clicked == scan_btn:
                self.guardian_controller.clear_verification(student_id)
                captured, frame = self.capture_student_face()
                if captured is None:
                    break  # user canceled camera
                recognized, guardian_name = self.match_guardian(student_id, captured)
                if recognized:
                    self.handle_recognized_guardian(student_id, fullname, guardian_name, status)
                    break
                else:
                    # continue loop → show Verification Pending again
                    continue

            # ---------------- Add Guardian ----------------
            if clicked == add_btn:
                name, ok = QInputDialog.getText(self, "Manual Pick-up", "Guardian Name:")
                if ok and name.strip():
                    self.guardian_controller.manual_pickup(student_id, name.strip())
                    self.guardian_controller.clear_verification(student_id)
                break  # exit loop

        # while True:  # loop until user closes or adds guardian
        #     msg = QtWidgets.QMessageBox(self)
        #     msg.setWindowTitle("Verification Pending")
        #     msg.setTextFormat(Qt.TextFormat.RichText)
        #     msg.setText(f"""
        #     <div style="text-align:center;">
        #         <p><b>Verification Pending</b></p>
        #         <hr>
        #         <p><b>Emergency Contact</b></p>
        #         <p style="color:#8b2fdb;">{emergency_contact}</p>
        #         <p>{fullname}</p>
        #     </div>
        #     """)

        #     # Add custom buttons
        #     scan_btn = msg.addButton("Scan Again", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        #     add_btn  = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.ActionRole)

        #     msg.exec()
        #     clicked = msg.clickedButton()


        #     # ❌ X → user closed popup
        #     if clicked is None:
        #         # User closed with X
        #         self.guardian_controller.clear_verification(student_id)
        #         break
            


        #     # ---------------- Scan Again ----------------
        #     if clicked == scan_btn:
        #         self.guardian_controller.clear_verification(student_id)
        #         captured, frame = self.capture_student_face()
        #         if captured is None:
        #             break  # user canceled camera

        #         recognized, guardian_name = self.match_guardian(student_id, captured)
        #         if recognized:
        #             self.handle_recognized_guardian(student_id, fullname, guardian_name, status)
        #             break
        #         else:
        #             # continue loop → show Verification Pending again
        #             continue

        #     # ---------------- Add Guardian ----------------
        #     if clicked == add_btn:
        #         name, ok = QInputDialog.getText(self, "Manual Pick-up", "Guardian Name:")
        #         if ok and name.strip():
        #             self.guardian_controller.manual_pickup(student_id, name.strip())
        #             self.guardian_controller.clear_verification(student_id)
        #         break  # exit loop
            
            






    # ---------------- Pop-up Helpers ----------------

    def show_unrecognized_popup(self, title, action, fullname, emergency_contact,
                            add_guardian_callback, show_scan_again=False, item=None):

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(f"""
        <div style="text-align:center;">
            <p><b>{title}</b></p>
            <p>Action: {action}</p>
            <hr>
            <p><b>Emergency Contact</b></p>
            <p style="color:#8b2fdb;">{emergency_contact}</p>
            <hr>
            <p>{fullname}</p>
        </div>
        """)

        add_btn = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        if show_scan_again:
            scan_btn = msg.addButton("Scan Again", QtWidgets.QMessageBox.ButtonRole.ActionRole)

        # msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
        msg.exec()

        clicked = msg.clickedButton()

        # ✅ X or Cancel
        if clicked is None or clicked == msg.button(QtWidgets.QMessageBox.StandardButton.Cancel):
            return

        if clicked == add_btn:
            name, ok = QInputDialog.getText(self, "Add Guardian", "Guardian Name:")
            if ok and name.strip():
                add_guardian_callback(name.strip())

        elif show_scan_again and clicked == scan_btn:
            self.handle_student_click(item)

    def show_verification_pending_popup(self, fullname, emergency_contact, student_id, item):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Verification Pending")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(f"""
        <div style="text-align:center;">
            <p><b>Verification Pending</b></p>
            <hr>
            <p><b>Emergency Contact</b></p>
            <p style="color:#8b2fdb;">{emergency_contact}</p>
            <p>{fullname}</p>
        </div>
        """)

        scan_btn = msg.addButton("Scan Again", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        add_btn  = msg.addButton("Add Guardian Name", QtWidgets.QMessageBox.ButtonRole.ActionRole)
        # msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)

        msg.exec()
        clicked = msg.clickedButton()

        # ✅ X OR CANCEL → DO NOTHING
        if clicked is None or clicked == msg.button(QtWidgets.QMessageBox.StandardButton.Cancel):
            return

        if clicked == scan_btn:
            self.handle_student_click(item)

        elif clicked == add_btn:
            name, ok = QInputDialog.getText(self, "Manual Pick-up", "Guardian Name:")
            if ok and name.strip():
                self.guardian_controller.manual_pickup(student_id, name.strip())
                self.guardian_controller.clear_verification(student_id)

    def show_verify_parent_popup(self, fullname, emergency_contact):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Guardian Not Recognized")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(f"""
        <div style="text-align:center;">
            <p><b>Guardian NOT Recognized</b></p>
            <p>Action: PICK-UP</p>
            <hr>
            <p><b>Emergency Contact</b></p>
            <p style="color:#8b2fdb;">{emergency_contact}</p>
            <p>Status: Waiting for parent verification</p>
        </div>
        """)

        msg.addButton("Verify Parent", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        msg.exec()


    
    def show_scan_again_popup(self, fullname, emergency_contact, student_id, item):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Verification Pending")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(f"""
        <div style="text-align:center;">
            <p><b>Verification Pending</b></p>
            <hr>
            <p><b>Emergency Contact</b></p>
            <p style="color:#8b2fdb;">{emergency_contact}</p>
            <p>{fullname}</p>
        </div>
        """)

        scan_btn = msg.addButton("Scan Again", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        # msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
        msg.exec()

        if msg.clickedButton() == scan_btn:
            self.capture_and_retry_pickup(student_id, item)


    def capture_and_retry_pickup(self, student_id, item):
        captured, frame = self.capture_student_face()
        if captured is None:
            return

        recognized, guardian_name = self.match_guardian(student_id, captured)

        student = self.get_student_from_item(item)
        fullname = f"{student['studlname']}, {student['studfname']} {student['studmname'] or ''}".strip()
        emergency_contact = student.get("studcontact") or "No emergency contact"

        if recognized:
            self.guardian_controller.call_pickup(student_id, guardian_name, True)
            self.guardian_controller.clear_verification(student_id)
            QtWidgets.QMessageBox.information(self, "Pick-up Recorded", guardian_name)
        else:
            self.show_verify_parent_popup(fullname, emergency_contact)

    # ----------------------------------------------------
    # BACK TO CHOOSE MODE
    # ----------------------------------------------------
    def go_back(self):
        from views.mode import ChooseModeWindow
        self.mode = ChooseModeWindow(self.username)
        self.mode.show()
        self.close()
