"""
GraphManager: Centralized graph manager that coordinates mutations and emits signals.

This module is Qt-independent. It emits signals via QApplication singleton (if available)
to notify UI layers of changes. Works headless if no QApplication exists.
"""

from typing import Dict, List, Any, Optional, Callable
from PySide6 import QtCore

from .node import Node
from .edge import Edge


class GraphManager:
    """
    Centralized manager for graph mutations and state.

    Owns all nodes and edges. All mutations go through this manager.
    Emits signals via QApplication (if available) to notify UI layers.

    Works headless (without UI) if QApplication is not instantiated.
    """

    def __init__(self):
        """Initialize empty graph."""
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

        # Optional callbacks for headless operation
        self._on_node_created: List[Callable[[Node], None]] = []
        self._on_node_deleted: List[Callable[[str], None]] = []
        self._on_node_moved: List[Callable[[Node], None]] = []
        self._on_edge_created: List[Callable[[Edge], None]] = []
        self._on_edge_deleted: List[Callable[[str], None]] = []

    def _emit_signal(self, signal_name: str, *args) -> None:
        """
        Emit a signal via QApplication if available, otherwise do nothing.

        This allows the graph manager to work with or without a Qt application.

        Args:
            signal_name: Name of the signal to emit (e.g., "sig_vertex_created")
            *args: Arguments to pass to the signal
        """
        try:
            app = QtCore.QApplication.instance()
            if app and hasattr(app, signal_name):
                signal = getattr(app, signal_name)
                signal.emit(*args)
        except Exception:
            # If anything fails (no QApplication, signal doesn't exist, etc.), silently continue
            pass

    def _notify_callbacks(self, callbacks: List[Callable], *args) -> None:
        """
        Call all registered callbacks with given arguments.

        Used for headless operation when signals aren't available.

        Args:
            callbacks: List of callback functions to invoke
            *args: Arguments to pass to callbacks
        """
        for callback in callbacks:
            try:
                callback(*args)
            except Exception as e:
                print(f"Warning: Callback error: {e}")

    # ========== NODE OPERATIONS ==========

    def create_node(
        self,
        type: str,
        x: float,
        y: float,
        id: str | None = None,
        **properties
    ) -> Node:
        """
        Create a new node.

        Args:
            type: Node type (e.g., "pump", "reactor")
            x: Visual x-coordinate
            y: Visual y-coordinate
            id: Optional custom ID (auto-generated if not provided)
            **properties: Additional node properties

        Returns:
            The created Node instance

        Emits:
            sig_vertex_created(node: Node)
        """
        node = Node.create(name=type, x=x, y=y, id=id, **properties)
        self.nodes[node.id] = node

        # Emit signal
        self._emit_signal("sig_vertex_created", node)
        self._notify_callbacks(self._on_node_created, node)

        return node

    def delete_node(self, node_id: str) -> bool:
        """
        Delete a node and all its connected edges.

        Args:
            node_id: ID of the node to delete

        Returns:
            True if node was deleted, False if not found

        Emits:
            sig_vertex_deleted(node_id: str)
            sig_edge_deleted(edge_id: str) for each connected edge
        """
        if node_id not in self.nodes:
            return False

        # Delete all connected edges
        connected_edges = [
            eid for eid, edge in self.edges.items()
            if edge.source == node_id or edge.target == node_id
        ]
        for edge_id in connected_edges:
            self.delete_edge(edge_id)

        # Delete node
        del self.nodes[node_id]
        self._emit_signal("sig_vertex_deleted", node_id)
        self._notify_callbacks(self._on_node_deleted, node_id)

        return True

    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def move_node(self, node_id: str, x: float, y: float) -> Optional[Node]:
        """
        Move a node to new coordinates.

        Args:
            node_id: ID of the node
            x: New x-coordinate
            y: New y-coordinate

        Returns:
            The updated Node, or None if not found

        Emits:
            sig_vertex_moved(node: Node)
        """
        if node_id not in self.nodes:
            return None

        node = self.nodes[node_id]
        node.x = x
        node.y = y

        self._emit_signal("sig_vertex_moved", node)
        self._notify_callbacks(self._on_node_moved, node)

        return node

    def set_node_property(self, node_id: str, key: str, value: Any) -> bool:
        """
        Set a property on a node.

        Args:
            node_id: ID of the node
            key: Property key
            value: Property value

        Returns:
            True if property was set, False if node not found
        """
        if node_id not in self.nodes:
            return False

        self.nodes[node_id].properties[key] = value
        return True

    # ========== EDGE OPERATIONS ==========

    def create_edge(
        self,
        source: str,
        target: str,
        type: str,
        id: str | None = None,
        **properties
    ) -> Optional[Edge]:
        """
        Create a new edge connecting two nodes.

        Args:
            source: ID of source node
            target: ID of target node
            type: Edge type (e.g., "material", "energy")
            id: Optional custom ID (auto-generated if not provided)
            **properties: Additional edge properties

        Returns:
            The created Edge instance, or None if source/target not found

        Emits:
            sig_edge_created(edge: Edge)
        """
        # Validate nodes exist
        if source not in self.nodes or target not in self.nodes:
            return None

        edge = Edge.create(source=source, target=target, type=type, id=id, **properties)
        self.edges[edge.id] = edge

        self._emit_signal("sig_edge_created", edge)
        self._notify_callbacks(self._on_edge_created, edge)

        return edge

    def delete_edge(self, edge_id: str) -> bool:
        """
        Delete an edge.

        Args:
            edge_id: ID of the edge to delete

        Returns:
            True if edge was deleted, False if not found

        Emits:
            sig_edge_deleted(edge_id: str)
        """
        if edge_id not in self.edges:
            return False

        del self.edges[edge_id]
        self._emit_signal("sig_edge_deleted", edge_id)
        self._notify_callbacks(self._on_edge_deleted, edge_id)

        return True

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """Get an edge by ID."""
        return self.edges.get(edge_id)

    def set_edge_property(self, edge_id: str, key: str, value: Any) -> bool:
        """
        Set a property on an edge.

        Args:
            edge_id: ID of the edge
            key: Property key
            value: Property value

        Returns:
            True if property was set, False if edge not found
        """
        if edge_id not in self.edges:
            return False

        self.edges[edge_id].properties[key] = value
        return True

    # ========== QUERY OPERATIONS ==========

    def get_edges_from_node(self, node_id: str) -> List[Edge]:
        """Get all edges originating from a node."""
        return [e for e in self.edges.values() if e.source == node_id]

    def get_edges_to_node(self, node_id: str) -> List[Edge]:
        """Get all edges pointing to a node."""
        return [e for e in self.edges.values() if e.target == node_id]

    def get_connected_edges(self, node_id: str) -> List[Edge]:
        """Get all edges connected to a node (incoming or outgoing)."""
        return self.get_edges_from_node(node_id) + self.get_edges_to_node(node_id)

    # ========== SERIALIZATION ==========

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the entire graph to a dictionary.

        Returns:
            Dictionary with 'nodes' and 'edges' keys
        """
        return {
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges.values()],
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load graph from a dictionary (clears existing graph).

        Args:
            data: Dictionary with 'nodes' and 'edges' keys
        """
        self.nodes.clear()
        self.edges.clear()

        # Load nodes
        for node_data in data.get("nodes", []):
            node = Node.from_dict(node_data)
            self.nodes[node.id] = node

        # Load edges
        for edge_data in data.get("edges", []):
            edge = Edge.from_dict(edge_data)
            self.edges[edge.id] = edge

    # ========== CALLBACKS (HEADLESS MODE) ==========

    def on_node_created(self, callback: Callable[[Node], None]) -> None:
        """Register callback for node creation (headless)."""
        self._on_node_created.append(callback)

    def on_node_deleted(self, callback: Callable[[str], None]) -> None:
        """Register callback for node deletion (headless)."""
        self._on_node_deleted.append(callback)

    def on_node_moved(self, callback: Callable[[Node], None]) -> None:
        """Register callback for node movement (headless)."""
        self._on_node_moved.append(callback)

    def on_edge_created(self, callback: Callable[[Edge], None]) -> None:
        """Register callback for edge creation (headless)."""
        self._on_edge_created.append(callback)

    def on_edge_deleted(self, callback: Callable[[str], None]) -> None:
        """Register callback for edge deletion (headless)."""
        self._on_edge_deleted.append(callback)
