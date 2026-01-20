# Filename: main.py
# Module name: N/A
# Description: Application entry point for the Climate Action Tool.

"""
Entry point and application initialization for the Climate Action Tool.

This module instantiates the main application, applies styling and fonts,
and initializes the user interface based on command-line arguments.
Supports command-line flags for the startup dialog and backend optimization control.
"""

from __future__ import annotations
import dataclasses
import resources  # noqa: F401 - Required to register Qt resources (DO NOT REMOVE)
import argparse
import logging
import sys

from PySide6 import QtGui, QtCore, QtWidgets
from gui.main_ui.window import MainWindow
from gui.startup.window import StartupWindow


class ClimateActionTool(QtWidgets.QApplication):
    """
    Main application class for the Climate Action Tool (see Qt docs for more info).

    Handles application initialization including style, fonts, and UI setup.
    Must be instantiated before other Qt components.
    """

    backend_flag = True  # Flag to enable/disable the backend optimization module.
    startup_flag = True  # Flag to enable/disable the startup dialog.
    startup_file = str()  # User-selected project (if available).

    @dataclasses.dataclass(frozen=True)
    class Options:
        """Configuration options for the application.

        Attributes:
            image: Path to the application's icon.
            theme: Path to the application's QSS stylesheet.
            fonts: Path to the application's font directory.
            bezel: Padding around the window bounds (in pixels).
        """

        image: str = ":/logo/logo.png"
        theme: str = ":/theme/dark.qss"
        fonts: str = ":/fonts"
        bezel: int = 64

    def __init__(self):
        """Initialize the application with style, fonts, and UI components."""

        super().__init__(sys.argv)
        super().setObjectName("climate-action-tool")

        self._opts = ClimateActionTool.Options()
        image = self._opts.image
        bezel = self._opts.bezel
        theme = self._opts.theme
        fonts = QtCore.QDir(self._opts.fonts)

        # Compute window geometry by padding screen bounds:
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()
        padded = bounds.adjusted(bezel, bezel, -bezel, -bezel)

        self._init_args()
        self._init_style(theme)
        self._init_fonts(fonts)
        self.setWindowIcon(QtGui.QIcon(image))

        # Show startup dialog if enabled:
        if self.startup_flag:
            self.startup_code, self.startup_file = self._show_startup()

        # Create and show the main window if the startup succeeded:
        if self.startup_code:
            self._win = MainWindow(project=self.startup_file)
            self._win.setWindowTitle("Climate Action Tool")
            self._win.setGeometry(padded)
            self._win.show()
        else:
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

    def _init_fonts(self, path: QtCore.QDir) -> None:
        """
        Installs the fonts in the specified directory with platform-specific sizing.

        Args:
            path: Path to the 'fonts' directory.
        """

        import platform

        # Get the list of TTF fonts and compute platform-specific size:
        font_list = path.entryList(["*.ttf"])
        font_size = 12 if platform.system().lower() == "darwin" else 8

        # Attempt to load each font and track failures
        for font in font_list:
            path = f":/fonts/{font}"
            QtGui.QFontDatabase.addApplicationFont(path)

        # `Fira Code` is the default for all widgets:
        self.setFont(QtGui.QFont("Fira Code", font_size))

    def _init_style(self, path: str) -> None:
        """
        Loads and applies the QSS stylesheet to the application.

        Args:
            path: Path to the QSS stylesheet file.
        """

        qss_file = QtCore.QFile(path)
        if qss_file.open(QtCore.QFile.OpenModeFlag.ReadOnly):
            contents = QtCore.QTextStream(qss_file).readAll()
            self.setStyleSheet(contents)
        else:
            logging.warning("Failed to read stylesheet file: %s", path)

    @staticmethod
    def _show_startup() -> tuple[int, str | None]:
        """
        Displays the startup dialog and returns the result.

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
