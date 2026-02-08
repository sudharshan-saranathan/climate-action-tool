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
from core.flow.dimensions import (
    Dimension,
    Mass,
    Volume,
    Energy,
    Currency,
    Temperature,
    Pressure,
)

# Time and flow mixin
from core.flow.time import Time, FlowMixin

# Profile system
from core.flow.profiles import (
    Profile,
    ProfileType,
    FixedProfile,
    LinearProfile,
    SteppedProfile,
    ProfileRef,
)

# Basic flows
from core.flow.flows import (
    MassFlow,
    VolumeFlow,
    EnergyFlow,
    CurrencyFlow,
)

# Parameters
from core.flow.parameters import (
    Parameter,
    TemperatureParam,
    PressureParam,
    Factor,
    Ratio,
)

# Composite flows
from core.flow.combos import (
    Fuel,
    Material,
    Product,
    Electricity,
    Fluid,
)


# === Lookup Dictionaries ===

ResourceDictionary: Dict[str, Type[FlowMixin]] = {
    "mass_flow": MassFlow,
    "volume_flow": VolumeFlow,
    "energy_flow": EnergyFlow,
    "currency_flow": CurrencyFlow,
    "fuel": Fuel,
    "material": Material,
    "electricity": Electricity,
    "product": Product,
    "fluid": Fluid,
}

ParameterDictionary: Dict[str, Type[Parameter]] = {
    "temperature": TemperatureParam,
    "pressure": PressureParam,
}


# === Export Groups ===

BasicFlows = [MassFlow, VolumeFlow, EnergyFlow, CurrencyFlow]
ComboFlows = [Fuel, Material, Product, Electricity, Fluid]
AllFlows = BasicFlows + ComboFlows


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
    "BasicFlows",
    "ComboFlows",
    "AllFlows",
    # Utilities
    "get_params",
]
