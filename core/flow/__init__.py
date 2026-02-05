"""Flow module - stream and parameter definitions."""

from __future__ import annotations
from typing import Dict, Type
from core.flow.basic import Flow, ItemFlow, MassFlow, EnergyFlow, CreditFlow
from core.flow.param import Parameter, Expense, Revenue, SpecificEnergy, EmissionFactor
from core.flow.combo import Fuel, Material, Power, Product

# Dictionaries for lookup by KEY
BasicFlows: Dict[str, Type[Flow]] = {
    "item_flow": ItemFlow,
    "mass_flow": MassFlow,
    "energy_flow": EnergyFlow,
    "credit_flow": CreditFlow,
}

Parameters: Dict[str, Type[Parameter]] = {
    "expense": Expense,
    "revenue": Revenue,
    "specific_energy": SpecificEnergy,
    "emission_factor": EmissionFactor,
}

ComboFlows: Dict[str, Type[Flow]] = {
    "fuel": Fuel,
    "material": Material,
    "power": Power,
    "product": Product,
}

# All flows combined
AllFlows: Dict[str, Type[Flow]] = {
    **BasicFlows,
    **ComboFlows,
}


def get_params(flow_instance) -> list:
    """Return Parameter classes associated with a flow instance."""
    return flow_instance.params

__all__ = [
    # Basic flows
    "Flow",
    "ItemFlow",
    "MassFlow",
    "EnergyFlow",
    "CreditFlow",
    # Parameters
    "Parameter",
    "Expense",
    "Revenue",
    "SpecificEnergy",
    "EmissionFactor",
    # Combo flows
    "Fuel",
    "Material",
    "Power",
    "Product",
    # Dictionaries
    "BasicFlows",
    "Parameters",
    "ComboFlows",
    "AllFlows",
    # Utilities
    "get_params",
]
