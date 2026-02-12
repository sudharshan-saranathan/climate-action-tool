# Filename: core/graph/__init__.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations

# Standard Library
from typing import Dict, Tuple, Any
import logging
import uuid
import json

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
        conns: Dict[Tuple[str, str], bool] = field(default_factory=dict)

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
        self.graph_db: Dict[str, GraphManager.Graph] = {}
        self.signal_bus = SignalBus()

        self._connect_to_session_manager()
        self._initialized = True

    def _connect_to_session_manager(self) -> None:

        self.signal_bus.data.create_graph.connect(self.create_graph)
        self.signal_bus.data.create_node_item.connect(self.create_node)
        self.signal_bus.data.create_edge_item.connect(self.create_edge)

        self.signal_bus.data.send_node_data.connect(self.send_node_data)
        self.signal_bus.data.send_edge_data.connect(self.send_edge_data)

    def create_graph(self, guid: str) -> None:

        if guid not in self.graph_db:
            logging.info(f"Creating new graph with GUID {guid}")
            self.graph_db[guid] = GraphManager.Graph()

        else:
            logging.warning(f"Graph with GUID {guid} already exists.")

    def create_node(self, guid: str, jstr: str) -> None:

        if guid not in self.graph_db:
            logging.warning(f"Graph with GUID {guid} does not exist. Creating it.")
            return

        try:
            _data = json.loads(jstr)
        except json.JSONDecodeError as e:
            logging.warning(f"Invalid JSON for node creation: {e}")
            return

        _nuid = uuid.uuid4().hex
        _node = Node(
            uid=_nuid,
            meta=_data,
        )

        # Store node reference and emit signal
        self.graph_db[guid].nodes[_nuid] = _node

        # Emit signal
        self.signal_bus.ui.create_node_repr.emit(guid, _nuid, jstr)

        # Log after emitting signal
        logging.info(f"Created node with UID {_nuid}")

    def create_edge(self, guid: str, jstr: str) -> None:

        if guid not in self.graph_db:
            logging.warning(f"Graph with GUID {guid} does not exist.")
            return

        # Parse the JSON payload
        try:
            _data = json.loads(jstr)
        except json.JSONDecodeError as e:
            logging.warning(f"Invalid JSON for edge creation: {e}")
            return

        # Check if keys exist and are connected
        source_uid = _data.get("source_uid", "")
        target_uid = _data.get("target_uid", "")

        if not source_uid or not target_uid:
            logging.warning(f"Missing source or target UID: {source_uid} {target_uid}")
            return

        if source_uid == target_uid:
            logging.warning(f"Source and target UIDs are the same: {source_uid}")
            return

        if (source_uid, target_uid) in self.graph_db[guid].conns:
            logging.warning(f"Connection already exists!")
            return

        # Create a new edge instance
        _euid = uuid.uuid4().hex
        _edge = Edge(
            uid=_euid,
            source_uid=source_uid,
            target_uid=target_uid,
            properties=_data.get("properties", {}),
        )

        # Store reference and update dictionaries
        self.graph_db[guid].edges[_euid] = _edge
        self.graph_db[guid].conns[(source_uid, target_uid)] = True

        # Emit signal
        self.signal_bus.ui.create_edge_repr.emit(guid, _euid, jstr)

        # Log after emitting signal
        logging.info(f"Created edge with UID {_euid}")

    def send_node_data(self, guid: str, nuid: str) -> None:

        if guid not in self.graph_db:
            logging.warning(f"Graph with GUID {guid} does not exist.")
            return

        _node = self.graph_db[guid].nodes.get(nuid)
        _json = json.dumps(_node.to_dict()) if _node else None

        self.signal_bus.ui.publish_node_data.emit(nuid, _json)

    def send_edge_data(self, guid: str, euid: str) -> None:
        pass


# Instantiate the singleton when this module is imported
# This ensures GraphManager is listening to signals before any GUI components are created
_graph_manager = GraphManager()

__all__ = ["Node", "Edge", "GraphManager"]
