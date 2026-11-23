import re
from mysql.connector import IntegrityError
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)
from app.services.department_service import get_all_departments
from app.services.faculty_service import (
    add_faculty,
    get_all_faculty,
    update_faculty,
    delete_faculty
)

class FacultyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Faculty Management")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("Faculty Management")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        layout.addWidget(title)

        # Faculty input form
        form_layout = QVBoxLayout()

        self.faculty_name = QLineEdit()
        self.faculty_name.setPlaceholderText("Enter Faculty Name")
        self.faculty_name.setMaxLength(100)

        self.faculty_email = QLineEdit()
        self.faculty_email.setPlaceholderText("Enter Faculty Email")
        self.faculty_email.setMaxLength(100)
        self.department_dropdown = QComboBox()
        self.department_dropdown.addItem("Select Department", None)

        form_layout.addWidget(self.faculty_name)
        form_layout.addWidget(self.faculty_email)
        form_layout.addWidget(self.department_dropdown)

        layout.addLayout(form_layout)
        self.load_departments()
        self.add_button = QPushButton("Add Faculty")
        self.add_button.clicked.connect(self.handle_add_faculty)
        self.update_button = QPushButton("Update Faculty")
        self.update_button.clicked.connect(self.handle_update_faculty)
        self.delete_button = QPushButton("Delete Faculty")
        self.delete_button.clicked.connect(self.handle_delete_faculty)
        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.clicked.connect(self.handle_clear_selection)

        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        button_layout = QHBoxLayout()

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)
        # Faculty records table
        self.faculty_table = QTableWidget()
        self.selected_faculty_id = None
        self.faculty_table.cellClicked.connect(self.select_faculty)
        self.faculty_table.setColumnCount(4)
        self.faculty_table.setHorizontalHeaderLabels(
            ["Faculty ID", "Faculty Name", "Email", "Department"]
        )

        self.faculty_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.faculty_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.faculty_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        layout.addWidget(self.faculty_table)
        self.load_faculty()

    def load_departments(self):
        try:
            departments = get_all_departments()

            self.department_dropdown.clear()
            self.department_dropdown.addItem("Select Department", None)

            for department_id, department_code, department_name in departments:
                self.department_dropdown.addItem(
                    f"{department_code} - {department_name}",
                    department_id
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load departments:\n{error}"
            )

    def handle_add_faculty(self):
        faculty_name = self.faculty_name.text().strip()
        faculty_email = self.faculty_email.text().strip()
        department_id = self.department_dropdown.currentData()

        if not faculty_name or not faculty_email or department_id is None:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter a faculty name, email, and select a department."
            )
            return

        if not self.is_valid_email(faculty_email):
            QMessageBox.warning(
                self,
                "Invalid Email",
                "Please enter a valid faculty email address."
            )
            return

        try:
            add_faculty(faculty_name, faculty_email, department_id)
            self.load_faculty()

            self.faculty_name.clear()
            self.faculty_email.clear()
            self.department_dropdown.setCurrentIndex(0)

            QMessageBox.information(
                self,
                "Success",
                "Faculty added successfully!"
            )

        except IntegrityError as error:
            if error.errno == 1062:
                QMessageBox.warning(
                    self,
                    "Duplicate Email",
                    "This email address is already registered to another faculty member."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Database Error",
                    f"Unable to add faculty:\n{error}"
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to add faculty:\n{error}"
            )

    def load_faculty(self):
        try:
            faculty_records = get_all_faculty()

            self.faculty_table.setRowCount(len(faculty_records))

            for row, record in enumerate(faculty_records):
                faculty_id, faculty_name, faculty_email, department_id, department_name = record

                self.faculty_table.setItem(
                    row, 0, QTableWidgetItem(str(faculty_id))
                )

                self.faculty_table.setItem(
                    row, 1, QTableWidgetItem(faculty_name)
                )

                self.faculty_table.setItem(
                    row, 2, QTableWidgetItem(faculty_email or "")
                )

                self.faculty_table.setItem(
                    row, 3, QTableWidgetItem(department_name)
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load faculty records:\n{error}"
            )

    def select_faculty(self, row, column):
        self.selected_faculty_id = int(
            self.faculty_table.item(row, 0).text()
        )

        faculty_name = self.faculty_table.item(row, 1).text()
        faculty_email = self.faculty_table.item(row, 2).text()

        self.faculty_name.setText(faculty_name)
        self.faculty_email.setText(faculty_email)

        faculty_records = get_all_faculty()

        for record in faculty_records:
            if record[0] == self.selected_faculty_id:
                department_id = record[3]

                index = self.department_dropdown.findData(department_id)
                self.department_dropdown.setCurrentIndex(index)
                break

        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def handle_update_faculty(self):
        if self.selected_faculty_id is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a faculty member first."
            )
            return

        faculty_name = self.faculty_name.text().strip()
        faculty_email = self.faculty_email.text().strip()
        department_id = self.department_dropdown.currentData()

        if not faculty_name or not faculty_email or department_id is None:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter a faculty name, email, and select a department."
            )
            return

        if not self.is_valid_email(faculty_email):
            QMessageBox.warning(
                self,
                "Invalid Email",
                "Please enter a valid faculty email address."
            )
            return

        try:
            rows_updated = update_faculty(
                self.selected_faculty_id,
                faculty_name,
                faculty_email,
                department_id
            )

            if rows_updated == 0:
                QMessageBox.information(
                    self,
                    "No Changes",
                    "No faculty record was changed."
                )
                return

            self.selected_faculty_id = None
            self.faculty_name.clear()
            self.faculty_email.clear()
            self.department_dropdown.setCurrentIndex(0)
            self.faculty_table.clearSelection()
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)

            self.load_faculty()

            QMessageBox.information(
                self,
                "Success",
                "Faculty updated successfully!"
            )

        except IntegrityError as error:
            if error.errno == 1062:
                QMessageBox.warning(
                    self,
                    "Duplicate Email",
                    "This email address is already registered to another faculty member."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Database Error",
                    f"Unable to update faculty:\n{error}"
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to update faculty:\n{error}"
            )

    def handle_delete_faculty(self):
        if self.selected_faculty_id is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a faculty member first."
            )
            return

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this faculty member?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            rows_deleted = delete_faculty(self.selected_faculty_id)

            if rows_deleted == 0:
                QMessageBox.warning(
                    self,
                    "Not Found",
                    "Faculty record was not found."
                )
                return

            self.selected_faculty_id = None
            self.faculty_name.clear()
            self.faculty_email.clear()
            self.department_dropdown.setCurrentIndex(0)
            self.faculty_table.clearSelection()
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)

            self.load_faculty()

            QMessageBox.information(
                self,
                "Success",
                "Faculty deleted successfully!"
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Deletion Failed",
                f"Unable to delete faculty:\n{error}"
            )

    def handle_clear_selection(self):
        self.selected_faculty_id = None

        self.faculty_name.clear()
        self.faculty_email.clear()
        self.department_dropdown.setCurrentIndex(0)

        self.faculty_table.clearSelection()

        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def is_valid_email(self, email):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.fullmatch(pattern, email) is not None