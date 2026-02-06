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

from core.flow.basic import MassFlow, EnergyFlow, CreditFlow
from core.flow.param import SpecificQuantity


class Fuel(MassFlow):
    """Fuel flow with energy content, emission factors, and cost."""

    @dataclass(frozen=True)
    class Attrs(MassFlow.Attrs):
        keyID: ClassVar[str] = "fuel"
        color: ClassVar[str] = "#bd8b9c"
        label: ClassVar[str] = "Fuel"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gas-station", color="#bd8b9c")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(EnergyFlow, MassFlow, label="specific_energy"),
                SpecificQuantity(MassFlow, MassFlow, label="emission_factor"),
                SpecificQuantity(CreditFlow, MassFlow, label="cost"),
            ]
        )


class Material(MassFlow):
    """Material flow with cost information."""

    @dataclass(frozen=True)
    class Attrs(MassFlow.Attrs):
        keyID: ClassVar[str] = "material"
        color: ClassVar[str] = "#f63c6b"
        label: ClassVar[str] = "Material"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gold", color="#f63c6b")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(CreditFlow, MassFlow, label="cost"),
            ]
        )


class Electricity(EnergyFlow):
    """Power/Electricity flow with cost."""

    @dataclass(frozen=True)
    class Attrs(EnergyFlow.Attrs):
        keyID: ClassVar[str] = "electricity"
        color: ClassVar[str] = "#8491a3"
        label: ClassVar[str] = "Electricity"
        image: ClassVar[QtGui.QIcon] = icon("mdi.flash", color="#8491a3")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(CreditFlow, EnergyFlow, label="tariff"),
            ]
        )


class Product(MassFlow):
    """Product flow with revenue information."""

    @dataclass(frozen=True)
    class Attrs(MassFlow.Attrs):
        keyID: ClassVar[str] = "product"
        color: ClassVar[str] = "#c5ff99"
        label: ClassVar[str] = "Product"
        image: ClassVar[QtGui.QIcon] = icon("mdi.cube", color="#c5ff99")

    def __init__(self):
        super().__init__(
            props=[
                SpecificQuantity(CreditFlow, MassFlow, label="revenue"),
            ]
        )
