# Filename: vertex.py
# Module name: graph
# Description: Vertex graphics item for node graphs.

from PySide6 import QtGui, QtCore, QtWidgets
from gui.graph.vector.vector import VectorItem
from gui.graph.reusable.text import Label
from gui.graph.enums import ItemState
import dataclasses
import qtawesome as qta


class VertexItem(QtWidgets.QGraphicsObject):

    # Signals:
    item_clicked = QtCore.Signal(QtWidgets.QGraphicsObject)
    item_shifted = QtCore.Signal(QtWidgets.QGraphicsObject)
    item_focused = QtCore.Signal(QtWidgets.QGraphicsObject)

    @dataclasses.dataclass(frozen=True)
    class Style:
        """Style attributes."""

        image: str = "mdi.function-variant"
        brush: dict[ItemState, QtGui.QBrush] = dataclasses.field(
            default_factory=lambda: {
                ItemState.NORMAL: QtGui.QBrush(QtGui.QColor(0x232A2E)),
                ItemState.SELECTED: QtGui.QBrush(QtGui.QColor(0xFFCB00)),
            }
        )

    @dataclasses.dataclass(frozen=True)
    class Geometry:
        """Geometric attributes."""

        rect: QtCore.QRectF = dataclasses.field(default_factory=QtCore.QRectF)
        bezel: int = 4
        radius: int = 4

    @dataclasses.dataclass(frozen=True)
    class Connections:
        """Database for incoming and outgoing connections."""

        incoming: dict[VertexItem, VectorItem] = dataclasses.field(default_factory=dict)
        outgoing: dict[VertexItem, VectorItem] = dataclasses.field(default_factory=dict)

    # Class constructor
    def __init__(self, parent=None, **kwargs):

        self._name = kwargs.pop("name", "Vertex")
        self._kind = kwargs.pop("kind", None)

        # Super-class initialization
        super().__init__(
            parent,
            pos=kwargs.get("pos", QtCore.QPointF()),
        )

        self._init_flags()
        self._init_attrs()

        # Label for displaying the vertex's name:
        self._label = Label(
            self._name,
            parent=self,
            width=120,
            align=QtCore.Qt.AlignmentFlag.AlignCenter,
            pos=QtCore.QPointF(-60, 18),
        )
        self._label.sig_text_changed.connect(self.setObjectName)
        self._label.sig_text_changed.emit(self._name)

    def _init_flags(self):
        """Initialize this item's flags."""

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges
        )

    def _init_attrs(self):
        """Instantiate the vertex's data classes."""

        # Style, geometry, and connections:
        self._style = VertexItem.Style(
            brush={
                ItemState.NORMAL: QtGui.QBrush(QtGui.QColor(0x232A2E)),
                ItemState.SELECTED: QtGui.QBrush(QtGui.QColor(0xFFCB00)),
            }
        )
        self._geometry = VertexItem.Geometry(rect=QtCore.QRectF(-16, -16, 32, 32))
        self._connections = VertexItem.Connections()

    def boundingRect(self) -> QtCore.QRectF:
        return self._geometry.rect.adjusted(
            -self._geometry.bezel,
            -self._geometry.bezel,
            self._geometry.bezel,
            self._geometry.bezel,
        )

    def paint(self, painter, option, widget=None):
        """Paint the vertex."""

        brush = self._style.brush[
            ItemState.SELECTED if self.isSelected() else ItemState.NORMAL
        ]

        # Draw the background rectangle first
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(brush)
        painter.drawRoundedRect(
            self.boundingRect(),
            self._geometry.radius,
            self._geometry.radius,
        )

        # Then paint the icon on top
        color = "black" if self.isSelected() else "white"
        image = qta.icon(self._style.image, color=color)
        image.paint(
            painter,
            self.boundingRect().adjusted(8, 8, -8, -8).toRect(),
        )

    def itemChange(self, change, value):

        if (
            change
            == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemScenePositionHasChanged
        ):
            self.item_shifted.emit(self)

        return super().itemChange(change, value)

    def mousePressEvent(self, event):

        if event.modifiers() == QtCore.Qt.KeyboardModifier.AltModifier:
            self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            self.item_clicked.emit(self)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events.

        Args:
            event: The mouse release event, internally managed by Qt.
        """
        super().setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        """Handle double-click events.

        Args:
            event: The mouse double-click event, internally managed by Qt.
        """

        # Required:
        from core.bus import EventsBus

        bus = EventsBus.instance()
        bus.sig_item_focused.emit(self)

    def signals(self) -> dict[str, QtCore.SignalInstance]:
        """Return dictionary of signals for dynamic connection."""

        return {
            "item_clicked": self.item_clicked,
            "item_shifted": self.item_shifted,
        }

    def connect_to(
        self,
        node: VertexItem,
    ) -> VectorItem | None:
        """
        Connect this vertex to another.

        Args:
            node: The target vertex to connect to.
        """

        if node in self._connections.outgoing:
            print(f"{self.objectName()} is already connected to {node.objectName()}")
            return None

        def _get_offset():
            xo = self.scenePos().x()
            xt = node.scenePos().x()
            return -8 if xo < xt else 8

        vector = VectorItem(
            None,
            origin=self,
            target=node,
        )

        vector.moveBy(0, _get_offset())
        self._connections.outgoing[node] = vector
        node._connections.incoming[self] = vector

        return vector
