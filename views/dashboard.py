# import sys
# from os import path
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

# BASE_DIR = path.dirname(path.abspath(__file__))
# PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

# UI_FILE = path.join(PROJECT_ROOT, "ui", "dashboard.ui")
# BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


# class AdminWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Load UI into QMainWindow
#         uic.loadUi(UI_FILE, self)

#         # --- Background image using QLabel (behind everything) ---
#         cw = self.findChild(QtWidgets.QWidget, "centralwidget")

#         self._bg_label = QtWidgets.QLabel(cw)
#         self._bg_pix = QPixmap(BG_FILE)
#         self._bg_label.setPixmap(self._bg_pix)
#         self._bg_label.setScaledContents(False)
#         self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
#         self._bg_label.lower()
#         self._bg_label.resize(cw.size())

#         # --- Sidebar toggle setup ---

#         self.menu_widget = self.findChild(QtWidgets.QWidget, "menuSubContainer")
#         self.main_widget = self.findChild(QtWidgets.QWidget, "mainContainer")

#         self.left_frame = self.findChild(QtWidgets.QFrame, "leftFrame")

#         # DON'T trust .width() at init — layouts might not be applied yet.
#         self._menu_expanded_width = 500  # preferred fallback width

#         # prepare animation (if the menu exists)
#         if self.menu_widget:
#             self._menu_animation = QPropertyAnimation(self.menu_widget, b"maximumWidth")
#             self._menu_animation.setDuration(250)
#             self._menu_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
#             self.menu_widget.setMaximumWidth(self._menu_expanded_width)
#         else:
#             self._menu_animation = None

#         # Connect toggle buttons (picBtn to collapse, picBtn_2 to expand)
#         pic_btn = self.findChild(QtWidgets.QPushButton, "picBtn") or self.findChild(QtWidgets.QLabel, "picBtn")
#         pic_btn_2 = self.findChild(QtWidgets.QPushButton, "picBtn_2") or self.findChild(QtWidgets.QLabel, "picBtn_2")

#         if pic_btn is not None:
#             try:
#                 pic_btn.clicked.connect(self.collapse_menu)
#             except Exception:
#                 pic_btn.mousePressEvent = lambda ev: self.collapse_menu()
#         if pic_btn_2 is not None:
#             try:
#                 pic_btn_2.clicked.connect(self.expand_menu)
#             except Exception:
#                 pic_btn_2.mousePressEvent = lambda ev: self.expand_menu()

#         # -------- START HIDDEN: collapse the sidebar initially --------
#         # Ensure left_frame (the small left bar with picBtn_2/welcomeLabel) is visible when collapsed
#         if self.left_frame:
#             self.left_frame.setVisible(True)

#         # Collapse the menu visually at startup by forcing maximumWidth to 0.
#         # Note: showEvent will still compute the real expanded width later.
#         if self.menu_widget:
#             self.menu_widget.setMaximumWidth(0)
#             # also resize to zero width to avoid a flicker in some systems
#             try:
#                 self.menu_widget.resize(0, self.menu_widget.height())
#             except Exception:
#                 pass

#     def showEvent(self, event):
#         """
#         After window shown and layouts applied, record the real expanded width.
#         """
#         super().showEvent(event)
#         if self.menu_widget:
#             real_w = self.menu_widget.width()
#             hint_w = self.menu_widget.sizeHint().width() or self._menu_expanded_width
#             self._menu_expanded_width = real_w if real_w > 50 else (hint_w if hint_w > 50 else self._menu_expanded_width)
#             # don't automatically expand — just ensure the stored expanded width is correct
#             self.menu_widget.setMaximumWidth(0)  # keep collapsed at startup

#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         # Resize background to fill area
#         try:
#             cw = self.findChild(QtWidgets.QWidget, "centralwidget")
#             scaled_bg = self._bg_pix.scaled(
#                 cw.size(),
#                 Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#                 Qt.TransformationMode.SmoothTransformation
#             )
#             self._bg_label.setPixmap(scaled_bg)
#             self._bg_label.resize(cw.size())
#             self._bg_label.move(0, 0)
#         except Exception:
#             pass

#     def _connect_finished_handler(self, handler):
#         """Helper: disconnect existing finished handlers then connect the new one."""
#         if not self._menu_animation:
#             return
#         try:
#             # attempt to disconnect all existing slots from finished
#             self._menu_animation.finished.disconnect()
#         except Exception:
#             # ignore if there were none
#             pass
#         try:
#             self._menu_animation.finished.connect(handler)
#         except Exception:
#             pass

#     def collapse_menu(self):
#         """
#         Animate sidebar to zero width (hide).
#         Show left_frame immediately (so it appears while sidebar is collapsed).
#         """
#         # If left_frame exists, show it immediately
#         if self.left_frame:
#             self.left_frame.setVisible(True)
#             # ensure UI updates immediately
#             self.left_frame.repaint()

#         if not self.menu_widget or not self._menu_animation:
#             return

#         current = self.menu_widget.width()

#         # finished handler: when collapse finishes, ensure maximumWidth stays at 0
#         def _on_collapse_finished():
#             try:
#                 # keep it collapsed
#                 self.menu_widget.setMaximumWidth(0)
#             except Exception:
#                 pass
#             try:
#                 self._menu_animation.finished.disconnect(_on_collapse_finished)
#             except Exception:
#                 pass

#         # connect handler and animate
#         self._connect_finished_handler(_on_collapse_finished)
#         self._menu_animation.stop()
#         self._menu_animation.setStartValue(current)
#         self._menu_animation.setEndValue(0)
#         self._menu_animation.start()

#     def expand_menu(self):
#         """
#         Animate sidebar back to original width (show).
#         Hide left_frame immediately so it won't be visible while sidebar is shown.
#         """
#         # Hide left_frame immediately (so it disappears before the expand)
#         if self.left_frame:
#             self.left_frame.setVisible(False)
#             # ensure UI updates immediately
#             self.left_frame.repaint()

#         if not self.menu_widget or not self._menu_animation:
#             return

#         current = self.menu_widget.width()
#         # recompute fallback if needed
#         if not self._menu_expanded_width or self._menu_expanded_width <= 50:
#             hint_w = self.menu_widget.sizeHint().width() or 500
#             self._menu_expanded_width = hint_w if hint_w > 50 else max(200, self._menu_expanded_width)

#         target = self._menu_expanded_width

#         # finished handler: after expand, set maximumWidth to target (stable)
#         def _on_expand_finished():
#             try:
#                 self.menu_widget.setMaximumWidth(target)
#             except Exception:
#                 pass
#             try:
#                 self._menu_animation.finished.disconnect(_on_expand_finished)
#             except Exception:
#                 pass

#         # connect handler and animate
#         self._connect_finished_handler(_on_expand_finished)
#         self._menu_animation.stop()
#         self._menu_animation.setStartValue(current)
#         self._menu_animation.setEndValue(target)
#         self._menu_animation.start()


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     win = AdminWindow()
#     win.show()
#     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()


import sys
from os import path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

BASE_DIR = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.abspath(path.join(BASE_DIR, ".."))

UI_FILE = path.join(PROJECT_ROOT, "ui", "dashboard.ui")
BG_FILE = path.join(PROJECT_ROOT, "assets", "images", "bg1.png")


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username   # store username

        uic.loadUi(UI_FILE, self)

        # Background setup
        cw = self.findChild(QtWidgets.QWidget, "centralwidget")
        self._bg_label = QtWidgets.QLabel(cw)
        self._bg_pix = QPixmap(BG_FILE)
        self._bg_label.setPixmap(self._bg_pix)
        self._bg_label.setScaledContents(False)
        self._bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._bg_label.lower()
        self._bg_label.resize(cw.size())

        # Sidebar
        self.menu_widget = self.findChild(QtWidgets.QWidget, "menuSubContainer")
        self.main_widget = self.findChild(QtWidgets.QWidget, "mainContainer")
        self.left_frame = self.findChild(QtWidgets.QFrame, "leftFrame")
        self._menu_expanded_width = 500

        if self.menu_widget:
            self._menu_animation = QPropertyAnimation(self.menu_widget, b"maximumWidth")
            self._menu_animation.setDuration(250)
            self._menu_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.menu_widget.setMaximumWidth(self._menu_expanded_width)
        else:
            self._menu_animation = None

        pic_btn = self.findChild(QtWidgets.QPushButton, "picBtn") or self.findChild(QtWidgets.QLabel, "picBtn")
        pic_btn_2 = self.findChild(QtWidgets.QPushButton, "picBtn_2") or self.findChild(QtWidgets.QLabel, "picBtn_2")

        if pic_btn:
            try:
                pic_btn.clicked.connect(self.collapse_menu)
            except:
                pic_btn.mousePressEvent = lambda ev: self.collapse_menu()

        if pic_btn_2:
            try:
                pic_btn_2.clicked.connect(self.expand_menu)
            except:
                pic_btn_2.mousePressEvent = lambda ev: self.expand_menu()

        # collapse initially
        if self.left_frame:
            self.left_frame.setVisible(True)

        if self.menu_widget:
            self.menu_widget.setMaximumWidth(0)
            try:
                self.menu_widget.resize(0, self.menu_widget.height())
            except:
                pass

        # --------------------------------
        # 🔥 DISPLAY USERNAME
        # --------------------------------
        self.adminLabel = self.findChild(QtWidgets.QLabel, "adminLabel")
        if self.adminLabel:
            self.adminLabel.setText(self.username)

        # --------------------------------
        # 🔥 LOGOUT BUTTON
        # --------------------------------
        self.logOutBtn = self.findChild(QtWidgets.QPushButton, "logOutBtn")
        if self.logOutBtn:
            self.logOutBtn.clicked.connect(self.logout)

        # --------------------------------
        # 🔥 ROUTE TO STUDENT PAGE
        # --------------------------------
        self.StudentBtn = self.findChild(QtWidgets.QPushButton, "StudentBtn")
        if self.StudentBtn:
            self.StudentBtn.clicked.connect(self.go_student_page)


    # ---------------- Logout Function ----------------
    def logout(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to log out?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            from views.login import LoginWindow
            self.close()
            self.login = LoginWindow()
            self.login.show()


    # ---------------- Route Student Page ----------------
    def go_student_page(self):
        from views.student import StudentWindow
        self.close()
        self.stud = StudentWindow(self.username)
        self.stud.show()
       
        
    
    # ---------------- COLLAPSE MENU ----------------
    def collapse_menu(self):
        if self.left_frame:
            self.left_frame.setVisible(True)

        if not self.menu_widget or not self._menu_animation:
            return

        current = self.menu_widget.width()

        self._menu_animation.stop()
        self._menu_animation.setStartValue(current)
        self._menu_animation.setEndValue(0)
        self._menu_animation.start()


    # ---------------- EXPAND MENU ----------------
    def expand_menu(self):
        if self.left_frame:
            self.left_frame.setVisible(False)

        if not self.menu_widget or not self._menu_animation:
            return

        current = self.menu_widget.width()
        target = self._menu_expanded_width

        self._menu_animation.stop()
        self._menu_animation.setStartValue(current)
        self._menu_animation.setEndValue(target)
        self._menu_animation.start()
