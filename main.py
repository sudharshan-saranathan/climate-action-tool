# Encoding: utf-8
# Filename: main.py
# Description: Entry point for the application
# Module: N/A

# Imports (standard):
from __future__ import annotations

import logging
import platform
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

        # Apply style and font:
        self.set_style(theme)  # `theme` refers to the default qss filepath
        self._init_font()  # Set an application-wide font

        # Instantiate the startup window:
        self._show_startup()

        # Instantiate and display the main user interface:
        self._win = QtWidgets.QMainWindow()
        self._win.setWindowTitle("Climate Action Tool")
        self._win.setGeometry(padded)
        self._win.show()

    # Private method called from `__init__()`:
    def set_style(self, path: str) -> None:
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

    # Private method called from `__init__()`:
    def _init_font(self) -> None:
        """
        Set the application's default font.

        :return: None
        """

        fonts = DefaultOpts.fonts
        envir = platform.system().lower()

        # Exit if the platform is not supported:
        if envir not in fonts:
            logging.warning(f"Unsupported platform: {envir}")
            return

        self.setFont(QtGui.QFont(fonts[envir].family, fonts[envir].pointSize))

    # Show the startup window:
    @staticmethod
    def _show_startup() -> None:
        """
        Displays the startup window.
        :return: None
        """

        # Import the startup window:
        from gui.startup.dialog import StartupDialog

        startup = StartupDialog()
        startup.exec()


# Main:
def main():
    # Instantiate the application and enter its event loop:
    application = ClimateActionTool()
    application.exec()


# Invoke `main`:
if __name__ == "__main__":
    main()
