# Filename: dialog.py
# Module name: startup
# Description: A modal QDialog subclass that is displayed at startup.

from __future__ import annotations
from PySide6 import QtCore, QtWidgets, QtGui
import dataclasses


class StartupWindow(QtWidgets.QDialog):

    @dataclasses.dataclass
    class Options:
        corner_radius: float = 4.0
        area_geometry: QtCore.QRect = dataclasses.field(
            default_factory=lambda: QtCore.QRect(0, 0, 800, 600)
        )

    def __init__(self, parent=None):
        super().__init__(parent)
        super()
        super().setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        super().setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # Instantiate options:
        self._opts = StartupWindow.Options()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.drawRoundedRect(self.rect())
