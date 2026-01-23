# Filename: basic.py
# Module name: flow
# Description: Basic flow types.

"""
Basic stream/flow type definitions.
"""

from __future__ import annotations


class Flow:
    """Base class representing a stream/flow type in the graph."""

    KEY: str = "flow"
    ICON: str = "mdi.water"
    COLOR: str = "#ffffff"
    LABEL: str = "Flow"
    UNITS: list = []
    DEFAULT: str = None

    def __repr__(self) -> str:
        return f"<Stream {self.KEY}>"


class ItemFlow(Flow):
    """Flow of countable items."""

    KEY = "item_flow"
    ICON = "mdi.package"
    COLOR = "#8a8a8a"
    LABEL = "Item"
    UNITS = ["count/year", "count/month", "count/day", "count/hr", "count/s"]
    DEFAULT = UNITS[0]


class MassFlow(Flow):
    """Flow of mass (weight)."""

    KEY = "mass_flow"
    ICON = "mdi.weight-gram"
    COLOR = "#78cad2"
    LABEL = "Mass"
    UNITS = [
        "kg/year",
        "kg/month",
        "kg/day",
        "kg/hr",
        "kg/s",
        "tonne/year",
        "tonne/month",
        "tonne/day",
        "tonne/hour",
        "tonne/s",
    ]
    DEFAULT = UNITS[0]


class EnergyFlow(Flow):
    """Flow of energy."""

    KEY = "energy_flow"
    ICON = "mdi.fire"
    COLOR = "#ffa500"
    LABEL = "Energy"
    UNITS = ["kW", "MW", "GW"]
    DEFAULT = UNITS[0]


class CreditFlow(Flow):
    """Flow of currency/credits."""

    KEY = "credit_flow"
    ICON = "mdi.cash-multiple"
    COLOR = "#5eb616"
    LABEL = "Credit"
    UNITS = ["INR/year", "INR/month", "INR/day", "INR/hour", "INR/s"]
    DEFAULT = UNITS[0]
