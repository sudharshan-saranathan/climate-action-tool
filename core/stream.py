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
    Flow,
    ItemFlow,
    MassFlow,
    EnergyFlow,
    CreditFlow,
    Parameter,
    SpecificQuantity,
    Temperature,
    Pressure,
    Fuel,
    Material,
    Power,
    Product,
    BasicFlows,
    Parameters,
    ComboFlows,
    AllFlows,
)

# Re-export for backwards compatibility
__all__ = [
    "Flow",
    "ItemFlow",
    "MassFlow",
    "EnergyFlow",
    "CreditFlow",
    "Parameter",
    "SpecificQuantity",
    "Temperature",
    "Pressure",
    "Fuel",
    "Material",
    "Power",
    "Product",
    "BasicFlows",
    "Parameters",
    "ComboFlows",
    "AllFlows",
]
