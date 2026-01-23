# Filename: param.py
# Module name: flow
# Description: Parameter types for derived flows.

"""
Parameter classes for flow attributes (expense, revenue, emission factors, etc).
"""

from __future__ import annotations
from core.flow.basic import Flow


class Parameter(Flow):
    """Base class for stream parameters."""

    KEY: str = "parameter"
    ICON: str = "mdi.pound"
    COLOR: str = "#8b0000"
    LABEL: str = "Parameter"
    UNITS: list = []
    DEFAULT: str = None


class Expense(Parameter):
    """Cost per unit of resource."""

    KEY = "expense"
    ICON = "mdi.cash-minus"
    COLOR = "#90ee90"
    LABEL = "Expense"
    UNITS = [
        "INR/count",
        "INR/kg",
        "INR/tonne",
        "INR/MJ",
        "INR/GJ",
        "INR/kWh",
        "INR/MWh",
    ]
    DEFAULT = UNITS[0]


class Revenue(Parameter):
    """Income per unit of product."""

    KEY = "revenue"
    ICON = "mdi.cash-plus"
    COLOR = "#90ee90"
    LABEL = "Revenue"
    UNITS = [
        "INR/count",
        "INR/kg",
        "INR/tonne",
        "INR/MJ",
        "INR/GJ",
        "INR/kWh",
        "INR/MWh",
    ]
    DEFAULT = UNITS[0]


class SpecificEnergy(Parameter):
    """Energy content per unit mass."""

    KEY = "specific_energy"
    ICON = "mdi.thermometer"
    COLOR = "#ffcb00"
    LABEL = "Specific Energy"
    UNITS = ["kJ/kg", "MJ/kg", "GJ/tonne"]
    DEFAULT = UNITS[0]


class EmissionFactor(Parameter):
    """Emissions per unit of flow."""

    KEY = "emission_factor"
    ICON = "mdi.percent"
    COLOR = "#a9a9a9"
    LABEL = "Emission Factor"
    UNITS = ["kg/kg", "kg/tonne", "kg/kWh", "kg/MWh"]
    DEFAULT = UNITS[0]
