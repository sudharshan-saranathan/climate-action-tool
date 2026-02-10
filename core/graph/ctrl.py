# Filename: core/graph/graph.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations
from typing import Dict
from typing import Literal

# PySide6 (Python/Qt)
from PySide6 import QtWidgets

# core.graph
from core.graph.node import Node
from core.graph.edge import Edge
from core.actions.manager import StackManager

# PySide6
from PySide6 import QtCore

# GUI
from gui.graph.node import NodeRepr
from gui.graph.edge.__init__ import EdgeRepr


class GraphCtrl:
    """
    A simple graph data structure managing nodes and edges.

    Attributes:
        nodes: Dictionary mapping node UIDs to Node objects
        edges: Dictionary mapping edge UIDs to Edge objects
    """

    def __init__(self):

        # Dictionary to map node- and edge-references
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

        # Reference maps
        self._item_to_repr: Dict[Node | Edge, NodeRepr | EdgeRepr] = {}
        self._repr_to_item: Dict[NodeRepr | EdgeRepr, Node | Edge] = {}

        # Undo/Redo stack manager (backend owns action history)
        self._stack_manager = StackManager()

        # Store application-reference
        self._app = QtWidgets.QApplication.instance()
        if hasattr(self._app, "graph_ctrl"):
            self._app.graph_ctrl.create_item.connect(self.create_item)
            self._app.graph_ctrl.delete_item.connect(self.delete_item)
            self._app.graph_ctrl.undo_action.connect(self.undo)
            self._app.graph_ctrl.redo_action.connect(self.redo)

    def create_item(self, key: Literal["NodeRepr", "EdgeRepr"], data: Dict):

        if key == "NodeRepr":
            node = Node(uid="#43s3da", name="", x=0, y=0, properties={})
            item = NodeRepr(pos=data.get("pos", QtCore.QPointF()))
            self._item_to_repr[node] = item
            self._repr_to_item[item] = node

        elif key == "EdgeRepr":
            edge = Edge.from_dict(data)
            origin = data.get("origin", None)
            target = data.get("target", None)

            print(f"[GraphCtrl] Creating EdgeRepr: {origin} -> {target}")
            item = EdgeRepr(None, origin=origin, target=target)
            self._item_to_repr[edge] = item
            self._repr_to_item[item] = edge

        else:
            return

        if hasattr(self._app, "scene_ctrl"):
            self._app.scene_ctrl.add_item.emit(item)

    def delete_item(self, key: Literal["node", "edge"], data: Dict):

        if hasattr(self._app, "scene_ctrl"):
            self._app.scene_ctrl.create_repr.emit(key, data)

    def undo(self) -> None:
        """Undo the most recent action."""
        self._stack_manager.undo()

    def redo(self) -> None:
        """Redo the most recently undone action."""
        self._stack_manager.redo()
