# Filename: canvas.py
# Module name: graph
# Description: A QGraphicsScene subclass for displaying graphs.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


# Dataclass
from dataclasses import field
from dataclasses import dataclass


class Canvas(QtWidgets.QGraphicsScene):

    # Dictionary of graph objects
    graphObjects = {
        "Vertex": QtWidgets.QGraphicsObject,
        "Vector": QtWidgets.QGraphicsObject,
        "Stream": QtWidgets.QGraphicsObject,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initial click position
        self._cpos = QtCore.QPoint()

        # Initialize the context menu
        self._init_menu()

    def _init_menu(self):

        self._menu = QtWidgets.QMenu()  # Main menu
        self._item = self._menu.addMenu("Create")  # Item-menu

        self._item.addAction("Vertex")
        self._item.addAction("Vector")
        self._item.addAction("Stream")

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):

        self._cpos = event.scenePos()
        self._menu.exec(event.screenPos())

    def create_item(self, item_class) -> QtWidgets.QGraphicsObject | None:

        if not item_class in Canvas.graphObjects:
            return None

        item = Canvas.graphObjects[item_class]()
        item.setPos(self._cpos)

        self.addItem(item)
        return item
