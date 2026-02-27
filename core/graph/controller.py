# Filename: core/graph/controller.py
# Module Name: core.graph.controller
# Description: Graph controller for managing graph data structure.

from __future__ import annotations


# Standard
import logging
import typing
import uuid
import json


# Dataclass
from dataclasses import field
from dataclasses import dataclass


# Climact Module(s): core.graph
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

        self._initialized = True

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

    async def create_graph(self, guid: str) -> dict:

        if guid in self.database:
            self._logger.warning(f"Graph with GUID {guid} already exists.")
            return {
                "status": "FAILED",
                "reason": f"Graph with GUID {guid} already exists.",
            }

        self.database[guid] = GraphController.Graph()
        return {
            "status": "OK",
            "response": {
                "guid": guid,
                "nodes": {},
                "edges": {},
            },
        }

    @guid_validator
    @json_parser
    async def create_node(self, guid: str, data: dict) -> dict:

        _nuid = uuid.uuid4().hex
        _node = Node(
            nuid=_nuid,
            meta=data,
        )

        # Store node reference
        self.database[guid].nodes[_nuid] = _node

        # Log after creation
        self._logger.info(f"Created node with UID {_nuid}")

        return {
            "status": "OK",
            "response": {
                "nuid": _nuid,
                "data": _node.to_dict() if hasattr(_node, "to_dict") else {},
            },
        }

    @guid_validator
    @json_parser
    async def create_edge(self, guid: str, data: dict) -> dict:

        try:
            suid = data["source_uid"]
            tuid = data["target_uid"]
        except KeyError as e:
            return {
                "status": "FAILED",
                "reason": f"Missing required field: {e}",
            }

        if suid == tuid:
            self._logger.warning(f"Source and target UIDs are the same: {suid}")
            return {
                "status": "FAILED",
                "reason": "Source and target UIDs cannot be the same.",
            }

        if (suid, tuid) in self.database[guid].conns:
            self._logger.warning(f"Connection already exists!")
            return {
                "status": "FAILED",
                "reason": "Connection already exists between these nodes.",
            }

        # Check if the source and target nodes have common streams
        if not self._verify_stream_matching(guid, suid, tuid):
            self._logger.warning(f"No matching streams between source and target!")
            return {
                "status": "FAILED",
                "reason": "At least one matching stream required between source and target.",
            }

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

        # Log after creation
        self._logger.info(f"Created edge with UID {_euid}")

        return {
            "status": "OK",
            "response": {
                "euid": _euid,
                "source_uid": suid,
                "target_uid": tuid,
            },
        }

    @guid_validator
    async def send_node_data(self, guid: str, nuid: str) -> dict:

        graph_node = self.database[guid].nodes.get(nuid)

        if not graph_node:
            return {
                "status": "FAILED",
                "reason": f"Node [UID={nuid}] not found.",
            }

        return {
            "status": "OK",
            "response": graph_node.to_dict() if hasattr(graph_node, "to_dict") else {},
        }

    @guid_validator
    async def send_edge_data(self, guid: str, euid: str) -> dict:

        graph_edge = self.database[guid].edges.get(euid)

        if not graph_edge:
            return {
                "status": "FAILED",
                "reason": f"Edge [UID={euid}] not found.",
            }

        return {
            "status": "OK",
            "response": {
                "euid": euid,
                "source_uid": graph_edge.source_uid,
                "target_uid": graph_edge.target_uid,
            },
        }

    @guid_validator
    @json_parser
    async def update_node_data(self, guid: str, data: dict, nuid: str = None) -> dict:

        if nuid is None:
            nuid = data.get("nuid")
            if not nuid:
                return {
                    "status": "FAILED",
                    "reason": "Missing 'nuid' field.",
                }

        _node = self.database[guid].nodes.get(nuid)
        if _node is None:
            self._logger.warning(f"Node [UID={nuid}] not found in graph [UID={guid}].")
            return {
                "status": "FAILED",
                "reason": f"Node [UID={nuid}] not found.",
            }

        # Update meta
        if "meta" in data:
            _node.meta.update(data["meta"])

        # Rebuild tech from JSON
        if "tech" in data:
            _node.tech.clear()
            for tech_name, tech_data in data["tech"].items():
                _node.tech[tech_name] = Technology.from_dict(tech_data)

        self._logger.info(f"Updated node [UID={nuid}]: {list(_node.tech.keys())}")

        return {
            "status": "OK",
            "response": {
                "nuid": nuid,
                "updated_fields": list(data.keys()),
            },
        }


def executable() -> typing.Callable:
    """
    Returns an async callable that routes graph commands to the controller.

    Expected payload format (JSON):
    {
        "guid": "graph-uuid",
        "data": {...action-specific data...}
    }
    """
    controller = GraphController()

    async def execute(action: str, payload: str) -> dict:
        try:
            data = json.loads(payload) if payload else {}
        except json.JSONDecodeError as e:
            return {
                "status": "FAILED",
                "reason": f"Invalid JSON payload: {e}",
            }

        guid = data.get("guid")
        if not guid:
            return {
                "status": "FAILED",
                "reason": "Missing 'guid' field in payload.",
            }

        # Route to appropriate method
        if action == "create_graph":
            return await controller.create_graph(guid)

        elif action == "create_node":
            node_data = data.get("data", {})
            return await controller.create_node(guid, json.dumps(node_data))

        elif action == "create_edge":
            edge_data = data.get("data", {})
            return await controller.create_edge(guid, json.dumps(edge_data))

        elif action == "get_node":
            nuid = data.get("nuid")
            if not nuid:
                return {
                    "status": "FAILED",
                    "reason": "Missing 'nuid' field.",
                }
            return await controller.send_node_data(guid, nuid)

        elif action == "get_edge":
            euid = data.get("euid")
            if not euid:
                return {
                    "status": "FAILED",
                    "reason": "Missing 'euid' field.",
                }
            return await controller.send_edge_data(guid, euid)

        elif action == "update_node":
            nuid = data.get("nuid")
            node_data = data.get("data", {})
            if not nuid:
                return {
                    "status": "FAILED",
                    "reason": "Missing 'nuid' field.",
                }
            return await controller.update_node_data(guid, json.dumps(node_data), nuid)

        else:
            _logger = logging.getLogger("core.graph")
            _logger.warning(f"Unknown graph action: {action}")
            return {
                "status": "FAILED",
                "reason": f"Unknown action: {action}",
            }

    return execute
