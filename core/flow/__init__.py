"""Flow module - stream and parameter definitions."""

from __future__ import annotations
from typing import Dict, Type
from core.flow.basic import Flow, ItemFlow, MassFlow, EnergyFlow, CreditFlow
from core.flow.param import Parameter, SpecificQuantity, Temperature, Pressure
from core.flow.combo import Fuel, Material, Electricity, Product

# Dictionaries for lookup by KEY
BasicFlows: Dict[str, Type[Flow]] = {
    "item_flow": ItemFlow,
    "mass_flow": MassFlow,
    "energy_flow": EnergyFlow,
    "credit_flow": CreditFlow,
}

Parameters: Dict[str, Type[Parameter]] = {
    "temperature": Temperature,
    "pressure": Pressure,
}

ComboFlows: Dict[str, Type[Flow]] = {
    "fuel": Fuel,
    "material": Material,
    "electricity": Electricity,
    "product": Product,
}

# All flows combined
AllFlows: Dict[str, Type[Flow]] = {
    **BasicFlows,
    **ComboFlows,
}


def get_params(flow_instance) -> list:
    """Return Parameter classes associated with a flow instance."""
    return flow_instance.props


__all__ = [
    # Basic flows
    "Flow",
    "ItemFlow",
    "MassFlow",
    "EnergyFlow",
    "CreditFlow",
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
    "BasicFlows",
    "Parameters",
    "ComboFlows",
    "AllFlows",
    # Utilities
    "get_params",
]
