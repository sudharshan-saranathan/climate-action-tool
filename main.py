from __future__ import annotations

import argparse
import logging
import platform
import sys

from PySide6 import QtCore, QtGui, QtWidgets  # noqa: PyUnresolvedReferences

import resources  # noqa: F401 - Required to register Qt resources (DO NOT REMOVE)
from gui import MainWindow, StartupCode, StartupDialog
from opts import DefaultOpts


class ClimateActionTool(QtWidgets.QApplication):
    """
    QtWidgets.QApplication subclass that initializes the application's window geometry and style. This class needs to
    be instantiated before any widgets are created.
    """

    backend_flag = True  # Whether to use the backend optimization module.
    startup_flag = True  # Whether to show the startup window.
    startup_file = None  # The path to the project file to open on startup (if any).
    startup_code = StartupCode.New

    _settings = DefaultOpts()

    def __init__(self):
        super().__init__(sys.argv)

        bezel = self._settings.bezel
        theme = self._settings.theme

        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()
        padded = bounds.adjusted(bezel, bezel, -bezel, -bezel)

        self._init_args()  # Parse cmd-line arguments and sets appropriate flags.
        self._init_font()
        self._init_style(theme)

        # When the `--no-startup` cmd-line option is used, the self.startup_flag is set to `False` and the startup
        # dialog is not shown:
        if self.startup_flag:
            self.startup_code, self.startup_file = self._show_startup()

        # At this point, the `self.startup_code` will either be its default value or can potentially become negative
        # or zero, in which case the application will quit. For positive values, the application will proceed to init
        # the main interface:
        if self.startup_code:
            self._win = MainWindow(project=self.startup_file)
            self._win.setWindowTitle("Climate Action Tool")
            self._win.setGeometry(padded)
            self._win.show()

        else:  # Manually exit the application. Otherwise, the event-loop will continue without an interface:
            sys.exit(0)

    def _init_args(self) -> None:
        """
        Parses command-line arguments and updates the application's flags accordingly. The flags do the following:
        1. `--no-startup`: Skips the startup window.
        2. `--no-backend`: Disables the backend optimization module.
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="version", version="%(prog)s 0.1")
        parser.add_argument("--no-startup", action="store_false", dest="startup")
        parser.add_argument("--no-backend", action="store_false", dest="backend")
        args = parser.parse_args()

        self.startup_flag = args.startup
        self.backend_flag = args.backend

    def _init_font(self) -> None:
        """
        Sets the application's default font.
        """

        fonts = DefaultOpts.fonts
        envir = platform.system().lower()

        if envir not in fonts:
            logging.warning(f"Unsupported platform: {envir}")
            return

        self.setFont(QtGui.QFont(fonts[envir].family, fonts[envir].pointSize))

    def _init_style(self, path: str) -> None:
        """
        Reads the provided QSS stylesheet and applies it to the application.
        Does not throw an exception if the file doesn't exist or cannot be read.

        Args:
            path (str): The path to the stylesheet file.
        """

        qss_file = QtCore.QFile(path)
        if qss_file.open(QtCore.QFile.OpenModeFlag.ReadOnly):
            contents = QtCore.QTextStream(qss_file).readAll()
            self.setStyleSheet(contents)
            logging.info("Stylesheet applied successfully.")

        else:
            logging.warning("Failed to read stylesheet file.")

    @staticmethod
    def _show_startup() -> tuple[int, str | None]:
        """
        Displays the startup window.

        Returns:
            result (int): The result code returned by the startup dialog.
        """

        startup = StartupDialog()
        startup.exec()

        result: int = startup.result()
        return result, None


def main():
    """
    Instantiates `ClimateActionTool` and enters its event loop.
    """

    application = ClimateActionTool()
    application.exec()
    sys.exit(0)


if __name__ == "__main__":
    main()
