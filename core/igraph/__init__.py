# Filename: __init__.py
# Module name: igraph
# Description: Graph data model package.

"""
Graph data model package for climate modeling.

Provides Graph, a subclass of igraph.Graph that automatically manages QGraphicsObjects
for visual representation, keeping model and view in sync.
"""

from .graph import Graph

__all__ = ["Graph"]