# Filename: main_ui.py
# Module name: gui
# Description: The main User Interface.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


# Standard
from dataclasses import field
from dataclasses import dataclass


# ----------------------------------------------------------------------------------------------------------------------
# Class Name: `MainWindow`
# Class Info: CAT's main top-level user interface (UI)
# Qt website: https://doc.qt.io/qtforpython-6/index.html


class MainWindow(QtWidgets.QMainWindow):

    @dataclass(frozen=True)
    class Style:
        """
        Border and background styling options for the main window.

        - border: QPen object used to draw the window's border.
        - background: QBrush object used to fill the window's background.
        """

        pen: dict = field(default_factory=lambda: {"color": 0x363E41, "width": 1.0})
        brs: dict = field(default_factory=lambda: {"color": 0x232A2E})

    @dataclass
    class Attrs:
        radius: int = 8
        rect: QtCore.QRect = field(
            default_factory=lambda: QtCore.QRect(100, 100, 1600, 900)
        )

    def __init__(self):
        super().__init__(parent=None)  # Must have no-parent

        # Define style and attribute(s)
        self._style = MainWindow.Style()
        self._attrs = MainWindow.Attrs()

        # Customize appearance and behaviour
        self.setContentsMargins(4, 4, 4, 4)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setGeometry(self._attrs.rect)

    def paintEvent(self, event: QtGui.QPaintEvent):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        brs = QtGui.QBrush(QtGui.QColor(self._style.brs["color"]))
        pen = QtGui.QPen(
            QtGui.QColor(self._style.pen["color"]), self._style.pen["width"]
        )

        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(self.rect(), self._attrs.radius, self._attrs.radius)
        painter.end()
