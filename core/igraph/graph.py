# Filename: graph.py
# Module name: igraph
# Description: Graph data model synced with QGraphicsScene.

"""
Graph data model that syncs with QGraphicsScene.

Provides Graph, an igraph.Graph subclass that automatically creates and manages QGraphicsObjects
when vertices and edges are added/removed. Maintains bidirectional mapping between igraph structure
and visual representation for seamless model-view synchronization.
"""

from __future__ import annotations
from PySide6 import QtWidgets
from PySide6 import QtGui
import igraph


# Class Graph:
class Graph(igraph.Graph):
    """
    A subclass of igraph.Graph that automatically creates and manages QGraphicsObjects
    when vertices and edges are added/removed.

    Maintains a bidirectional mapping between igraph structure and QGraphicsScene items.
    """

    def __init__(self, scene: QtWidgets.QGraphicsScene):
        """
        Initialize the Graph with a graphics scene.

        Args:
            scene: The QGraphicsScene to add graphics items to.
        """
        super().__init__()
        self.scene = scene

        # Maps igraph vertex indices to their corresponding QGraphicsObjects
        self._vertex_graphics = {}

        # Maps igraph edge indices to their corresponding QGraphicsObjects
        self._edge_graphics = {}

    def add_vertex(self, name: str = None, **attributes) -> int:
        """
        Add a vertex to the graph and create a corresponding QGraphicsObject.

        Args:
            name: Optional name for the vertex.
            **attributes: Additional attributes for the vertex.

        Returns:
            The index of the added vertex.
        """
        # Add the vertex to the igraph structure
        vertex_id = super().add_vertex(name=name, **attributes)

        # Create a placeholder QGraphicsItem for the vertex
        # (This can be overridden by subclasses or customized later)
        graphics_item = self._create_vertex_graphics(vertex_id)

        # Store the mapping
        self._vertex_graphics[vertex_id] = graphics_item

        return vertex_id

    def add_edge(self, source: int, target: int, **attributes) -> int:
        """
        Add an edge to the graph and create a corresponding QGraphicsObject.

        Args:
            source: Source vertex index.
            target: Target vertex index.
            **attributes: Additional attributes for the edge.

        Returns:
            The index of the added edge.
        """
        # Add the edge to the igraph structure
        edge_id = super().add_edge(source, target, **attributes)

        # Create a placeholder QGraphicsItem for the edge
        # (This can be overridden by subclasses or customized later)
        graphics_item = self._create_edge_graphics(edge_id, source, target)

        # Store the mapping:
        self._edge_graphics[edge_id] = graphics_item

        return edge_id

    def delete_vertices(self, vertices):
        """
        Remove vertices from the graph and clean up corresponding graphics items.

        Args:
            vertices: Vertex index or list of vertex indices to delete.
        """

        # Convert single vertex to list
        if isinstance(vertices, int):
            vertices = [vertices]

        # Remove graphics items before deleting from the graph:
        for vertex_id in vertices:
            if vertex_id in self._vertex_graphics:
                item = self._vertex_graphics[vertex_id]
                self.scene.removeItem(item)
                del self._vertex_graphics[vertex_id]

        # Delete vertices from the graph:
        super().delete_vertices(vertices)

    def delete_edges(self, edges):
        """
        Remove edges from the graph and clean up corresponding graphics items.

        Args:
            edges: Edge index or list of edge indices to delete.
        """
        # Convert single edge to list
        if isinstance(edges, int):
            edges = [edges]

        # Remove graphics items before deleting from graph
        for edge_id in edges:
            if edge_id in self._edge_graphics:
                item = self._edge_graphics[edge_id]
                self.scene.removeItem(item)
                del self._edge_graphics[edge_id]

        # Delete edges from the graph:
        super().delete_edges(edges)

    def _create_vertex_graphics(self, vertex_id: int) -> QtWidgets.QGraphicsItem:
        """
        Create a QGraphicsItem representation of a vertex.
        Override this method in subclasses to customize vertex appearance.

        Args:
            vertex_id: The igraph vertex index.

        Returns:
            A QGraphicsItem to represent the vertex.
        """
        # Default implementation: simple blue circle
        item = QtWidgets.QGraphicsEllipseItem(0, 0, 30, 30)
        item.setBrush(QtGui.QColor("steelblue"))
        item.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        self.scene.addItem(item)
        return item

    def _create_edge_graphics(self, edge_id: int, source: int, target: int) -> QtWidgets.QGraphicsItem:
        """
        Create a QGraphicsItem representation of an edge.
        Override this method in subclasses to customize edge appearance.

        Args:
            edge_id: The igraph edge index.
            source: Source vertex index.
            target: Target vertex index.

        Returns:
            A QGraphicsItem to represent the edge.
        """
        # Default implementation: black line
        item = QtWidgets.QGraphicsLineItem(0, 0, 100, 100)
        item.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        self.scene.addItem(item)
        return item

    def get_vertex_graphics(self, vertex_id: int) -> QtWidgets.QGraphicsItem | None:
        """Get the QGraphicsItem for a vertex."""
        return self._vertex_graphics.get(vertex_id)

    def get_edge_graphics(self, edge_id: int) -> QtWidgets.QGraphicsItem | None:
        """Get the QGraphicsItem for an edge."""
        return self._edge_graphics.get(edge_id)