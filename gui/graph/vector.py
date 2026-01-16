# Filename: vector.py
# Module name: graph
# Description: Graph edge connectors.

"""
Edge items connecting graph vertices.

Provides interactive edges (VectorItem) that visually connect two handles with
bezier curves. Supports preview vectors during connection creation and animated
path updates as endpoints move.
"""

from __future__ import annotations
from typing import Any
import logging
import weakref

from PySide6 import QtGui, QtCore, QtWidgets

import gui.custom as custom


VECTOR_OPTS = {
    "frame": QtCore.QRectF(-2.5, -2.5, 5, 5),
    "slack": 0.40,
    "radius": 4,
    "stroke": {
        "width": 2.0,
        "color": QtGui.QColor(0x232A2E),
        "style": QtCore.Qt.PenStyle.SolidLine,
    },
}


# Class VectorItem
class VectorItem(QtWidgets.QGraphicsObject):
    """
    A generic connector that connects two QGraphicsObject items in a QGraphicsScene.
    It supports bezier and angular curves, with customizable appearance and interactive behavior.
    """

    sig_item_focused = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_deleted = QtCore.Signal(QtWidgets.QGraphicsObject)

    def __init__(self, parent: QtWidgets.QGraphicsObject | None = None, **kwargs):
        super().__init__(parent)
        super().setZValue(-10)

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemIsSelectable, True)

        self._init_attr(kwargs)
        self._init_anim()

        self._arrow = custom.Image(":/svg/arrow.svg", parent=self)

        # Import HandleItem here to avoid circular imports
        from gui.graph.handle import HandleItem

        if isinstance(kwargs.get("origin", None), HandleItem) and isinstance(
            kwargs.get("target", None), HandleItem
        ):
            origin = kwargs.get("origin")
            target = kwargs.get("target")
            self._connect(origin, target)

        self._register_with_bus()

    def _init_attr(self, kwargs: dict[str, Any]):
        self.setProperty("curve", "bezier")
        self.setProperty("route", QtGui.QPainterPath())
        self.setProperty("slack", kwargs.get("slack", VECTOR_OPTS["slack"]))
        self.setProperty("frame", kwargs.get("frame", VECTOR_OPTS["frame"]))
        self.setProperty("stroke", kwargs.get("stroke", VECTOR_OPTS["stroke"]))
        self.base_width = VECTOR_OPTS["stroke"]["width"]

    def _init_anim(self):
        self._anim = QtCore.QPropertyAnimation(self, b"thickness")
        self._anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutSine)
        self._anim.setDuration(240)

    def _connect(self, origin: "HandleItem", target: "HandleItem") -> None:
        self.origin = weakref.ref(origin)
        self.target = weakref.ref(target)
        self.setProperty("color", origin.attr["flow"].COLOR)

        self.update_path(origin, target)

        origin.pair(self, target)
        target.pair(self, origin)
        target.set_stream(origin.attr["flow"].LABEL, mirror=False)

        origin.sig_item_moved.connect(self._on_endpoint_shifted)
        target.sig_item_moved.connect(self._on_endpoint_shifted)

    def _register_with_bus(self) -> None:
        from core.bus import EventsBus

        bus = EventsBus.instance()
        self.sig_item_focused.connect(bus.sig_item_focused)

    def boundingRect(self) -> QtCore.QRectF:
        return self.property("route").boundingRect().adjusted(-4, -4, 4, 4)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: QtWidgets.QWidget | None = None,
    ) -> None:
        color = self.property("stroke")["color"]
        width = self.property("stroke")["width"]
        style = self.property("stroke")["style"]
        color = color if not self.isSelected() else QtGui.QColor(0xFFCB00)
        pen = QtGui.QPen(
            color,
            width,
            style,
            QtCore.Qt.PenCapStyle.RoundCap,
            QtCore.Qt.PenJoinStyle.RoundJoin,
        )
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawPath(self.property("route"))

    def shape(self):
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(self.property("stroke")["width"] + 12)
        return stroker.createStroke(self.property("route"))

    def itemChange(self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        sc_changed = QtWidgets.QGraphicsItem.GraphicsItemChange.ItemSceneHasChanged
        vs_changed = QtWidgets.QGraphicsItem.GraphicsItemChange.ItemVisibleHasChanged

        if change == sc_changed and value:
            if hasattr(value, "delete_item"):
                self.sig_item_deleted.connect(value.delete_item)

        if change == vs_changed and value and hasattr(self, "origin") and hasattr(self, "target"):
            origin = self.origin()
            target = self.target()
            if origin and target:
                target.set_stream(origin.attr["flow"].LABEL, mirror=False)
                self.update_path(origin, target)

        return super().itemChange(change, value)

    def hoverEnterEvent(self, event) -> None:
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self._anim.stop()
        self._anim.setStartValue(self.base_width)
        self._anim.setEndValue(self.base_width + 2.0)
        self._anim.start()

    def hoverLeaveEvent(self, event) -> None:
        self.unsetCursor()
        self._anim.stop()
        self._anim.setStartValue(self.base_width + 2.0)
        self._anim.setEndValue(self.base_width)
        self._anim.start()

    def mouseDoubleClickEvent(self, event) -> None:
        self.sig_item_focused.emit(self)
        event.accept()
        super().mouseDoubleClickEvent(event)

    def clear(self) -> None:
        self._arrow.setPos(QtCore.QPointF())
        self.setProperty("route", QtGui.QPainterPath())
        self.prepareGeometryChange()
        self.update()

    def construct_path(self, initial: QtCore.QPointF, final: QtCore.QPointF) -> QtGui.QPainterPath:
        """Constructs the stream path from origin to target."""
        if initial.isNull() or final.isNull():
            return QtGui.QPainterPath()

        def _bezier(_slack: float):
            path = QtGui.QPainterPath()
            path.moveTo(initial)

            ctrl_one_x = initial.x() + (final.x() - initial.x()) * _slack
            ctrl_one_y = initial.y() + (final.y() - initial.y()) * 0.25
            ctrl_two_x = initial.x() + (final.x() - initial.x()) * (1 - _slack)
            ctrl_two_y = final.y() - (final.y() - initial.y()) * 0.25

            ctrl_one = QtCore.QPointF(ctrl_one_x, ctrl_one_y)
            ctrl_two = QtCore.QPointF(ctrl_two_x, ctrl_two_y)
            path.cubicTo(ctrl_one, ctrl_two, final)
            return path

        slack = self.property("slack") if initial.x() < final.x() else -10 * self.property("slack")
        return _bezier(slack)

    def update_path(
        self,
        origin: QtCore.QPointF | QtWidgets.QGraphicsObject,
        target: QtCore.QPointF | QtWidgets.QGraphicsObject,
    ) -> None:
        if isinstance(origin, QtWidgets.QGraphicsObject) and isinstance(
            target, QtWidgets.QGraphicsObject
        ):
            origin = origin.scenePos()
            target = target.scenePos()

        self.setProperty("route", self.construct_path(origin, target))
        self.prepareGeometryChange()
        self.update()

        route = QtGui.QPainterPath(self.property("route"))
        self._arrow.setPos(route.pointAtPercent(0.60))
        self._arrow.setRotation(-self.property("route").angleAtPercent(0.60))

    def show(self):
        origin = self.origin()
        target = self.target()

        if origin is None or target is None:
            super().show()
            return

        self.update_path(origin, target)
        super().show()

    @QtCore.Slot(QtWidgets.QGraphicsObject)
    def _on_endpoint_shifted(self, item) -> None:
        if self.origin and self.target and item in [self.origin(), self.target()]:
            self.update_path(self.origin(), self.target())

    @QtCore.Property(float)
    def thickness(self):
        return self.property("stroke").get("width", 2.0)

    @thickness.setter
    def thickness(self, value: float):
        stroke = self.property("stroke")
        stroke["width"] = float(value)
        self.setProperty("stroke", stroke)
        self.prepareGeometryChange()
        self.update()

    @QtCore.Property(QtGui.QColor)
    def color(self):
        return self.property("stroke").get("color", QtGui.QColor(0x363E41))

    @color.setter
    def color(self, value: str | int | QtGui.QColor):
        stroke = self.property("stroke")
        stroke["color"] = QtGui.QColor(value) if not isinstance(value, QtGui.QColor) else value
        self.setProperty("stroke", stroke)
        self.prepareGeometryChange()
        self.update()
