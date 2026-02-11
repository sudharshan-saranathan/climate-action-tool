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
            "consumed": self.consumed,
            "produced": self.produced,
            "expenses": {
                "capital": self.expenses.capital,
                "operating": self.expenses.operating,
            },
        }


# Dataclass
@dataclass
class Node:

    uid: str
    name: str
    meta: Dict[str, object]
    tech: dict[str, Any] = field(default_factory=dict)

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
            data.get("name", ""),
            data.get("meta", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "meta": self.meta,
            "tech": self.tech,
        }
