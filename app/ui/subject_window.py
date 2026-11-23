from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton, QHBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from app.services.department_service import get_all_departments
from PyQt6.QtWidgets import QMessageBox
from mysql.connector import IntegrityError
from app.services.subject_service import (
    add_subject,
    get_all_subjects,
    update_subject,
    delete_subject
)


class SubjectWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        title = QLabel("Subject Management")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("""
           font-size: 28px;
            font-weight: bold;
            padding: 0px;
            margin-bottom: 15px;
        """)

        self.layout.addWidget(title)

        self.subject_code_input = QLineEdit()
        self.subject_code_input.setPlaceholderText(
            "Enter Subject Code (e.g., CS301)"
        )

        self.subject_code_input.setStyleSheet("""
            QLineEdit {
                background-color: #252525;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        self.layout.addWidget(self.subject_code_input)

        self.subject_name_input = QLineEdit()
        self.subject_name_input.setPlaceholderText(
            "Enter Subject Name (e.g., Artificial Intelligence)"
        )

        self.subject_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #252525;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        self.layout.addWidget(self.subject_name_input)
        self.department_combo = QComboBox()

        self.department_combo.setStyleSheet("""
            QComboBox {
                background-color: #252525;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        self.department_combo.addItem("Select Department", None)

        self.layout.addWidget(self.department_combo)
        departments = get_all_departments()

        for department in departments:
            department_id = department[0]
            department_name = department[2]

            self.department_combo.addItem(
                department_name,
                department_id
            )
        self.subject_type_combo = QComboBox()

        self.subject_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #252525;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        self.subject_type_combo.addItem("Select Subject Type", None)
        self.subject_type_combo.addItem("Theory", "Theory")
        self.subject_type_combo.addItem("Lab", "Lab")

        self.layout.addWidget(self.subject_type_combo)
        self.periods_input = QSpinBox()

        self.periods_input.setRange(1, 30)
        self.periods_input.setValue(4)
        self.periods_input.setPrefix("Periods Per Week: ")

        self.periods_input.setStyleSheet("""
            QSpinBox {
                background-color: #252525;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        self.layout.addWidget(self.periods_input)
        self.add_button = QPushButton("Add Subject")

        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        self.update_button = QPushButton("Update Subject")

        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #047857;
            }
        """)

        self.delete_button = QPushButton("Delete Subject")

        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #475569;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #64748b;
            }
        """)

        button_layout.addWidget(self.clear_button)

        self.layout.addLayout(button_layout)
        self.add_button.clicked.connect(self.handle_add_subject)
        self.update_button.clicked.connect(self.handle_update_subject)
        self.delete_button.clicked.connect(self.handle_delete_subject)
        self.clear_button.clicked.connect(self.handle_clear_selection)
        self.subject_table = QTableWidget()

        self.subject_table.setColumnCount(6)

        self.subject_table.setHorizontalHeaderLabels([
            "ID",
            "Subject Code",
            "Subject Name",
            "Department",
            "Type",
            "Periods/Week"
        ])

        self.subject_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.subject_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.subject_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.subject_table.setStyleSheet("""
            QTableWidget {
                background-color: #252525;
                color: white;
                gridline-color: #444444;
                border: 1px solid #444444;
                border-radius: 6px;
            }

            QHeaderView::section {
                background-color: #333333;
                color: white;
                padding: 8px;
                border: 1px solid #444444;
            }
        """)

        self.layout.addWidget(self.subject_table, 1)
        self.load_subjects()
        self.selected_subject_id = None

        self.subject_table.itemSelectionChanged.connect(
            self.handle_subject_selection
        )

    def handle_add_subject(self):
        subject_code = self.subject_code_input.text().strip().upper()
        subject_name = self.subject_name_input.text().strip()
        department_id = self.department_combo.currentData()
        subject_type = self.subject_type_combo.currentData()
        periods_per_week = self.periods_input.value()

        if not subject_code or not subject_name:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the subject code and name."
            )
            return

        if department_id is None or subject_type is None:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please select a department and subject type."
            )
            return

        try:
            add_subject(
                subject_code,
                subject_name,
                department_id,
                subject_type,
                periods_per_week
            )

            self.load_subjects()

            QMessageBox.information(
                self,
                "Success",
                "Subject added successfully!"
            )

            self.subject_code_input.clear()
            self.subject_name_input.clear()
            self.department_combo.setCurrentIndex(0)
            self.subject_type_combo.setCurrentIndex(0)
            self.periods_input.setValue(4)

        except IntegrityError as error:
            if error.errno == 1062:
                message = "This subject code already exists."
            else:
                message = str(error)

            QMessageBox.warning(self, "Database Error", message)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Unable to add subject:\n{error}"
            )

    def load_subjects(self):
        try:
            subjects = get_all_subjects()

            self.subject_table.setRowCount(len(subjects))

            for row_index, subject in enumerate(subjects):
                values = [
                    subject[0],  # Subject ID
                    subject[1],  # Subject Code
                    subject[2],  # Subject Name
                    subject[4],  # Department Name
                    subject[5],  # Subject Type
                    subject[6]   # Periods Per Week
                ]

                for column_index, value in enumerate(values):
                    item = QTableWidgetItem(str(value))

                    self.subject_table.setItem(
                        row_index,
                        column_index,
                        item
                    )

            self.subject_table.resizeColumnsToContents()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load subjects:\n{error}"
            )

    def handle_subject_selection(self):
        selected_row = self.subject_table.currentRow()

        if selected_row < 0:
            self.selected_subject_id = None
            return

        subject_id_item = self.subject_table.item(selected_row, 0)

        if subject_id_item is None:
            return

        self.selected_subject_id = int(subject_id_item.text())

        subjects = get_all_subjects()

        for subject in subjects:
            if subject[0] == self.selected_subject_id:
                self.subject_code_input.setText(subject[1])
                self.subject_name_input.setText(subject[2])

                department_index = self.department_combo.findData(
                    subject[3]
                )
                self.department_combo.setCurrentIndex(department_index)

                type_index = self.subject_type_combo.findData(
                    subject[5]
                )
                self.subject_type_combo.setCurrentIndex(type_index)

                self.periods_input.setValue(subject[6])
                break

    def handle_update_subject(self):
        if self.selected_subject_id is None:
            QMessageBox.warning(
                self,
                "No Subject Selected",
                "Please select a subject from the table."
            )
            return

        subject_code = self.subject_code_input.text().strip().upper()
        subject_name = self.subject_name_input.text().strip()
        department_id = self.department_combo.currentData()
        subject_type = self.subject_type_combo.currentData()
        periods_per_week = self.periods_input.value()

        if not subject_code or not subject_name:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the subject code and name."
            )
            return

        if department_id is None or subject_type is None:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please select a department and subject type."
            )
            return

        try:
            rows_updated = update_subject(
                self.selected_subject_id,
                subject_code,
                subject_name,
                department_id,
                subject_type,
                periods_per_week
            )

            if rows_updated == 0:
                QMessageBox.warning(
                    self,
                    "No Changes",
                    "No subject was updated."
                )
                return

            self.subject_table.clearSelection()
            self.subject_table.setCurrentCell(-1, -1)
            self.selected_subject_id = None

            self.load_subjects()

            self.subject_code_input.clear()
            self.subject_name_input.clear()
            self.department_combo.setCurrentIndex(0)
            self.subject_type_combo.setCurrentIndex(0)
            self.periods_input.setValue(4)

            QMessageBox.information(
                self,
                "Success",
                "Subject updated successfully!"
            )

        except IntegrityError as error:
            if error.errno == 1062:
                message = "This subject code already exists."
            else:
                message = str(error)

            QMessageBox.warning(
                self,
                "Database Error",
                message
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Unable to update subject:\n{error}"
            )

    def handle_delete_subject(self):
        if self.selected_subject_id is None:
            QMessageBox.warning(
                self,
                "No Subject Selected",
                "Please select a subject to delete."
            )
            return

        subject_code = self.subject_code_input.text().strip()

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {subject_code}?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            rows_deleted = delete_subject(self.selected_subject_id)

            if rows_deleted == 0:
                QMessageBox.warning(
                    self,
                    "Not Found",
                    "The selected subject no longer exists."
                )
                return

            self.subject_table.clearSelection()
            self.subject_table.setCurrentCell(-1, -1)
            self.selected_subject_id = None

            self.load_subjects()

            self.subject_code_input.clear()
            self.subject_name_input.clear()
            self.department_combo.setCurrentIndex(0)
            self.subject_type_combo.setCurrentIndex(0)
            self.periods_input.setValue(4)

            QMessageBox.information(
                self,
                "Success",
                "Subject deleted successfully!"
            )

        except IntegrityError as error:
            QMessageBox.warning(
                self,
                "Cannot Delete Subject",
                "This subject may be used in teaching allocations "
                "or timetables and cannot be deleted."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Unable to delete subject:\n{error}"
            )

    def handle_clear_selection(self):
        self.subject_table.clearSelection()
        self.subject_table.setCurrentCell(-1, -1)

        self.selected_subject_id = None

        self.subject_code_input.clear()
        self.subject_name_input.clear()
        self.department_combo.setCurrentIndex(0)
        self.subject_type_combo.setCurrentIndex(0)
        self.periods_input.setValue(4)