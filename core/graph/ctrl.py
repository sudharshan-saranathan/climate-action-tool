# Filename: core/graph/graph.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations
from typing import Dict
import uuid


# Core module(s)
from core.session import Manager
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

        # Connect to the session-manager's signals
        self._connect_to_session_manager()

    def _connect_to_session_manager(self) -> None:

        self.manager = Manager()
        self.manager.graph_commands.create_node_item.connect(self.create_node)
        self.manager.graph_commands.create_edge_item.connect(self.create_edge)

    def create_node(self, guid: int, name: str, data: Dict[str, object]) -> None:

        if guid != id(self):
            return

        nuid = uuid.uuid4().hex
        node = Node(nuid, name, **data)

        # Store node reference
        self.nodes[nuid] = node

        # Emit signal
        self.manager.scene_commands.create_node_repr.emit(id(self), nuid, data)

    def create_edge(self, guid: int, name: str, data: Dict[str, object]) -> None:

        if guid != id(self):
            return

        euid = uuid.uuid4().hex
        edge = Edge(euid, name, **data)

        # Store edge reference
        self.edges[euid] = edge

        # Emit signal
        self.manager.scene_commands.create_edge_repr.emit(id(self), euid, data)
