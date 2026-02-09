"""
Edge: A directed connection between nodes.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
from uuid import uuid4


@dataclass
class Edge:
    """
    A directed edge connecting two nodes.

    Attributes:
        id: Unique identifier for the edge
        source: ID of the source node
        target: ID of the target node
        type: Edge type (e.g., "material", "energy", "signal")
        properties: Arbitrary key-value properties
    """

    id: str
    source: str
    target: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        source: str,
        target: str,
        type: str,
        id: str | None = None,
        **properties
    ) -> "Edge":
        """
        Factory method to create an edge with optional auto-generated ID.

        Args:
            source: ID of source node
            target: ID of target node
            type: Edge type
            id: Optional ID (auto-generated if not provided)
            **properties: Additional properties

        Returns:
            New Edge instance
        """
        return cls(
            id=id or str(uuid4())[:8],
            source=source,
            target=target,
            type=type,
            properties=properties
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize edge to dictionary."""
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "type": self.type,
            "properties": self.properties.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge":
        """Deserialize edge from dictionary."""
        return cls(
            id=data["id"],
            source=data["source"],
            target=data["target"],
            type=data["type"],
            properties=data.get("properties", {})
        )
