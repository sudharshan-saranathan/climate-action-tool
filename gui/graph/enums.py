# Filename: enums.py
# Module name: graph
# Description: Enums for graph item roles and states.

"""
Enumeration types for graph items.

Defines ItemRole (input, output, parameter, equation) and ItemState (active, hidden)
used throughout the graph module for type-safe item classification.
"""

from __future__ import annotations
import enum


class ItemRole(enum.Enum):
    """Represents the functional role of a graph item."""

    INP = enum.auto()  # Input/sink connection
    OUT = enum.auto()  # Output/source connection
    PAR = enum.auto()  # Parameter
    EQN = enum.auto()  # Equation


class ItemState(enum.Enum):
    """Represents the visibility/active state of a graph item."""

    HIDDEN = 0  # Item is hidden (isVisible() == False)
    ACTIVE = 1  # Item is visible and active (isVisible() == True)
