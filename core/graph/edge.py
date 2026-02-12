# Filename: core/graph/__init__.py
# Module name: core.graph
# Description: Edge dataclass for graph connections

from __future__ import annotations

# Standard
from typing import Type, Dict

# Dataclass
from dataclasses import field
from dataclasses import dataclass


@dataclass
class Edge:

    uid: str
    source_uid: str
    target_uid: str
    payload: Dict[str, str] = field(default_factory=dict)

    # Hash based on uid
    def __hash__(self) -> int:
        return hash(self.uid)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Edge):
            return False

        return self.uid == other.uid

    @classmethod
    def from_dict(cls: Type[Edge], data: dict) -> Edge:

        source = data.get("source_uid")
        target = data.get("target_uid")
        payload = data.get("payload", {})

        return cls(
            data.get("uid", ""),
            source,
            target,
            payload=payload,
        )
