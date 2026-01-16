# Filename: image.py
# Module name: custom
# Description: SVG icon rendering for graphics scenes.

"""
QGraphicsObject-based SVG icon rendering.

Provides SVG image items (Image) that can be displayed and manipulated on a QGraphicsScene.
Supports resizing, opacity adjustments, and conversion to QIcon.
"""

from __future__ import annotations
from PySide6 import QtSvg, QtCore, QtWidgets, QtGui


ImageOpts = {
    "size": QtCore.QSize(20, 20),
    "anim": False,
}


class Image(QtWidgets.QGraphicsObject):
    """A QGraphicsObject that renders SVG icons."""

    def __init__(
        self, buffer: str | QtGui.QIcon, parent: QtWidgets.QGraphicsObject | None = None, **kwargs
    ):
        super().__init__(parent)

        self.setProperty("size", kwargs.get("size", ImageOpts["size"]))
        self.setProperty("anim", kwargs.get("anim", False))
        self.setProperty("buffer", buffer if isinstance(buffer, str) else self.from_icon(buffer))

        self.renderer = QtSvg.QSvgRenderer(self.property("buffer"), self)

        if kwargs.get("movable", False):
            self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(
            -self.property("size").width() / 2,
            -self.property("size").height() / 2,
            self.property("size").width(),
            self.property("size").height(),
        )

    def paint(self, painter, option, widget=None):
        painter.save()
        self.renderer.render(painter, self.boundingRect())
        painter.restore()

    def to_icon(self):
        """Converts the SVG icon to a QIcon object."""
        pixmap = QtGui.QPixmap(self.property("size"))
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(pixmap)
        self.renderer.render(painter)
        painter.end()

        return QtGui.QIcon(pixmap)

    def set_buffer(self, buffer: str) -> None:
        """Sets a new SVG buffer for the icon."""
        self.setProperty("buffer", buffer)
        self.renderer.load(self.property("buffer"))
        self.update()

    @staticmethod
    def from_icon(icon: QtGui.QIcon) -> str:
        """Convert a QIcon to SVG string (simplified - returns empty string)."""
        return ""
