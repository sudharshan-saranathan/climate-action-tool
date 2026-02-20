# Filename: core/graph/server.py
# Module name: core.graph.server
# Description: Server-side implementation for graph-related operations

# Standard Library
import logging

# Climact Module(s): core.graph
from core.graph import GraphManager

# Module-level logger
_logger = logging.getLogger("GraphServer")


class GraphServer:

    def __init__(self):
        self._graph_manager = GraphManager()
