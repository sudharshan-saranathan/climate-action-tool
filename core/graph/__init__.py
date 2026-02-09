"""
core.graph: Backend graph representation and manipulation.

Provides Node, Edge, and GraphManager for building and manipulating directed graphs.
The GraphManager is Qt-independent and works with or without a QApplication.
When a QApplication is available, mutations emit signals for UI synchronization.
"""

from .node import Node
from .edge import Edge
from .graph_manager import GraphManager

__all__ = ["Node", "Edge", "GraphManager"]
