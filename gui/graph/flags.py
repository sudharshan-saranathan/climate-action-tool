# Filename: enums.py
# Module name: graph
# Description: Enum definitions for graph item types.

"""Enum definitions for graph item types."""

from enum import StrEnum
from PySide6 import QtWidgets


class GraphElementType(StrEnum):
    NODE = "node"
    EDGE = "edge"
    FLOW = "flow"


ItemState = QtWidgets.QStyle.StateFlag
