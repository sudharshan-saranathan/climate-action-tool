# Filename: config.py
# Module name: vertex
# Description: Vertex configuration dialog.

from PySide6 import QtGui, QtCore, QtWidgets

from gui.widgets import ToolBar
from gui.widgets.layouts import VLayout, HLayout, GLayout
from qtawesome import icon as qta_icon
import dataclasses

"""Vertex configuration dialog."""


class VertexConfig(QtWidgets.QDialog):
    """Vertex configuration dialog."""

    @dataclasses.dataclass(frozen=True)
    class Style:
        """Vertex configuration styling options."""

        pen: QtGui.QPen = dataclasses.field(default_factory=QtGui.QPen)
        brush: QtGui.QBrush = dataclasses.field(default_factory=QtGui.QBrush)
        pattern: str = ":/theme/pattern.png"
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

        # Instantiate style and geometry objects before calling super().__init__()
        self._geometry = VertexConfig.Geometry(size=QtCore.QSize(1080, 720))
        self._style = VertexConfig.Style(
            pen=QtGui.QPen(QtGui.QColor(0x393E41)),
            brush=QtGui.QBrush(QtGui.QColor(0x232A2E)),
        )
        self._pixmap = QtGui.QPixmap(self._style.pattern)
        self._style.brush.setTexture(self._pixmap)

        super().__init__(parent)
        super().setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        super().setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        super().resize(self._geometry.size)

        # UI components
        self._tabs = self._init_tabs()

        # Main Layout:
        layout = VLayout(self, margins=(8, 4, 8, 8), widgets=[self._tabs])

    def _init_header(self) -> QtWidgets.QLabel:
        """
        Create and configure the window header with title and subtitle.

        Returns:
            A QLabel displaying the application title and tagline with centered alignment.
        """
        header = QtWidgets.QLabel(self.objectName(), self)
        header.setContentsMargins(12, 0, 12, 0)
        header.setOpenExternalLinks(True)
        return header

    # Initialize the tab widget:
    def _init_tabs(self):
        """Create and arrange the tab widget."""

        table = QtWidgets.QTabWidget(self)
        table.addTab(
            QtWidgets.QTableWidget(columnCount=4, rowCount=4),
            qta_icon("mdi.arrow-down-bold", color="#efefef"),
            "Inputs",
        )
        table.addTab(
            QtWidgets.QTableWidget(columnCount=4, rowCount=4),
            qta_icon("mdi.arrow-up-bold", color="#efefef"),
            "Outputs",
        )
        table.addTab(
            QtWidgets.QTableWidget(columnCount=4, rowCount=4),
            qta_icon("mdi.alpha", color="#efefef"),
            "Parameters",
        )
        table.addTab(
            QtWidgets.QTableWidget(columnCount=4, rowCount=4),
            qta_icon("mdi.math-integral", color="#efefef"),
            "Equations",
        )

        # Corner widget:
        toolbar = ToolBar(
            parent=self,
            iconSize=QtCore.QSize(20, 20),
            actions=[
                (
                    qta_icon("mdi.plus", color="lightblue", active_color="white"),
                    "Add",
                    self.new_object,
                )
            ],
        )

        table.setCornerWidget(toolbar, QtCore.Qt.Corner.TopRightCorner)
        return table

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

    def new_object(self):
        """Create a new object."""

        pass
