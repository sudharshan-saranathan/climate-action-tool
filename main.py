# Filename: main.py
# Module name: main_ui
# Description: Entry point for the Climate Action Tool.

from __future__ import annotations  # For type annotations and forward references.

import dataclasses  # For storing options.
import resources  # noqa: F401 - Required to register Qt resources (DO NOT REMOVE).
import argparse
import logging
import types
import sys

# PySide6 (Python/Qt framework):
from PySide6 import QtGui  # Required for styling.
from PySide6 import QtCore
from PySide6 import QtWidgets  # For pre-defined widgets.

from gui.main_ui.window import MainWindow
from gui.startup.window import StartupWindow

"""
Entry point and application initialization for the Climate Action Tool.

This module instantiates the main application, applies styling and fonts,
and initializes the user interface based on command-line arguments.
"""


class ClimateActionTool(QtWidgets.QApplication):
    """
    Main application class for the Climate Action Tool (see Qt docs for more info).

    Handles application initialization including style, fonts, and UI setup.
    Must be instantiated before other Qt components.
    """

    backend_flag = True  # Flag to enable/disable the backend optimization module.
    startup_flag = True  # Flag to enable/disable the startup dialog.
    startup_file = (
        None  # User-selected project file path from the startup dialog (if available).
    )

    @dataclasses.dataclass(frozen=True)
    class Options:
        """Default configuration options for the Climate Action Tool."""

        image: str = ":/logo/logo.png"  # Application logo path
        theme: str = ":/theme/dark.qss"  # Default theme stylesheet path
        bezel: int = 64  # Padding around the main window at application startup.

    def __init__(self):
        super().__init__(sys.argv)
        super().setObjectName("climate-action-tool")

        self._opts = ClimateActionTool.Options()
        image = self._opts.image  # Application logo.
        bezel = self._opts.bezel  # Padding around the main window.
        theme = self._opts.theme  # Application-wide theme.

        # Compute window geometry by padding screen bounds with bezel.
        # Example: 1920x1080 screen yields 1720x880 for a bezel of 100 pixels.
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()
        padded = bounds.adjusted(bezel, bezel, -bezel, -bezel)

        self._init_style(theme)  # Apply the theme first.
        self._install_fonts()  # Font-setting should succeed style-setting.
        self._init_args()  # Finally, parse command-line arguments.
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
        Parse command-line arguments and update application flags.

        Supported flags:
        - --version: Display the application version and exit.
        - --no-startup: Skip the startup dialog.
        - --no-backend: Disable the backend optimization module.
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="version", version="%(prog)s 1.0")
        parser.add_argument("--no-startup", action="store_false", dest="startup")
        parser.add_argument("--no-backend", action="store_false", dest="backend")
        args = parser.parse_args()

        self.startup_flag = args.startup
        self.startup_code = 1
        self.backend_flag = args.backend

    def _install_fonts(self) -> None:

        # Required for platform-dependent sizing:
        import platform

        fonts_path = QtCore.QDir(":/fonts")
        fonts_list = fonts_path.entryList(["*.ttf"])
        fonts_size = 8 if platform.system().lower() == "windows" else 10

        # Install all available fonts:
        for font in fonts_list:
            QtGui.QFontDatabase.addApplicationFont(f":/fonts/{font}")

        self.setFont(QtGui.QFont("Fira Code", fonts_size))

    def _init_style(self, path: str) -> None:
        """
        Apply a QSS stylesheet to the application. Log a warning if the file cannot be found or read.

        Args:
            path: Path to the QSS stylesheet file.
        """

        qss_file = QtCore.QFile(path)
        if qss_file.open(QtCore.QFile.OpenModeFlag.ReadOnly):
            contents = QtCore.QTextStream(qss_file).readAll()
            self.setStyleSheet(contents)

        else:
            logging.warning("Failed to read stylesheet file.")

    @staticmethod
    def _show_startup() -> tuple[int, str | None]:
        """
        Display the startup dialog and return the result.

        Returns:
            A tuple of (exit_code, project_path) where exit_code indicates
            success (1) or cancellation (0).
        """

        startup = StartupWindow()
        startup.exec()

        result: int = startup.result()
        return result, None

    @property
    def options(self) -> Options:
        return self._opts


def main() -> None:
    """Instantiate the application and enter the event loop."""

    application = ClimateActionTool()
    application.exec()  # This call is blocking by default.
    sys.exit(0)


if __name__ == "__main__":
    main()
