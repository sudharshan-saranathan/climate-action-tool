# Filename: main.py
# Module name: N/A
# Description: Entry point for the Climate Action Tool (CAT)

# Python
import argparse
import logging
import typing
import sys

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# Climact
import rsrc
from gui.startup.window import StartupWindow
from gui.main_ui.window import MainWindow
import core.graph  # Import to ensure GraphManager singleton is initialized


class ClimateActionTool(QtWidgets.QApplication):
    """
    Main application class to manage app lifecycle and UI components.
    """

    # Class logger
    _logger = logging.getLogger("ClimateActionTool")

    # Flags
    backend_flag: bool = True
    startup_flag: bool = True
    startup_code: int = 1
    startup_file: str = ""

    @dataclass(frozen=True)
    class Resources:
        """Resource paths.

        Attributes:
            image: Path to the application's taskbar icon (PNG).
            theme: Path to the application's QSS stylesheet.
            fonts: Path to the application's font directory.
        """

        image: str = ":/logo/logo.png"
        theme: str = ":/theme/dark.qss"
        fonts: str = ":/fonts"

    @dataclass(frozen=True)
    class Geometric:
        """Geometric attribute(s).

        Attributes:
            margin: The application's default margin (on all sides)
            normal: The application's default geometry.
        """

        margin: int = 64
        normal: QtCore.QRect = field(default_factory=QtCore.QRect)

    def __init__(self):

        super().__init__(sys.argv)
        super().setObjectName("climate-action-tool")

        # Instantiate dataclasses
        self._rsrc = ClimateActionTool.Resources()
        self._geom = ClimateActionTool.Geometric()

        image = self._rsrc.image  # The application's taskbar logo.
        theme = self._rsrc.theme  # Path to the QSS stylesheet.
        bezel = self._geom.margin  #
        fonts = QtCore.QDir(self._rsrc.fonts)

        # Compute window geometry by padding screen bounds (primary screen only)
        screen = QtWidgets.QApplication.primaryScreen()
        bounds = screen.availableGeometry()
        padded = bounds.adjusted(bezel, bezel, -bezel, -bezel)

        # Initialize application attributes
        self._init_args()
        self._init_theme(theme)
        self._init_fonts(fonts)
        self.setWindowIcon(QtGui.QIcon(image))

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

        # Display the startup dialog, if enabled
        if self.startup_flag:
            self.startup_code = self._show_startup()

        # Create and show the main window
        if self.startup_code:

            self._win = MainWindow()
            self._win.setWindowTitle("Climate Action Tool")
            self._win.setGeometry(padded)
            self._win.show()

        else:
            sys.exit(0)

    def _init_geometry(self):
        pass

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
        Set the application's theme based on the specified QSS stylesheet.

        :param path: Path to the QSS stylesheet file.
        :return: None
        """

        theme = QtCore.QFile(path)
        state = theme.open(QtCore.QFile.OpenModeFlag.ReadOnly)

        if state:
            stream = QtCore.QTextStream(theme)
            string = stream.readAll()
            self.setStyleSheet(string)

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

    def resources(self):
        return self._rsrc


def main() -> None:
    """Instantiate the application and enter its event loop."""

    application = ClimateActionTool()
    application.exec()  # This call is blocking by default.
    sys.exit(0)


if __name__ == "__main__":
    main()
