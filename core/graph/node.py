# Filename: core/graph/node.py
# Module name: core.graph
# Description: A backend data-structure for bi-directional, multi-graphs

from __future__ import annotations

# Standard Library
from typing import Dict, Type, Any
from types import SimpleNamespace

import logging
import json

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# core.streams
from core.streams.quantity import ResourceStream


@dataclass
class Technology:
    consumed: dict[str, ResourceStream] = field(default_factory=dict)
    produced: dict[str, ResourceStream] = field(default_factory=dict)
    expenses: SimpleNamespace = field(
        default_factory=lambda: SimpleNamespace(
            capital=0,
            operating=0,
        )
    )

    params: dict[str, ResourceStream] = field(default_factory=dict)
    equations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "consumed": {
                name: stream.to_dict() for name, stream in self.consumed.items()
            },
            "produced": {
                name: stream.to_dict() for name, stream in self.produced.items()
            },
            "expenses": {
                "capital": self.expenses.capital,
                "operating": self.expenses.operating,
            },
            "params": {name: param.to_dict() for name, param in self.params.items()},
            "equations": self.equations,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Technology:
        """Reconstruct Technology from the dictionary."""

        return cls(
            consumed={
                name: ResourceStream.from_dict(stream_data)
                for name, stream_data in data.get("consumed", {}).items()
            },
            produced={
                name: ResourceStream.from_dict(stream_data)
                for name, stream_data in data.get("produced", {}).items()
            },
            expenses=SimpleNamespace(
                capital=data.get("expenses", {}).get("capital", 0),
                operating=data.get("expenses", {}).get("operating", 0),
            ),
            params={
                name: ResourceStream.from_dict(stream_data)
                for name, stream_data in data.get("params", {}).items()
            },
            equations=data.get("equations", []),
        )


# Dataclass
@dataclass(frozen=True)
class Node:

    uid: str
    meta: Dict[str, Any]
    tech: dict[str, Technology] = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.uid)

    def __eq__(self, other) -> bool:

        if not isinstance(other, Node):
            return False

        return self.uid == other.uid

    @classmethod
    def from_dict(cls: Type[Node], data: dict) -> Node:
        """Reconstruct Node from the dictionary with full Technology deserialization."""

        # Deserialize tech dictionary
        technology = {
            _name: Technology.from_dict(_data)
            for _name, _data in data.get("tech", {}).items()
        }

        return cls(
            uid=data.get("uid", ""),
            meta=data.get("meta", {}),
            tech=technology,
        )

    @classmethod
    def from_json(cls: Type[Node], jstr: str) -> Node:
        return cls.from_dict(json.loads(jstr))

    def to_dict(self) -> dict[str, Any]:

        return {
            "uid": self.uid,
            "meta": self.meta,
            "tech": {
                tech_name: tech.to_dict() for tech_name, tech in self.tech.items()
            },
        }

    def get_produced(self) -> set[str]:
        """
        Return this node's output streams as a set.
        :return: Set of produced stream names.
        """

        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.produced.keys()
        )

    def get_consumed(self) -> set[str]:
        """
        Return this node's input streams as a set.
        :return: Set of consumed stream names.
        """

        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.consumed.keys()
        )

    def set_branch(self, branch: str, jstr: str) -> None:
        """Set a specific branch of the technology tree for this node."""

        # Import SignalBus
        from core.signals import SignalBus

        try:
            dictionary = json.loads(jstr)
            self.tech[branch] = Technology.from_dict(dictionary)

        except json.JSONDecodeError as e:
            logging.warning(f"Invalid JSON for set_branch: {e}")
            bus = SignalBus()
            bus.ui.notify.emit(
                self.uid,
                f"ERROR: Invalid JSON for set_branch: {e}",
            )
