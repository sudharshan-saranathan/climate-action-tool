#  Filename: gui/widgets/field.py
#  Module name: gui.widgets
#  Description: Custom widgets for the GUI

from __future__ import annotations

# Standard Library
from typing import Any


# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets
from qtawesome import icon


class Field(QtWidgets.QLineEdit):
    def __init__(self, parent: QtWidgets.QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.value_entered = False
        self.returnPressed.connect(self._on_return_pressed)

        self._tick = icon("mdi.check-bold", color="cyan")

    def _on_return_pressed(self) -> None:

        QtCore.QTimer.singleShot(0, lambda: self.set_updated_flag(True))
        QtCore.QTimer.singleShot(1000, lambda: self.set_updated_flag(False))

    def set_updated_flag(self, flag: bool) -> None:
        self.value_entered = flag

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:

        super().paintEvent(event)
        if self.value_entered:
            painter = QtGui.QPainter(self)
            painter.drawPixmap(self.rect().topRight(), self._tick.pixmap(16, 16))
