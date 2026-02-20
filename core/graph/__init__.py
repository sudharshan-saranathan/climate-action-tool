# Filename: __init__.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations

# Climact Module(s): core.graph
from core.graph.node import Node, Technology
from core.graph.edge import Edge
from core.graph.server import GraphServer

# Instantiate the singleton when this module is imported
# This ensures GraphServer is listening to signals before any GUI components are created
graph_server = GraphServer()

__all__ = ["Node", "Edge", "GraphServer"]
