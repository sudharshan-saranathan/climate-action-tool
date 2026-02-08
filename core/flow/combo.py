# Filename: combo.py
# Module name: flow
# Description: Derived/combo flow types.

"""
Derived flow types that combine basic flows with parameters.
"""

from __future__ import annotations

from PySide6 import QtGui
from qtawesome import icon
from typing import ClassVar
from dataclasses import dataclass

from core.flow.basic import Mass, Energy, Credit
from core.flow.param import SpecificQuantity, Temperature, Pressure, Factor


class Fuel(Mass):
    """Fuel flow with energy content, emission factors, and cost."""

    @dataclass(frozen=True)
    class Attrs(Mass.Attrs):
        keyID: ClassVar[str] = "fuel"
        color: ClassVar[str] = "#bd8b9c"
        label: ClassVar[str] = "Fuel"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gas-station", color="#bd8b9c")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(Energy, Mass, label="specific_energy"),
                SpecificQuantity(Mass, Mass, label="emission_factor"),
                SpecificQuantity(Credit, Mass, label="cost"),
            ]
        )


class Material(Mass):
    """Material flow with cost information."""

    @dataclass(frozen=True)
    class Attrs(Mass.Attrs):
        keyID: ClassVar[str] = "material"
        color: ClassVar[str] = "#f63c6b"
        label: ClassVar[str] = "Material"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gold", color="#f63c6b")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(Credit, Mass, label="cost"),
            ]
        )


class Electricity(Energy):
    """Power/Electricity flow with cost, emissions, and grid characteristics."""

    @dataclass(frozen=True)
    class Attrs(Energy.Attrs):
        keyID: ClassVar[str] = "electricity"
        color: ClassVar[str] = "#8491a3"
        label: ClassVar[str] = "Electricity"
        image: ClassVar[QtGui.QIcon] = icon("mdi.flash", color="#8491a3")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(Credit, Energy, label="tariff"),
                SpecificQuantity(Mass, Energy, label="emissions_factor"),
                Factor("Variability", color="#daa520", icon_name="mdi.sine-wave"),
                Factor("Ramp Rate", color="#20b2aa", icon_name="mdi.speedometer"),
            ]
        )


class Product(Mass):
    """Product flow with revenue information."""

    @dataclass(frozen=True)
    class Attrs(Mass.Attrs):
        keyID: ClassVar[str] = "product"
        color: ClassVar[str] = "#c5ff99"
        label: ClassVar[str] = "Product"
        image: ClassVar[QtGui.QIcon] = icon("mdi.cube", color="#c5ff99")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(Credit, Mass, label="revenue"),
            ]
        )


class Fluid(Mass):
    """Fluid flow with thermodynamic properties."""

    @dataclass(frozen=True)
    class Attrs(Mass.Attrs):
        keyID: ClassVar[str] = "fluid"
        color: ClassVar[str] = "#1e90ff"
        label: ClassVar[str] = "Fluid"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gas-cylinder", color="#ffd791")

    def __init__(self):
        super().__init__(
            props=[
                Temperature(),
                Pressure(),
            ]
        )
