# Filename: core/graph/node.py
# Module name: core.graph
# Description: A backend data-structure for bi-directional, multi-graphs

from __future__ import annotations
from typing import Dict, Type, Any
from types import SimpleNamespace
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
            "consumed": self.consumed,
            "produced": self.produced,
            "expenses": {
                "capital": self.expenses.capital,
                "operating": self.expenses.operating,
            },
        }


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

        return cls(
            data.get("uid", ""),
            data.get("meta", {}),
            data.get("tech", {}),
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

    def produced(self) -> set[str]:

        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.produced.keys()
        )

    def consumed(self) -> set[str]:

        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.consumed.keys()
        )
