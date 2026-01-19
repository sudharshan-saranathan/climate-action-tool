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

    @staticmethod
    def _init_menu() -> QtWidgets.QMenu:
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
        objects_menu.addAction("Vertex")
        objects_menu.addAction("Input")
        objects_menu.addAction("Output")

        return context_menu

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        """
        Display the context menu at the location of the right-click event.

        Args:
            event: The context menu event containing screen position.
        """
        self._menu.exec_(event.screenPos())

    def create_item(self, item_type: str, pos: QtCore.QPointF) -> None:
        """
        Create a new graph item of the specified type at the given position.

        This method is a placeholder for future implementation of item creation.

        Args:
            item_type: Type of item to create (e.g., "Vertex", "Input", "Output").
            pos: Scene position where the item will be created.
        """
