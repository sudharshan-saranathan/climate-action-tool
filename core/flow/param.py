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

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "parameter")
        kwargs.setdefault("color", "#8b0000")
        kwargs.setdefault("label", "Parameter")
        kwargs.setdefault("image", "mdi.pound")
        super().__init__(**kwargs)


class Expense(Parameter):
    """Cost per unit of resource."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "expense")
        kwargs.setdefault("color", "#90ee90")
        kwargs.setdefault("label", "Expense")
        kwargs.setdefault("image", "mdi.cash-minus")
        units = ["INR/count", "INR/kg", "INR/tonne", "INR/MJ", "INR/GJ", "INR/kWh", "INR/MWh"]
        super().__init__(units=units, default=units[0], **kwargs)


class Revenue(Parameter):
    """Income per unit of product."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "revenue")
        kwargs.setdefault("color", "#90ee90")
        kwargs.setdefault("label", "Revenue")
        kwargs.setdefault("image", "mdi.cash-plus")
        units = ["INR/count", "INR/kg", "INR/tonne", "INR/MJ", "INR/GJ", "INR/kWh", "INR/MWh"]
        super().__init__(units=units, default=units[0], **kwargs)


class SpecificEnergy(Parameter):
    """Energy content per unit mass."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "specific_energy")
        kwargs.setdefault("color", "#ffcb00")
        kwargs.setdefault("label", "Specific Energy")
        kwargs.setdefault("image", "mdi.thermometer")
        units = ["kJ/kg", "MJ/kg", "GJ/tonne"]
        super().__init__(units=units, default=units[0], **kwargs)


class EmissionFactor(Parameter):
    """Emissions per unit of flow."""

    def __init__(self, **kwargs):
        kwargs.setdefault("key", "emission_factor")
        kwargs.setdefault("color", "#a9a9a9")
        kwargs.setdefault("label", "Emission Factor")
        kwargs.setdefault("image", "mdi.percent")
        units = ["kg/kg", "kg/tonne", "kg/kWh", "kg/MWh"]
        super().__init__(units=units, default=units[0], **kwargs)
