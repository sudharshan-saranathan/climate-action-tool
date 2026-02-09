# Filename: core/graph/graph.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations

import uuid
from typing import Dict, Optional, List

from PySide6 import QtWidgets, QtCore
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
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        self._connect_signals()

    @QtCore.Slot(str)
    def create_node(
        self,
        name: str,
        x: float = 0.0,
        y: float = 0.0,
        properties: Optional[Dict[str, str]] = None,
    ) -> Node:
        """
        Create and add a new node to the graph.

        Args:
            name: The node's name/label
            x: X coordinate
            y: Y coordinate
            properties: Optional metadata dictionary

        Returns:
            The created Node object
        """
        uid = str(uuid.uuid4())
        node = Node(uid=uid, name=name, x=x, y=y, properties=properties or {})
        self.nodes[uid] = node

        # Create the node's UI representation
        app = QtWidgets.QApplication.instance()
        if app and hasattr(app, "scene_ctrl"):
            app.scene_ctrl.req_repr_create.emit(
                name, pos=properties.get("pos", QtCore.QPointF())
            )

        return node

    @QtCore.Slot(str)
    def delete_node(self, uid: str) -> bool:
        """
        Delete a node and all its connected edges.

        Args:
            uid: The node's UID

        Returns:
            True if the node was deleted, False if not found
        """
        if uid not in self.nodes:
            return False

        # Delete all edges connected to this node
        edges_to_delete = [
            edge_uid
            for edge_uid, edge in self.edges.items()
            if edge.source_uid == uid or edge.target_uid == uid
        ]
        for edge_uid in edges_to_delete:
            self.delete_edge(edge_uid)

        del self.nodes[uid]
        return True

    def get_node(self, uid: str) -> Optional[Node]:
        """Get a node by UID."""
        return self.nodes.get(uid)

    def create_edge(
        self,
        source_uid: str,
        target_uid: str,
        properties: Optional[Dict[str, str]] = None,
    ) -> Optional[Edge]:
        """
        Create and add a new edge between two nodes.

        Args:
            source_uid: UID of source node
            target_uid: UID of target node
            properties: Optional metadata dictionary

        Returns:
            The created Edge object, or None if nodes don't exist
        """
        if source_uid not in self.nodes or target_uid not in self.nodes:
            return None

        uid = str(uuid.uuid4())
        edge = Edge(
            uid=uid,
            source_uid=source_uid,
            target_uid=target_uid,
            properties=properties or {},
        )
        self.edges[uid] = edge
        return edge

    def delete_edge(self, uid: str) -> bool:
        """
        Delete an edge.

        Args:
            uid: The edge's UID

        Returns:
            True if edge was deleted, False if not found
        """
        if uid not in self.edges:
            return False

        del self.edges[uid]
        return True

    def get_edge(self, uid: str) -> Optional[Edge]:
        """Get an edge by UID."""
        return self.edges.get(uid)

    def get_edges_for_node(self, uid: str) -> tuple[List[Edge], List[Edge]]:
        """
        Get all edges connected to a node.

        Args:
            uid: The node's UID

        Returns:
            Tuple of (outgoing_edges, incoming_edges)
        """
        outgoing = [e for e in self.edges.values() if e.source_uid == uid]
        incoming = [e for e in self.edges.values() if e.target_uid == uid]
        return outgoing, incoming

    def clear(self) -> None:
        """Clear all nodes and edges from the graph."""
        self.nodes.clear()
        self.edges.clear()

    def _connect_signals(self) -> None:
        """Connect to application-level signals."""
        app = QtWidgets.QApplication.instance()
        if app and hasattr(app, "graph_ctrl"):
            app.graph_ctrl.req_item_create.connect(self.create_node)
            app.graph_ctrl.req_item_delete.connect(self.delete_node)
