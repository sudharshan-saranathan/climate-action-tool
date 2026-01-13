# Filename: banner.py
# Module name: startup
# Description: Banner displaying the application's logo, title, and subtitle in the startup window.

import dataclasses
from qtawesome import icon as qta_icon
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets
from gui.widgets import GLayout, ToolBar


class StartupBanner(QtWidgets.QWidget):
    """
    A banner displaying the application's title, logo, subtitle(s), and relevant links.
    """

    @dataclasses.dataclass
    class Options:
        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtCore.Qt.BrushStyle.NoBrush
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        self._opts = StartupBanner.Options() # Required for painting.

        # UI components:
        self._title = QtWidgets.QLabel( # Title
            "<span style='color:white; font-size:24pt'>Climate Action Tool</font>",
            self,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )


        # Arrange in a horizontal layout:
        layout = GLayout(self)
        layout.addWidget(self._title, 0, 1, QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft)