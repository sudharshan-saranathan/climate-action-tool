# Filename: core/graph/__init__.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations
from typing import Dict
import logging
import uuid

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# Core module(s)
from core.signals import SignalBus
from core.graph.node import Node
from core.graph.edge import Edge


class GraphManager:
    """
    A graph-manager that manages multiple graphs (Singleton).
    """

    _instance = None

    @dataclass
    class Graph:
        nodes: Dict[str, Node] = field(default_factory=dict)
        edges: Dict[str, Edge] = field(default_factory=dict)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # Only initialize once
        if self._initialized:
            return

        # Global graph database
        self.graph_db: Dict[int, GraphManager.Graph] = {}
        self._connect_to_session_manager()
        self._initialized = True

    def _connect_to_session_manager(self) -> None:

        self.manager = SignalBus()
        self.manager.graph_commands.create_new_graph.connect(self.create_graph)
        self.manager.graph_commands.create_node_item.connect(self.create_node)
        self.manager.graph_commands.create_edge_item.connect(self.create_edge)

    def create_graph(self, guid: int) -> None:

        if guid not in self.graph_db:
            logging.info(f"Creating new graph with GUID {guid}")
            self.graph_db[guid] = GraphManager.Graph()

        else:
            logging.warning(f"Graph with GUID {guid} already exists.")

    def create_node(self, guid: int, name: str, data: Dict[str, object]) -> None:

        if guid not in self.graph_db:
            logging.warning(f"Graph with GUID {guid} does not exist. Creating it.")
            self.create_graph(guid)

        nuid = uuid.uuid4().hex
        node = Node(
            uid=nuid,
            name=name,
            x=0.0,
            y=0.0,
            properties={},
        )

        # Store node reference
        self.graph_db[guid].nodes[nuid] = node

        # Emit signal
        self.manager.scene_commands.create_node_repr.emit(guid, nuid, data)

    def create_edge(self, guid: int, name: str, data: Dict[str, object]) -> None:

        if guid not in self.graph_db:
            logging.warning(f"Graph with GUID {guid} does not exist. Creating it.")
            self.create_graph(guid)

        euid = uuid.uuid4().hex
        edge = Edge(
            uid=euid,
            source_uid=data.get("source_uid", ""),
            target_uid=data.get("target_uid", ""),
            properties=data.get("properties", {}),
        )

        # Store edge reference
        self.graph_db[guid].edges[euid] = edge

        # Emit signal
        self.manager.scene_commands.create_edge_repr.emit(guid, euid, data)


# Instantiate the singleton when this module is imported
# This ensures GraphManager is listening to signals before any GUI components are created
_graph_manager = GraphManager()

__all__ = ["Node", "Edge", "GraphManager"]
