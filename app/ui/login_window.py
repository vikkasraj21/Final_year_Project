
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame,
    QMessageBox
)
from PyQt6.QtCore import Qt
from app.services.auth_service import authenticate_admin
from app.ui.dashboard_window import DashboardWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Login")
        self.resize(1000, 650)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #F3F4F6;
                font-family: Segoe UI;
            }

            QFrame#loginCard {
                background-color: #1B1F2A;
                border-radius: 18px;
            }

            QLineEdit {
                background-color: #252B38;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #3B82F6;
            }

            QPushButton {
                background-color: #3B82F6;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2563EB;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(400)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(35, 40, 35, 40)
        layout.setSpacing(18)

        title = QLabel("ADMIN LOGIN")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 26px; font-weight: bold;"
        )

        subtitle = QLabel("College Timetable Management System")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            "color: #9CA3AF; font-size: 13px;"
        )

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)

        main_layout.addWidget(card)

    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter both username and password."
            )
            return

        if authenticate_admin(username, password):
            QMessageBox.information(
                self,
                "Login Successful",
                "Welcome, Admin!"
            )

            self.password.clear()

            self.dashboard = DashboardWindow()
            self.dashboard.show()
            self.close()

        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )

            self.password.clear()
