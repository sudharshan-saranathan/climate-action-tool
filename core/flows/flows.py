# Filename: flows.py
# Module name: flow
# Description: Basic flow types combining dimensions with time.

"""
Basic flow types representing different physical quantities per unit time.

Each flow combines a physical dimension with FlowMixin to create
flow rates with appropriate units:
    MassFlow: mass per time (kg/hr, g/s, etc.)
    VolumeFlow: volume per time (L/min, m³/day, etc.)
    EnergyFlow: energy per time / power (kW, MJ/hr, etc.)
    CurrencyFlow: currency per time / flow rate (USD/yr, INR/day, etc.)
"""

from __future__ import annotations

from PySide6 import QtGui
from qtawesome import icon
from typing import ClassVar
from dataclasses import dataclass

from core.flows.dimensions import Mass, Volume, Energy, Currency, Power
from core.flows.time import FlowMixin


class MassFlow(FlowMixin, Mass):
    """Flow of mass per unit time."""

    @dataclass(frozen=True)
    class Attrs(Mass.Attrs):
        keyID: ClassVar[str] = "mass"
        label: ClassVar[str] = "Mass"


class VolumeFlow(FlowMixin, Volume):
    """Flow of volume per unit time."""

    @dataclass(frozen=True)
    class Attrs(Volume.Attrs):
        keyID: ClassVar[str] = "volume"
        label: ClassVar[str] = "Volume"


class EnergyFlow(FlowMixin, Energy):
    """Flow of energy per unit time (power)."""

    @dataclass(frozen=True)
    class Attrs(Energy.Attrs):
        keyID: ClassVar[str] = "energy"
        label: ClassVar[str] = "Energy"


class CurrencyFlow(FlowMixin, Currency):
    """Flow of currency per unit time."""

    @dataclass(frozen=True)
    class Attrs(Currency.Attrs):
        keyID: ClassVar[str] = "currency"
        label: ClassVar[str] = "Currency"
