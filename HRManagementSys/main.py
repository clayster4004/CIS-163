"""
Finished by Clay Beal,
In association with Zachary Bauer and Ariana Corbin
"""

from gui_student import *
import gui_student


def main():
    """
    Creates an instance of an application and runs the program
    """
    app = QtWidgets.QApplication([])
    form = gui_student.MainWindow()
    form.show()
    app.exec()


if __name__ == '__main__':
    main()

