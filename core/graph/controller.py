# Filename: core/graph/controller.py
# Module Name: core.graph.controller
# Description: Graph controller for managing graph data structure via signal-driven architecture.

from __future__ import annotations


# Standard
import logging
import typing
import uuid
import json


# Dataclass
from dataclasses import field
from dataclasses import dataclass


# Climact Module(s): core.graph, core.signals
from core.signals import SignalBus
from core.graph.node import Node, Technology
from core.graph.edge import Edge
from core.graph.decorators import guid_validator, json_parser


class GraphController:
    """
    A graph-server that manages multiple graphs (Singleton).
    """

    _server = None
    _logger = logging.getLogger("GraphController")

    @dataclass
    class Graph:
        nodes: typing.Dict[str, Node] = field(default_factory=dict)
        edges: typing.Dict[str, Edge] = field(default_factory=dict)
        conns: typing.Dict[typing.Tuple[str, str], bool] = field(default_factory=dict)

    def __new__(cls):
        if cls._server is None:
            cls._server = super().__new__(cls)
            cls._server._initialized = False
        return cls._server

    def __init__(self):

        # Only initialize once
        if self._initialized:
            return

        # Global graph database
        self.database: typing.Dict[str, GraphController.Graph] = {}
        self.cmds_bus = SignalBus()

        self._connect_to_session_manager()
        self._initialized = True
        self._ignore = False

    def _connect_to_session_manager(self) -> None:

        self.cmds_bus.data.create_graph.connect(self.create_graph)
        self.cmds_bus.data.create_node_item.connect(self.create_node)
        self.cmds_bus.data.create_edge_item.connect(self.create_edge)

        self.cmds_bus.data.get_node_data.connect(self.send_node_data)
        self.cmds_bus.data.get_edge_data.connect(self.send_edge_data)
        self.cmds_bus.data.update_node_data.connect(self.update_node_data)

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
        graph = self.database.get(guid)
        source_node = graph.nodes.get(source_uid)
        target_node = graph.nodes.get(target_uid)

        source_produced = source_node.get_out_streams()
        target_consumed = target_node.get_inp_streams()

        if not source_produced.intersection(target_consumed):
            self._logger.warning(
                f"No matching streams found between source and target nodes."
            )
            return False

        else:
            return True

    def create_graph(self, guid: str) -> GraphController.Graph | None:

        if guid in self.database:
            self._logger.warning(f"Graph with GUID {guid} already exists.")
            return None

        self.database[guid] = GraphController.Graph()
        return self.database[guid]

    @guid_validator
    @json_parser
    def create_node(self, guid: str, jstr: str, data: dict) -> str:

        _nuid = uuid.uuid4().hex
        _node = Node(
            nuid=_nuid,
            meta=data,
        )

        # Store node reference and emit signal
        self.database[guid].nodes[_nuid] = _node

        # Emit signal
        self.cmds_bus.ui.create_node_repr.emit(guid, _nuid, jstr)

        # Log after emitting signal
        self._logger.info(f"Created node with UID {_nuid}")

        return _nuid

    @guid_validator
    @json_parser
    def create_edge(self, guid: str, jstr: str, data: dict) -> str:

        # Check if keys exist and are connected
        suid = data["source_uid"]  # KeyError raised if source_uid not found
        tuid = data["target_uid"]  # KeyError raised if target_uid not found

        if suid == tuid:
            self._logger.warning(f"Source and target UIDs are the same: {suid}")
            return str()

        if (suid, tuid) in self.database[guid].conns:
            self._logger.warning(f"Connection already exists!")
            return str()

        # Check if the source and target nodes have common streams. That is, there must be at least one output
        # stream in the source node that matches with an input stream in the target node
        if not self._verify_stream_matching(guid, suid, tuid):
            self._logger.warning(f"No matching streams between source and target!")
            self.cmds_bus.ui.notify.emit(
                guid,
                "ERROR: At least one matching stream required between source and target.\n"
                "Reconfigure the nodes and try again.",
            )
            return ""

        # Create a new edge instance
        _euid = uuid.uuid4().hex
        _edge = Edge(
            uid=_euid,
            source_uid=suid,
            target_uid=tuid,
        )

        # Store reference and update dictionaries
        self.database[guid].edges[_euid] = _edge
        self.database[guid].conns[(suid, tuid)] = True

        # Emit signal
        self.cmds_bus.ui.create_edge_repr.emit(guid, _euid, jstr)

        # Log after emitting signal
        self._logger.info(f"Created edge with UID {_euid}")

        return _euid

    @guid_validator
    def send_node_data(self, guid: str, nuid: str) -> None:

        # Graph UID is already validated by `guid_validator` decorator
        graph_node = self.database[guid].nodes.get(nuid, None)

        if graph_node:
            jstr = json.dumps(graph_node.to_dict())
            self.cmds_bus.ui.put_node_data.emit(nuid, jstr)

    @guid_validator
    def send_edge_data(self, guid: str, euid: str) -> None:
        pass

    @guid_validator
    def update_node_data(self, guid: str, nuid: str, jstr: str) -> None:

        _node = self.database[guid].nodes.get(nuid)
        if _node is None:
            self._logger.warning(f"Node [UID={nuid}] not found in graph [UID={guid}].")
            return

        try:
            data = json.loads(jstr)
        except json.JSONDecodeError as e:
            self._logger.warning(f"Invalid JSON for update_node_data: {e}")
            return

        # Update meta
        if "meta" in data:
            _node.meta.update(data["meta"])

        # Rebuild tech from JSON
        if "tech" in data:
            _node.tech.clear()
            for tech_name, tech_data in data["tech"].items():
                _node.tech[tech_name] = Technology.from_dict(tech_data)

        self._logger.info(f"Updated node [UID={nuid}]: {list(_node.tech.keys())}")
