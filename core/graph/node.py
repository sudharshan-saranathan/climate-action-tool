# Filename: core/graph/node.py
# Module name: core.graph
# Description: A backend data-structure for bi-directional, multi-graphs

from __future__ import annotations

# Dataclass
from dataclasses import dataclass
from typing import Literal, Dict, Optional, Type


# Dataclass
@dataclass
class Node:

    uid: str
    name: str
    x: float
    y: float
    properties: Dict[str, str]

    @classmethod
    def from_node(cls, node: Node) -> Node:
        return cls(
            node.uid,
            node.name,
            node.x,
            node.y,
            node.properties,
        )

    @classmethod
    def from_dict(cls: Type[Node], data: dict) -> Node:
        return cls(data["uid"], data["name"], data["x"], data["y"], data["properties"])
