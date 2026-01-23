# Filename: canvas.py
# Module name: graph
# Description: Graphics scene for displaying node graphs.

"""
A QGraphicsScene subclass for displaying and editing graphs.
"""

from __future__ import annotations
from PySide6 import QtGui, QtCore, QtWidgets
from gui.graph.vector.vector import VectorItem
import dataclasses
import logging
import types


class Canvas(QtWidgets.QGraphicsScene):
    """
    A QGraphicsScene subclass for displaying and editing graphs.
    """

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

    def _init_menu(self) -> QtWidgets.QMenu:
        """
        Initialize the context menu with graph editing actions.

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
        objects_menu.addAction(
            "Vertex",
            lambda: self.create_item(
                "VertexItem",
                icon="mdi.function-variant",
                color="#efefef",
            ),
        )

        objects_menu.addAction(
            "Source",
            lambda: self.create_item(
                "StreamItem",
                icon="mdi.arrow-fat-line-up",
                color="#efefef",
            ),
        )

        objects_menu.addAction(
            "Sink",
            lambda: self.create_item(
                "StreamItem",
                icon="mdi.arrow-fat-line-down",
                color="#efefef",
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

        self.setProperty("_rmb_coordinate", event.scenePos())
        self._menu.exec_(event.screenPos())

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        if self._prev.active:
            # Use stored click position from origin vertex

            origin = self._prev.origin.scenePos()
            target = event.scenePos()
            self._prev.vector.update_path(origin, target)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        # Required:
        from gui.graph.vertex.vertex import VertexItem

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

        # Map class names to their corresponding classes
        item_classes = {
            "VertexItem": VertexItem,
            "StreamItem": VertexItem,
        }

        # Get the item's class object from the class name
        item_class = item_classes.get(class_name, None)

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
