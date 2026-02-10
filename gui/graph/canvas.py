# Filename: canvas.py
# Module name: graph
# Description: Graphics scene for displaying node graphs.

"""
A QGraphicsScene subclass for displaying and editing graphs.
"""

from __future__ import annotations

from idlelib.run import manage_socket

# Standard
import qtawesome as qta
import logging
import typing
import types

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact
from gui.graph.node import NodeRepr
from gui.graph.edge import EdgeRepr
from core.signals import SignalBus


# Dataclass
from dataclasses import field
from dataclasses import dataclass


class Canvas(QtWidgets.QGraphicsScene):
    """
    A QGraphicsScene subclass for displaying and editing graphs.

    Key attributes:
        - clipboard: A class-level cross-canvas clipboard for copy-paste operations.
    """

    # Class-level clipboard for cross-canvas copy-paste
    representations: typing.ClassVar[dict[str, type]] = {
        "NodeRepr": NodeRepr,
        "EdgeRepr": EdgeRepr,
    }

    clipboard: list[QtWidgets.QGraphicsItem] = []
    _register: dict = {}

    @dataclass
    class Appearance:
        brush: QtGui.QBrush = field(default_factory=QtGui.QBrush)

    @dataclass
    class Geometry:
        bounds: QtCore.QRectF = field(default_factory=QtCore.QRectF)

    def __init__(self, parent=None):
        """
        Initialize the graphics scene.
        """

        # Instantiate options before super-class:
        self._geometry = Canvas.Geometry(bounds=QtCore.QRectF(0, 0, 5000, 5000))
        self._style = Canvas.Appearance(
            brush=QtGui.QBrush(
                QtGui.QColor("#ffffff"),
                QtCore.Qt.BrushStyle.SolidPattern,
            ),
        )

        # Super-class initialization:
        super().__init__(
            self._geometry.bounds,
            parent=parent,
            backgroundBrush=self._style.brush,
        )

        # Members
        self._rmb_coordinate = QtCore.QPoint()
        self._menu = self._init_menu()
        self._preview = types.SimpleNamespace(
            active=False,
            origin=None,
            vector=EdgeRepr(None),
        )
        self.addItem(self._preview.vector)

        # Connect to application signals
        self._connect_to_signal_bus()

    def _init_menu(self) -> QtWidgets.QMenu:
        """
        Initialize the context menu with graph editing actions.
        """

        cxt_menu = QtWidgets.QMenu()
        obj_menu = cxt_menu.addMenu(qta.icon("mdi.plus", color="cyan"), "Create")

        # Undo/Redo operations
        undo_action = QtGui.QAction(
            "Undo",
            parent=cxt_menu,
            icon=qta.icon("mdi.undo", color="#efefef"),
            toolTip="Undo the last action",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Undo),
        )
        cxt_menu.addAction(undo_action)

        redo_action = QtGui.QAction(
            "Redo",
            parent=cxt_menu,
            icon=qta.icon("mdi.redo", color="#efefef"),
            toolTip="Redo the last undone action",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Redo),
        )
        cxt_menu.addAction(redo_action)
        cxt_menu.addSeparator()

        # Copy/Paste/Delete operations
        copy_action = QtGui.QAction(
            "Copy",
            parent=cxt_menu,
            icon=qta.icon("mdi.content-copy", color="#efefef"),
            toolTip="Copy selected items",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Copy),
        )
        cxt_menu.addAction(copy_action)

        paste_action = QtGui.QAction(
            "Paste",
            parent=cxt_menu,
            icon=qta.icon("mdi.content-paste", color="#efefef"),
            toolTip="Paste items from clipboard",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Paste),
        )
        cxt_menu.addAction(paste_action)

        delete_action = QtGui.QAction(
            "Delete",
            parent=cxt_menu,
            icon=qta.icon("mdi.delete", color="red"),
            toolTip="Delete selected items",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Delete),
        )
        cxt_menu.addAction(delete_action)
        cxt_menu.addSeparator()

        # Create submenu actions
        node_action = QtGui.QAction(
            "Node",
            parent=obj_menu,
            icon=qta.icon("ph.browser-fill", color="darkcyan"),
            toolTip="Create a new node",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence("Alt+N"),
        )
        node_action.triggered.connect(lambda: self._raise_create_request("NodeRepr"))
        obj_menu.addAction(node_action)

        source_action = QtGui.QAction(
            "Source",
            parent=obj_menu,
            icon=qta.icon("mdi.arrow-down-bold"),
            toolTip="Create a new inlet port",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence("Alt+I"),
        )
        source_action.triggered.connect(lambda: self._raise_create_request("NodeRepr"))
        obj_menu.addAction(source_action)

        sink_action = QtGui.QAction(
            "Sink",
            parent=obj_menu,
            icon=qta.icon("mdi.arrow-up-bold"),
            toolTip="Create a new outlet port",
            iconVisibleInMenu=True,
            shortcut=QtGui.QKeySequence("Alt+O"),
        )
        sink_action.triggered.connect(lambda: self._raise_create_request("NodeRepr"))
        obj_menu.addAction(sink_action)

        return cxt_menu

    def _connect_to_signal_bus(self) -> None:
        """Connect to application-level controller signals."""

        # Connect to the session-manager's signals
        bus = SignalBus()  # Get the singleton instance
        bus.ui.create_node_repr.connect(self.create_node_repr)
        bus.ui.delete_node_repr.connect(self.delete_node_repr)

        # Create a graph instance for this canvas
        bus.data.create_graph.emit(id(self))

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        """
        Display the context menu at the location of the right-click event.
        :param event: The right-click event, forwarded by Qt.
        """

        super().contextMenuEvent(event)
        if event.isAccepted():
            return

        self._rmb_coordinate = event.scenePos()
        self._menu.exec_(event.screenPos())

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        if self._preview.active:
            # Use stored click position from origin vertex

            origin = self._preview.origin.scenePos()
            target = event.scenePos()
            self._preview.vector.update_path(origin, target)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        if self._preview.active:

            origin = self._preview.origin
            target = self.itemAt(event.scenePos(), QtGui.QTransform())

            if (
                isinstance(target, NodeRepr)
                and hasattr(origin, "connect_to")
                and target is not origin
            ):
                origin.connect_to(target)

        self._preview_off()
        super().mouseReleaseEvent(event)

    def addItem(
        self,
        item: QtWidgets.QGraphicsItem,
    ) -> None:

        if isinstance(item, NodeRepr):
            self._register_item_signals(item)

        super().addItem(item)

    def _preview_on(self, vertex: QtWidgets.QGraphicsObject):

        if self._preview.active:
            return  # Do nothing if the preview is already active.

        self._preview.active = True
        self._preview.origin = vertex
        self._preview.vector.show()

    def _preview_off(self):
        self._preview.active = False
        self._preview.origin = None
        self._preview.vector.clear()
        self._preview.vector.hide()

    def _register_item_signals(self, item: QtWidgets.QGraphicsObject):
        """Connects the item's signals to appropriate slots."""

        if callable(signals := getattr(item, "signals", None)):

            sig_dictionary = typing.cast(dict, signals())
            for name, instance in sig_dictionary.items():
                if method := getattr(self, f"_on_{name}", None):
                    instance.connect(method, QtCore.Qt.ConnectionType.QueuedConnection)

        else:
            logging.warning(f"Item {item} has no signals defined.")

    @QtCore.Slot(str)
    def _raise_create_request(self, key: str) -> None:

        # Initialize data for the request
        name = "Node" if key == "NodeRepr" else "Edge"
        data = {
            "x": self._rmb_coordinate.x(),
            "y": self._rmb_coordinate.y(),
        }

        manager = SignalBus()  # Get the singleton instance
        manager.data.create_node_item.emit(id(self), name, data)

    @QtCore.Slot(str)
    def _raise_delete_request(self, key: str) -> None:

        manager = SignalBus()  # Get the singleton instance
        manager.data.delete_node_item.emit(key)

    @QtCore.Slot(NodeRepr)
    def _on_activate_preview(self, item: NodeRepr):

        if not isinstance(item, NodeRepr):
            return

        self._preview_on(item)

    # Public methods
    # --------------

    def create_node_repr(self, uid: str, data: dict = None) -> NodeRepr | None:
        """Create a new node representation."""

        # Prepare data for item instantiation
        data = data or {}
        cpos = QtCore.QPointF(data.get("x", 0), data.get("y", 0))

        node = NodeRepr(uid=uid, pos=cpos)
        self.addItem(node)
        return node

    def delete_node_repr(self, uid: str, data: dict = None) -> None:
        """Delete a node representation."""

        item = self.find_item_by_uid(uid)
        if item:
            self.removeItem(item)

    def find_item_by_name(self, name: str) -> QtWidgets.QGraphicsItem | None:
        """Find an item in the canvas by its object name."""

        items: list[QtWidgets.QGraphicsItem] = self.items()
        for item in items:

            object_name = getattr(item, "objectName", None)
            if callable(object_name) and object_name() == name:
                return item

        return None

    def find_item_by_uid(self, uid: str) -> QtWidgets.QGraphicsItem | None:
        """Find an item in the canvas by its unique identifier."""

        return next(
            (
                item
                for item in self.items()
                if isinstance(item, QtWidgets.QGraphicsObject)
                and item.objectName() == uid
            ),
            None,
        )
