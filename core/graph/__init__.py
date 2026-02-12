# Filename: core/graph/__init__.py
# Module name: core.graph
# Description: Graph data structure managing nodes and edges

from __future__ import annotations

# Standard Library
from typing import Dict, Tuple, Any, Callable
import logging
import uuid
import json
import functools

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# Core module(s)
from core.signals import SignalBus
from core.graph.node import Node
from core.graph.edge import Edge


# Module-level loggers
_decorator_logger = logging.getLogger("core.graph.decorators")


# Decorator to validate GUID
def guid_validator(func: Callable) -> Callable:
    """Decorator to validate that a GUID exists in graph_db before executing."""

    @functools.wraps(func)
    def wrapper(self, guid: str, *args, **kwargs):
        if guid not in self.graph_db:
            self.signal_bus.ui.notify(f"ALERT: Graph [UID={guid}] does not exist.")
            return None

        result = func(self, guid, *args, **kwargs)
        return result

    return wrapper


# Decorator to parse JSON string
def json_parser(func: Callable) -> Callable:
    """Decorator to parse JSON string and pass parsed dict to the function.

    The wrapped function receives both jstr and data (parsed dict) as arguments.
    """

    @functools.wraps(func)
    def wrapper(self, guid: str, jstr: str, *args, **kwargs):
        try:
            data = json.loads(jstr)
        except json.JSONDecodeError as e:
            _decorator_logger.warning(f"Invalid JSON for {func.__name__}: {e}")
            return None

        # Pass both original jstr and parsed data
        return func(self, guid, jstr, data, *args, **kwargs)

    return wrapper


class GraphManager:
    """
    A graph-manager that manages multiple graphs (Singleton).
    """

    _instance = None
    _logger = logging.getLogger("GraphManager")

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
        self._ignore = False

    def _connect_to_session_manager(self) -> None:

        self.signal_bus.data.create_graph.connect(self.create_graph)
        self.signal_bus.data.create_node_item.connect(self.create_node)
        self.signal_bus.data.create_edge_item.connect(self.create_edge)

        self.signal_bus.data.send_node_data.connect(self.send_node_data)
        self.signal_bus.data.send_edge_data.connect(self.send_edge_data)

    def _verify_stream_matching(
        self, guid: str, source_uid: str, target_uid: str
    ) -> bool:
        """
        This method checks for at least one matching stream between the source's outputs and the target's inputs.

        :param guid: Graph GUID
        :param source_uid: UID of the source node
        :param target_uid: UID of the target node
        :return: True if there is at least one matching stream, False otherwise
        """
        graph = self.graph_db.get(guid)
        source_node = graph.nodes.get(source_uid)
        target_node = graph.nodes.get(target_uid)

        source_produced = source_node.get_produced()
        target_consumed = target_node.get_consumed()

        if not source_produced.intersection(target_consumed):
            self._logger.warning(
                f"No matching streams found between source and target nodes."
            )
            return False

        else:
            return True

    def create_graph(self, guid: str) -> None:

        if guid in self.graph_db:
            self._logger.warning(f"Graph with GUID {guid} already exists.")
            return

        self.graph_db[guid] = GraphManager.Graph()

    @guid_validator
    @json_parser
    def create_node(self, guid: str, jstr: str, data: dict) -> None:

        _nuid = uuid.uuid4().hex
        _node = Node(
            uid=_nuid,
            meta=data,
        )

        # Store node reference and emit signal
        self.graph_db[guid].nodes[_nuid] = _node

        # Emit signal
        self.signal_bus.ui.create_node_repr.emit(guid, _nuid, jstr)

        # Log after emitting signal
        self._logger.info(f"Created node with UID {_nuid}")

    @guid_validator
    @json_parser
    def create_edge(self, guid: str, jstr: str, data: dict) -> None:

        # Check if keys exist and are connected
        suid = data["source_uid"]  # KeyError raised if source_uid not found
        tuid = data["target_uid"]  # KeyError raised if target_uid not found

        if suid == tuid:
            self._logger.warning(f"Source and target UIDs are the same: {suid}")
            return

        if (suid, tuid) in self.graph_db[guid].conns:
            self._logger.warning(f"Connection already exists!")
            return

        # Check if the source and target nodes have common streams. That is, there must be at least one output
        # stream in the source node that matches with an input stream in the target node
        if not self._verify_stream_matching(guid, suid, tuid):
            self._logger.warning(f"No matching streams between source and target!")
            self.signal_bus.ui.notify.emit(
                guid,
                "ERROR: At least one matching stream required between source and target.\n"
                "Reconfigure the nodes and try again.",
            )
            return

        # Create a new edge instance
        _euid = uuid.uuid4().hex
        _edge = Edge(
            uid=_euid,
            source_uid=suid,
            target_uid=tuid,
        )

        # Store reference and update dictionaries
        self.graph_db[guid].edges[_euid] = _edge
        self.graph_db[guid].conns[(suid, tuid)] = True

        # Emit signal
        self.signal_bus.ui.create_edge_repr.emit(guid, _euid, jstr)

        # Log after emitting signal
        self._logger.info(f"Created edge with UID {_euid}")

    @guid_validator
    def send_node_data(self, guid: str, nuid: str) -> None:

        _node = self.graph_db[guid].nodes.get(nuid)
        _json = json.dumps(_node.to_dict()) if _node else None

        self.signal_bus.ui.publish_node_data.emit(nuid, _json)

    @guid_validator
    def send_edge_data(self, guid: str, euid: str) -> None:
        pass


# Instantiate the singleton when this module is imported
# This ensures GraphManager is listening to signals before any GUI components are created
_graph_manager = GraphManager()

__all__ = ["Node", "Edge", "GraphManager"]
