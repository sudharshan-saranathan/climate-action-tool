# Filename: canvas.py
# Module name: graph
# Description: Graphics scene for displaying node graphs.

"""
A QGraphicsScene subclass for displaying and editing graphs.
"""

from __future__ import annotations

# Standard
import qtawesome as qta
import logging
import typing
import types
import uuid

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
        self._uid = uuid.uuid4().hex
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
            shortcutVisibleInContextMenu=False,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Undo),
        )
        cxt_menu.addAction(undo_action)

        redo_action = QtGui.QAction(
            "Redo",
            parent=cxt_menu,
            icon=qta.icon("mdi.redo", color="#efefef"),
            toolTip="Redo the last undone action",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=False,
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
            shortcutVisibleInContextMenu=False,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Copy),
        )
        cxt_menu.addAction(copy_action)

        paste_action = QtGui.QAction(
            "Paste",
            parent=cxt_menu,
            icon=qta.icon("mdi.content-paste", color="#efefef"),
            toolTip="Paste items from clipboard",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=False,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Paste),
        )
        cxt_menu.addAction(paste_action)

        delete_action = QtGui.QAction(
            "Delete",
            parent=cxt_menu,
            icon=qta.icon("mdi.delete", color="red"),
            toolTip="Delete selected items",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=False,
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
            shortcutVisibleInContextMenu=False,
            shortcut=QtGui.QKeySequence("Alt+N"),
        )
        node_action.triggered.connect(self._raise_create_node_request)
        obj_menu.addAction(node_action)

        source_action = QtGui.QAction(
            "Source",
            parent=obj_menu,
            icon=qta.icon("mdi.arrow-down-bold"),
            toolTip="Create a new inlet port",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=False,
            shortcut=QtGui.QKeySequence("Alt+I"),
        )
        source_action.triggered.connect(self._raise_create_node_request)
        obj_menu.addAction(source_action)

        sink_action = QtGui.QAction(
            "Sink",
            parent=obj_menu,
            icon=qta.icon("mdi.arrow-up-bold"),
            toolTip="Create a new outlet port",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=False,
            shortcut=QtGui.QKeySequence("Alt+O"),
        )
        sink_action.triggered.connect(self._raise_create_node_request)
        obj_menu.addAction(sink_action)

        return cxt_menu

    def _connect_to_signal_bus(self) -> None:
        """Connect to application-level controller signals."""

        # Connect to the session-manager's signals
        bus = SignalBus()  # Get the singleton instance
        bus.ui.create_node_repr.connect(self.create_node_repr)
        bus.ui.delete_node_repr.connect(self.delete_node_repr)
        bus.ui.create_edge_repr.connect(self.create_edge_repr)
        bus.ui.delete_edge_repr.connect(self.delete_edge_repr)

        # Create a graph instance for this canvas
        bus.data.create_graph.emit(self._uid)

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

            if isinstance(target, NodeRepr) and origin is not target:
                self._raise_create_edge_request(origin.uid, target.uid)

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

    @QtCore.Slot()
    def _raise_create_node_request(self) -> None:

        # Initialize data for the request
        name = "Node"
        data = {
            "x": self._rmb_coordinate.x(),
            "y": self._rmb_coordinate.y(),
        }

        manager = SignalBus()  # Get the singleton instance
        manager.data.create_node_item.emit(self._uid, name, data)

    @QtCore.Slot(str)
    def _raise_delete_node_request(self, nuid: str) -> None:

        manager = SignalBus()  # Get the singleton instance
        manager.data.delete_node_item.emit(self._uid, nuid)

    @QtCore.Slot()
    def _raise_create_edge_request(self, suid: str, tuid: str) -> None:

        # Initialize data for the request
        data = {
            "source_uid": suid,
            "target_uid": tuid,
        }

        manager = SignalBus()  # Get the singleton instance
        manager.data.create_edge_item.emit(self._uid, "Edge", data)

    @QtCore.Slot(str, str)
    def _raise_delete_edge_request(self, euid: str) -> None:

        manager = SignalBus()  # Get the singleton instance
        manager.data.delete_edge_item.emit(self._uid, euid)

    @QtCore.Slot(NodeRepr)
    def _on_activate_preview(self, item: NodeRepr):

        if not isinstance(item, NodeRepr):
            return

        self._preview_on(item)

    # Public methods
    # --------------

    def create_node_repr(
        self, cuid: int, nuid: str, data: dict = None
    ) -> NodeRepr | None:
        """Create a new node representation."""

        # Check if the canvas ID matches
        if self._uid != cuid:
            return None

        # Prepare data for item instantiation
        data = data or {}
        cpos = QtCore.QPointF(data.get("x", 0), data.get("y", 0))

        node = NodeRepr(nuid, pos=cpos)
        self.addItem(node)
        return node

    def create_edge_repr(
        self, cuid: str, euid: str, data: dict = None
    ) -> EdgeRepr | None:
        """Create a new edge representation."""

        if self._uid != cuid:
            return None

        data = data or {}
        source_uid = data.get("source_uid")
        target_uid = data.get("target_uid")

        source = self.find_item_by_uid(source_uid)
        target = self.find_item_by_uid(target_uid)

        if not (source and target):
            return None

        edge = EdgeRepr(euid, origin=source, target=target)
        self.addItem(edge)
        return edge

    def delete_node_repr(self, cuid: str, nuid: str) -> None:
        """Delete a node representation."""

        if self._uid != cuid:
            return

        item = self.find_item_by_uid(nuid)
        if item:
            self.removeItem(item)

    def delete_edge_repr(self, cuid: str, euid: str) -> None:
        """Delete an edge representation."""

        if self._uid != cuid:
            return

        item = self.find_item_by_uid(euid)
        if item:
            self.removeItem(item)

    def find_item_by_uid(self, uid: str) -> QtWidgets.QGraphicsItem | None:
        """Find an item in the canvas by its unique identifier."""

        return next(
            (
                item
                for item in self.items()
                if isinstance(item, (NodeRepr, EdgeRepr)) and item.uid == uid
            ),
            None,
        )
