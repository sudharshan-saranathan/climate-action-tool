# Filename: dimensions.py
# Module name: flow
# Description: Base dimension classes representing physical quantities.

"""
Physical dimension classes with metadata (color, icon, label, units).

Each dimension represents a fundamental physical quantity:
- Mass: weight/mass
- Volume: spatial volume
- Energy: thermal/mechanical energy
- Currency: monetary value
- Temperature: thermal intensity
- Pressure: force per area

Dimensions form the basis for flow types (e.g., MassFlow = Mass / Time).
"""

from __future__ import annotations

from abc import ABC
from PySide6 import QtGui
from qtawesome import icon
from typing import ClassVar
from dataclasses import dataclass

import pint

ureg = pint.UnitRegistry()


class Dimension(ABC):
    """Abstract base class for physical dimensions with metadata."""

    @dataclass(frozen=True)
    class Attrs:
        """Metadata for a dimension (color, icon, label, units)."""

        keyID: ClassVar[str] = "dimension"
        color: ClassVar[str] = "#ffffff"
        label: ClassVar[str] = "Dimension"
        units: ClassVar[list[str]] = []
        image: ClassVar[QtGui.QIcon] = icon("mdi.help-circle", color="#ffffff")

    @property
    def label(self) -> str:
        """Display label for this dimension."""
        return self.Attrs.label

    @property
    def image(self) -> QtGui.QIcon:
        """Icon for this dimension."""
        return self.Attrs.image

    @property
    def color(self) -> str:
        """Color code for this dimension."""
        return self.Attrs.color

    @property
    def units(self) -> list[str]:
        """Available units for this dimension."""
        return self.Attrs.units


class Mass(Dimension):
    """Mass/weight dimension."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "mass"
        color: ClassVar[str] = "#78cad2"
        label: ClassVar[str] = "Mass"
        units: ClassVar[list[str]] = [
            ureg.gram,
            ureg.kilogram,
            ureg.metric_ton,
        ]
        image: ClassVar[QtGui.QIcon] = icon("mdi.weight-gram", color="#78cad2")


class Volume(Dimension):
    """Volume dimension."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "volume"
        color: ClassVar[str] = "#87ceeb"
        label: ClassVar[str] = "Volume"
        units: ClassVar[list[str]] = ["L", "m³", "gal"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.cube", color="#87ceeb")


class Energy(Dimension):
    """Energy dimension."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "energy"
        color: ClassVar[str] = "#ffa500"
        label: ClassVar[str] = "Energy"
        units: ClassVar[list[str]] = ["J", "kJ", "MJ", "GJ"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.fire", color="#ffa500")


class Currency(Dimension):
    """Currency/monetary value dimension."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "currency"
        color: ClassVar[str] = "#5eb616"
        label: ClassVar[str] = "Currency"
        units: ClassVar[list[str]] = ["INR", "USD", "EUR"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.cash-multiple", color="#5eb616")


class Temperature(Dimension):
    """Temperature dimension."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "temperature"
        color: ClassVar[str] = "#ff6347"
        label: ClassVar[str] = "Temperature"
        units: ClassVar[list[str]] = ["K", "°C", "°F"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.thermometer", color="#ff6347")


class Pressure(Dimension):
    """Pressure dimension."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "pressure"
        color: ClassVar[str] = "#4682b4"
        label: ClassVar[str] = "Pressure"
        units: ClassVar[list[str]] = ["Pa", "kPa", "MPa", "bar", "atm"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.gauge", color="#4682b4")


class Power(Dimension):
    """Power dimension - rate of energy delivery (fundamental, not derived)."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "power"
        color: ClassVar[str] = "#8491a3"
        label: ClassVar[str] = "Power"
        units: ClassVar[list[str]] = ["W", "kW", "MW", "GW"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.flash", color="#8491a3")
