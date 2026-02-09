# Filename: core/graph/edge.py
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

    @classmethod
    def from_dict(cls: Type[Edge], data: dict) -> Edge:
        return cls(data["uid"], data["source_uid"], data["target_uid"], data["properties"])
