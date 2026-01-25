# Filename: config.py
# Module name: vertex
# Description: Vertex configuration dialog.

from PySide6 import QtGui, QtCore, QtWidgets
from gui.widgets.layouts import VLayout, HLayout, GLayout
import dataclasses

"""Vertex configuration dialog."""


class VertexConfig(QtWidgets.QDialog):
    """Vertex configuration dialog."""

    @dataclasses.dataclass(frozen=True)
    class Style:
        """Vertex configuration styling options."""

        pen: QtGui.QPen = dataclasses.field(default_factory=QtGui.QPen)
        brush: QtGui.QBrush = dataclasses.field(default_factory=QtGui.QBrush)
        style: str = (
            "QPushButton {"
            "   padding: 4px 0px 4px 0px;"
            "   color: #aaaaaa;"
            "   width: 200px;"
            "   text-align: right;"
            "   border-radius: 0px;"
            "   background-color: transparent;"
            "}"
            "QPushButton:hover {"
            "   color: #efefef;"
            "}"
            "QPushButton:checked {"
            "   color: white;"
            "   font-weight: bold;"
            "}"
        )

    @dataclasses.dataclass(frozen=True)
    class Geometry:
        """Vertex configuration attributes."""

        size: QtCore.QSize = dataclasses.field(default_factory=QtCore.QSize)
        radius: int = 10

    def __init__(self, parent: QtWidgets.QDialog = None):
        super().__init__(parent)
        super().setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        super().setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self._geometry = VertexConfig.Geometry(size=QtCore.QSize(1080, 720))
        self._style = VertexConfig.Style(
            pen=QtGui.QPen(QtGui.QColor(0x393E41)),
            brush=QtGui.QBrush(QtGui.QColor(0x232A2E)),
        )

    def paintEvent(self, event):
        """Paint the vertex configuration dialog."""

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setPen(self._style.pen)
        painter.setBrush(self._style.brush)
        painter.drawRoundedRect(
            self.rect(),
            self._geometry.radius,
            self._geometry.radius,
        )
