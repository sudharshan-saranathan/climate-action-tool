# Filename: enums.py
# Module name: graph
# Description: Enum definitions for graph item types.

"""Enum definitions for graph item types."""

from enum import Enum


class ItemState(Enum):
    NORMAL = 0
    HIDDEN = 1
    SELECTED = 2
