# Filename: canvas.py
# Module name: graph
# Description: Graphics scene for displaying node graphs.

"""
A QGraphicsScene subclass for displaying and editing graphs.
"""

from __future__ import annotations
from PySide6 import QtGui, QtCore, QtWidgets
from gui.graph.vertex.vertex import VertexItem
from gui.graph.vector.vector import VectorItem
from core.actions import ActionsManager, CreateAction, DeleteAction, BatchActions
import qtawesome as qta
import dataclasses
import logging
import types


class Canvas(QtWidgets.QGraphicsScene):
    """
    A QGraphicsScene subclass for displaying and editing graphs.
    """

    # Class-level clipboard for cross-canvas copy-paste
    clipboard: list[QtWidgets.QGraphicsItem] = []
    _register: dict = {}

    @dataclasses.dataclass
    class Style:
        brush: QtGui.QBrush = dataclasses.field(default_factory=QtGui.QBrush)

    @dataclasses.dataclass
    class Geometry:
        bounds: QtCore.QRectF = dataclasses.field(default_factory=QtCore.QRectF)

    def __init__(self, parent=None):
        """
        Initialize the graphics scene.

        Args:
            parent: Parent object (optional).
        """

        # Instantiate options before super-class:
        self._geometry = Canvas.Geometry(bounds=QtCore.QRectF(0, 0, 5000, 5000))
        self._style = Canvas.Style(
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

    def _init_menu(self) -> QtWidgets.QMenu:
        """
        Initialize the context menu with graph editing actions.

        Returns:
            A configured QMenu ready for display on right-click.
        """
        context_menu = QtWidgets.QMenu()
        objects_menu = context_menu.addMenu(qta.icon("mdi.plus", color="cyan"), "Create")

        # Undo/Redo operations
        context_menu.addAction(qta.icon("mdi.undo", color="#efefef"), "Undo", self.undo)
        context_menu.addAction(qta.icon("mdi.redo", color="#efefef"), "Redo", self.redo)
        context_menu.addSeparator()

        # Copy/Paste operations
        context_menu.addAction(qta.icon("mdi.content-copy", color="#efefef"), "Copy", self.clone_items)
        context_menu.addAction(qta.icon("mdi.content-paste", color="#efefef"), "Paste", self.paste_items)
        context_menu.addAction(qta.icon("mdi.delete", color="red"), "Delete", self.delete_items)
        context_menu.addSeparator()

        # Create menu actions
        objects_menu.addAction(
            qta.icon("ph.browser-fill", color="cyan"),
            "Vertex",
            lambda: self.create_item(
                "VertexItem",
                pos=self._rmb_coordinate,
                image="mdi.function-variant",
                color="#efefef",
            ),
        )

        objects_menu.addAction(
            qta.icon("ph.flow-arrow", color="lightgreen"),
            "Source",
            lambda: self.create_item(
                "StreamItem",
                pos=self._rmb_coordinate,
                image="ph.arrow-circle-up-fill",
                color="lightgreen",
                draw_background=False,
                incoming_enabled=False,
            ),
        )

        objects_menu.addAction(
            qta.icon("ph.flow-arrow", color="darkred"),
            "Sink",
            lambda: self.create_item(
                "StreamItem",
                pos=self._rmb_coordinate,
                image="ph.arrow-circle-down-fill",
                color="darkred",
                draw_background=False,
                outgoing_enabled=False,
            ),
        )

        return context_menu

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
                isinstance(target, VertexItem)
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

    def create_item(self, class_name: str, **kwargs) -> QtWidgets.QGraphicsItem | None:
        """
        Create and return a graph item of the specified class.
        :param class_name: The name of the item class to instantiate.
        :return: The newly created item, or None if an error occurred.
        """

        # Required:
        from gui.graph.vertex.vertex import VertexItem

        # Map class-names to the respective class objects
        item_classes = {
            "VertexItem": VertexItem,
            "StreamItem": VertexItem,
        }

        # Get the item's class object from the class name
        item_class = item_classes.get(class_name, None)

        # If the class is valid, instantiate and add the item to the scene:
        if item_class:
            item = item_class(**kwargs)
            self.register_signals(item)
            self.addItem(item)
            self._actions_manager.do(CreateAction(self, item))
            return item

        else:
            print(f"Error: Invalid item class '{class_name}'")
            return None

    def find_item(self, name: str) -> QtWidgets.QGraphicsItem | None:
        """Find an item in the canvas by its object name."""

        items: list[QtWidgets.QGraphicsItem] = self.items()
        for item in items:
            if hasattr(item, "objectName"):
                if item.objectName() == name:
                    return item

        return None

    def register_signals(self, item: QtWidgets.QGraphicsObject):
        """Connects the given item's signals to appropriate slots."""

        if hasattr(item, "signals"):
            sig_list = item.signals()

            for name, signal in sig_list.items():
                method = f"_on_{name}"
                if hasattr(self, method):
                    signal.connect(getattr(self, method))

        else:
            logging.warning(f"Item {item} has no signals defined.")

    @QtCore.Slot(QtWidgets.QGraphicsObject)
    def _on_item_clicked(self, item: QtWidgets.QGraphicsObject):

        # Required:
        from gui.graph.vertex.vertex import VertexItem

        if not isinstance(item, VertexItem):
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

            if hasattr(item, "clone"):
                clone = item.clone()
                clone.setSelected(True)
                item.setSelected(False)

                Canvas._register[item] = clone
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
            if isinstance(item, VertexItem):
                batch.add_to_batch(DeleteAction(self, item))

        self._actions_manager.do(batch)
