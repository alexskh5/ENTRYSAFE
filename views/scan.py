import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

BASE_DIR = path.dirname(path.abspath(__file__))       
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))  

UI_FILE = path.join(PROJECT_ROOT, "ui", "scan.ui")
LOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "appLogo.png")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")
AMLOGO_FILE = path.join(PROJECT_ROOT, "assets", "images", "AMLogo.png")
FACESCAN_FILE = path.join(PROJECT_ROOT, "assets", "images", "faceScan.png")

class ScanWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI into QMainWindow
        uic.loadUi(UI_FILE, self)

        # --- Ensure attendance page is the initial page in the stacked widget ---
        # "scanPage" name sa next page na iclick para mugwas ang camera
        self.stacked = self.findChild(QtWidgets.QStackedWidget, "stackedWidget") 
        if self.stacked:
            attendance_page = self.findChild(QtWidgets.QWidget, "attendancePage")
            if attendance_page:
                self.stacked.setCurrentWidget(attendance_page)
            else:
                # fallback to index 0
                try:
                    self.stacked.setCurrentIndex(0)
                except Exception:
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

        # frames transparent
        for name in ("rightFrame", "textFrame", "logoFrame"):
            frame = self.findChild(QtWidgets.QFrame, name)
            if frame:
                frame.setStyleSheet("background: transparent;")
                frame.setAutoFillBackground(False)

        # --- Labels and pixmaps ---
        self.logo_label = self.findChild(QtWidgets.QLabel, "logoLabel")
        self._orig_logo_pix = QPixmap(LOGO_FILE)

        self.am_logo_label = self.findChild(QtWidgets.QLabel, "amLogo")
        self._am_logo_pix = QPixmap(AMLOGO_FILE)

        self.facescan_btn = self.findChild(QtWidgets.QPushButton, "scanBtn")
        self._facescan_pix = QPixmap(FACESCAN_FILE)


        # ensure labels won't auto-scale their contents; we'll scale manually for quality
        for lbl in (self.logo_label, self.am_logo_label, self.facescan_btn):
            if lbl is not None:
                try:
                    lbl.setScaledContents(False)
                    lbl.setStyleSheet("background: transparent;")
                except Exception:
                    pass

        self.setWindowTitle("EntrySafe - Gate")

        # Logo scaling settings
        self.MAX_PROP = 0.40
        self.ABS_MAX_W = 800
        self.ABS_MIN_W = 120
        


        # "listWidget" name na ara sa qt designer para gawsanan sa results nig search sa attendance
        # nagtesting koy butang unta dummy data para makita nakon say itsura sa results para maadjust css ang blema kay nagvinugo si chatgpt



    def _scale_to_label(self, pix: QPixmap, label: QtWidgets.QLabel) -> None:
        """Scale pixmap to the label's current size keeping aspect ratio & quality."""
        if pix is None or pix.isNull() or label is None:
            return
        lbl_size = label.size()
        if lbl_size.width() <= 0 or lbl_size.height() <= 0:
            return
        scaled = pix.scaled(
            QSize(lbl_size.width(), lbl_size.height()),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        label.setPixmap(scaled)

    def _scale_icon_to_button(self, pixmap: QPixmap, button: QtWidgets.QPushButton):
        """Scale a QPixmap and set it as the QPushButton icon (keeps aspect ratio)."""
        if pixmap is None or pixmap.isNull() or button is None:
            return
        btn_w = max(1, button.width())
        btn_h = max(1, button.height())
        target_side = min(btn_w, btn_h)

        scaled = pixmap.scaled(
            QSize(target_side, target_side),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # wrap scaled QPixmap in a QIcon
        button.setIcon(QIcon(scaled))
        button.setIconSize(scaled.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # --- Resize background to fill centralwidget (cover behavior) ---
        cw = self.findChild(QtWidgets.QWidget, "centralwidget") or self.centralWidget()
        if getattr(self, "_bg_pix", None) and not self._bg_pix.isNull():
            scaled_bg = self._bg_pix.scaled(
                cw.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._bg_label.setPixmap(scaled_bg)
            self._bg_label.resize(cw.size())
            self._bg_label.move(0, 0)

        # --- Scale each image to its LABEL size (matches Designer preview) ---
        if getattr(self, "_orig_logo_pix", None) and self.logo_label:
            self._scale_to_label(self._orig_logo_pix, self.logo_label)

        if getattr(self, "_am_logo_pix", None) and self.am_logo_label:
            self._scale_to_label(self._am_logo_pix, self.am_logo_label)

        if getattr(self, "_facescan_pix", None) and self.facescan_btn:
            self._scale_icon_to_button(self._facescan_pix, self.facescan_btn)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = ScanWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
