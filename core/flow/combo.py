# Filename: combo.py
# Module name: flow
# Description: Derived/combo flow types.

"""
Derived flow types that combine basic flows with parameters.
"""

from __future__ import annotations
from core.flow.basic import MassFlow, EnergyFlow


class Fuel(MassFlow):
    """Fuel flow with energy content and emission factors."""

    KEY = "fuel"
    ICON = "mdi.gas-station"
    COLOR = "#bd8b9c"
    LABEL = "Fuel"


class Material(MassFlow):
    """Material flow with cost information."""

    KEY = "material"
    ICON = "mdi.gold"
    COLOR = "#f63c6b"
    LABEL = "Material"


class Power(EnergyFlow):
    """Power/Electricity flow with cost."""

    KEY = "power"
    ICON = "mdi.flash"
    COLOR = "#8491a3"
    LABEL = "Power"


class Product(MassFlow):
    """Product flow with revenue information."""

    KEY = "product"
    ICON = "mdi.cube"
    COLOR = "#c5ff99"
    LABEL = "Product"
