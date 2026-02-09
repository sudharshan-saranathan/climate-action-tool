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

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact
from gui.graph.node import NodeRepr
from gui.graph.edge.vector import VectorItem
from core.actions import ActionsManager, CreateAction, DeleteAction, BatchActions
from core.graph import GraphCtrl


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

        # Backend graph controller for this scene
        self._graph = GraphCtrl()

        # Member(s):
        self._rmb_coordinate = QtCore.QPoint()
        self._menu = self._init_menu()
        self._prev = types.SimpleNamespace(
            active=False,
            origin=None,
            vector=VectorItem(None),
        )
        self.addItem(self._prev.vector)

        # Undo/redo manager
        self._actions_manager = ActionsManager()

        # Connect to application signals
        self._init_controllers()

    def _init_menu(self) -> QtWidgets.QMenu:
        """
        Initialize the context menu with graph editing actions.

        Returns:
            A configured QMenu ready for display on right-click.
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
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Undo),
        )
        undo_action.triggered.connect(self.undo)
        cxt_menu.addAction(undo_action)

        redo_action = QtGui.QAction(
            "Redo",
            parent=cxt_menu,
            icon=qta.icon("mdi.redo", color="#efefef"),
            toolTip="Redo the last undone action",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Redo),
        )
        redo_action.triggered.connect(self.redo)
        cxt_menu.addAction(redo_action)
        cxt_menu.addSeparator()

        # Copy/Paste/Delete operations
        copy_action = QtGui.QAction(
            "Copy",
            parent=cxt_menu,
            icon=qta.icon("mdi.content-copy", color="#efefef"),
            toolTip="Copy selected items",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Copy),
        )
        copy_action.triggered.connect(self.clone_items)
        cxt_menu.addAction(copy_action)

        paste_action = QtGui.QAction(
            "Paste",
            parent=cxt_menu,
            icon=qta.icon("mdi.content-paste", color="#efefef"),
            toolTip="Paste items from clipboard",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Paste),
        )
        paste_action.triggered.connect(self.paste_items)
        cxt_menu.addAction(paste_action)

        delete_action = QtGui.QAction(
            "Delete",
            parent=cxt_menu,
            icon=qta.icon("mdi.delete", color="red"),
            toolTip="Delete selected items",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Delete),
        )
        delete_action.triggered.connect(self.delete_items)
        cxt_menu.addAction(delete_action)
        cxt_menu.addSeparator()

        # Create submenu actions
        node_action = QtGui.QAction(
            "Node",
            parent=obj_menu,
            icon=qta.icon("ph.browser-fill", color="darkcyan"),
            toolTip="Create a new node",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence("Alt+N"),
        )
        node_action.triggered.connect(lambda: self._raise_create_request("node"))
        obj_menu.addAction(node_action)

        source_action = QtGui.QAction(
            "Source",
            parent=obj_menu,
            icon=qta.icon("mdi.arrow-down-bold"),
            toolTip="Create a new inlet port",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence("Alt+I"),
        )
        source_action.triggered.connect(lambda: self._raise_create_request("node"))
        obj_menu.addAction(source_action)

        sink_action = QtGui.QAction(
            "Sink",
            parent=obj_menu,
            icon=qta.icon("mdi.arrow-up-bold"),
            toolTip="Create a new outlet port",
            iconVisibleInMenu=True,
            shortcutVisibleInContextMenu=True,
            shortcut=QtGui.QKeySequence("Alt+O"),
        )
        sink_action.triggered.connect(lambda: self._raise_create_request("node"))
        obj_menu.addAction(sink_action)

        return cxt_menu

    def _init_controllers(self) -> None:
        """Connect to application-level scene signals."""

        app = QtWidgets.QApplication.instance()
        grc = getattr(app, "graph_ctrl", None)
        scc = getattr(app, "scene_ctrl", None)

        if scc is not None:
            scc.create_repr.connect(self.create_item)

        self._ctrl = grc

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        """
        Display the context menu at the location of the right-click event.

        Args:
            event: The context menu event containing screen position.
        """

        super().contextMenuEvent(event)
        if event.isAccepted():
            return

        self._rmb_coordinate = event.scenePos()
        self._menu.exec_(event.screenPos())

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        if self._prev.active:
            # Use stored click position from origin vertex

            origin = self._prev.origin.scenePos()
            target = event.scenePos()
            self._prev.vector.update_path(origin, target)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        if self._prev.active:

            origin = self._prev.origin
            target = self.itemAt(event.scenePos(), QtGui.QTransform())

            if (
                isinstance(target, NodeRepr)
                and hasattr(origin, "connect_to")
                and target is not origin
            ):

                vector = origin.connect_to(target)
                if vector is not None:
                    self.addItem(vector)
                    self._actions_manager.do(CreateAction(self, vector))

        self.prev_off()
        super().mouseReleaseEvent(event)

    def prev_on(self, vertex: QtWidgets.QGraphicsObject):

        if self._prev.active:
            return  # Do nothing if the preview is already active.

        self._prev.active = True
        self._prev.origin = vertex
        self._prev.vector.show()

    def prev_off(self):
        self._prev.active = False
        self._prev.origin = None
        self._prev.vector.clear()
        self._prev.vector.hide()

    def create_item(
        self,
        name: typing.Literal["node", "edge"],
        data: dict | None = None,
    ) -> QtWidgets.QGraphicsItem | None:
        """
        Create and return a graph item of the specified class.
        :param name: Item class name
        :param data: Optional dict with keyword arguments like 'cpos'
        :return: The newly created item, or None if an error occurred.
        """

        # Map class-names to the respective class objects
        item_classes = {
            "node": NodeRepr,
            "edge": VectorItem,
        }

        # Parse keyword-arguments
        data = data or {}
        cpos = data.get("cpos", self._rmb_coordinate)

        # Get the item's class object from the class name
        item_class = item_classes.get(name, None)

        # If the class is valid, instantiate and add the item to the scene:
        if item_class:
            item = item_class(pos=cpos)
            self.register_signals(item)
            self.addItem(item)
            self._actions_manager.do(CreateAction(self, item))
            return item

        return None

    def find_item(self, name: str) -> QtWidgets.QGraphicsItem | None:
        """Find an item in the canvas by its object name."""

        items: list[QtWidgets.QGraphicsItem] = self.items()
        for item in items:

            object_name = getattr(item, "objectName", None)
            if callable(object_name) and object_name() == name:
                return item

        return None

    def register_signals(self, item: NodeRepr):
        """Connects the given item's signals to appropriate slots."""


        signals = getattr(item, "signals", None)

        if callable(signals):

            sig_list = typing.cast(dict, signals())

            for sig_name, sig_instance in sig_list.items():
                
                method_name = f"_on_{sig_name}"
                if hasattr(self, method_name):
                    sig_instance.connect(
                        getattr(self, method_name),
                        QtCore.Qt.ConnectionType.QueuedConnection,
                    )





        if hasattr(item, "signals") and callable(getattr(item, "signals")):
            sig_list = item.signals()

            for name, signal in sig_list.items():
                method = f"_on_{name}"
                if hasattr(self, method):
                    signal.connect(
                        getattr(self, method), QtCore.Qt.ConnectionType.QueuedConnection
                    )

        else:
            logging.warning(f"Item {item} has no signals defined.")

    @QtCore.Slot(object)
    def _raise_create_request(self, key: typing.Literal["node", "edge"]) -> None:

        if self._ctrl is not None:
            self._ctrl.create_item.emit(key, {"pos": self._rmb_coordinate})

    @QtCore.Slot(object)
    def _raise_delete_request(self, key: str) -> None:

        app = QtWidgets.QApplication.instance()
        graph_ctrl = getattr(app, "graph_ctrl", None) if app else None
        if graph_ctrl is not None:
            graph_ctrl.delete_item.emit(key)

    @QtCore.Slot(QtWidgets.QGraphicsObject)
    def _on_item_clicked(self, item: QtWidgets.QGraphicsObject):

        if not isinstance(item, NodeRepr):
            return

        self.prev_on(item)

    # -------------------------------------------------------------------------
    # Undo/Redo
    # -------------------------------------------------------------------------

    def undo(self) -> None:
        """Undo the most recent action."""
        self._actions_manager.undo()

    def redo(self) -> None:
        """Redo the most recently undone action."""
        self._actions_manager.redo()

    # -------------------------------------------------------------------------
    # Copy/Paste
    # -------------------------------------------------------------------------

    def clone_items(self) -> None:
        """Clone selected items, preserving connections between them."""

        Canvas.clipboard = [
            item
            for item in self.selectedItems()
            if getattr(item, "_allow_cloning", False)
        ]

    def paste_items(self) -> None:
        """Paste items from the clipboard into the scene."""

        if not Canvas.clipboard:
            return

        Canvas._register.clear()
        batch = BatchActions()

        # First pass: Clone and add items in the clipboard
        for item in Canvas.clipboard:

            clone_method = getattr(item, "clone", None)
            if clone_method is not None and callable(clone_method):
                
                clone = typing.cast(QtWidgets.QGraphicsObject, clone_method())
                clone.setSelected(True)
                item.setSelected(False)

                Canvas._register[item] = clone
                if isinstance(clone, NodeRepr):
                    self.register_signals(clone)
                self.addItem(clone)
                batch.add_to_batch(CreateAction(self, clone))

        # Second pass: Recreate connections between cloned items
        for vertex, clone in Canvas._register.items():
            for conjugate in vertex.importers():

                target = Canvas._register.get(conjugate, None)
                vector = clone.connect_to(target)
                if vector is not None:
                    self.addItem(vector)
                    batch.add_to_batch(CreateAction(self, vector))

        self._actions_manager.do(batch)

    def delete_items(self) -> None:
        """Delete selected items from the scene."""

        selected = self.selectedItems()
        if not selected:
            return

        batch = BatchActions()
        for item in selected:
            if isinstance(item, NodeRepr):
                batch.add_to_batch(DeleteAction(self, item))

        self._actions_manager.do(batch)
