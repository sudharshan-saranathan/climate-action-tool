# Encoding: utf-8
# Filename: outline
# Description: A QGraphicsObject wrapper for shapely Polygons

# Imports (standard)
from __future__ import annotations
from typing import Optional

# Imports (third party)
from PySide6 import QtGui, QtCore, QtWidgets


# Class Outline:
class Outline(QtWidgets.QGraphicsObject):
    """
    A QGraphicsObject wrapper that constructs its path from a shapely Polygon, handling exterior rings and providing
    simple styling options.
    """

    # Signal(s):
    sig_show_coordinate = QtCore.Signal(str)

    # Initializer:
    def __init__(
        self,
        polygon,
        minx: float,
        maxy: float,
        zoom: Optional[float] = 10.0,
    ) -> None:
        super().__init__()
        super().setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        # Attribute(s):
        self._path = QtGui.QPainterPath()
        self._poly = polygon.simplify(0.001, preserve_topology=True)
        self._minx = minx
        self._maxy = maxy
        self._zoom = zoom

        # Styling:
        self._pen = QtGui.QPen(QtGui.QColor(0xFFFFFF), 2.0)
        self._brush = QtGui.QBrush(QtGui.QColor(0x333E41))
        self.setAcceptHoverEvents(True)
        self.setZValue(-10)

        # Build the path:
        self._build_path()
        self._init_menu()

    # Context menu initializer:
    def _init_menu(self):
        self._menu = QtWidgets.QMenu()
        self._menu.addAction("Create Graph")

    # Convert lon/lat to scene coordinates:
    def _coord_to_scene(self, longitude: float, latitude: float) -> tuple[float, float]:
        x = (float(longitude) - self._minx) * self._zoom
        y = (self._maxy - float(latitude)) * self._zoom
        return x, y

    # Convert scene coordinates to lon/lat:
    def _scene_to_coord(self, x: float, y: float) -> tuple[float, float]:
        longitude = (x / self._zoom) + self._minx
        latitude = self._maxy - (y / self._zoom)
        return longitude, latitude

    # Build the painter path from polygon coordinates:
    def _build_path(self):
        exterior_coords = list(self._poly.exterior.coords)

        def _draw_coords(coords):
            xx, yy = self._coord_to_scene(coords[0][0], coords[0][1])
            self._path.moveTo(xx, yy)

            for lon, lat in coords[1:]:
                x, y = self._coord_to_scene(lon, lat)
                self._path.lineTo(x, y)

            self._path.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            self._path.closeSubpath()

        _draw_coords(exterior_coords)

    # QGraphicsObject required method:
    def boundingRect(self) -> QtCore.QRectF:
        if self._path.isEmpty():
            return QtCore.QRectF()
        return self._path.boundingRect().adjusted(-0.5, -0.5, 0.5, 0.5)

    # Paint the outline:
    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget=None,
    ) -> None:
        style = (
            QtCore.Qt.BrushStyle.SolidPattern
            if self.isUnderMouse()
            else QtCore.Qt.BrushStyle.Dense1Pattern
        )
        color = QtGui.QColor(0xFFCB00) if self.isSelected() else QtGui.QColor(0x333E41)

        brush = QtGui.QBrush(color, style)
        painter.setPen(self._pen)
        painter.setBrush(brush)
        painter.drawPath(self._path)

    # Return the shape for hit testing:
    def shape(self) -> QtGui.QPainterPath:
        return self._path

    # Handle context menu event:
    def contextMenuEvent(self, event) -> None:
        self._menu.exec(event.screenPos())

    # Handle mouse press event:
    def mousePressEvent(self, event) -> None:
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            event.modifiers() != QtCore.Qt.KeyboardModifier.ShiftModifier,
        )
        super().mousePressEvent(event)
