# Filename: vector.py
# Module name: graph
# Description: Edge item for displaying graph connections.

"""Edge item for displaying graph connections."""

from PySide6 import QtCore, QtGui, QtWidgets
from gui.graph.reusable.image import Image
from gui.graph.flags import ItemState
import dataclasses
import weakref


class VectorItem(QtWidgets.QGraphicsObject):
    """Edge item for displaying graph connections."""

    @dataclasses.dataclass
    class Style:
        """Edge styling options.

        Attributes:
            width: Line width in pixels (default: 2).
            slack: The Bézier curve's slack factor (default: 0.4).
            pen: The vector's pen style.
        """

        width: float = 3.0
        slack: float = 0.4
        pen: dict[ItemState, QtGui.QPen] = dataclasses.field(default_factory=dict)

    def __init__(self, parent=None, origin=None, target=None):
        super().__init__(parent)
        # Class member(s):
        self._path = QtGui.QPainterPath()
        self._arrow = Image(":/svg/arrow.svg", parent=self)
        self._style = VectorItem.Style(
            pen={
                ItemState.State_None: QtGui.QPen(QtGui.QColor(0xBEBEBE)),
                ItemState.State_Selected: QtGui.QPen(QtGui.QColor(0xFFCB00)),
            }
        )

        self._init_attr()
        self._init_anim()
        self._init_endpoints(origin, target)

    def _init_attr(self):

        self.setZValue(-10)
        self.setPos(QtCore.QPointF(0, 0))
        self.setAcceptHoverEvents(True)
        self.setProperty("linewidth", self._style.width)

    def _init_anim(self):
        """Initializes hover animation."""

        self._anim = QtCore.QPropertyAnimation(self, b"thickness")
        self._anim.setEasingCurve(QtCore.QEasingCurve.Type.OutQuad)
        self._anim.setDuration(360)

    def _init_endpoints(self, origin, target):
        """
        Initialize the vector's endpoints.

        Args:
            origin: Reference to the origin vertex.
            target: Reference to the target vertex.
        """
        self._origin = weakref.ref(origin) if origin else None
        self._target = weakref.ref(target) if target else None

        if self._origin and self._target:
            self._origin().item_shifted.connect(self._on_endpoint_shifted)
            self._target().item_shifted.connect(self._on_endpoint_shifted)
            self.update_path(
                self._origin().scenePos(),
                self._target().scenePos(),
            )

    def boundingRect(self) -> QtCore.QRectF:
        return self._path.boundingRect().adjusted(-4, -4, 4, 4)

    def shape(self):
        stroker = QtGui.QPainterPathStroker()
        current_width = self.property("linewidth") or self._style.width
        stroker.setWidth(current_width + 12)
        return stroker.createStroke(self._path)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: QtWidgets.QWidget = ...,
    ) -> None:

        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # First pass: Use a thicker stroke for the border
        pen_border = QtGui.QPen(self._style.pen[ItemState.State_None])
        pen_border.setColor(QtGui.QColor(0x232A2E))
        pen_border.setWidthF(self.property("linewidth") or self._style.width + 1.0)
        painter.setPen(pen_border)
        painter.drawPath(self._path)

        # Second pass: Draw the main stroke on top
        pen = QtGui.QPen(
            self._style.pen[
                ItemState.State_Selected if self.isSelected() else ItemState.State_None
            ]
        )
        pen.setWidthF(self.property("linewidth") or self._style.width)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(self._path)

    def hoverEnterEvent(self, event, /):
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._anim.stop()
        self._anim.setStartValue(self._style.width)
        self._anim.setEndValue(self._style.width + 2.0)
        self._anim.start()

    def hoverLeaveEvent(self, event, /):
        self.unsetCursor()
        self._anim.stop()
        self._anim.setStartValue(self._style.width + 2.0)
        self._anim.setEndValue(self._style.width)
        self._anim.start()

    def _compute(
        self,
        origin: QtCore.QPointF,
        target: QtCore.QPointF,
    ) -> QtGui.QPainterPath:

        path = QtGui.QPainterPath()
        path.moveTo(origin)

        # Calculate control points for cubic Bezier curve
        slack = self._style.slack

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
            true_origin_pos = self._origin().scenePos()
            true_target_pos = self._target().scenePos()

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

    @QtCore.Slot(QtCore.QPointF)
    def _on_endpoint_shifted(self, pos: QtCore.QPointF) -> None:

        if self._origin and self._target:
            origin = self._origin().scenePos()
            target = self._target().scenePos()
            self.update_path(origin, target)

    @QtCore.Property(float)
    def thickness(self) -> float:
        return self.property("linewidth")

    @thickness.setter
    def thickness(self, value: float) -> None:
        self.setProperty("linewidth", value)
        self.prepareGeometryChange()
        self.update()
