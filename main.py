# Filename: main.py
# Module name: N/A
# Description: Entry point for the Climate Action Tool (CAT)

import dataclasses
import resources  # noqa: F401 - Required to register Qt resources (DO NOT REMOVE)
import argparse
import logging
import sys

from PySide6 import QtGui, QtCore, QtWidgets
from gui.startup.window import StartupWindow
from gui.main_ui.window import MainWindow


class ClimateActionTool(QtWidgets.QApplication):
    """
    Main application class to manage app lifecycle and UI components.
    """

    backend_flag = True  # Flag to enable/disable the backend optimization module.
    startup_flag = True  # Flag to enable/disable the startup dialog.
    startup_file = None  # User-selected project file to load (if available).

    @dataclasses.dataclass(frozen=True)
    class Style:
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

        # Instantiate application options
        self._style = ClimateActionTool.Style()
        image = self._style.image
        bezel = self._style.bezel
        theme = self._style.theme
        fonts = QtCore.QDir(self._style.fonts)

        # Compute window geometry by padding screen bounds (primary screen only)
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()
        padded = bounds.adjusted(bezel, bezel, -bezel, -bezel)

        # Initialize application attributes
        self._init_args()
        self._init_theme(theme)
        self._init_fonts(fonts)
        self.setWindowIcon(QtGui.QIcon(image))

        # Display the startup dialog, if enabled
        if self.startup_flag:
            self.startup_code = self._show_startup()

        # Create and show the main window
        if self.startup_code:

            try:
                self._win = MainWindow(project=self.startup_file)
                self._win.setWindowTitle("Climate Action Tool")
                self._win.setGeometry(padded)
                self._win.show()

            except Exception as e:
                logging.error(e)
                sys.exit(1)  # Exit with non-zero status code

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

        self.backend_flag = args.backend
        self.startup_flag = args.startup
        self.startup_code = 1

    def _init_fonts(self, path: QtCore.QDir) -> None:
        """
        Install fonts from the specified directory and set platform-specific size.

        Args:
            path: Path to the 'fonts' directory.
        """

        # For system platform detection
        import platform

        # Get the list of TTF fonts and compute platform-specific size:
        font_list = path.entryList(["*.ttf"])
        font_size = 12 if platform.system().lower() == "darwin" else 8

        # Load fonts
        for font in font_list:
            path = f":/fonts/{font}"
            QtGui.QFontDatabase.addApplicationFont(path)

        # Set default font
        self.setFont(QtGui.QFont("Fira Code", font_size))

    def _init_theme(self, path: str) -> None:
        """
        Loads and applies the QSS stylesheet to the application.

        Args:
            path: Path to the QSS stylesheet file.
        """

        try:

            theme = QtCore.QFile(path)
            if theme.open(QtCore.QFile.OpenModeFlag.ReadOnly):
                theme = QtCore.QTextStream(theme).readAll()
                self.setStyleSheet(theme)

        except Exception as e:
            logging.warning(f"Unable to apply theme {e}. Using system default.")

    @staticmethod
    def _show_startup() -> int:
        """
        Display the startup dialog and return the result

        Returns:
            A tuple of (exit_code, project_path) where exit_code indicates
            success (1) or cancellation (0).
        """

        startup = StartupWindow()
        startup.exec()

        result: int = startup.result()
        return result

    @property
    def options(self) -> Style:
        return self._style


def main() -> None:
    """Instantiate the application and enter its event loop."""

    application = ClimateActionTool()
    application.exec()  # This call is blocking by default.
    sys.exit(0)


if __name__ == "__main__":
    main()
