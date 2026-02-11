#  Filename: core/streams/fundamental.py
#  Module name: core.streams.fundamental
#  Description: SI base units (7 fundamental physical quantities)

from __future__ import annotations
from core.streams.quantity import ResourceStream


__all__ = [
    "Mass",
    "Length",
    "Time",
    "Temperature",
    "ElectricCurrent",
    "LuminousIntensity",
    "AmountOfSubstance",
]


# ============================================================================
# SI Base Units
# ============================================================================


class Mass(ResourceStream):
    _canonical = "kilogram"
    _label = "Mass"


class Length(ResourceStream):
    _canonical = "meter"
    _label = "Length"


class Time(ResourceStream):
    _canonical = "second"
    _label = "Time"


class Temperature(ResourceStream):
    _canonical = "kelvin"
    _label = "Temperature"


class ElectricCurrent(ResourceStream):
    _canonical = "ampere"
    _label = "Electric Current"


class LuminousIntensity(ResourceStream):
    _canonical = "candela"
    _label = "Luminous Intensity"


class AmountOfSubstance(ResourceStream):
    _canonical = "mole"
    _label = "Amount of Substance"
