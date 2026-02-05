# Filename: combo.py
# Module name: flow
# Description: Derived/combo flow types.

"""
Derived flow types that combine basic flows with parameters.
"""

from __future__ import annotations
from core.flow.basic import MassFlow, EnergyFlow
from core.flow.param import Expense, Revenue, SpecificEnergy, EmissionFactor


class Fuel(MassFlow):
    """Fuel flow with energy content, emission factors, and cost."""

    def __init__(self):
        _se, _ef, _ex = SpecificEnergy(), EmissionFactor(), Expense()
        super().__init__(
            key="fuel", color="#bd8b9c", label="Fuel", image="mdi.gas-station",
            primary=MassFlow,
            params={_se.key: _se, _ef.key: _ef, _ex.key: _ex},
        )


class Material(MassFlow):
    """Material flow with cost information."""

    def __init__(self):
        _ex = Expense()
        super().__init__(
            key="material", color="#f63c6b", label="Material", image="mdi.gold",
            primary=MassFlow,
            params={_ex.key: _ex},
        )


class Power(EnergyFlow):
    """Power/Electricity flow with cost."""

    def __init__(self):
        _ex = Expense()
        super().__init__(
            key="power", color="#8491a3", label="Power", image="mdi.flash",
            primary=EnergyFlow,
            params={_ex.key: _ex},
        )


class Product(MassFlow):
    """Product flow with revenue information."""

    def __init__(self):
        _rv = Revenue()
        super().__init__(
            key="product", color="#c5ff99", label="Product", image="mdi.cube",
            primary=MassFlow,
            params={_rv.key: _rv},
        )
