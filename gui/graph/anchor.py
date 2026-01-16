# Filename: anchor.py
# Module name: graph
# Description: Anchor rails for handles on vertices.

"""
Anchor item for positioning handles on vertices.

Provides a transparent rail (AnchorItem) along which handles can be positioned.
Emits signals when clicked to facilitate handle creation at specific positions.
"""

from __future__ import annotations
from PySide6 import QtGui, QtCore, QtWidgets
from gui.graph.handle import HandleOpts


# Default config
AnchorOpts = {
    "frame": QtCore.QRectF(-1, -18, 2, 32),
    "round": 0,
    "style": {
        "color": QtGui.QPen(QtCore.Qt.GlobalColor.transparent),
        "brush": QtGui.QBrush(QtGui.QColor(0xFFFFFF), QtCore.Qt.BrushStyle.SolidPattern),
    },
}


# Class Anchor
class AnchorItem(QtWidgets.QGraphicsObject):
    """Transparent rails for anchoring handles to a vertex."""

    sig_anchor_clicked = QtCore.Signal(QtCore.QPointF)

    def __init__(self, role: int, parent: QtWidgets.QGraphicsObject | None = None, **kwargs):
        super().__init__(parent)
        super().setAcceptHoverEvents(True)

        self.setProperty("role", role)
        self.setProperty("cpos", kwargs.get("cpos", QtCore.QPointF(0, 0)))
        self.setProperty("frame", kwargs.get("frame", AnchorOpts["frame"]))
        self.setProperty("round", kwargs.get("round", AnchorOpts["round"]))
        self.setProperty("style", kwargs.get("style", AnchorOpts["style"]))
        self.setProperty("ordinate", None)

        self.setPos(self.property("cpos"))

        # Initialize handle hint:
        self._hint = QtWidgets.QGraphicsEllipseItem(self)
        self._hint.setRect(HandleOpts["frame"])
        self._hint.setPen(QtGui.QPen(QtGui.QColor(0x000000), 0.50))
        self._hint.setBrush(QtGui.QBrush(HandleOpts["color"]))
        self._hint.setVisible(False)

        # Hook onto callbacks:
        if kwargs.get("callback", None):
            self.sig_anchor_clicked.connect(
                kwargs.get("callback"), QtCore.Qt.ConnectionType.UniqueConnection
            )

    def boundingRect(self):
        return self.property("frame").adjusted(-2, 0, 2, 0)

    def paint(self, painter, option, widget=...):
        painter.setPen(self.property("style")["color"])
        painter.setBrush(self.property("style")["brush"])
        painter.drawRoundedRect(
            self.property("frame").adjusted(0.75, 0.75, -0.75, -0.75),
            self.property("round"),
            self.property("round"),
        )

    def hoverEnterEvent(self, event, /):
        super().hoverEnterEvent(event)
        super().setProperty("ordinate", event.pos().y())
        super().setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self._hint.show()

    def hoverMoveEvent(self, event, /):
        super().setProperty("ordinate", event.pos().y())
        super().hoverMoveEvent(event)
        self._hint.setY(event.pos().y())

    def hoverLeaveEvent(self, event, /):
        super().setProperty("ordinate", None)
        super().unsetCursor()
        super().hoverLeaveEvent(event)
        self._hint.hide()

    def mousePressEvent(self, event, /):
        self.sig_anchor_clicked.emit(QtCore.QPointF(0, event.pos().y()))

    def resize(self, bottom: float, /):
        """Resize the anchor to the specified bottom position."""
        rect = self.property("frame")
        rect.setBottom(bottom)
        self.setProperty("frame", rect)

    @QtCore.Property(int)
    def role(self):
        return self.property("role")

    @role.setter
    def role(self, value):
        pass
