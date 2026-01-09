# Encoding: utf-8
# Filename: main.py
# Description: Entry point for the application
# Module: N/A

# Imports (compatibility):
from __future__ import annotations

# Imports (standard):
import logging
import platform
import sys

# Imports (3rd party):
from PySide6 import QtCore, QtGui, QtWidgets  # noqa: PyUnresolvedReferences

# Imports (local):
import resources  # noqa: F401 - Required to register Qt resources (DO NOT REMOVE)
from gui import MainWindow, StartupCode, StartupDialog
from opts import DefaultOpts


# Class ClimateActionTool:
class ClimateActionTool(QtWidgets.QApplication):
    # Application-wide flags:
    backend_flag = True  # Whether the backend-module should be loaded.
    startup_flag = True  # Whether the startup window should be displayed.
    startup_file = True  # Whether the startup closed with a file-selection.
    startup_code = StartupCode.New  # Result code returned by the startup dialog

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
        self._init_args()  # Parse command-line arguments
        self._init_style(theme)  # `theme` refers to the default qss filepath
        self._init_font()  # Set an application-wide font

        # Get startup flag:
        if self.startup_flag:
            self.startup_code = self._show_startup()

        # If the startup window was closed with a file selection or a new project, begin the main application:
        if self.startup_code:
            self._win = MainWindow()
            self._win.setWindowTitle("Climate Action Tool")
            self._win.setGeometry(padded)
            self._win.show()

        else:
            sys.exit(0)

    # Private method called from `__init__()`:
    def _init_args(self):
        """
        Parse command-line arguments and set appropriate flags.
        :return:
        """

        # Imports (standard):
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="version", version="%(prog)s 0.1")
        parser.add_argument("--no-startup", action="store_false", dest="startup")
        parser.add_argument("--no-backend", action="store_false", dest="backend")
        args = parser.parse_args()

        self.startup_flag = args.startup
        self.backend_flag = args.backend

    # Private method called from `__init__()`:
    def _init_font(self) -> None:
        """
        Set the application's default font.

        :return: None
        """

        fonts = DefaultOpts.fonts  # Default fonts for each platform
        envir = platform.system().lower()  # Get the current platform

        # Exit if the platform is not supported:
        if envir not in fonts:
            logging.warning(f"Unsupported platform: {envir}")
            return

        self.setFont(QtGui.QFont(fonts[envir].family, fonts[envir].pointSize))

    # Private method called from `__init__()`:
    def _init_style(self, path: str) -> None:
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

        else:
            logging.warning("Failed to read stylesheet file.")

    # Show the startup window:
    @staticmethod
    def _show_startup() -> int:
        """
        Displays the startup window.
        :return: None
        """

        startup = StartupDialog()
        startup.exec()

        return startup.result()


# Main:
def main():
    # Instantiate the application and enter its event loop:
    application = ClimateActionTool()
    application.exec()


# Invoke `main`:
if __name__ == "__main__":
    main()
