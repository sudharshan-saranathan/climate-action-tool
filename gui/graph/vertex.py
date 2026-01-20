# Filename: vertex.py
# Module name: graph
# Description: Vertex graphics item for node graphs.

from __future__ import annotations
from PySide6 import QtGui, QtCore, QtWidgets
from gui.graph.icon import QtaItem
from gui.graph.text import Label
import dataclasses


class VertexItem(QtWidgets.QGraphicsObject):

    @dataclasses.dataclass
    class Options:
        """
        Default vertex styling options.
        """

        bounds: QtCore.QRectF = dataclasses.field(
            default_factory=lambda: QtCore.QRectF(-20, -20, 40, 40)
        )
        border: QtGui.QPen = dataclasses.field(
            default_factory=lambda: QtGui.QPen(QtGui.QColor(0x232A2E), 2.0)
        )
        select: QtGui.QPen = dataclasses.field(
            default_factory=lambda: QtGui.QPen(QtGui.QColor(0xFFCB00), 2.0)
        )
        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(
                QtGui.QColor(0x232A2E), QtCore.Qt.BrushStyle.SolidPattern
            )
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize options:
        self._opts = VertexItem.Options()

        # Behaviour:
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # Node-icon:
        self._icon = QtaItem("mdi.mouse", 24, parent=self, color="#efefef")
        self._name = Label(
            "Vertex",
            parent=self,
            color="black",
            width=120,
            align=QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        self._name.moveBy(-60, -40)

    def boundingRect(self) -> QtCore.QRectF:
        return self._opts.bounds

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: QtWidgets.QWidget = ...,
    ) -> None:

        pen = self._opts.select if self.isSelected() else self._opts.border
        brush = (
            QtGui.QBrush(QtGui.QColor(0xFFCB00))
            if self.isSelected()
            else self._opts.background
        )

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRoundedRect(self.boundingRect(), 4, 4)
