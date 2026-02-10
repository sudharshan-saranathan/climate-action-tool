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
                print(f"Error: {e}")


class Manager:
    """Session management for the application."""

    @dataclass
    class GraphCommands:

        @staticmethod
        def _sig(*types):
            return field(default_factory=Signal(*types))

        create_node_item: Signal = _sig(int, str, Dict[str, object])
        create_edge_item: Signal = _sig(int, str, Dict[str, object])
        delete_node_item: Signal = _sig(int, str)
        delete_edge_item: Signal = _sig(int, str)

    @dataclass
    class SceneCommands:

        @staticmethod
        def _sig(*types):
            return field(default_factory=Signal(*types))

        create_node_repr: Signal = _sig(int, str, Dict[str, object])
        create_edge_repr: Signal = _sig(int, str, Dict[str, object])
        delete_node_repr: Signal = _sig(int, str)
        delete_edge_repr: Signal = _sig(int, str)

    def __init__(self):
        self.graph_commands = self.GraphCommands()
        self.scene_commands = self.SceneCommands()
