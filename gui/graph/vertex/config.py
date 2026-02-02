# Filename: config.py
# Module name: vertex
# Description: Vertex configuration dialog.

from PySide6 import QtGui, QtCore, QtWidgets

from gui.widgets import ToolBar
from gui.widgets.combobox import ComboBox
from gui.widgets.layouts import VLayout, HLayout, GLayout
from qtawesome import icon as qta_icon
import dataclasses


class VertexConfig(QtWidgets.QDialog):
    """A dialog window for configuring vertex inputs, outputs, parameters, and equations."""

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
        radius: int = 8

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
        self._form = self._init_form()
        self._tabs = self._init_tabs()

        # Main Layout:
        HLayout(self, margins=(8, 4, 8, 8), widgets=[self._form, self._tabs])

    def _init_form(self) -> QtWidgets.QFrame:

        container = QtWidgets.QFrame(self)
        container.setMinimumWidth(280)

        layout = QtWidgets.QFormLayout(container)
        layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        layout.setContentsMargins(40, 4, 40, 0)
        layout.setSpacing(4)

        layout.addRow("Name:", QtWidgets.QLabel("Vertex"))
        layout.addRow("Type/Tech:", ComboBox(editable=True))

        return container

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

        button = QtWidgets.QPushButton("Add", self)
        button.setIcon(qta_icon("mdi.plus", color="lightblue", active_color="white"))
        button.setStyleSheet(self._style.style)

        table.setCornerWidget(button, QtCore.Qt.Corner.TopRightCorner)
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
