# Filename: vector.py
# Module name: graph
# Description: Edge item for displaying graph connections.

"""Edge item for displaying graph connections."""

from __future__ import annotations
from PySide6 import QtCore, QtGui, QtWidgets
from gui.graph.reusable.image import Image
import dataclasses


class VectorItem(QtWidgets.QGraphicsObject):
    """Edge item for displaying graph connections."""

    @dataclasses.dataclass
    class Options:
        """Edge styling options.

        Attributes:
            width: Line width in pixels (default: 2).
            slack: The Bézier curve's slack factor (default: 0.4).
            color: Line color (default: gray).
            select: Line color when selected (default: yellow).
        """

        width: float = 3.0
        slack: float = 0.4
        color: QtGui.QColor = dataclasses.field(
            init=False,
            default_factory=lambda: QtGui.QColor(0xABABAB),
        )

        select: QtGui.QColor = dataclasses.field(
            init=False,
            default_factory=lambda: QtGui.QColor(0xFFCB00),
        )

    def __init__(self, parent=None, origin=None, target=None):
        super().__init__(parent)
        super().setZValue(-10)
        super().setPos(QtCore.QPointF(0, 0))
        super().setAcceptHoverEvents(True)

        # Class member(s):
        self._opts = VectorItem.Options()
        self._path = QtGui.QPainterPath()
        self._arrow = Image(":/svg/arrow.svg", parent=self)
        self._origin = origin  # True origin vertex
        self._target = target  # True target vertex

        # Set property before creating animation:
        self.setProperty("linewidth", self._opts.width)

        # Initialize hover animation:
        self._anim = self._init_anim()

    def _init_anim(self):
        """Initializes hover animation."""

        anim = QtCore.QPropertyAnimation(self, b"thickness")
        anim.setDuration(360)
        anim.setEasingCurve(QtCore.QEasingCurve.Type.OutQuad)
        return anim

    def boundingRect(self) -> QtCore.QRectF:
        return self._path.boundingRect().adjusted(-4, -4, 4, 4)

    def shape(self):
        stroker = QtGui.QPainterPathStroker()
        current_width = self.property("linewidth") or self._opts.width
        stroker.setWidth(current_width + 12)
        return stroker.createStroke(self._path)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: QtWidgets.QWidget = ...,
    ) -> None:

        color = self._opts.select if self.isSelected() else self._opts.color
        pen = QtGui.QPen(
            color,
            self.property("linewidth"),
            QtGui.Qt.PenStyle.SolidLine,
            QtGui.Qt.PenCapStyle.RoundCap,
            QtGui.Qt.PenJoinStyle.RoundJoin,
        )

        painter.setPen(pen)
        painter.drawPath(self._path)

    def hoverEnterEvent(self, event, /):
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._anim.stop()
        self._anim.setStartValue(self._opts.width)
        self._anim.setEndValue(self._opts.width + 2.0)
        self._anim.start()

    def hoverLeaveEvent(self, event, /):
        self.unsetCursor()
        self._anim.stop()
        self._anim.setStartValue(self._opts.width + 2.0)
        self._anim.setEndValue(self._opts.width)
        self._anim.start()

    def _compute(
        self,
        origin: QtCore.QPointF,
        target: QtCore.QPointF,
    ) -> QtGui.QPainterPath:

        path = QtGui.QPainterPath()
        path.moveTo(origin)

        # Calculate control points for cubic Bezier curve
        slack = self._opts.slack

        ctrl_one_x = origin.x() + (target.x() - origin.x()) * slack
        ctrl_one_y = origin.y() + (target.y() - origin.y()) * 0.25
        ctrl_two_x = origin.x() + (target.x() - origin.x()) * (1 - slack)
        ctrl_two_y = target.y() - (target.y() - origin.y()) * 0.25

        ctrl_one = QtCore.QPointF(ctrl_one_x, ctrl_one_y)
        ctrl_two = QtCore.QPointF(ctrl_two_x, ctrl_two_y)

        path.cubicTo(ctrl_one, ctrl_two, target)
        return path

    def update_path(self, origin: QtCore.QPointF, target: QtCore.QPointF):
        """Update the path between two points.

        When the origin/target vertex references are available, the method automatically
        determines the correct flow direction by comparing provided coordinates
        with stored vertex positions.

        Args:
            origin: Origin point coordinate
            target: Target point coordinate
        """
        self.prepareGeometryChange()

        # If we have stored vertex references, check if coordinates are swapped:
        if self._origin is not None and self._target is not None:
            true_origin_pos = self._origin.scenePos()
            true_target_pos = self._target.scenePos()

            # Convert to QPoint (integers) to avoid floating point comparison issues:
            origin_int = origin.toPoint()
            target_int = target.toPoint()
            true_origin_int = true_origin_pos.toPoint()
            true_target_int = true_target_pos.toPoint()

            # If origin matches target and target matches origin, they're swapped:
            if origin_int == true_target_int and target_int == true_origin_int:
                origin, target = target, origin  # Swap to correct order

        self._path.clear()
        self._path = self._compute(origin, target)

        # Position arrow at 50% along the path
        self._arrow.setPos(self._path.pointAtPercent(0.50))

        # Arrow always points in the origin -> target direction
        angle = -self._path.angleAtPercent(0.5)
        self._arrow.setRotation(angle)
        self.update()

    def clear(self):
        self._arrow.setPos(QtCore.QPointF())
        self._path.clear()

    @QtCore.Property(float)
    def thickness(self) -> float:
        return self.property("linewidth")

    @thickness.setter
    def thickness(self, value: float) -> None:
        self.setProperty("linewidth", value)
        self.prepareGeometryChange()
        self.update()
