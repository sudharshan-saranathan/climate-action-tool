from __future__ import annotations
from enum import StrEnum
from .node import NodeRepr
from .edge import EdgeRepr
from .canvas import Canvas
from .reusable.image import Image
from .reusable.label import Label


class GraphElementType(StrEnum):
    NODE = "NodeRepr"
    EDGE = "EdgeRepr"
    FLOW = "FlowRepr"


__all__ = [
    "GraphElementType",
    "NodeRepr",
    "EdgeRepr",
    "Canvas",
    "Image",
    "Label",
]
