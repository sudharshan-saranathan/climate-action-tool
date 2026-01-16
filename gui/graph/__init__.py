# Schematic module initialization
from .enums import ItemRole, ItemState
from .vertex import VertexItem
from .vector import VectorItem
from .anchor import AnchorItem
from .handle import HandleItem
from .canvas import Canvas


# Global Graph-items registry
GraphItemsRegistry = {
    "VertexItem": VertexItem,
    "VectorItem": VectorItem,
}


__all__ = [
    "ItemRole",
    "ItemState",
    "VertexItem",
    "VectorItem",
    "AnchorItem",
    "HandleItem",
    "Canvas",
    "GraphItemsRegistry",
]
