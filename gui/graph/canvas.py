# Filename: canvas.py
# Module name: graph
# Description: Graph editing canvas for the Climate Action Tool.

"""
QGraphicsScene-based canvas for interactive graph editing.

Provides a canvas for creating and editing graph structures interactively:
- Create vertices and edges via context menu
- Connect handles with preview vectors
- Clone and paste items
- Undo/redo support (when actions module is ported)
"""

from __future__ import annotations
import logging
import types
from typing import Any

from PySide6 import QtGui, QtCore, QtWidgets
from qtawesome import icon as qta_icon

from core.bus import EventsBus
# from core.actions import *  # TODO: Port actions module
from gui.graph.enums import ItemRole
from gui.graph.vertex import VertexItem
from gui.graph.vector import VectorItem
from gui.graph.anchor import AnchorItem
from gui.graph.handle import HandleItem

logger = logging.getLogger(__name__)


# Class Canvas: A QGraphicsScene-subclass for the Climact application
class Canvas(QtWidgets.QGraphicsScene):
    """
    A QGraphicsScene subclass that serves as the main canvas for the Climact application.
    It manages graph items, preview, context menus, and item state tracking.
    """

    sig_canvas_updated = QtCore.Signal(QtWidgets.QGraphicsObject)

    # Class-level clipboard for cross-canvas copy-paste
    clipboard: list[QtWidgets.QGraphicsObject] = []

    def __init__(self, parent: QtCore.QObject | None = None, **kwargs):
        super().__init__(parent, **kwargs)

        self._menu = self._init_menu()
        self._cpos = QtCore.QPointF()

        # Preview object for drawing preview vectors during connections
        self.preview = types.SimpleNamespace(
            active=False,
            origin=None,
            vector=VectorItem(),
        )

        self.addItem(self.preview.vector) if self.preview.vector else None

        # Actions manager for undo/redo
        # self.actions_manager: ActionsManager = ActionsManager()  # TODO: Uncomment when actions module is ported

        # Connect the bus' signals to appropriate slots
        self._bus = EventsBus.instance()
        self._bus.sig_item_clicked.connect(self._on_item_clicked)
        self._bus.sig_item_created.connect(self._on_item_created)
        self._bus.sig_item_deleted.connect(self._on_item_deleted)

    def __str__(self) -> str:
        return f"Canvas(items={len(self.items())})"

    def _init_menu(self):
        """Initialize the context menu."""
        menu = QtWidgets.QMenu("Context Menu", None)
        subm = menu.addMenu("Add")

        # Menu item to create a new vertex
        create_vertex_action = subm.addAction(
            qta_icon("ph.browser-fill", color="cyan"), "Vertex", self._on_item_inserted
        )
        create_vertex_action.setData({"class": "VertexItem", "kwargs": {}})

        # Menu item to create a source stream
        create_source_action = subm.addAction(
            qta_icon("ph.flow-arrow", color="green"), "Source", self._on_item_inserted
        )
        create_source_action.setData({"class": "VertexItem", "kwargs": {"role": ItemRole.OUT}})

        # Menu item to create a sink stream
        create_sink_action = subm.addAction(
            qta_icon("ph.flow-arrow", color="#ffcb00"), "Sink", self._on_item_inserted
        )
        create_sink_action.setData(
            {"class": "VertexItem", "kwargs": {"role": ItemRole.INP, "snap": False}}
        )

        create_vertex_action.setIconVisibleInMenu(True)
        create_source_action.setIconVisibleInMenu(True)
        create_sink_action.setIconVisibleInMenu(True)

        # Other actions
        menu.addSeparator()
        menu.addAction(qta_icon("mdi.content-copy", color="#efefef"), "Clone", self.clone_items)
        menu.addAction(qta_icon("mdi.content-paste", color="#efefef"), "Paste", self.paste_items)
        menu.addAction(qta_icon("ph.selection-all-fill", color="lightblue"), "Select All", None)

        menu.addSeparator()
        menu.addAction(qta_icon("mdi.eraser", color="red"), "Clear", None)
        menu.addAction(qta_icon("mdi.magnify", color="pink"), "Find", None)

        return menu

    def contextMenuEvent(self, event, /):
        """Reimplemented QGraphicsScene.contextMenuEvent"""
        super().contextMenuEvent(event)
        if event.isAccepted():
            return

        self._cpos = event.scenePos()
        self._menu.exec(event.screenPos())

    def mouseMoveEvent(self, event, /):
        """Reimplemented QGraphicsScene.mouseMoveEvent to update the preview vector"""
        if self.preview.active:
            target = event.scenePos()
            origin = self.preview.origin.scenePos()
            self.preview.vector.update_path(origin, target)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event, /):
        """Event handler for mouse release during connection creation."""
        if self.preview.active:
            # batch = BatchActions([])  # TODO: Uncomment when actions module is ported
            origin = self.preview.origin
            target = self.itemAt(event.scenePos(), QtGui.QTransform())

            # Case B: Create a new handle at the clicked position, then proceed with connection
            if isinstance(target, AnchorItem) and target.parentItem() is not origin.parentItem():
                role = ItemRole.OUT if target.pos().x() > 0 else ItemRole.INP
                cpos = target.mapFromScene(event.scenePos())
                cpos = QtCore.QPointF(0, cpos.y())
                cpos = target.mapToParent(cpos)

                vertex = target.parentItem()
                if isinstance(vertex, VertexItem):
                    target = vertex.create_handle(role, cpos)
                    # batch.add_to_batch(CreateAction(vertex, target))  # TODO: Uncomment when actions module is ported

            # Connect two compatible handles
            if isinstance(target, HandleItem) and not target.connected and origin is not target:
                vector = VectorItem(
                    origin=(origin if origin.attr["role"] == ItemRole.OUT else target),
                    target=(target if target.attr["role"] == ItemRole.INP else origin),
                )
                self.addItem(vector)
                # batch.add_to_batch(CreateAction(self, vector))  # TODO: Uncomment when actions module is ported

            # if batch.size():  # TODO: Uncomment when actions module is ported
            #     self.actions_manager.do(batch)

        self.preview_off()
        super().mouseReleaseEvent(event)

    def preview_on(self, origin: HandleItem):
        """Begin drawing the preview vector."""
        if origin.connected:
            logging.warning("Cannot begin preview from an already-connected handle.")
            return

        if self.preview.active:
            return

        self.preview.active = True
        self.preview.origin = origin

    def preview_off(self):
        """Reset the preview."""
        self.preview.active = False
        self.preview.origin = None
        self.preview.target = None
        self.preview.vector.clear()

    def create_item(
        self,
        class_name: str,
        **kwargs,
    ) -> QtWidgets.QGraphicsObject | None:
        """Create an item and add it to the scene."""
        from gui.graph import GraphItemsRegistry

        item_class = GraphItemsRegistry.get(class_name, None)

        if item_class:
            item = item_class(self._cpos, **kwargs)
            self.addItem(item)
            # self.actions_manager.do(CreateAction(self, item))  # TODO: Uncomment when actions module is ported
            return item
        else:
            print(f"Error: Invalid item class '{class_name}'")
            return None

    def delete_item(self, item: QtWidgets.QGraphicsObject):
        """Delete an item from the scene."""
        # self.actions_manager.do(DeleteAction(self, item))  # TODO: Uncomment when actions module is ported
        self.removeItem(item)

    def clone_items(self):
        """Clone selected items to the clipboard."""
        self.clipboard.clear()

        if not self.selectedItems():
            logger.info("No items to copy!")
            return

        for item in self.selectedItems():
            if hasattr(item, "clone"):
                clone = item.clone()
                clone.setPos(item.scenePos() + QtCore.QPointF(20, 20))
                self.clipboard.append(clone)

        logger.info("Items copied to clipboard.")

    def fetch_items(self, classes, visibility=True) -> list:
        """
        Fetch items of specific types, optionally filtered by visibility.

        Args:
            classes: A type or tuple of types to filter by.
            visibility: Whether to return visible or hidden items.

        Returns:
            A list of matching items.
        """
        if isinstance(classes, type):
            classes = (classes,)
        elif isinstance(classes, (list, tuple)):
            classes = tuple(classes)
        else:
            raise TypeError("`classes` must be a type or an iterable of types")

        items: list[QtWidgets.QGraphicsItem] = [
            item
            for item in self.items()
            if isinstance(item, tuple(classes))
            and item is not self.preview.vector
            and item.isVisible() == visibility
        ]

        return items

    def paste_items(self):
        """Paste items from the clipboard."""
        self.clearSelection()

        # batch = BatchActions([])  # TODO: Uncomment when actions module is ported

        for item in self.clipboard:
            if hasattr(item, "clone"):
                clone = item.clone()
                clone.setSelected(True)
                clone.setPos(item.scenePos() + QtCore.QPointF(20, 20))
                self.addItem(clone)
                # batch.add_to_batch(CreateAction(self, clone))  # TODO: Uncomment when actions module is ported

        # self.actions_manager.do(batch)  # TODO: Uncomment when actions module is ported

    def undo(self):
        """Undo the last action."""
        # self.actions_manager.undo()  # TODO: Uncomment when actions module is ported
        pass

    def redo(self):
        """Redo the last undone action."""
        # self.actions_manager.redo()  # TODO: Uncomment when actions module is ported
        pass

    def _on_item_created(self, item: QtWidgets.QGraphicsObject):
        """Slot called when a new item is created."""
        # if type(item) is HandleItem:  # TODO: Uncomment when actions module is ported
        #     self.actions_manager.do(CreateAction(item.parentItem(), item))
        # else:
        #     self.actions_manager.do(CreateAction(self, item))

    @QtCore.Slot(QtWidgets.QGraphicsObject)
    def _on_item_clicked(self, item: QtWidgets.QGraphicsObject):
        """Slot called when a graph item is clicked."""
        if isinstance(item, HandleItem):
            self.preview_on(item)

    def _on_item_deleted(self, item: QtWidgets.QGraphicsObject):
        """Slot called when a graph item is deleted."""
        # if type(item) is VertexItem:  # TODO: Uncomment when actions module is ported
        #     self.actions_manager.do(DeleteAction(self, item))
        # elif type(item) is VectorItem:
        #     self.actions_manager.do(DeleteAction(self, item))
        # elif type(item) is HandleItem:
        #     self.actions_manager.do(DeleteAction(item.parentItem(), item))
        self.removeItem(item)

    @QtCore.Slot()
    def _on_item_inserted(self):
        """Callback when inserting an item from the context menu."""
        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return

        dictionary = action.data()
        item_class = dictionary.get("class", None)
        item_kwargs = dictionary.get("kwargs", {})

        self.create_item(item_class, **item_kwargs)

    def _attempt_connection(self, origin: HandleItem, target: Any):
        """Attempt a connection between two handles."""
        if isinstance(target, AnchorItem):
            coords = target.mapFromScene(origin.scenePos())
            coords = QtCore.QPointF(0, coords.y())
            target.sig_anchor_clicked.emit(coords)

        if origin.parentItem() is target.parentItem():
            return

        vector = VectorItem(
            origin=(origin if origin.attr["role"] == ItemRole.OUT else target),
            target=(target if target.attr["role"] == ItemRole.INP else origin),
        )

        self.addItem(vector)
        # self.actions_manager.do(CreateAction(self, vector))  # TODO: Uncomment when actions module is ported

    @QtCore.Slot(QtWidgets.QGraphicsObject)
    def deregister(self, item: QtWidgets.QGraphicsObject):
        """Deregister an item from the canvas."""
        self.removeItem(item)
