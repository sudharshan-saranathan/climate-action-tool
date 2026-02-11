#  Filename: core/streams/__init__.py
#  Module name: core.streams
#  Description: Physical quantity types with unit validation and automatic type dispatch

from __future__ import annotations

# Base class and registry
from core.streams.quantity import ResourceStream, ureg

# SI base units
from core.streams.fundamental import (
    Mass,
    Length,
    Time,
    Temperature,
    ElectricCurrent,
    LuminousIntensity,
    AmountOfSubstance,
)

# Derived units
from core.streams.derived import (
    # Mechanical
    Area,
    Volume,
    Velocity,
    Acceleration,
    Force,
    Pressure,
    Energy,
    Power,
    Momentum,
    AngularVelocity,
    SpecificVolume,
    SurfaceTension,
    # Thermodynamic
    Entropy,
    SpecificHeatCapacity,
    SpecificEnergy,
    ChemicalPotential,
    MolarEntropy,
    ThermalConductivity,
    HeatTransferCoefficient,
    HeatFlux,
    ThermalResistance,
    ThermalExpansionCoefficient,
    # Fluid Mechanics
    DynamicViscosity,
    # Radiation
    Emissivity,
    Absorptivity,
    Reflectivity,
    Transmittance,
    # Electromagnetic
    ElectricCharge,
    Voltage,
    Resistance,
    Capacitance,
    MagneticFlux,
    MagneticFluxDensity,
    Inductance,
    ElectricalConductivity,
    Resistivity,
    # Chemical & Material
    Diffusivity,
    CatalyticActivity,
    # Transport & Flow
    Frequency,
    Density,
    MolarMass,
    Concentration,
    VolumetricFlowRate,
    MassFlowRate,
    PowerDensity,
    SpecificPower,
    CarbonIntensity,
    # Economic
    Currency,
    CostPerEnergy,
    CostPerMass,
    CostPerPower,
    CostPerVolume,
)


__all__ = [
    # Base
    "ResourceStream",
    "ureg",
    # Fundamental
    "Mass",
    "Length",
    "Time",
    "Temperature",
    "ElectricCurrent",
    "LuminousIntensity",
    "AmountOfSubstance",
    # Derived - Mechanical
    "Area",
    "Volume",
    "Velocity",
    "Acceleration",
    "Force",
    "Pressure",
    "Energy",
    "Power",
    "Momentum",
    "AngularVelocity",
    "SpecificVolume",
    "SurfaceTension",
    # Derived - Thermodynamic
    "Entropy",
    "SpecificHeatCapacity",
    "SpecificEnergy",
    "ChemicalPotential",
    "MolarEntropy",
    "ThermalConductivity",
    "HeatTransferCoefficient",
    "HeatFlux",
    "ThermalResistance",
    "ThermalExpansionCoefficient",
    # Derived - Fluid Mechanics
    "DynamicViscosity",
    # Derived - Radiation
    "Emissivity",
    "Absorptivity",
    "Reflectivity",
    "Transmittance",
    # Derived - Electromagnetic
    "ElectricCharge",
    "Voltage",
    "Resistance",
    "Capacitance",
    "MagneticFlux",
    "MagneticFluxDensity",
    "Inductance",
    "ElectricalConductivity",
    "Resistivity",
    # Derived - Chemical & Material
    "Diffusivity",
    "CatalyticActivity",
    # Derived - Transport & Flow
    "Frequency",
    "Density",
    "MolarMass",
    "Concentration",
    "VolumetricFlowRate",
    "MassFlowRate",
    "PowerDensity",
    "SpecificPower",
    "CarbonIntensity",
    # Derived - Economic
    "Currency",
    "CostPerEnergy",
    "CostPerMass",
    "CostPerPower",
    "CostPerVolume",
]
