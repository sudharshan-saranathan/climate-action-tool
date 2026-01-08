# Encoding: utf-8
# Filename: main.py
# Description: Entry point for the application
# Module: N/A

# Imports (standard):
from __future__ import annotations

import logging
import sys

# Imports (3rd party):
from PySide6 import QtCore, QtGui, QtWidgets  # noqa: PyUnresolvedReferences

import resources  # Icons, style-files, and other assets

# Imports (local):
from opts import DefaultOpts


# Class ClimateActionTool:
class ClimateActionTool(QtWidgets.QApplication):
    # Initializer:
    def __init__(self):
        super().__init__(sys.argv)  # Required!

        # Shorthand for default options:
        bezel = DefaultOpts.bezel
        theme = DefaultOpts.theme

        # Get screen geometry to compute application window size:
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()
        padded = bounds.adjusted(bezel, bezel, -bezel, -bezel)

        # Apply the stylesheet:
        self.apply_style(theme)

        # Instantiate and display the main user interface:
        self._win = QtWidgets.QMainWindow()
        self._win.setWindowTitle("Climate Action Tool")
        self._win.setGeometry(padded)
        self._win.show()

    # Private method called from `__init__()`:
    def apply_style(self, path: str) -> None:
        """
        Read and apply the stylesheet from the specified file.

        :param path: Path to the stylesheet file.
        :return: None
        """

        # Read and apply the stylesheet:
        qss_file = QtCore.QFile(path)  # Requires a compiled resource file!
        if qss_file.open(QtCore.QFile.OpenModeFlag.ReadOnly):
            contents = QtCore.QTextStream(qss_file).readAll()
            self.setStyleSheet(contents)


# Main:
def main():
    # Instantiate the application and enter its event loop:
    application = ClimateActionTool()
    application.exec()


# Invoke `main`:
if __name__ == "__main__":
    main()
