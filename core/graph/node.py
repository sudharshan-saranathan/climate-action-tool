# Filename: core/graph/node.py
# Module name: core.graph
# Description: A backend data-structure for bi-directional, multi-graphs

from __future__ import annotations
from typing import Dict, Type, Any
from types import SimpleNamespace

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# core.streams
from core.streams.fundamental import Fundamental


@dataclass(frozen=True)
class Technology:
    consumed: dict[str, Fundamental] = field(default_factory=dict)
    produced: dict[str, Fundamental] = field(default_factory=dict)
    expenses: SimpleNamespace = field(
        default_factory=lambda: SimpleNamespace(
            capital=0,
            operating=0,
        )
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "consumed": {key: str(value) for key, value in self.consumed.items()},
            "produced": {key: str(value) for key, value in self.produced.items()},
            "expenses": {
                "capital": str(self.expenses.capital),
                "operating": str(self.expenses.operating),
            },
        }


# Dataclass
@dataclass
class Node:

    uid: str
    name: str
    meta: Dict[str, object]
    technology: dict[str, Any] = field(default_factory=dict)
    conjugates: set[str] = field(default_factory=set)

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
            data.get("label", ""),
            data.get("attrs", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "uid": self.uid,
            "label": self.name,
            "attrs": self.meta,
            "technology": self.technology,
            "conjugates": list(self.conjugates),
        }

    def is_connected_to(self, other: Node) -> bool:
        return other.uid in self.conjugates

    def get_attributes(self) -> str:
        return ", ".join(f"{key}: {value}" for key, value in self.meta.items())
