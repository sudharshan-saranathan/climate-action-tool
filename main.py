# Filename: main.py
# Module name: N/A
# Description: Entry point for the application.

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Standard
import sys
import logging

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# Climate Action Tool (CAT)
import rsrc
from gui.main_ui.window import MainWindow


# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# ----------------------------------------------------------------------------------------------------------------------
# Class Name: MainApplication
# Class Info: The main application class for the Climate Action Tool (CAT)
# Qt website: https://doc.qt.io/qtforpython-6/index.html


class MainApplication(QtWidgets.QApplication):

    @dataclass
    class GlobalConfig:
        bezel: int = 120
        theme: str = ":/theme/dark.qss"
        fonts: dict = field(
            default_factory=lambda: {
                "Alkatra": ":/fonts/Alkatra-Regular.ttf",
                "Bitcount": ":/fonts/Bitcount-Regular.ttf",
                "Bitcount Single": ":/fonts/BitcountSingle-Regular.ttf",
                "Baloo 2": ":/fonts/Baloo2-Regular.ttf",
                "Doto": ":/fonts/Doto-Regular.ttf",
                "Ubuntu": ":/fonts/Ubuntu-Regular.ttf",
                "Special Elite": ":/fonts/SpecialElite-Regular.ttf",
                "Fira Code": ":/fonts/FiraCode-Regular.ttf",
                "Marmelad": ":/fonts/Marmelad-Regular.ttf",
                "Roboto Mono": ":/fonts/RobotoMono-Regular.ttf",
                "Bilbo": ":/fonts/Bilbo-Regular.ttf",
            }
        )

    def __init__(self):
        super().__init__(sys.argv)
        super().setObjectName("Climate Action Tool (CAT)")

        # Instantiate options
        self._config = MainApplication.GlobalConfig()

        # Customization
        self._install_theme(self._config.theme)  # Install the theme before fonts.
        self._install_fonts(self._config.fonts)

        # Main window
        self._ui = MainWindow()
        self._ui.show()

    def _install_theme(self, qrc_file: str) -> None:
        """
        Parse and install the given stylesheet application-wide.

        :param qrc_file: Path to the stylesheet.
        :return: None
        """

        if not (qrc_file.startswith(":") and qrc_file.endswith(".qss")):
            logging.warning("Invalid stylesheet path: %s", qrc_file)
            qrc_file = self._config.theme

        file = QtCore.QFile(qrc_file)
        code = file.open(QtCore.QFile.OpenModeFlag.ReadOnly)

        if code:
            stream = QtCore.QTextStream(file)
            string = stream.readAll()
            self.setStyleSheet(string)

    def _install_fonts(self, fonts: dict[str, str]) -> None:
        """
        Install the given fonts using QFontDatabase.

        :param fonts: A dictionary of font-names and paths.
        :return: None
        """

        # Required for platform-based font sizing.
        import platform

        # Abort for invalid argument
        if not isinstance(fonts, dict):
            logging.error("Expected a dictionary of fonts, got: %s", type(fonts))
            return

        # Iterate and install available fonts
        for font, path in fonts.items():
            if QtCore.QFile(path).exists():
                QtGui.QFontDatabase.addApplicationFont(path)

        name = "Fira Code"
        size = 11 if platform.system().lower() == "darwin" else 8
        font = QtGui.QFont(name, size)
        self.setFont(font)


def main():

    app = MainApplication()
    rsp = app.exec()
    sys.exit(rsp)


if __name__ == "__main__":
    main()
