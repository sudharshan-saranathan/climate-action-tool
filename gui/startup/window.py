# Filename: dialog.py
# Module name: startup
# Description: A modal QDialog subclass that is displayed at startup.

import dataclasses
from PySide6 import QtCore, QtWidgets, QtGui

from gui.startup import StartupBanner
from gui.startup.choice import StartupChoice
from gui.widgets import VLayout, HLayout


class StartupWindow(QtWidgets.QDialog):

    @dataclasses.dataclass(frozen=True)
    class Options:

        radius: float = 10.0  # Radius of the rounded corners.
        border: QtGui.QPen = (
            dataclasses.field(  # Window border style (default: no border).
                default_factory=lambda: QtGui.QPen(QtGui.QColor(0x393E41), 2.0)
            )
        )

        background: QtGui.QBrush = dataclasses.field(  # Background color and style.
            default_factory=lambda: QtGui.QBrush(
                QtGui.QColor(0x232A2E),
                QtCore.Qt.BrushStyle.SolidPattern,
            )
        )

        foreground: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(
                QtGui.QColor(0x393E41),
                QtCore.Qt.BrushStyle.Dense1Pattern,
            )
        )

        rect: QtCore.QSize = (
            dataclasses.field(  # Size of the window (default: 900x640).
                default_factory=lambda: QtCore.QSize(900, 640)
            )
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        # Instantiate options and set attribute(s):
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        # UI components:
        self._pattern = QtGui.QPixmap(":/theme/startup.png")
        self._choice = StartupChoice()

        self._opts = StartupWindow.Options()
        self._opts.background.setTexture(self._pattern)
        self.resize(self._opts.rect)

        # Arrange widgets in a grid:
        layout = HLayout(self, spacing=4, margins=(4, 4, 4, 4))
        layout.addWidget(self._choice)
        layout.addWidget(QtWidgets.QTableWidget(), stretch=5)


    def paintEvent(self, event: QtGui.QPaintEvent) -> None:

        painter = QtGui.QPainter(self)
        painter.setPen(self._opts.border)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setBrush(self._opts.background)
        painter.drawRoundedRect(self.rect(), self._opts.radius, self._opts.radius)
