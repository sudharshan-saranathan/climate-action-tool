"""Flow module - stream and parameter definitions."""

from __future__ import annotations
from typing import Dict, Type
from core.flow.basic import Flow, Item, Mass, Energy, Credit
from core.flow.param import Parameter, SpecificQuantity, Temperature, Pressure
from core.flow.combo import Fuel, Material, Electricity, Product

# Dictionaries for lookup by KEY
ResourceDictionary: Dict[str, Type[Flow]] = {
    "item": Item,
    "mass": Mass,
    "energy": Energy,
    "credit": Credit,
    "fuel": Fuel,
    "material": Material,
    "electricity": Electricity,
    "product": Product,
}

ParameterDictionary: Dict[str, Type[Parameter]] = {
    "temperature": Temperature,
    "pressure": Pressure,
}


def get_params(flow_instance) -> list:
    """Return Parameter classes associated with a flow instance."""
    return flow_instance.props


__all__ = [
    # Basic flows
    "Flow",
    "Item",
    "Mass",
    "Energy",
    "Credit",
    # Parameters
    "Parameter",
    "SpecificQuantity",
    "Temperature",
    "Pressure",
    # Combo flows
    "Fuel",
    "Material",
    "Electricity",
    "Product",
    # Dictionaries
    "ResourceDictionary",
    "ParameterDictionary",
    # Utilities
    "get_params",
]
