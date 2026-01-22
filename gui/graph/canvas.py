# Filename: canvas.py
# Module name: graph
# Description: Graphics scene for displaying node graphs.

"""
Graphics scene for node-based graph editing.

Provides a QGraphicsScene subclass configured for displaying and editing
node graphs with customizable appearance and scene layout.
"""

from __future__ import annotations
from PySide6 import QtGui, QtCore, QtWidgets
from gui.graph.vector.vector import VectorItem
import dataclasses
import types


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
            default_factory=lambda: QtGui.QBrush(QtGui.QColor(0xFFFFFF))
        )

    def __init__(self, parent=None):
        """
        Initialize the graphics scene.

        Args:
            parent: Parent object (optional).
        """

        # Instantiate options before super-class:
        self._opts = Canvas.Options()

        # Super-class initialization:
        super().__init__(
            self._opts.sceneRect,
            parent=parent,
            backgroundBrush=self._opts.background,
        )

        # Store right-click position for context menu actions
        self.setProperty("_rmb_coordinate", QtCore.QPoint())

        # Set up the context menu:
        self._menu = self._init_menu()
        self._prev = types.SimpleNamespace(
            active=False,
            origin=None,
            vector=VectorItem(),
        )
        self.addItem(self._prev.vector)

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
        objects_menu.addAction("Stream")

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

        self.setProperty("_rmb_coordinate", event.scenePos())
        self._menu.exec_(event.screenPos())

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        if self._prev.active:
            # Use stored click position from origin vertex
            origin = self._prev.origin.property("click_pos")
            target = event.scenePos()
            self._prev.vector.update_path(origin, target)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        # Required:
        from gui.graph.vertex.vertex import VertexItem

        if self._prev.active:

            origin = self._prev.origin
            target = self.itemAt(event.scenePos(), QtGui.QTransform())

            # If we hit a child item (label), traverse up to find parent vertex
            while target and not isinstance(target, VertexItem):
                target = target.parentItem()

            if isinstance(target, VertexItem):
                # Get origin position (stored from click)
                origin_pos = origin.property("click_pos")

                # Enforce target position: use target vertex center x, release y
                target_pos = QtCore.QPointF(target.scenePos().x(), event.scenePos().y())

                vector = origin.connect_to(target, origin_pos, target_pos)
                if vector is not None:
                    self.addItem(vector)

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
        from gui.graph.vertex.vertex import VertexItem

        # Map class names to their corresponding classes
        item_classes = {
            "VertexItem": VertexItem,
            "StreamItem": None,
        }

        # Get the item's class object from the class name
        item_class = item_classes.get(class_name)

        # If the class is valid, instantiate and add the item to the scene:
        if item_class:

            cpos = kwargs.pop("pos", self.property("_rmb_coordinate"))
            item = item_class(**kwargs)
            item.setPos(cpos)

            self.register_signals(item)
            self.addItem(item)

            return item

        else:
            print(f"Error: Invalid item class '{class_name}'")
            return None

    def find_item(self, name: str) -> QtWidgets.QGraphicsItem | None:

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
                signal.connect(getattr(self, method))

    @QtCore.Slot(QtWidgets.QGraphicsObject)
    def _on_item_clicked(self, item: QtWidgets.QGraphicsObject):

        # Required:
        from gui.graph.vertex.vertex import VertexItem

        if not isinstance(item, VertexItem):
            return

        self.prev_on(item)
