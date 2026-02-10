#  Filename: core/signals/__init__.py
#  Module name: core.signals
#  Description: Signal management for the application.

from __future__ import annotations
from typing import Dict, Optional

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

    @staticmethod
    def factory(*types) -> Signal:
        return field(default_factory=lambda: Signal(*types))


class SignalBus:
    """Session management for the application (Singleton)."""

    _instance = None

    @dataclass
    class Backend:

        create_graph: Signal = Signal.factory(str)
        delete_graph: Signal = Signal.factory(str)

        create_node_item: Signal = Signal.factory(str, str, Optional[Dict[str, object]])
        create_edge_item: Signal = Signal.factory(str, str, Optional[Dict[str, object]])
        delete_node_item: Signal = Signal.factory(str, str)
        delete_edge_item: Signal = Signal.factory(str, str)

    @dataclass
    class Frontend:

        create_node_repr: Signal = Signal.factory(str, str, Optional[Dict[str, object]])
        create_edge_repr: Signal = Signal.factory(str, str, Optional[Dict[str, object]])
        delete_node_repr: Signal = Signal.factory(str, str)
        delete_edge_repr: Signal = Signal.factory(str, str)

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self):

        # Only initialize once
        if self._initialized:
            return

        self.data = self.Backend()
        self.ui = self.Frontend()

        self._initialized = True
