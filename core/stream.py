# Filename: stream.py
# Module name: core
# Description: Stream types for graph connections.

"""
Stream type definitions for graph connections.

Defines different stream/flow types (Item, Mass, Energy, Credit) that can be
passed through graph edges. Each stream type has associated metadata like icons
and colors for visual representation.
"""

from __future__ import annotations
from typing import Dict, Type


# Base stream class
class Stream:
    """Base class representing a stream/flow type in the graph."""

    KEY: str = "stream"
    ICON: str = "mdi.water"
    COLOR: str = "#ffffff"
    LABEL: str = "Stream"
    UNITS: list = []
    DEFAULT: str = None

    def __repr__(self) -> str:
        return f"<Stream {self.KEY}>"


# Basic flow types
class ItemFlow(Stream):
    KEY = "item_flow"
    ICON = "mdi.package"
    COLOR = "#8a8a8a"
    LABEL = "Item"
    UNITS = ["count/year", "count/month"]
    DEFAULT = UNITS[0]


class MassFlow(Stream):
    KEY = "mass_flow"
    ICON = "mdi.weight-gram"
    COLOR = "#78cad2"
    LABEL = "Mass"
    UNITS = ["kg/year", "tonne/year"]
    DEFAULT = UNITS[0]


class EnergyFlow(Stream):
    KEY = "energy_flow"
    ICON = "mdi.fire"
    COLOR = "#ffa500"
    LABEL = "Energy"
    UNITS = ["kW", "MW", "GW"]
    DEFAULT = UNITS[0]


class CreditFlow(Stream):
    KEY = "credit_flow"
    ICON = "mdi.cash-multiple"
    COLOR = "#5eb616"
    LABEL = "Credit"
    UNITS = ["INR/year", "INR/month"]
    DEFAULT = UNITS[0]


# Dictionary of basic flows
BasicFlows: Dict[str, Type[Stream]] = {
    "ItemFlow": ItemFlow,
    "MassFlow": MassFlow,
    "EnergyFlow": EnergyFlow,
    "CreditFlow": CreditFlow,
}

# Dictionary of combo/derived flows (can be extended later)
ComboFlows: Dict[str, Type[Stream]] = {}
