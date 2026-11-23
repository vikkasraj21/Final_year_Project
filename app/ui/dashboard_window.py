from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QHBoxLayout, QFrame,
    QGridLayout, QStackedWidget
)

from PyQt6.QtCore import Qt
from app.services.dashboard_service import get_dashboard_stats
from app.ui.department_window import DepartmentWindow
from app.ui.faculty_window import FacultyWindow
from app.ui.subject_window import SubjectWindow


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Dashboard")
        self.resize(1100, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #F3F4F6;
                font-family: Segoe UI;
            }

            QFrame#header {
                background-color: #1B1F2A;
                border-radius: 12px;
            }

            QLabel#heading {
                font-size: 26px;
                font-weight: bold;
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

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1B1F2A;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 30, 15, 20)
        sidebar_layout.setSpacing(12)

        sidebar_title = QLabel("TIMETABLE ADMIN")
        sidebar_title.setStyleSheet(
            "font-size: 17px; font-weight: bold; color: #60A5FA;"
        )
        sidebar_layout.addWidget(sidebar_title)

        menu_items = [
            "Dashboard",
            "Departments",
            "Faculty",
            "Subjects",
            "Class Sections",
            "Classrooms",
            "Teaching Allocations",
            "Generate Timetable",
            "View Timetable",
            "Faculty Leaves",
            "Alteration Management"
        ]

        for item in menu_items:
            button = QPushButton(item)
            button.clicked.connect(
                lambda checked=False, page=item: self.change_page(page)
            )
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        main_layout.addWidget(sidebar)

        self.page_stack = QStackedWidget()
        self.page_stack.addWidget(content)

        self.department_page = DepartmentWindow()
        self.page_stack.addWidget(self.department_page)

        self.faculty_page = FacultyWindow()
        self.page_stack.addWidget(self.faculty_page)

        self.subject_window = SubjectWindow()
        self.page_stack.addWidget(self.subject_window)

        main_layout.addWidget(self.page_stack)

        header = QFrame()
        header.setObjectName("header")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 20, 25, 20)

        heading = QLabel("Admin Dashboard")
        heading.setObjectName("heading")

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.handle_logout)
        logout_button.setFixedWidth(120)

        header_layout.addWidget(heading)
        header_layout.addStretch()
        header_layout.addWidget(logout_button)

        welcome = QLabel(
            "Welcome to the College Timetable Management System"
        )
        self.page_heading = heading
        self.welcome_label = welcome
        welcome.setStyleSheet(
            "font-size: 18px; color: #9CA3AF;"
        )

        content_layout.addWidget(header)
        content_layout.addWidget(welcome)

        stats = get_dashboard_stats()

        stats_grid = QGridLayout()
        stats_grid.setSpacing(18)

        card_titles = {
            "departments": "Departments",
            "faculty": "Faculty Members",
            "subjects": "Subjects",
            "classrooms": "Classrooms",
            "class_sections": "Class Sections",
            "timetable_entries": "Timetable Entries"
        }

        for index, (key, title) in enumerate(card_titles.items()):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #1B1F2A;
                    border-radius: 12px;
                }
            """)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)

            count_label = QLabel(str(stats[key]))
            count_label.setStyleSheet(
                "font-size: 32px; font-weight: bold; color: #60A5FA;"
            )

            title_label = QLabel(title)
            title_label.setStyleSheet(
                "font-size: 14px; color: #9CA3AF;"
            )

            card_layout.addWidget(count_label)
            card_layout.addWidget(title_label)

            row = index // 3
            column = index % 3

            stats_grid.addWidget(card, row, column)

        content_layout.addLayout(stats_grid)
        content_layout.addStretch()

    def handle_logout(self):
        from app.ui.login_window import LoginWindow

        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def change_page(self, page_name):
        if page_name == "Departments":
            self.page_stack.setCurrentWidget(self.department_page)

        elif page_name == "Faculty":
            self.page_stack.setCurrentWidget(self.faculty_page)

        elif page_name == "Subjects":
            self.page_stack.setCurrentWidget(self.subject_window)

        else:
            self.page_stack.setCurrentIndex(0)

            self.page_heading.setText(
                "Admin Dashboard" if page_name == "Dashboard" else page_name
            )

            if page_name == "Dashboard":
                self.welcome_label.setText(
                "Welcome to the College Timetable Management System"
                )
            else:
                self.welcome_label.setText(
                    f"{page_name} Management Module"
                )
