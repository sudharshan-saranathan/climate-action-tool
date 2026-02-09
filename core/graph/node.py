"""
Node: A graph vertex with properties.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
from uuid import uuid4


@dataclass
class Node:
    """
    A vertex in the graph.

    Attributes:
        uid: Unique identifier for the node
        name: Node type (e.g., "pump", "reactor", "separator")
        x: Visual x-coordinate
        y: Visual y-coordinate
        properties: Arbitrary key-value properties
    """

    uid: str
    name: str
    x: float
    y: float
    properties: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, name: str, x: float, y: float, uid: str = str(), **properties) -> "Node":
        """
        Factory method to create a node with optional auto-generated ID.

        Args:
            name: Node type
            x: Visual x-coordinate
            y: Visual y-coordinate
            uid: Optional ID (auto-generated if not provided)
            **properties: Additional properties

        Returns:
            New Node instance
        """
        return cls(
            uid=uid or uuid4(),
            name=name,
            x=x,
            y=y,
            properties=properties
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize node to dictionary."""
        return {
            "id": self.uid,
            "type": self.name,
            "x": self.x,
            "y": self.y,
            "properties": self.properties.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        """Deserialize node from dictionary."""
        return cls(
            uid=data["uid"],
            name=data["type"],
            x=data["x"],
            y=data["y"],
            properties=data.get("properties", {})
        )