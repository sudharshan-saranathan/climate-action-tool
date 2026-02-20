# Filename: __init__.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations

from core.graph.node import Node, Technology
from core.graph.edge import Edge
from core.graph.manager import GraphManager

# Instantiate the singleton when this module is imported
# This ensures GraphManager is listening to signals before any GUI components are created
_graph_manager = GraphManager()

__all__ = ["Node", "Edge", "GraphManager"]
