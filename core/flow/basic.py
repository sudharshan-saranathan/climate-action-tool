# Filename: basic.py
# Module name: flow
# Description: Basic flow types.

"""
Basic stream/flow type definitions.
"""

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from qtawesome import icon

from dataclasses import field
from dataclasses import dataclass


class Flow:
    """Base class representing a stream/flow type in the graph."""

    @dataclass(frozen=True)
    class Attrs:
        key: str = "flow"
        color: int = "#ffffff"
        label: str = "Flow"
        image: QtGui.QIcon = field(
            default_factory=lambda: icon("mdi.minus", color="#ffffff")
        )

    def __init__(
        self,
        units: list[str] = None,
        default: str = str(),
        primary: float = None,
        params: dict[str, type] = None,
        **kwargs,
    ):

        # Instantiate dataclass
        self._attrs = Flow.Attrs(
            key=kwargs.get("key", Flow.Attrs.key),
            color=kwargs.get("color", Flow.Attrs.color),
            label=kwargs.get("label", Flow.Attrs.label),
            image=icon(
                kwargs.get("image", "mdi.minus"),
                color=kwargs.get("color", Flow.Attrs.color),
            ),
        )

        # Main class-members
        self.units = units or []
        self.default = default
        self.primary = primary
        self.params = params or {}

    @property
    def key(self):
        return self._attrs.key

    @property
    def color(self):
        return self._attrs.color

    @property
    def label(self):
        return self._attrs.label

    @property
    def image(self):
        return self._attrs.image

    def icon(self) -> QtGui.QIcon:
        return self._attrs.image


class ItemFlow(Flow):
    """Flow of countable items."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "item_flow")
        kwargs.setdefault("color", "#8a8a8a")
        kwargs.setdefault("label", "Item")
        kwargs.setdefault("image", "mdi.package")
        units = ["count/year", "count/month", "count/day", "count/hr", "count/s"]
        super().__init__(units=units, default=units[0], **kwargs)


class MassFlow(Flow):
    """Flow of mass (weight)."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "mass_flow")
        kwargs.setdefault("color", "#78cad2")
        kwargs.setdefault("label", "Mass")
        kwargs.setdefault("image", "mdi.weight-gram")
        units = [
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
        super().__init__(units=units, default=units[0], **kwargs)


class EnergyFlow(Flow):
    """Flow of energy."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "energy_flow")
        kwargs.setdefault("color", "#ffa500")
        kwargs.setdefault("label", "Energy")
        kwargs.setdefault("image", "mdi.fire")
        units = ["kW", "MW", "GW"]
        super().__init__(units=units, default=units[0], **kwargs)


class CreditFlow(Flow):
    """Flow of currency/credits."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "credit_flow")
        kwargs.setdefault("color", "#5eb616")
        kwargs.setdefault("label", "Credit")
        kwargs.setdefault("image", "mdi.cash-multiple")
        units = ["INR/year", "INR/month", "INR/day", "INR/hour", "INR/s"]
        super().__init__(units=units, default=units[0], **kwargs)
