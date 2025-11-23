from PyQt6.QtWidgets import QMainWindow, QLabel

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EntrySafe Dashboard")

        label = QLabel("Login / Signup Successful!", self)
        label.setGeometry(50, 50, 300, 40)
