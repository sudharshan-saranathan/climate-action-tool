"""Flow module - dimension-based flow architecture with time-varying profiles.

This module provides:
- Dimensions: Physical quantities (Mass, Volume, Energy, Currency, Temperature, Pressure)
- Flows: Dimension per time (MassFlow, VolumeFlow, EnergyFlow, CurrencyFlow)
- Profiles: Time-varying parameter values (Fixed, Linear, Stepped)
- Parameters: Flow properties with profile support (Temperature, Pressure, Factor, Ratio)
- Composite flows: Domain-specific flows (Fuel, Material, Product, Electricity, Fluid)
"""

from __future__ import annotations
from typing import Dict, Type

# Core dimensions
from core.flows.dimensions import (
    Dimension,
    Mass,
    Volume,
    Energy,
    Currency,
    Temperature,
    Pressure,
    Power,
)

# Time and flow mixin
from core.flows.time import Time, FlowMixin

# Profile system
from core.flows.profiles import (
    Profile,
    ProfileType,
    FixedProfile,
    LinearProfile,
    SteppedProfile,
    ProfileRef,
)

# Basic flows
from core.flows.flows import (
    MassFlow,
    VolumeFlow,
    EnergyFlow,
    CurrencyFlow,
)

# Parameters
from core.flows.parameters import (
    Parameter,
    TemperatureParam,
    PressureParam,
    Factor,
    Ratio,
)

# Composite flows
from core.flows.combos import (
    Fuel,
    Material,
    Product,
    Electricity,
    Fluid,
)

# === Lookup Dictionaries ===

ResourceDictionary: Dict[str, Type] = {
    "Mass": MassFlow,
    "Fuel": Fuel,
    "Fluid": Fluid,
    "Volume": VolumeFlow,
    "Energy": EnergyFlow,
    "Product": Product,
    "Currency": CurrencyFlow,
    "Material": Material,
    "Electricity": Electricity,
}

ParameterDictionary: Dict[str, Type[Parameter]] = {
    "temperature": TemperatureParam,
    "pressure": PressureParam,
}


# === Export Groups ===
FundamentalGroup = [MassFlow, VolumeFlow, EnergyFlow, CurrencyFlow]
CombinationGroup = [Fuel, Material, Product, Electricity, Fluid]
UniversalGroup = FundamentalGroup + CombinationGroup

# === Utility Functions ===


def get_params(flow_instance) -> dict:
    """Return Parameter dictionary associated with a flow instance.

    Args:
        flow_instance: A flow instance (MassFlow, Fuel, etc.)

    Returns:
        Dictionary of Parameter instances for this flow
    """
    return flow_instance.props


# === Public API ===

__all__ = [
    # Dimensions
    "Dimension",
    "Mass",
    "Volume",
    "Energy",
    "Currency",
    "Temperature",
    "Pressure",
    # Time
    "Time",
    "FlowMixin",
    # Profiles
    "Profile",
    "ProfileType",
    "FixedProfile",
    "LinearProfile",
    "SteppedProfile",
    "ProfileRef",
    # Dimensions
    "Power",
    # Basic flows
    "MassFlow",
    "VolumeFlow",
    "EnergyFlow",
    "CurrencyFlow",
    # Parameters
    "Parameter",
    "TemperatureParam",
    "PressureParam",
    "Factor",
    "Ratio",
    # Composite flows
    "Fuel",
    "Material",
    "Product",
    "Electricity",
    "Fluid",
    # Dictionaries
    "ResourceDictionary",
    "ParameterDictionary",
    # Groups
    "VirginStreams",
    "DerivedFlows",
    "TotalFlows",
    # Utilities
    "get_params",
]
