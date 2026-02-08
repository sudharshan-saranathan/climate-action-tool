# Filename: stream.py
# Module name: core
# Description: Stream types for graph connections (deprecated - use core.flow instead).

"""
Stream type definitions for graph connections.

This module is maintained for backwards compatibility.
New code should import from core.flow instead.
"""

from typing import Dict, Type
from core.flow import (
    MassFlow,
    VolumeFlow,
    EnergyFlow,
    CurrencyFlow,
    Parameter,
    TemperatureParam,
    PressureParam,
    Ratio,
    Fuel,
    Material,
    Electricity,
    Product,
    Fluid,
    BasicFlows,
    ComboFlows,
    AllFlows,
)

# Aliases for backwards compatibility
Flow = MassFlow  # Base flow was MassFlow in old architecture
ItemFlow = VolumeFlow  # Item was countable, VolumeFlow is similar
CreditFlow = CurrencyFlow  # Credit was currency
SpecificQuantity = Ratio  # SpecificQuantity was the old name for Ratio
Temperature = TemperatureParam
Pressure = PressureParam
Parameters = [TemperatureParam, PressureParam]

# Re-export for backwards compatibility
__all__ = [
    "Flow",
    "ItemFlow",
    "MassFlow",
    "VolumeFlow",
    "EnergyFlow",
    "CurrencyFlow",
    "CreditFlow",
    "Parameter",
    "TemperatureParam",
    "PressureParam",
    "Ratio",
    "SpecificQuantity",
    "Temperature",
    "Pressure",
    "Fuel",
    "Material",
    "Electricity",
    "Product",
    "Fluid",
    "BasicFlows",
    "Parameters",
    "ComboFlows",
    "AllFlows",
]
