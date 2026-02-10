#  Filename: core/session/__init__.py
#  Module name: core.session
#  Description: Session management for the application.

from __future__ import annotations
from typing import Callable, Any, Dict

# Dataclass
from dataclasses import field
from dataclasses import dataclass


class Signal:
    """A pure Python implementation of a Signal."""

    def __init__(self, *types):
        self._types = types
        self._listeners = []

    def connect(self, listener):
        self._listeners.append(listener)

    def emit(self, *args, **kwargs):
        for listener in self._listeners:

            try:
                listener(*args, **kwargs)
            except Exception as e:
                import traceback

                print(f"Error in signal listener: {e}")
                print(f"Listener: {listener}")
                print(f"Args: {args}")
                traceback.print_exc()


class SignalBus:
    """Session management for the application (Singleton)."""

    _instance = None

    @dataclass
    class GraphCommands:

        def _sig(*types):
            return field(default_factory=lambda: Signal(*types))

        create_new_graph: Signal = _sig(int)
        create_node_item: Signal = _sig(int, str, Dict[str, object])
        create_edge_item: Signal = _sig(int, str, Dict[str, object])
        delete_node_item: Signal = _sig(int, str)
        delete_edge_item: Signal = _sig(int, str)

    @dataclass
    class SceneCommands:

        def _sig(*types):
            return field(default_factory=lambda: Signal(*types))

        create_node_repr: Signal = _sig(int, str, Dict[str, object])
        create_edge_repr: Signal = _sig(int, str, Dict[str, object])
        delete_node_repr: Signal = _sig(int, str)
        delete_edge_repr: Signal = _sig(int, str)

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self):

        # Only initialize once
        if self._initialized:
            return

        self.graph_commands = self.GraphCommands()
        self.scene_commands = self.SceneCommands()

        self._initialized = True
