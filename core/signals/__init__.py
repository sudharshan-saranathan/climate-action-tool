#  Filename: core/signals/__init__.py
#  Module name: core.signals
#  Description: Signal management for the application.

from __future__ import annotations

# Standard
from typing import Dict, Optional, Any
import logging
import uuid

# Dataclass
from dataclasses import field
from dataclasses import dataclass


class Signal:
    """A pure Python implementation of a Signal."""

    _logger = logging.getLogger("Signal")

    def __init__(self, *types):
        self._types = types
        self._listeners = dict()

    def connect(self, listener):

        uid = listener.uid if hasattr(listener, "uid") else uuid.uuid4().hex
        self._listeners[uid] = listener

    def emit(self, *args, **kwargs):

        for listener in self._listeners.values():

            try:
                listener(*args, **kwargs)

            except Exception as e:

                import traceback

                self._logger.error(f"Error in signal listener: {e}")
                self._logger.debug(f"Listener: {listener}")
                self._logger.debug(f"Args: {args}")
                traceback.print_exc()

    @staticmethod
    def factory(*types) -> Signal:
        return field(default_factory=lambda: Signal(*types))


class SignalBus:
    """Session management for the application (Singleton)."""

    _instance = None
    _logger = logging.getLogger("SignalBus")

    @dataclass
    class Graph:

        create_graph: Signal = Signal.factory(str)
        delete_graph: Signal = Signal.factory(str)

        create_node_item: Signal = Signal.factory(str, str)  # guid, payload
        create_edge_item: Signal = Signal.factory(str, str)  # guid, payload
        delete_node_item: Signal = Signal.factory(str, str)  # guid, nuid
        delete_edge_item: Signal = Signal.factory(str, str)  # guid, euid

        send_node_data: Signal = Signal.factory(str, str)  # guid, nuid, payload
        send_edge_data: Signal = Signal.factory(str, str)  # guid, euid, payload

    @dataclass
    class Graphics:

        create_node_repr: Signal = Signal.factory(str, str, str)  # guid, nuid, payload
        create_edge_repr: Signal = Signal.factory(str, str, str)  # guid, euid, payload
        delete_node_repr: Signal = Signal.factory(str, str)  # guid, nuid
        delete_edge_repr: Signal = Signal.factory(str, str)  # guid, euid
        publish_node_data: Signal = Signal.factory(str, str)  # nuid, payload
        publish_edge_data: Signal = Signal.factory(str, str)  # euid, payload

        notify: Signal = Signal.factory(str, str)  # guid, nuid/euid

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self):

        # Only initialize once
        if self._initialized:
            return

        self.data = self.Graph()
        self.ui = self.Graphics()

        self._init_signal_dictionary()
        self._initialized = True

    def _init_signal_dictionary(self) -> None:

        self._signal_dictionary = {
            "create_graph": self.data.create_graph,
            "delete_graph": self.data.delete_graph,
            # Target: Backend
            "create_node_item": self.data.create_node_item,
            "create_edge_item": self.data.create_edge_item,
            "delete_node_item": self.data.delete_node_item,
            "delete_edge_item": self.data.delete_edge_item,
            "send_node_data": self.data.send_node_data,
            "send_edge_data": self.data.send_edge_data,
            # Target: Frontend
            "create_node_repr": self.ui.create_node_repr,
            "create_edge_repr": self.ui.create_edge_repr,
            "delete_node_repr": self.ui.delete_node_repr,
            "delete_edge_repr": self.ui.delete_edge_repr,
            "publish_node_data": self.ui.publish_node_data,
            "publish_edge_data": self.ui.publish_edge_data,
        }

    def raise_request(
        self,
        command: str,
        *args,
    ) -> None:
        """Raise a signal to create a node in the graph identified by GUID, name, and data.

        Arguments:
            command [str]: The command to be executed. Commands include:
                - "create_node_item": Create a new backend node item in the graph.
                - "create_edge_item": Create a new backend edge item in the graph.
                - "delete_node_item": Delete a backend node item from the graph.
                - "delete_edge_item": Delete a backend edge item from the graph.
                - "create_node_repr": Create a new frontend node representation in the canvas.
                - "create_edge_repr": Create a new frontend edge representation in the canvas.
                - "delete_node_repr": Delete a frontend node representation from the canvas.
                - "delete_edge_repr": Delete a frontend edge representation from the canvas.
            guid [str]: The unique identifier of the graph.
            name [str]: The name of the node.
            payload [str]: The data payload for the node (JSON String). Can include the following keys:
                - "x": The x-coordinate of the node in the QGraphicsScene.
                - "y": The y-coordinate of the node in the QGraphicsScene.
                - "source_uid": The unique identifier of the source node for an edge.
                - "target_uid": The unique identifier of the target node for an edge.
        """

        signal = self._signal_dictionary.get(command, None)
        if signal is None:
            self._logger.warning(f"Invalid request type: {command}")
            return

        signal.emit(*args)
