# Filename: dialog.py
# Module name: startup
# Description: A modal QDialog subclass that is displayed at startup.

import dataclasses
from PySide6 import QtCore, QtWidgets, QtGui

from gui.startup import StartupChoice
from gui.widgets import GLayout


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

        rect: QtCore.QSize = (
            dataclasses.field(  # Size of the window (default: 900x640).
                default_factory=lambda: QtCore.QSize(900, 640)
            )
        )

    def __init__(self, parent=None):
        """
        Initializes the window, configures attributes, and adds child widgets.
        """
        super().__init__(parent)
        super().setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        super().setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        # UI components:
        self._pixmap = QtGui.QPixmap(":/theme/startup.png")
        self._header = self._init_header()
        self._h_line = self._init_h_line()
        self._choice = StartupChoice()
        self._ftable = QtWidgets.QTableWidget()

        self._opts = StartupWindow.Options()
        self._opts.background.setTexture(self._pixmap)
        self.resize(self._opts.rect)

        # Arrange UI components in a layout:
        layout = GLayout(  # Horizontal layout.
            self,
            spacing=12,
            margins=(24, 4, 4, 4),
        )

        layout.setRowStretch(0, 5)
        layout.addWidget(self._header, 1, 0)
        layout.addWidget(self._h_line, 2, 0)
        layout.addWidget(self._choice, 3, 0)
        layout.addWidget(self._ftable, 0, 1, 5, 1)
        layout.setRowStretch(4, 5)


    def _init_header(self) -> QtWidgets.QLabel:
        """
        Creates a title header for the startup window.
        """

        header = QtWidgets.QLabel(
            "<span style='color:white; "
            "font-size:24pt'>Climate Action Tool</font>",
            self,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        return header

    def _init_h_line(self) -> QtWidgets.QFrame:
        """
        Creates and returns a light gray horizontal separator.
        """

        h_line = QtWidgets.QFrame(self)
        h_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        h_line.setStyleSheet("QFrame {background:#4f4f4f;}")
        h_line.setLineWidth(2)
        return h_line

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:

        painter = QtGui.QPainter(self)
        painter.setPen(self._opts.border)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setBrush(self._opts.background)
        painter.drawRoundedRect(self.rect(), self._opts.radius, self._opts.radius)
