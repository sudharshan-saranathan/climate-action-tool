# Filename: param.py
# Module name: flow
# Description: Parameter types for flows.

"""
Parameter and SpecificQuantity classes for flow attributes.

Parameter: A known input value with fixed units (Temperature, Pressure, etc.)
SpecificQuantity:  A ratio of two flow/parameter types — units are auto-generated
           from the cross-product of numerator and denominator units.
"""

from __future__ import annotations

from PySide6 import QtGui
from qtawesome import icon
from typing import ClassVar
from dataclasses import dataclass


class Parameter:
    """Base class for standalone parameters (known input values, not computed)."""

    @dataclass(frozen=True)
    class Attrs:
        keyID: ClassVar[str] = "parameter"
        color: ClassVar[str] = "#8b0000"
        label: ClassVar[str] = "Parameter"
        units: ClassVar[list[str]] = []
        image: ClassVar[QtGui.QIcon] = icon("mdi.pound", color="#8b0000")

    def __init__(self):
        self.value = 0.0

    @property
    def label(self) -> str:
        return self.Attrs.label

    @property
    def image(self) -> QtGui.QIcon:
        return self.Attrs.image

    @property
    def color(self) -> str:
        return self.Attrs.color

    @property
    def units(self) -> list[str]:
        return self.Attrs.units


class Temperature(Parameter):
    """Temperature parameter."""

    @dataclass(frozen=True)
    class Attrs(Parameter.Attrs):
        keyID: ClassVar[str] = "temperature"
        color: ClassVar[str] = "#ff6347"
        label: ClassVar[str] = "Temperature"
        units: ClassVar[list[str]] = ["K", "°C", "°F"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.thermometer", color="#ff6347")


class Pressure(Parameter):
    """Pressure parameter."""

    @dataclass(frozen=True)
    class Attrs(Parameter.Attrs):
        keyID: ClassVar[str] = "pressure"
        color: ClassVar[str] = "#4682b4"
        label: ClassVar[str] = "Pressure"
        units: ClassVar[list[str]] = ["Pa", "kPa", "MPa", "bar", "atm"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.gauge", color="#4682b4")


class SpecificQuantity(Parameter):
    """A ratio parameter derived from two types (numerator/denominator).

    Units are the cross-product: [n/d for n in numerator.units for d in denominator.units].

    Examples:
        SpecificQuantity(CreditFlow, MassFlow)   → INR/grams, INR/kgs, USD/tonnes, ...
        SpecificQuantity(EnergyFlow, MassFlow)   → J/grams, kJ/kgs, MJ/tonnes, ...
        SpecificQuantity(MassFlow, MassFlow)     → grams/grams, kgs/kgs, ...  (emission factors)
    """

    def __init__(self, numerator: type, denominator: type, label: str = None):
        super().__init__()
        self._numerator = numerator
        self._denominator = denominator
        self._label = label

    @property
    def label(self) -> str:
        return self._label or f"{self._numerator.Attrs.label.lower()}_per_{self._denominator.Attrs.label.lower()}"

    @property
    def image(self) -> QtGui.QIcon:
        return self._numerator.Attrs.image

    @property
    def units(self) -> list[str]:
        num_units = self._numerator.Attrs.units
        den_units = self._denominator.Attrs.units
        return [f"{n}/{d}" for n in num_units for d in den_units]
