# Filename: core/graph/node/__init__.py
# Module Name: core/graph/node
# Description: Graphical representation of a graph-node, based on QGraphicsObject


# Standard
import typing

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass


# Climact
from gui.graph.flags import ItemState


class NodeRepr(QtWidgets.QGraphicsObject):

    # Signals:
    item_clicked = QtCore.Signal(QtWidgets.QGraphicsObject)
    item_shifted = QtCore.Signal(QtWidgets.QGraphicsObject)
    item_focused = QtCore.Signal(QtWidgets.QGraphicsObject)

    @dataclass
    class Attrs:
        """Default node attributes.

        Attributes:
            label: The node's default name/label.
            image: The node's default qtawesome icon-name.
            color: The node's default qtawesome color.
        """

        label: str = "Node"
        image: str = "mdi.function-variant"
        color: str = "#efefef"

    @dataclass(frozen=True)
    class Appearance:
        """Default options for the node's appearance.

        Attributes:
            border: The node's border style.
            background: The node's background style.
        """

        border: dict[ItemState, QtGui.QBrush] = field(
            default_factory=lambda: {
                ItemState.State_Enabled: QtGui.QPen(QtGui.QColor(0x232A2E), 1.0),
                ItemState.State_Selected: QtGui.QPen(QtGui.QColor(0xFFCB00), 1.0),
                ItemState.State_MouseOver: QtGui.QPen(QtGui.QColor(0x232A2E), 1.0),
            }
        )

        background: dict[ItemState, QtGui.QBrush] = field(
            default_factory=lambda: {
                ItemState.State_Enabled: QtGui.QBrush(QtGui.QColor(0x232A2E)),
                ItemState.State_Selected: QtGui.QBrush(QtGui.QColor(0xFFCB00)),
                ItemState.State_MouseOver: QtGui.QBrush(QtGui.QColor(0x232A2E)),
            }
        )

    @dataclass(frozen=True)
    class Geometric:
        """Default geometric options.

        Attributes:
            border_radius: Radius of the node's rounded corners.
            padding: The node's default padding.
            dimensions: The node's default dimensions when created (fixed).
        """

        border_radius: int = 4
        padding: int = 4
        dimensions: QtCore.QRectF = field(
            default_factory=lambda: QtCore.QRectF(-16, -16, 32, 32)
        )

    @dataclass(frozen=True)
    class Connections:
        """Dictionaries to store the node's connections.

        Attributes:
            incoming: The node's incoming connections.
            outgoing: The node's outgoing connections.
        """

        incoming: dict[object, object] = field(default_factory=dict)
        outgoing: dict[object, object] = field(default_factory=dict)

    def __init__(self, parent: QtWidgets.QGraphicsObject = None, **kwargs) -> None:

        # Instantiate dataclasses before super().__init__()
        self._geometry = NodeRepr.Geometric()
        self._attributes = NodeRepr.Attrs()
        self._appearance = NodeRepr.Appearance()
        self._connections = NodeRepr.Connections()

        # Initialize super-class with appropriate data
        super().__init__(parent, pos=kwargs.pop("pos", QtCore.QPointF()), z=0)

        # Toggle interactivity
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        # UI child elements
        self._init_image()
        self._init_label()

    def boundingRect(self):
        return self._geometry.dimensions.adjusted(
            self._geometry.padding,
            self._geometry.padding,
            self._geometry.padding,
            self._geometry.padding,
        )

    def paint(self, painter, option, /, widget=...):

        pen_dict = self._appearance.border
        brs_dict = self._appearance.background

        if option.state & ItemState.State_Selected:
            painter.setPen(pen_dict[ItemState.State_Selected])
            painter.setBrush(brs_dict[ItemState.State_Selected])

        else:
            painter.setPen(pen_dict[ItemState.State_Enabled])
            painter.setBrush(brs_dict[ItemState.State_Enabled])

        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        painter.drawRoundedRect(
            self._geometry.dimensions,
            self._geometry.border_radius,
            self._geometry.border_radius,
        )

        pass

    def _init_image(self):

        from gui.graph.reusable.icon import QtaItem

        icon = QtaItem(
            self._attributes.image,
            width=16,
            color=self._attributes.color,
            parent=self,
        )

    def _init_label(self):

        pass
