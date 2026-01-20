# Filename: canvas.py
# Module name: graph
# Description: Graphics scene for displaying node graphs.

"""
Graphics scene for node-based graph editing.

Provides a QGraphicsScene subclass configured for displaying and editing
node graphs with customizable appearance and scene layout.
"""

from __future__ import annotations
import dataclasses
from PySide6 import QtGui, QtCore, QtWidgets


class Canvas(QtWidgets.QGraphicsScene):
    """
    A graphics scene for displaying and editing node graphs.

    Provides a configured QGraphicsScene with default scene bounds and background styling.
    """

    @dataclasses.dataclass
    class Options:
        """
        Canvas configuration options.

        Attributes:
            sceneRect: QRect defining scene bounds (default: 0,0 to 5000x5000).
            background: QBrush for scene background color (default: light gray #EFEFEF).
        """

        sceneRect: QtCore.QRect = dataclasses.field(
            default_factory=lambda: QtCore.QRect(0, 0, 5000, 5000)
        )
        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(QtGui.QColor(0xEFEFEF))
        )

    def __init__(self, parent=None):
        """
        Initialize the graphics scene.

        Args:
            parent: Parent object (optional).
        """

        self._opts = Canvas.Options()
        super().__init__(
            self._opts.sceneRect, parent=parent, backgroundBrush=self._opts.background
        )

        # Store right-click position for context menu actions
        self.setProperty("_rmb_coordinate", QtCore.QPoint())

        # Set up context menu with graph editing actions
        self._menu = self._init_menu()

    def _init_menu(self) -> QtWidgets.QMenu:
        """
        Initialize the context menu with graph editing actions.

        Creates a menu with file operations (Open, Save), editing operations
        (Undo, Redo, Clone, Clear), and a submenu for creating graph objects
        (Vertex, Input, Output).

        Returns:
            A configured QMenu ready for display on right-click.
        """
        context_menu = QtWidgets.QMenu()
        objects_menu = context_menu.addMenu("Create")

        # File and edit operations
        context_menu.addSeparator()
        context_menu.addAction("Open")
        context_menu.addAction("Save")
        context_menu.addSeparator()

        context_menu.addAction("Undo")
        context_menu.addAction("Redo")
        context_menu.addAction("Clone")
        context_menu.addAction("Clear")
        context_menu.addSeparator()

        # Object creation submenu
        objects_menu.addAction("Vertex", lambda: self.create_item("VertexItem"))
        objects_menu.addAction("Input")
        objects_menu.addAction("Output")

        return context_menu

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        """
        Display the context menu at the location of the right-click event.

        Args:
            event: The context menu event containing screen position.
        """
        self.setProperty("_rmb_coordinate", event.scenePos())
        self._menu.exec_(event.screenPos())

    def create_item(self, class_name: str, **kwargs) -> QtWidgets.QGraphicsItem | None:
        """
        Create a new graph item of the specified type at the given position.

        Creates an item instance from the given class name, adds it to the scene,
        and emits a creation signal via the event bus.

        Args:
            class_name: Name of the item class to create (e.g., "VertexItem").
            **kwargs: Additional keyword arguments passed to the item constructor.

        Returns:
            The created QGraphicsObject instance, or None if creation failed.
        """

        # Required:
        from gui.graph.vertex import VertexItem
        from core.bus import EventsBus

        # Map class names to their corresponding classes
        item_classes = {
            "VertexItem": VertexItem,
            "StreamItem": None,
        }

        # Get the item's class object from the class name
        item_class = item_classes.get(class_name)

        # If the class is valid, create an item and add it to the scene
        if item_class:
            # Use the context menu position if not provided in kwargs:
            pos = kwargs.pop("pos", self.property("_rmb_coordinate"))

            item = item_class(**kwargs)
            item.setPos(pos)
            self.addItem(item)

            # Emit signal via event bus
            bus = EventsBus.instance()
            bus.sig_item_created.emit(item)

            return item
        else:
            print(f"Error: Invalid item class '{class_name}'")
            return None
