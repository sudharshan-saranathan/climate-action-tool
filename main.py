# Filename: main.py
# Module name: main_ui
# Description: Entry point for the Climate Action Tool.

from __future__ import annotations

#
import dataclasses
import resources  # noqa: F401 - Required to register Qt resources (DO NOT REMOVE)
import argparse
import platform
import logging
import types
import sys

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


from gui.main_ui import MainWindow
from gui.startup import StartupWindow


class ClimateActionTool(QtWidgets.QApplication):
    """
    Subclass of `QtWidgets.QApplication`. Sets style, font, and initializes the main user interface.
    Must be instantiated before QtWidgets.
    """

    backend_flag = True  # Flag to enable/disable the backend optimization module.
    startup_flag = True  # Flag to enable/disable the startup dialog.
    startup_file = None  # The path to the project file to open on startup (if any).

    @dataclasses.dataclass
    class Options:
        """
        Default options for the Climate Action Tool.
        """

        image: str = ":/logo/logo.png"  # The application's logo
        theme: str = ":/theme/dark.qss"  # The qss-file to use as the default theme.
        bezel: int = (
            64  # Initial padding around the main window at application startup.
        )
        fonts = {  # Keys should match values returned by `platform.system()`.
            "windows": types.SimpleNamespace(family="Fira Code", pointSize=8),
            "darwin": types.SimpleNamespace(family="Spot Mono", pointSize=14),
            "linux": types.SimpleNamespace(family="Ubuntu Sans Mono", pointSize=9),
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

        self._init_style(theme)  # Apply the theme first.
        self._init_font()  # Font-setting should succeed style-setting.
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
        Sets the application's font based on the platform.
        Windows - "Fira Code"
        macOS - "Menlo"
        Linux - "Ubuntu Sans Mono"
        """

        fonts: dict[str, types.SimpleNamespace] = self._opts.fonts
        envir: str = platform.system().lower()

        # Install custom fonts using Qt's font database:
        QtGui.QFontDatabase.addApplicationFont(":/fonts/MarckScript-Regular.ttf")
        QtGui.QFontDatabase.addApplicationFont(":/fonts/Bilbo-Regular.ttf")

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

        else:
            logging.warning("Failed to read stylesheet file.")

    @staticmethod
    def _show_startup() -> tuple[int, str | None]:
        """
        Displays the startup window.

        Returns:
            result (int): The startup window.
        """

        startup = StartupWindow()
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
