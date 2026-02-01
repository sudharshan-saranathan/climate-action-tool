# Filename: vertex.py
# Module name: graph
# Description: Vertex graphics item for node graphs.

from PySide6 import QtGui, QtCore, QtWidgets
from gui.graph.vertex.config import VertexConfig
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

    @dataclasses.dataclass
    class Attrs:
        """Vertex attributes."""

        label: str = "Vertex"
        image: str = "mdi.function-variant"
        color: str = "#efefef"

    @dataclasses.dataclass(frozen=True)
    class Style:
        """Style attributes."""

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

        self._attr = VertexItem.Attrs(
            label=kwargs.get("label", VertexItem.Attrs.label),
            image=kwargs.get("image", VertexItem.Attrs.image),
            color=kwargs.get("color", VertexItem.Attrs.color),
        )

        # Super-class initialization
        super().__init__(
            parent,
            pos=kwargs.get("pos", QtCore.QPointF()),
        )

        self._init_flags()
        self._init_attrs()
        self._init_label()

        self._allow_cloning: bool = kwargs.get("allow_cloning", True)
        self._outgoing_enabled: bool = kwargs.get("outgoing_enabled", True)
        self._incoming_enabled: bool = kwargs.get("incoming_enabled", True)

        # Configuration widget:
        self._config = VertexConfig()

    def _init_flags(self):
        """Initialize this item's flags."""

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges
        )
        self.setAcceptHoverEvents(True)

    def _init_attrs(self):
        """Instantiate the vertex's data classes."""

        self._style = VertexItem.Style(
            brush={
                ItemState.NORMAL: QtGui.QBrush(QtGui.QColor(0x232A2E)),
                ItemState.SELECTED: QtGui.QBrush(QtGui.QColor(0xFFCB00)),
            },
        )
        self._geometry = VertexItem.Geometry(rect=QtCore.QRectF(-16, -16, 32, 32))
        self._connections = VertexItem.Connections()

    def _init_label(self):
        """Initialize the vertex's label."""

        self._label = Label(
            self._attr.label,
            parent=self,
            width=120,
            align=QtCore.Qt.AlignmentFlag.AlignCenter,
            pos=QtCore.QPointF(-60, 18),
        )
        self._label.sig_text_changed.connect(self.rename)

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

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(brush)
        painter.drawRoundedRect(
            self.boundingRect(),
            self._geometry.radius,
            self._geometry.radius,
        )

        # Then paint the icon on top
        icon = qta.icon(self._attr.image, color=self._attr.color)
        icon.paint(
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
        event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events.

        Args:
            event: The mouse release event, internally managed by Qt.
        """
        super().setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        super().mouseReleaseEvent(event)

        event.accept()

    def mouseDoubleClickEvent(self, event):
        """Handle double-click events.

        Args:
            event: The mouse double-click event, internally managed by Qt.
        """

        # Required:
        from core.bus import EventsBus

        bus = EventsBus.instance()
        bus.sig_item_focused.emit(self)

        code = self._config.open()

    def hoverEnterEvent(self, event):
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        event.accept()

    def hoverLeaveEvent(self, event):
        self.unsetCursor()
        event.accept()

    # Public methods

    def signals(self) -> dict[str, QtCore.SignalInstance]:
        """Return dictionary of signals for dynamic connection."""

        return {
            "item_clicked": self.item_clicked,
            "item_shifted": self.item_shifted,
        }

    def connect_to(self, node: VertexItem) -> VectorItem | None:
        """
        Connect this vertex to another.

        Args:
            node: The target vertex to connect to.
        """

        if (
            not node  # Filters out None values
            or not self._outgoing_enabled  # If outgoing from this vertex is disabled
            or not node._incoming_enabled  # If the node's incoming connections are disabled
            or node in self._connections.outgoing.keys()  # Existing connection
        ):
            return None

        # Add an offset to the connection
        def _get_offset():
            xo = self.scenePos().x()
            xt = node.scenePos().x()
            return -8 if xo < xt else 8

        # Instantiate the connection
        vector = VectorItem(
            None,
            origin=self,
            target=node,
        )
        vector.moveBy(0, _get_offset())

        self._connections.outgoing[node] = vector
        node._connections.incoming[self] = vector
        return vector

    def set_icon(self, image: str, color: str = "#efefef"):
        """Set the vertex icon."""

        self._attr.image = image
        self._attr.color = color

    def clone(self, offset: QtCore.QPointF = QtCore.QPointF(25, 25)) -> VertexItem:
        """
        Create a duplicate of this vertex.

        Args:
            offset: Position offset for the clone. Defaults to (25, 25).

        Returns:
            A new VertexItem with the same attributes.
        """

        clone = VertexItem(
            pos=self.scenePos() + offset,
            label=self._attr.label,
            image=self._attr.image,
            color=self._attr.color,
            outgoing_enabled=self._outgoing_enabled,
            incoming_enabled=self._incoming_enabled,
        )

        return clone

    def rename(self, text: str):
        """Rename the vertex."""

        self._attr.label = text
        self.setObjectName(text)

    def importers(self) -> set[VertexItem]:
        """The set of vertices that import from this vertex."""
        return set([vertex for vertex in self._connections.outgoing.keys()])

    def exporters(self):
        """The set of vertices that export to this vertex."""
        return set([vertex for vertex in self._connections.incoming.keys()])
