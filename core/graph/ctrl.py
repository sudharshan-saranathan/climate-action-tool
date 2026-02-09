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

        # Store application-reference
        self._app = QtWidgets.QApplication.instance()
        if hasattr(self._app, "graph_ctrl"):
            self._app.graph_ctrl.create_item.connect(self.create_item)
            self._app.graph_ctrl.delete_item.connect(self.delete_item)

    def create_item(self, key: Literal["node", "edge"], data: Dict):

        if hasattr(self._app, "scene_ctrl"):
            self._app.scene_ctrl.create_repr.emit(key, data)

    def delete_item(self, key: Literal["node", "edge"], data: Dict):

        if hasattr(self._app, "scene_ctrl"):
            self._app.scene_ctrl.create_repr.emit(key, data)
