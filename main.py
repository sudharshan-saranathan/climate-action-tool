# Encoding: utf-8
# Filename: main.py
# Description: Entry point for the application
# Module: N/A

# Imports (standard):
from __future__ import annotations
import logging
import assets
import sys

# Imports (3rd party):
from PySide6 import QtGui, QtCore, QtWidgets # noqa: PyUnresolvedReferences

# Class ClimactApplication:
class ClimactApplication(QtWidgets.QApplication):

    # Initializer:
    def __init__(self):
        super().__init__(sys.argv)  # Required!

        # Get screen geometry to adjust app-size:
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()

        # Set style:
        qss_file = ":/theme/dark.qss"
        with open(qss_file, "r") as f:
            qss = f.read()
            self.setStyleSheet(qss)

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