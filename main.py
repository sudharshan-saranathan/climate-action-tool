from __future__ import annotations

import argparse
import dataclasses
import logging
import platform
import sys
import types

from PySide6 import QtCore, QtGui, QtWidgets  # noqa: PyUnresolvedReferences

import resources  # noqa: F401 - Required to register Qt resources (DO NOT REMOVE)
from gui import MainWindow, StartupCode, StartupDialog
from opts import DefaultOpts


class ClimateActionTool(QtWidgets.QApplication):
    """
    QtWidgets.QApplication subclass that initializes the application's window geometry and style. This class needs to
    be instantiated before any widgets are created.
    """

    backend_flag = True  # Flag to enable/disable the backend optimization module.
    startup_flag = True  # Flag to enable/disable the startup dialog.
    startup_file = None  # The path to the project file to open on startup (if any).
    startup_code = StartupCode.New

    @dataclasses.dataclass
    class Options:
        """
        Default asset(s) and resource(s) for the Climate Action Tool.
        """

        image: str = ":/logo/logo.png"  # The application's logo
        theme: str = ":/theme/dark.qss"  # The qss-file to use as the default theme.
        bezel: int = (
            64  # Initial padding around the main window at application startup.
        )
        fonts = {  # Keys should match values returned by `platform.system()`.
            "windows": types.SimpleNamespace(family="Fira Code", pointSize=8),
            "darwin": types.SimpleNamespace(family="Menlo", pointSize=11),
            "linux": types.SimpleNamespace(family="Noto Sans", pointSize=11),
        }

    def __init__(self):
        super().__init__(sys.argv)
        super().setObjectName("climate-action-tool")

        self._opts = ClimateActionTool.Options()
        image = self._opts.image  # Application logo.
        bezel = self._opts.bezel  # Initial padding around the main window.
        theme = self._opts.theme  # Application-wide theme.

        # Compute window geometry by padding screen bounds with bezel.
        # Example: 1920x1080 screen yields 1720x880 for a bezel of 100 pixels.
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()
        padded = bounds.adjusted(bezel, bezel, -bezel, -bezel)

        self._init_args()  # Parse arguments first to allow user-modified styling in the future.
        self._init_font()
        self._init_style(theme)
        self.setWindowIcon(QtGui.QIcon(image))

        # `self.startup_flag` is True by default, False when `--no-startup` is passed:
        if self.startup_flag:
            self.startup_code, self.startup_file = self._show_startup()

        # `self.startup_code` is non-zero by default, <=0 when the user cancels or quits:
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

    @property
    def options(self) -> Options:
        return self._opts


def main():
    """
    Instantiates `ClimateActionTool` and enters its event loop.
    """

    application = ClimateActionTool()
    application.exec()
    sys.exit(0)


if __name__ == "__main__":
    main()
