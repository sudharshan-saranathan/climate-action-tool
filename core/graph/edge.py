# Filename: core/graph/__init__.py
# Module name: core.graph
# Description: Edge dataclass for graph connections

from __future__ import annotations

# Dataclass
from dataclasses import dataclass
from typing import Type, Dict


@dataclass
class Edge:

    uid: str
    source_uid: str
    target_uid: str
    properties: Dict[str, str]

    def __hash__(self) -> int:
        return hash(self.uid)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Edge):
            return False

        return self.uid == other.uid

    @classmethod
    def from_dict(cls: Type[Edge], data: dict) -> Edge:
        return cls(
            data.get("uid", ""),
            data.get("source_uid", ""),
            data.get("target_uid", ""),
            data.get("properties", {}),
        )
