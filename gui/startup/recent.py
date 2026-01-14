# Filename: recent.py
# Module name: startup
# Description: A scrollable widget that displays recent projects.

import glob
import dataclasses
from qtawesome import icon as qta_icon
from PySide6 import QtWidgets, QtCore, QtGui
from gui.widgets import HLayout


class RecentProjects(QtWidgets.QFrame):

    # Signal:
    sig_open_recent = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Get recent projects from the folder:
        recents = [project for project in glob.glob("recents/*.h5")]

        layout = HLayout(self)
        for project in recents:
            layout.addWidget(self._create_icon_button(project))

    def _create_icon_button(self, path: str):

        tool_button = QtWidgets.QToolButton()
        tool_button.setIcon(
            qta_icon("mdi.file-chart", color="gray", color_active="white")
        )
        tool_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )
        tool_button.setText(path)
        tool_button.clicked.connect(lambda: self.sig_open_recent.emit(path))
        return tool_button

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor(0x393E41))
        painter.drawRoundedRect(self.rect(), 8, 8)
