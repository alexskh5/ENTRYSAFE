import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

BASE_DIR = path.dirname(path.abspath(__file__))        
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))  

UI_FILE = path.join(PROJECT_ROOT, "ui", "signup.ui")
LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")

class SignupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI into QMainWindow
        uic.loadUi(UI_FILE, self)

        # Stacked widget navigation
        try:
            self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
            self.signUpPage = self.findChild(QtWidgets.QWidget, "signUpPage")
            self.securityPage = self.findChild(QtWidgets.QWidget, "securityPage")

            # set initial page to mainStudentPage
            if self.stacked and self.signUpPage:
                self.stacked.setCurrentWidget(self.signUpPage)

            # find navigation buttons
            self.nextBtn = self.findChild(QtWidgets.QPushButton, "nextBtn")
            self.backToLoginBtn = self.findChild(QtWidgets.QPushButton, "backToLoginBtn")
            self.backToSignupBtn = self.findChild(QtWidgets.QPushButton, "backToSignupBtn")
            self.signupBtn = self.findChild(QtWidgets.QPushButton, "signupBtn")

            # connect buttons (only if both button and target page exist)
            if self.nextBtn and self.securityPage:
                self.nextBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.securityPage))
            if self.backToSignupBtn and self.signUpPage:
                self.backToSignupBtn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.signUpPage))
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
        self._bg_label.lower()      # send to back
        self._bg_label.resize(cw.size())

        # --- Make rightFrame transparent ---
        right = self.findChild(QtWidgets.QFrame, "rightFrame")
        if right:
            right.setStyleSheet("background: transparent;")
            right.setAutoFillBackground(False)

        # --- Make leftFrame transparent ---
        left = self.findChild(QtWidgets.QFrame, "leftFrame")
        if left:
            left.setStyleSheet("background: transparent;")
            left.setAutoFillBackground(False)


        # --- Logo Label ---
        self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
        self._orig_logo_pix = QPixmap(LOGO_FILE)
        if self.logo_label and not self._orig_logo_pix.isNull():
            self.logo_label.setScaledContents(False)
            self.logo_label.setStyleSheet("background: transparent;")
            self.logo_label.setPixmap(self._orig_logo_pix)

        self.setWindowTitle("EntrySafe - Sign Up")

        # Logo scaling settings
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 800
        self.ABS_MIN_W = 120

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # --- Resize background to fill area ---
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        scaled_bg = self._bg_pix.scaled(
            cw.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self._bg_label.setPixmap(scaled_bg)
        self._bg_label.resize(cw.size())
        self._bg_label.move(0, 0)

        # --- Resize logo ---
        if not self._orig_logo_pix.isNull() and self.logo_label:
            target_w = int(self.width() * self.MAX_PROP)
            target_w = max(self.ABS_MIN_W, min(target_w, self.ABS_MAX_W))

            scaled_logo = self._orig_logo_pix.scaled(
                target_w, target_w,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = SignupWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
