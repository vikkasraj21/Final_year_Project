from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)

from app.services.department_service import (
    get_all_departments,
    add_department,
    update_department,
    delete_department
)
from mysql.connector import IntegrityError
from mysql.connector.errorcode import ER_ROW_IS_REFERENCED_2, ER_ROW_IS_REFERENCED

class DepartmentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Department Management")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Page heading
        title = QLabel("Department Management")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )
        layout.addWidget(title)

        # Department input form
        form_layout = QHBoxLayout()

        self.department_code = QLineEdit()
        self.department_code.setPlaceholderText(
            "Department Code (e.g., MECH)"
        )
        self.department_code.setMaxLength(20)

        self.department_name = QLineEdit()
        self.department_name.setPlaceholderText(
            "Enter Department Name"
        )

        self.add_button = QPushButton("Add Department")
        self.update_button = QPushButton("Update Department")
        self.update_button.setEnabled(False)
        self.update_button.clicked.connect(self.handle_update_department)
        self.add_button.clicked.connect(self.handle_add_department)
        self.delete_button = QPushButton("Delete Department")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.handle_delete_department)

        form_layout.addWidget(self.department_code)
        form_layout.addWidget(self.department_name)
        form_layout.addWidget(self.add_button)
        form_layout.addWidget(self.update_button)
        form_layout.addWidget(self.delete_button)

        layout.addLayout(form_layout)

        # Department records table
        self.department_table = QTableWidget()
        self.selected_department_id = None

        self.department_table.cellClicked.connect(
            self.select_department
        )
        self.department_table.setColumnCount(3)
        self.department_table.setHorizontalHeaderLabels(
            ["Department ID", "Department Code", "Department Name"]
        )

        self.department_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.department_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.department_table)
        self.load_departments()

    def load_departments(self):
        try:
            departments = get_all_departments()

            self.department_table.setRowCount(len(departments))

            for row, (department_id, department_code, department_name) in enumerate(departments):
                self.department_table.setItem(
                    row, 0, QTableWidgetItem(str(department_id))
                )

                self.department_table.setItem(
                    row, 1, QTableWidgetItem(department_code)
                )

                self.department_table.setItem(
                    row, 2, QTableWidgetItem(department_name)
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to load departments:\n{error}"
            )

    def handle_add_department(self):
        department_code = self.department_code.text().strip().upper()
        department_name = self.department_name.text().strip()

        if not department_code or not department_name:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter both department code and name."
            )
            return

        if len(department_code) > 20 or len(department_name) > 100:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Department code must be at most 20 characters "
                "and department name at most 100 characters."
            )
            return

        try:
            add_department(department_code, department_name)

            self.department_code.clear()
            self.department_name.clear()
            self.load_departments()

            QMessageBox.information(
                self,
                "Success",
                "Department added successfully!"
            )

        except IntegrityError:
            QMessageBox.warning(
                self,
                "Duplicate Department",
                "This department code already exists."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to add department:\n{error}"
            )

    def handle_update_department(self):
        if self.selected_department_id is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a department first."
            )
            return

        department_code = self.department_code.text().strip().upper()
        department_name = self.department_name.text().strip()

        if not department_code or not department_name:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter both department code and name."
            )
            return

        if len(department_code) > 20 or len(department_name) > 100:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Department code must be at most 20 characters "
                "and department name at most 100 characters."
            )
            return

        try:
            rows_updated = update_department(
                self.selected_department_id,
                department_code,
                department_name
            )

            if rows_updated == 0:
                QMessageBox.information(
                    self,
                    "No Changes",
                    "No department was changed."
                )
                return

            self.selected_department_id = None
            self.department_code.clear()
            self.department_name.clear()
            self.update_button.setEnabled(False)
            self.department_table.clearSelection()

            self.load_departments()

            QMessageBox.information(
                self,
                "Success",
                "Department updated successfully!"
            )

        except IntegrityError:
            QMessageBox.warning(
                self,
                "Duplicate Department",
                "This department code already exists."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to update department:\n{error}"
            )

    def select_department(self, row, column):
        self.selected_department_id = int(
            self.department_table.item(row, 0).text()
        )

        department_code = self.department_table.item(row, 1).text()
        department_name = self.department_table.item(row, 2).text()

        self.department_code.setText(department_code)
        self.department_name.setText(department_name)

        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def handle_delete_department(self):
        if self.selected_department_id is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a department first."
            )
            return

        department_name = self.department_name.text().strip()

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{department_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            deleted_rows = delete_department(self.selected_department_id)

            if deleted_rows == 0:
                QMessageBox.warning(
                    self,
                    "Not Found",
                    "This department no longer exists."
                )
            else:
                QMessageBox.information(
                    self,
                    "Success",
                    "Department deleted successfully!"
                )

            self.selected_department_id = None
            self.department_code.clear()
            self.department_name.clear()
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.department_table.clearSelection()
            self.load_departments()

        except IntegrityError as error:
            if error.errno in (ER_ROW_IS_REFERENCED, ER_ROW_IS_REFERENCED_2):
                QMessageBox.warning(
                    self,
                    "Cannot Delete Department",
                    "This department is linked to other records "
                    "and cannot be deleted."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Database Error",
                    f"Unable to delete department:\n{error}"
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to delete department:\n{error}"
            )