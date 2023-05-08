"""Employee Module

Holds very simple information about multiple types of employees at our company.  Our business rules indicate
that we cannot have a generic Employee listed in our system.  We have Salaried and Hourly Employee types,
but cannot have generics of these either.  Our concrete types are Executives and Managers (Salaried),
and Permanent and Temporary (Hourly).  Subtypes may hold custom data (but aren't required to).

Ira Woodring
Winter 2023

Finished by Clay Beal,
In association with Zachary Bauer and Ariana Corbin
"""
import abc
import datetime
from enum import Enum


class InvalidRoleException(Exception):
    """Exception for when an invalid role is passed in"""
    def __init__(self, message: str):
        """
        Creates a custom exception called "InvalidRoleException"
        Parameters:
            message (str): Message to be printed to the user when ex is raised
        """
        super().__init__(message)


class InvalidDepartmentException(Exception):
    """Exception for when an invalid department is passed in"""
    def __init__(self, message):
        """
        Creates a custom exception called "InvalidDepartmentException"
        Parameters:
            message (str): Message to be printed to the user when ex is raised
        """
        super().__init__(message)


class Role(Enum):
    """Enum class for Roles"""
    CEO = 1
    CFO = 2
    CIO = 3

    def __str__(self) -> str:
        """
        Str method for Roles
        Returns:
            (str): name of the role
        """
        return f'{self.name}'


class Department(Enum):
    """Enum class for Departments"""
    ACCOUNTING = 1
    FINANCE = 2
    HR = 3
    R_AND_D = 4
    MACHINING = 5

    def __str__(self) -> str:
        """
        Str method for Departments
        Returns:
            (str): name of the department
        """
        return f'{self.name}'


class Employee(abc.ABC):
    """
    Employee is an abstract class that holds common information about all employees.  We will be
    making heavy use of properties in this project, as is reflected in this code.
    Attributes:
        CURRENT_ID (int): Static Variable for ID number
        IMAGE_PLACEHOLDER (str): Image placeholder if the employee doesn't have an image

        _name (str): Holds a name variable for the employee
        _email (str): Holds an email variable for the employee
        _id_number (int): Holds an id number for the employee
        _imgae (str): Holds an image for the employee
    """
    # Static variables for ID and a placeholder for images
    CURRENT_ID = 1
    IMAGE_PLACEHOLDER = "./images/placeholder.png"

    def __init__(self, name: str, email: str) -> None:
        """
        Initializes all the variables every employee must have
        Parameters:
            name (str): Holds a name variable for the employee
            email (str): Holds an email variable for the employee
        """
        self.name: str = name
        self.email: str = email
        self._id_number: int = Employee.CURRENT_ID
        Employee.CURRENT_ID += 1
        self.image: str = Employee.IMAGE_PLACEHOLDER

    def __str__(self) -> str:
        """
        String method that returns the id number and name of an employee
        Returns:
            (str): id number and name of employee
        """
        return f'{self._id_number}:{self._name}'

    def __repr__(self) -> str:
        """
        Representation method that returns a str of the name, email,
        and image of an employee
        Returns:
            (str): 'name','email','image'
        """
        return f'{self._name},{self._email},{self._image}'

    @property
    def id_number(self) -> int:
        """
        Property for employee ID number
        Returns:
            _id_number (int): employees ID number
        """
        return self._id_number

    @property
    def name(self) -> str:
        """
        Property for employees name
        Returns:
            _name (str): employees name
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Setter for employees name
        Parameters:
            name (str): name of an employee
        Raises:
            ValueError: If the passed in name is blank
        """
        if not name:
            raise ValueError('Name must not be blank.')
        self._name = name

    @property
    def email(self) -> str:
        """
        Property for employees email
        Returns:
            _email (str): employees email
        """
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        """
        Setter for employees email
        Parameters:
            email (str): email for an employee
        Raises:
            ValueError: if the passed in email is blank
        """
        if not email:
            raise ValueError('Email must not be blank.')
        self._email = email

    @property
    def image(self) -> str:
        """
        Property for employees image
        Returns:
            _image (str): employees image
        """
        return self._image

    @image.setter
    def image(self, image: str) -> None:
        """
        Setter for employees image
        Parameters:
            image (str): image for an employee
        Raises:
            ValueError: If the passed in image is blank
        """
        if not image:
            raise ValueError('Image must not be blank.')
        self._image = image

    @abc.abstractmethod
    def calc_pay(self) -> float:
        """This function calculates the weekly pay for the current
        employee for our pay report."""
        pass


class Salaried(Employee):
    """
    A Salaried Employee is one who has a yearly salary.
    Attributes:
        _yearly (float): Holds how much an employee makes in a year
    """

    def __init__(self, name: str, email: str, yearly: float) -> None:
        """
        Creates an instance of a salaried employee
        Parameters:
            yearly (float): Holds how much an employee makes in a year
        """
        super().__init__(name, email)
        self.yearly: float = yearly

    @property
    def yearly(self) -> float:
        """
        Property for yearly salary
        Returns:
            _yearly (float): employees yearly salary
        """
        return self._yearly

    @yearly.setter
    def yearly(self, yearly: float) -> None:
        """
        Setter for yearly salary
        Parameters:
            yearly (float): yearly salary for an employee
        Raises:
            ValueError: If yearly salary is below 50,000
        """
        if float(yearly) < 50000:
            raise ValueError('Yearly salary cannot be below $50,000.00')
        self._yearly = float(yearly)

    def calc_pay(self) -> float:
        """
        Calculates weekly pay
        Returns:
            (float): Employees weekly pay based off their salary
        """
        return self._yearly / 52.0

    def __repr__(self) -> str:
        """
        Representation method of a salaried employee
        Returns:
            (str): Previous repr and yearly salary added on
        """
        return f'{super().__repr__()},{self._yearly}'


class Executive(Salaried):
    """
    An Executive is a Salaried Employee with no additional information held.
    Attributes:
        _role (Role): Holds a role for an employee
    """
    def __init__(self, name: str, email: str, yearly: float, role: Role):
        """
        Creates an instance of an Executive employee
        Parameters:
            role (Role): The role of an employee
        """
        super().__init__(name, email, yearly)
        self._role = role

    def __str__(self):
        """
        String method for an Executive employee
        Returns:
            (str): Employees role
        """
        return f'{self._role}'

    @property
    def role(self) -> Role:
        """
        Property for employees role
        Returns:
            _role (Role): Employees role
        """
        return self._role

    @role.setter
    def role(self, role: Role) -> None:
        """
        Setter for role variable
        Parameters:
            role (Role): passed in role for an employee
        Raises:
            InvalidRoleException: If the passed in role isn't an instance
                                  of the Role Enum
        """
        if not isinstance(role, Role):
            raise InvalidRoleException('That is not a valid role.')
        self._role = role

    def __repr__(self) -> str:
        """
        Representation of an Executive employee
        Returns:
            (str): Previous repr with role added on
        """
        return f'Executive,{super().__repr__()},{self._role}'


class Manager(Salaried):
    """
    A Manager is a Salaried Employee with no additional information held.  May want to add
    a department, etc. for increased scope.
    Attributes:
        _department (Department): Holds a department for the employee
    """
    def __init__(self, name: str, email: str, yearly: float, department: Department):
        """
        Creates an instance of a Manager
        Parameters:
            department (Department): Holds a department for the employee
        """
        super().__init__(name, email, yearly)
        self._department = department

    def __str__(self):
        """
        String method for the manager class
        Returns:
            (str): The managers department
        """
        return f'{self._department}'

    @property
    def department(self) -> Department:
        """
        Property for the employees department
        Returns:
            _department(Department): The department enum for the employee
        """
        return self._department

    @department.setter
    def department(self, department: Department) -> None:
        """
        Setter for the employees department
        Raises:
            InvalidDepartmentException: If the passed in department isn't
                                        an instance of the Department Enum
        """
        if not isinstance(department, Department):
            raise InvalidDepartmentException('That is not a valid department.')
        self._department = department

    def __repr__(self) -> str:
        """
        Representation of a manager employee
        Returns:
            (str): Previous repr with department added
        """
        return f'Manager,{super().__repr__()},{self._department}'


class Hourly(Employee):
    """
    An Hourly Employee adds an hourly wage.
    Attributes:
        _hourly (float): Holds the employees hourly wage
    """
    def __init__(self, name: str, hourly: float, email: str) -> None:
        """
        Creates an instance of an hourly employee
        Parameters:
            hourly (float): Holds the hourly wage for an employee
        """
        super().__init__(name, email)
        self.hourly = hourly

    @property
    def hourly(self) -> float:
        """
        Property for the employees hourly pay
        Returns:
            _hourly (float): Hourly wage for an employee
        """
        return self._hourly

    @hourly.setter
    def hourly(self, hourly: float) -> None:
        """
        Setter for an employees hourly pay
        Parameters:
            hourly (float): employees hourly pay
        Raises:
            ValueError: If passed in hourly isn't between 15 and 99.99
        """
        if not 15 < float(hourly) < 99.99:
            raise ValueError('Hourly pay must be between $15 and $99.99')
        self._hourly = float(hourly)

    def calc_pay(self) -> float:
        """
        Calculates weekly pay
        Returns:
            (float): Employees weekly pay
        """
        return self._hourly * 40

    def __repr__(self) -> str:
        """
        Representation of an hourly employee
        Returns:
            (str): Previous repr in addition to hourly pay
        """
        return f'{super().__repr__()},{self._hourly}'


class Permanent(Hourly):
    """
    Hourly Employees may be Permanent.  A Permanent Hourly Employee has a hired date.
    Attributes:
        _hired_date (datetime): Holds an employees hired date
    """

    def __init__(self, name: str, hourly: float, email: str, hired_date: datetime.datetime) -> None:
        """
        Creates an instance of a permanent employee
        Parameters:
            hired_date (datetime): employees hired date
        """
        super().__init__(name, hourly, email)
        self._hired_date = hired_date

    @property
    def hired_date(self) -> datetime.datetime:
        """
        Property for an employees hired date
        Returns:
            hired_date (datetime): employees hired date
        """
        return self._hired_date

    @hired_date.setter
    def hired_date(self, hired_date: datetime.datetime) -> None:
        """
        Setter for an employees hired date
        Parameters:
            hired_date (datetime): employees hired date
        Raises:
            ValueError: If hired date isn't from the datetime class
        """
        if not isinstance(hired_date, datetime.datetime):
            raise ValueError('Hired date must be from the datetime class.')
        self._hired_date = hired_date

    def __repr__(self) -> str:
        """
        Representation of a permanent employee
        Returns:
            (str): Previous repr in addition to a hired date
        """
        return f'Permanent,{super().__repr__()},{self._hired_date}'


class Temp(Hourly):
    """
    A Temp Employee is paid hourly but has a date they can no longer work past.
    Attributes:
        _last_day (str): Holds an employees last day
    """
    def __init__(self, name: str, hourly: float, email: str, last_day: str) -> None:
        """
        Creates an instance of a temporary employee
        Parameters:
            last_day (str): Passed in last day for an employee
        """
        super().__init__(name, hourly, email)
        self.last_day = last_day

    @property
    def last_day(self) -> str:
        """
        Property for an employees last day
        Returns:
            _last_day (str): Last day for an employee
        """
        return self._last_day

    @last_day.setter
    def last_day(self, last_day: str) -> None:
        """
        Setter for the employees last day
        Parameters:
            last_day (str): Employees last day
        Raises:
            ValueError: If passed in last day is blank
        """
        if not last_day:
            raise ValueError('Last day cannot be blank.')
        self._last_day = last_day

    def __repr__(self) -> str:
        """
        Representation method for Temporary employees
        Returns:
            (str): previous repr in addition to the employees last day
        """
        return f'Temp,{super().__repr__()},{self._last_day}'
