#  Filename: core/streams/__init__.py
#  Module name: core.streams
#  Description: Physical quantity types with unit validation and automatic type dispatch

from __future__ import annotations

# Base class and registry
from core.streams.quantity import ResourceStream, ureg

# SI base units
from core.streams.physical import (
    Mass,
    Length,
    Time,
    Temperature,
    ElectricCurrent,
    LuminousIntensity,
    AmountOfSubstance,
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

# Composite resources
from core.streams.composite import Material, Electricity, FossilFuel

# Class registry for deserialization
CLASS_REGISTRY = {
    # Base
    "ResourceStream": ResourceStream,
    # Fundamental
    "Mass": Mass,
    "Length": Length,
    "Time": Time,
    "Temperature": Temperature,
    "ElectricCurrent": ElectricCurrent,
    "LuminousIntensity": LuminousIntensity,
    "AmountOfSubstance": AmountOfSubstance,
    # Derived - Mechanical
    "Area": Area,
    "Volume": Volume,
    "Velocity": Velocity,
    "Acceleration": Acceleration,
    "Force": Force,
    "Pressure": Pressure,
    "Energy": Energy,
    "Power": Power,
    "Momentum": Momentum,
    "AngularVelocity": AngularVelocity,
    "SpecificVolume": SpecificVolume,
    "SurfaceTension": SurfaceTension,
    # Derived - Thermodynamic
    "Entropy": Entropy,
    "SpecificHeatCapacity": SpecificHeatCapacity,
    "SpecificEnergy": SpecificEnergy,
    "ChemicalPotential": ChemicalPotential,
    "MolarEntropy": MolarEntropy,
    "ThermalConductivity": ThermalConductivity,
    "HeatTransferCoefficient": HeatTransferCoefficient,
    "HeatFlux": HeatFlux,
    "ThermalResistance": ThermalResistance,
    "ThermalExpansionCoefficient": ThermalExpansionCoefficient,
    # Derived - Fluid Mechanics
    "DynamicViscosity": DynamicViscosity,
    # Derived - Radiation
    "Emissivity": Emissivity,
    "Absorptivity": Absorptivity,
    "Reflectivity": Reflectivity,
    "Transmittance": Transmittance,
    # Derived - Electromagnetic
    "ElectricCharge": ElectricCharge,
    "Voltage": Voltage,
    "Resistance": Resistance,
    "Capacitance": Capacitance,
    "MagneticFlux": MagneticFlux,
    "MagneticFluxDensity": MagneticFluxDensity,
    "Inductance": Inductance,
    "ElectricalConductivity": ElectricalConductivity,
    "Resistivity": Resistivity,
    # Derived - Chemical & Material
    "Diffusivity": Diffusivity,
    "CatalyticActivity": CatalyticActivity,
    # Derived - Transport & Flow
    "Frequency": Frequency,
    "Density": Density,
    "MolarMass": MolarMass,
    "Concentration": Concentration,
    "VolumetricFlowRate": VolumetricFlowRate,
    "MassFlowRate": MassFlowRate,
    "PowerDensity": PowerDensity,
    "SpecificPower": SpecificPower,
    "CarbonIntensity": CarbonIntensity,
    # Derived - Economic
    "Currency": Currency,
    "CostPerEnergy": CostPerEnergy,
    "CostPerMass": CostPerMass,
    "CostPerPower": CostPerPower,
    "CostPerVolume": CostPerVolume,
    # Composite
    "Material": Material,
    "Electricity": Electricity,
    "FossilFuel": FossilFuel,
}


__all__ = [
    # Base
    "ResourceStream",
    "ureg",
    "CLASS_REGISTRY",
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
