# Filename: core/graph/node/__init__.py
# Module Name: core/graph/node
# Description: QGraphicsObject-based graphical representation of a graph-node.


from __future__ import annotations

# Standard
import logging

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from core.signals import SignalBus

ItemState = QtWidgets.QStyle.StateFlag


class NodeRepr(QtWidgets.QGraphicsObject):

    # Class logger
    _logger = logging.getLogger("NodeRepr")

    # Signals:
    activate_preview = QtCore.Signal(QtWidgets.QGraphicsObject)
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

        border: dict[ItemState, QtGui.QPen] = field(
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

    # Constructor
    def __init__(
        self,
        nuid: str,
        parent: QtWidgets.QGraphicsObject | None = None,
        **kwargs,
    ) -> None:

        # Instantiate dataclasses before super().__init__()
        self._uid = nuid
        self._geometry = NodeRepr.Geometric()
        self._attributes = NodeRepr.Attrs()
        self._appearance = NodeRepr.Appearance()
        self._connections = NodeRepr.Connections()

        # Initialize super-class with appropriate data
        super().__init__(parent, pos=kwargs.pop("pos", QtCore.QPointF()), z=0)

        # Toggle flags
        graphics_item_flag = QtWidgets.QGraphicsItem.GraphicsItemFlag
        self.setFlag(graphics_item_flag.ItemIsMovable)
        self.setFlag(graphics_item_flag.ItemIsSelectable)
        self.setFlag(graphics_item_flag.ItemSendsScenePositionChanges)

        # UI child elements
        self._init_image()
        self._init_label()

        # Config dialog (lazy init)
        self._config_dialog = None

        # Get the signal bus instance
        self._signal_bus = SignalBus()
        self._connect_to_signal_bus()

    def _init_image(self):

        # QtAwesome Icon
        from qtawesome import icon as qta_icon

        self._node_icon = qta_icon(
            self._attributes.image,
            color=self._attributes.color,
            color_active="black",
        )

    def _init_label(self):

        # Import `Label` from gui.graph.reusable
        from gui.graph.reusable.label import Label

        # TODO: Find a better way to locate the situate the label w.r.t the node.
        label = Label(
            self._attributes.label,
            parent=self,
            width=120,
            align=QtCore.Qt.AlignmentFlag.AlignCenter,
            pos=QtCore.QPointF(-60, 18),
        )

        label.sig_text_changed.connect(self.setObjectName)
        self.objectNameChanged.connect(lambda text: label.setPlainText(text))
        self.objectNameChanged.connect(
            lambda text: print(f"Node name changed to {text}")
        )

    def _connect_to_signal_bus(self) -> None:

        self._signal_bus.ui.publish_node_data.connect(self._on_publish_node_data)

    # Section: Reimplementation
    # -------------------------

    def boundingRect(self):
        return self._geometry.dimensions.adjusted(
            -self._geometry.padding,
            -self._geometry.padding,
            self._geometry.padding,
            self._geometry.padding,
        )

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        /,
        widget: QtWidgets.QWidget | None = None,
    ) -> None:

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

        # If an icon is available, paint it on top
        from qtawesome import icon as qta_icon

        color = "black" if self.isSelected() else self._attributes.color
        qta_icon(self._attributes.image, color=color).paint(
            painter,
            self.boundingRect().adjusted(8, 8, -8, -8).toRect(),
        )

    def itemChange(self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value):

        graphics_item_change = QtWidgets.QGraphicsItem.GraphicsItemChange
        if change == graphics_item_change.ItemScenePositionHasChanged:
            self.item_shifted.emit(self)

        return super().itemChange(change, value)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        mbt = event.button()
        mod = event.modifiers()

        if (
            mbt == QtCore.Qt.MouseButton.LeftButton
            and mod == QtCore.Qt.KeyboardModifier.AltModifier
        ):
            self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            self.activate_preview.emit(self)
            return

        super().mousePressEvent(event)
        if event.isAccepted():
            return

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        super().mouseReleaseEvent(event)
        if event.isAccepted():
            return

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        # Request node data from backend
        cuid = getattr(self.scene(), "uid", None)
        if cuid:
            self._signal_bus.raise_request(
                "send_node_data",
                cuid,
                self.uid,
            )
        else:
            self._logger.warning(f"Canvas UID not found for node!")

        # Show the config dialog
        from gui.graph.node.config import NodeConfig

        if self._config_dialog is None:
            self._config_dialog = NodeConfig()

        self._config_dialog.set_label_text(self._attributes.label)
        self._config_dialog.show()
        self._config_dialog.raise_()

    # Callback(s)

    @QtCore.Slot(str, str)
    def _on_publish_node_data(self, nuid: str, jstr: str) -> None:

        if nuid != self._uid:
            return

        self._logger.info(f"Received data for node:\n{jstr}")

    # Section: Public methods
    # -----------------------

    def signals(self) -> dict[str, QtCore.SignalInstance]:
        return {
            "activate_preview": self.activate_preview,
            "item_shifted": self.item_shifted,
            "item_focused": self.item_focused,
        }

    # Properties
    # ----------

    @property
    def uid(self) -> str:
        return self._uid
