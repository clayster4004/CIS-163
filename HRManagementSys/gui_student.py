"""GUI Module for Employee Information

We provide a default form with common Employee information, then inherit and subclass
to create custom forms for each type.

Ira Woodring
Winter 2023

Finished by Clay Beal,
In association with Zachary Bauer and Ariana Corbin
"""

import csv

from PyQt6 import QtWidgets
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QLabel, QLineEdit, QMenu, QHeaderView, QTableView, QMainWindow, QAbstractItemView, \
    QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QComboBox, QMessageBox

import employee_student
from employee_student import *
from typing import *


class HRTableModel(QAbstractTableModel):
    """The HRTableModel allows us to display our information in a QTableView."""
    def __init__(self, data) -> None:
        super(HRTableModel, self).__init__()
        self._columns = ["ID#", "Type", "Name", "Pay", "Email"]
        self._data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        """Gives the header info in a format PyQt wants."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            # return f"Column {section + 1}"
            return self._columns[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return f"{section + 1}"

    def data(self, index, role) -> str:
        """Returns the data at some table index."""
        if role == Qt.ItemDataRole.DisplayRole:
            e = self._data[index.row()]
            field = e.id_number
            if index.column() == 1:
                field = type(e).__name__
            if index.column() == 2:
                field = e.name
            if index.column() == 3:
                if isinstance(e, Salaried):
                    field = '${:,.2f}'.format(e.yearly)
                else:
                    field = '${:,.2f}'.format(e.hourly)
            if index.column() == 4:
                field = e.email
            return field

    def rowCount(self, index) -> int:
        """Provides the way for PyQt to get our row count."""
        return len(self._data)

    def columnCount(self, index) -> int:
        """Provides the column count, as PyQt expects."""
        return len(self._columns)


class MainWindow(QMainWindow):
    """MainWindow will have menus and a central list widget."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Employee Management v1.0.0")
        self.resize(800, 600)
        self._data = []
        self.load_file()
        self._model = HRTableModel(self._data)
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._table.setAlternatingRowColors(True)
        self._header = self._table.horizontalHeader()
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.setCentralWidget(self._table)
        self._create_menu_bar()
        self._employee_form = None
        self._about_form = AboutForm()

    def _create_menu_bar(self) -> None:
        # Create the menus.
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = QMenu("&File", self)
        edit_menu = QMenu("&Edit", self)
        help_menu = QMenu("&Help", self)
        self._exit_action = QAction("&Exit")
        self._exit_action.triggered.connect(exit)
        self._load_action = QAction("&Load HR Data")
        self._save_action = QAction("&Save HR Data")
        self._save_action.setShortcut('Ctrl+S')
        file_menu.addAction(self._load_action)
        self._load_action.setShortcut('Ctrl+O')
        self._load_action.triggered.connect(self.load_file)
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._exit_action)
        self._edit_action = QAction("&Edit current employee")
        edit_menu.addAction(self._edit_action)
        self._edit_action.triggered.connect(self.edit_employee)
        self._edit_action.setShortcut('Ctrl+E')
        self._save_action.triggered.connect(self.save_file)
        self._about_action = QAction("About this software")
        self._about_action.triggered.connect(self.show_help)
        help_menu.addAction(self._about_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)
        self.setMenuBar(menu_bar)

    def show_help(self) -> None:
        """Our 'help' form merely shows who wrote this, the version, and a description."""
        self._about_form.show()

    def data_to_rows(self) -> List[str]:
        """It is sometimes useful for us to have our model data as a list.  This method
        provides that feature."""
        data = []
        for e in self._data:
            row = [e.id_number, type(e).__name__, e.name]
            if isinstance(e, Salaried):
                row.append(str(e.yearly))
            else:
                row.append(str(e.hourly))
            row.append(e.email)
            data.append(row)
        return data

    def refresh_width(self) -> None:
        """Resize our table to fit our data width."""
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    def edit_employee(self) -> None:
        """Update an employee object by populating the correct type of form with the selected type of
        employee data."""
        index = self._table.selectionModel().selectedIndexes()
        if not index:
            return
        index = index[0].row()
        if isinstance(self._data[index], Executive):
            self._employee_form = ExecutiveForm(self)
        if isinstance(self._data[index], Manager):
            self._employee_form = ManagerForm(self)
        if isinstance(self._data[index], Permanent):
            self._employee_form = PermanentForm(self)
        if isinstance(self._data[index], Temp):
            self._employee_form = TempForm(self)

        self._employee_form.fill_in(index)
        self._employee_form.show()

    def load_file(self) -> None:
        """Read a representation of all of our Employees from a file and store in our
        _data variable.  The table will automatically be populated by this variable."""
        # Opens the employee.data file
        with open('./employee.data') as datafile:
            # Reads the file
            reader = csv.reader(datafile, quoting=csv.QUOTE_MINIMAL)

            # Loops through each row in the file
            for row in reader:
                # Checks to see if the first word is 'executive', if so
                # creates an instance of an executive
                if row[0].lower() == 'executive':
                    employee = Executive(row[1], row[2], float(row[4]), row[5])
                    # Checks to see if the image is NOT a placeholder image
                    if row[3] != './images/placeholder.png':
                        # Assigns employee to the passed in image
                        employee.image = row[3]
                # Checks if the employee is a manager
                elif row[0].lower() == 'manager':
                    employee = Manager(row[1], row[2], float(row[4]), row[5])
                    if row[3] != './images/placeholder.png':
                        employee.image = row[3]
                # Checks if the employee is a permanent
                elif row[0].lower() == 'permanent':
                    employee = Permanent(row[1], float(row[4]), row[2], row[5])
                    if row[3] != './images/placeholder.png':
                        employee.image = row[3]
                # Checks if the employee is a temp
                elif row[0].lower() == 'temp':
                    employee = Temp(row[1], float(row[4]), row[2], row[5])
                    if row[3] != './images/placeholder.png':
                        employee.image = row[3]
                # Appends the employee just made to the data list
                self._data.append(employee)

    def save_file(self) -> None:
        """Save a representation of all the Employees to a file."""
        # Opens / creates a file called employee.data
        file = open("./employee.data", "w")
        # Goes through employee.data and write the repr for each line
        # in the data
        for item in self._data:
            print(item)
            file.write(repr(item))
            file.write('\n')
        file.close()


class EmployeeForm(QtWidgets.QWidget):
    """There will never be a generic employee form, but we don't want to repeat code
    , so we put it all here.  Each subtype of form will add to it."""
    def __init__(self, parent=None, employee: Employee = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Initializes parent
        self._parent = parent
        outer_layout = QVBoxLayout()
        self.layout = QtWidgets.QFormLayout()
        self.setLayout(outer_layout)
        self._id_label = QLabel()
        self.layout.addRow(QLabel("ID#"), self._id_label)
        self._name_edit = QLineEdit()
        self.layout.addRow(QLabel("Name: "), self._name_edit)
        self._pay_edit = QLineEdit()
        self._email_edit = QLineEdit()
        self.layout.addRow(QLabel("Email address:"), self._email_edit)
        self._image_path_edit = QLineEdit()
        self.layout.addRow(QLabel("Image path:"), self._image_path_edit)
        self._image = QLabel()
        self._image.setPixmap(QPixmap(Employee.IMAGE_PLACEHOLDER))
        self.layout.addWidget(self._image)
        update = QPushButton("Update")
        update.clicked.connect(self.update_employee)
        outer_layout.addLayout(self.layout)
        outer_layout.addWidget(update)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def update_employee(self) -> None:
        """
        Change the selected employee's data to the updated values.
        ValueErrors are caught in this function when the bad data is
        being used to update the employee, an error popup box is implemented
        """
        # Tries to set the employees name, email, and image to the one
        # set by the user
        try:
            self._employee.name = self._name_edit.text()
        # Excepts ValueError, implements a popup box that says you cannot
        # set the values to the user typed values
        except ValueError as error_message:
            QMessageBox.critical(self, "Error", str(error_message))
        try:
            self._employee.email = self._email_edit.text()
        except ValueError as error_message:
            QMessageBox.critical(self, "Error", str(error_message))
        try:
            self._employee.image = self._image_path_edit.text()
        except ValueError as error_message:
            QMessageBox.critical(self, "Error", str(error_message))
        self.setVisible(False)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        self._employee = self._parent._data[index]
        self.setWindowTitle("Edit " + type(self._employee).__name__ + " Employee Information")
        self._id_label.setText(str(self._employee.id_number))
        self._name_edit.setText(self._employee.name)
        self._email_edit.setText(self._employee.email)
        if self._employee.image == "placeholder":
            self._image_path_edit.setText('')
        else:
            self._image_path_edit.setText(self._employee.image)
        self._image.setPixmap(QPixmap(self._employee.image))


# Complete the following forms so that they update and fill-in
# their custom information.

class SalariedForm(EmployeeForm):
    """
    Creates an instance of a Salaried Employee Form
    Attributes:
        _pay_edit (QLineEdit): An editable variable that can hold salary
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializer that takes in any arguments and initializes the pay_edit
        and adds a row to the program layout to make space to display the
        salary
        Parameters:
            *args and **kwargs
        """
        super().__init__(*args, **kwargs)
        # Make an editable line for yearly pay
        self._pay_edit = QLineEdit()
        # Add a row with a salary label and add the pay next to it
        self.layout.addRow(QLabel("Salary:"), self._pay_edit)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        # Set pay line to the employees yearly salary
        self._pay_edit.setText(str(self._employee.yearly))

    def update_employee(self) -> None:
        """Updates the employee to the file and trys to set the
        employees yearly salary to the text in the program, catches
        errors and makes a popup box for errors"""
        super().update_employee()
        # Try to set the employees yearly salary to the pay line
        try:
            self._employee.yearly = self._pay_edit.text()
        # If the pay doesn't fit the exceptions put a popup box with an error message
        except ValueError as error_message:
            QMessageBox.critical(self, "Error", str(error_message))


class ExecutiveForm(SalariedForm):
    """
    Creates an instance of an Executive Employee Form
    Attributes:
        _role_combo (QComboBox): A dropdown box that holds roles
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializer that takes in any arguments and initializes the role_combo
        and adds a row to the program layout to make space to display the
        role dropdown box
        Parameters:
            *args and **kwargs
        """
        super().__init__(*args, **kwargs)
        # Creates a combo box that holds many values in a dropdown menu
        self._role_combo = QComboBox()
        # Adds all the options from the role enum class
        self._role_combo.addItems([x.name for x in employee_student.Role])
        # Adds a row and label to the layout to label the combo box
        self.layout.addRow(QLabel("Role:"), self._role_combo)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        # Sets the current text of the combo box to the employees role str
        self._role_combo.setCurrentText(str(self._employee.role))

    def update_employee(self) -> None:
        """Updates the employee to the file and trys to set the
        employees role salary to the text in the program, catches
        errors and makes a popup box for errors"""
        super().update_employee()
        # Tries to set the role to what the user selected
        try:
            self._employee.role = Role[self._role_combo.currentText()]
        # If the selection is invalid a popup box alerts the user
        except InvalidRoleException as error_message:
            QMessageBox.critical(self, "Error", str(error_message))


class ManagerForm(SalariedForm):
    """
    Creates an instance of a Manager Employee Form
    Attributes:
        _department_combo (QComboBox): A dropdown box that holds departments
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializer that takes in any arguments and initializes the department_combo
        and adds a row to the program layout to make space to display the
        department dropdown box
        Parameters:
            *args and **kwargs
        """
        super().__init__(*args, **kwargs)
        # Creates a combo box that holds many values in a dropdown menu
        self._department_combo = QComboBox()
        # Adds all the options from the department enum class
        self._department_combo.addItems([x.name for x in employee_student.Department])
        # Adds a row and label to the layout to label the combo box
        self.layout.addRow(QLabel("Head of Department:"), self._department_combo)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        # Sets the current text of the combo box to the employees department str
        self._department_combo.setCurrentText(str(self._employee.department))

    def update_employee(self) -> None:
        """Updates the employee to the file and trys to set the
        employees department salary to the text in the program, catches
        errors and makes a popup box for errors"""
        super().update_employee()
        # Tries to set the department to what the user selected
        try:
            self._employee.department = Department[self._department_combo.currentText()]
        # If the selection is invalid a popup box alerts the user
        except InvalidDepartmentException as error_message:
            QMessageBox.critical(self, "Error", str(error_message))


class HourlyForm(EmployeeForm):
    """
    Creates an instance of an Hourly Employee Form
    Attributes:
        _pay_edit (QLineEdit): An editable line that holds employee pay
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializer that takes in any arguments and initializes the pay_edit
        and adds a row to the program layout to make space to display the
        hourly pay
        Parameters:
            *args and **kwargs
        """
        super().__init__(*args, **kwargs)
        # Make an editable line for hourly pay
        self._pay_edit = QLineEdit()
        # Add a row with an Hourly Wage label and add the pay next to it
        self.layout.addRow(QLabel("Hourly Wage:"), self._pay_edit)

    def update_employee(self) -> None:
        """Updates the employee to the file and trys to set the
        employees hourly salary to the text in the program, catches
        errors and makes a popup box for errors"""
        super().update_employee()
        # Tries to set the hourly pay to what the user selected
        try:
            self._employee.hourly = self._pay_edit.text()
        # If the selection is invalid a popup box alerts the user
        except ValueError as error_message:
            QMessageBox.critical(self, "Error", str(error_message))

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        # Sets the editable pay line to the current str value of an
        # employees hourly pay
        self._pay_edit.setText(str(self._employee.hourly))


class TempForm(HourlyForm):
    """
    Creates an instance of a Temp Employee Form
    Attributes:
        _last_day_label (QLabel): A label that holds an employees last day
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializer that takes in any arguments and initializes the
        _last_day_label
        Parameters:
            *args and **kwargs
        """
        super().__init__(*args, **kwargs)
        # Creates a label to hold the employees last day
        self._last_day_label = QLabel()
        self.layout.addRow(QLabel("Last Day"), self._last_day_label)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        # Sets the employees last day label on the program to the last day str
        self._last_day_label.setText(self._employee.last_day)


class PermanentForm(HourlyForm):
    """
    Creates an instance of a Permanent Employee Form
    Attributes:
        _hired_date_label (QLabel): A label that holds an employees hired day
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializer that takes in any arguments and initializes the
        _hired_date_label
        Parameters:
            *args and **kwargs
        """
        super().__init__(*args, **kwargs)
        # Creates a label to hold the employees hired date
        self._hired_date_label = QLabel()
        self.layout.addRow(QLabel("Hired Day"), self._hired_date_label)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        # Sets the employees last day label on the program to the hired date str
        self._hired_date_label.setText(self._employee.hired_date)


class AboutForm(QtWidgets.QWidget):
    """An About Form just gives information about our app to users who want to see it.  Automatically
    sets itself visible on creation."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("HR Management System"))
        self.layout.addWidget(QLabel("version 1.0.0"))
        self.layout.addWidget(QLabel("A simple system for storing important pieces of information about employees."))
        self.close = QPushButton("Close")
        self.close.clicked.connect(self.close_form)
        self.layout.addWidget(self.close)
        self.setLayout(self.layout)

    def close_form(self) -> None:
        """Hide the form."""
        self.setVisible(False)
