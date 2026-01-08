# Encoding: utf-8
# Filename: main.py
# Description: Entry point for the application
# Module: N/A

# Imports (standard):
from __future__ import annotations
import logging
import sys

# Imports (3rd party):
from PySide6 import QtGui, QtCore, QtWidgets # noqa: PyUnresolvedReferences

# Imports (local):
import resources    # Icons, style-files, and other assets

# Class ClimactApplication:
class ClimactApplication(QtWidgets.QApplication):

    # Initializer:
    def __init__(self):
        super().__init__(sys.argv)  # Required!

        # Get screen geometry to adjust app-size:
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()

        # Set style:
        qss_file = QtCore.QFile(":/theme/dark.qss")
        qss_file.open(QtCore.QFile.OpenModeFlag.ReadOnly | QtCore.QFile.OpenModeFlag.Text)
        contents = str(qss_file.readAll())

        self.setStyleSheet(contents)

        # Instantiate and display the main user interface:
        self._win = QtWidgets.QMainWindow()
        self._win.setWindowTitle("Climate Action Tool")
        self._win.setGeometry(bounds.adjusted(100, 100, -100, -100))
        self._win.setWindowFlags(QtCore.Qt.WindowType.Window)
        self._win.show()

# Main:
def main():

    # Instantiate the application and enter its event loop:
    application = ClimactApplication()
    application.exec()


#
if __name__ == "__main__":
    main()