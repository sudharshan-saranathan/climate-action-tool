# Filename: core/graph/node.py
# Module name: core.graph
# Description: A backend data-structure for bi-directional, multi-graphs

from __future__ import annotations

# Dataclass
from dataclasses import dataclass
from typing import Dict, Type


# Dataclass
@dataclass
class Node:

    uid: str
    name: str
    x: float
    y: float
    properties: Dict[str, str]

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
            data.get("x", 0.0),
            data.get("y", 0.0),
            data.get("properties", {}),
        )
