# Filename: tabber.py
# Module name: gui
# Description: A QTabWidget subclass for displaying various widgets.

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


class Tabber(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super().__init__(
            parent,
            tabsClosable=True,
            tabBarAutoHide=True,
        )

    def paintEvent(self, event: QtGui.QPaintEvent):

        index = self.currentIndex()
        rect = self.tabBar().tabRect(index)
        rect = rect.adjusted(0, 12, -4, 8)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor(0xEFEFEF))
        painter.drawRect(rect)
