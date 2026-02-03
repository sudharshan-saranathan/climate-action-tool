# Filename: main.py
# Module name: N/A
# Description: Entry point for the application.

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Standard
import os
import sys
import logging
import dataclasses


# Climate Action Tool
import resources
from gui.main_ui import MainWindow


class MainApplication(QtWidgets.QApplication):

    @dataclasses.dataclass
    class GlobalConfig:
        bezel: int = 120
        theme: str = ":/theme/dark.qss"
        fonts: dict = dataclasses.field(
            default_factory=lambda: {
                "Fira Code": ":/fonts/FiraCode-Regular.ttf",
                "Marmelad": ":/fonts/Marmelad-Regular.ttf",
                "Bilbo": ":/fonts/Bilbo-Regular.ttf",
            }
        )

    def __init__(self):
        super().__init__(sys.argv)
        super().setObjectName("Climate Action Tool")

        # Instantiate options
        self._config = MainApplication.GlobalConfig()
        self._logger = logging.getLogger(__name__)

        # Customization
        self._install_theme(self._config.theme)
        self._install_fonts(self._config.fonts)

        # Main window
        self._ui = MainWindow()
        self._ui.resize(1280, 960)
        self._ui.show()

    def _install_theme(self, filename: str):
        """
        Read and apply the provided QSS file.

        :param filename:
        :return: None
        """

        if not filename.endswith(".qss"):
            logging.error("Invalid QSS file: %s", filename)
            filename = self._config.theme

        file = QtCore.QFile(filename)
        code = file.open(QtCore.QFile.OpenModeFlag.ReadOnly)

        if code:
            qss = QtCore.QTextStream(file).readAll()
            self.setStyleSheet(qss)

    def _install_fonts(self, fonts: dict[str, str]) -> None:
        """
        Install the given fonts using QFontDatabase.

        :param fonts: A dictionary of font names and paths.
        :return: None
        """

        if not isinstance(fonts, dict):
            logging.error("Expected a dictionary of fonts, got: %s")
            return

        [
            QtGui.QFontDatabase.addApplicationFont(font)
            for font in fonts.values()
            if QtCore.QFile(font).exists()
        ]

        self.setFont(QtGui.QFont("Fira Code", 8))


def main():

    app = MainApplication()
    rsp = app.exec()
    sys.exit(rsp)


if __name__ == "__main__":
    main()
