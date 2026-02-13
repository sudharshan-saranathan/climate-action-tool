#  Filename: core/streams/physical.py
#  Module name: core.streams.fundamental
#  Description: SI base units (7 fundamental physical quantities)

from __future__ import annotations
from core.streams.quantity import ResourceStream


__all__ = [
    "Mass",
    "Length",
    "Time",
    "Temperature",
    "ElectricCurrent",
    "LuminousIntensity",
    "AmountOfSubstance",
    # Mechanical
    "Area",
    "Volume",
    "Velocity",
    "Acceleration",
    "Force",
    "Pressure",
    "Energy",
    "EnergyFlowRate",
    "Momentum",
    "AngularVelocity",
    "SpecificVolume",
    "SurfaceTension",
    # Thermodynamic
    "Entropy",
    "SpecificHeatCapacity",
    "SpecificEnergy",
    "ChemicalPotential",
    "MolarEntropy",
    "ThermalConductivity",
    "HeatTransferCoefficient",
    "ThermalResistance",
    "ThermalExpansionCoefficient",
    # Fluid Mechanics
    "DynamicViscosity",
    # Radiation
    "Emissivity",
    "Absorptivity",
    "Reflectivity",
    "Transmittance",
    # Electromagnetic
    "ElectricCharge",
    "Voltage",
    "Resistance",
    "Capacitance",
    "MagneticFlux",
    "MagneticFluxDensity",
    "Inductance",
    "ElectricalConductivity",
    "Resistivity",
    # Chemical & Material
    "Diffusivity",
    "CatalyticActivity",
    # Transport & Flow
    "Frequency",
    "Density",
    "MolarMass",
    "Concentration",
    "VolumetricFlowRate",
    "MassFlowRate",
    "MassFlux",
    "EnergyFlux",
    "PowerDensity",
    "SpecificPower",
    "CarbonIntensity",
    # Economic
    "Currency",
    "CostPerEnergy",
    "CostPerMass",
    "CostPerPower",
    "CostPerVolume",
]


# ============================================================================
# SI Base Units
# ============================================================================


class Mass(ResourceStream):
    _canonical = "kilogram"
    _label = "Mass"


class Length(ResourceStream):
    _canonical = "meter"
    _label = "Length"


class Time(ResourceStream):
    _canonical = "second"
    _label = "Time"


class Temperature(ResourceStream):
    _canonical = "kelvin"
    _label = "Temperature"


class ElectricCurrent(ResourceStream):
    _canonical = "ampere"
    _label = "Electric Current"


class LuminousIntensity(ResourceStream):
    _canonical = "candela"
    _label = "Luminous Intensity"


class AmountOfSubstance(ResourceStream):
    _canonical = "mole"
    _label = "Amount of Substance"


# ============================================================================
# Derived Quantities - Mechanical
# ============================================================================


class Area(ResourceStream):
    _canonical = "meter**2"
    _label = "Area"


class Volume(ResourceStream):
    _canonical = "meter**3"
    _label = "Volume"


class Velocity(ResourceStream):
    _canonical = "meter/second"
    _label = "Velocity"


class Acceleration(ResourceStream):
    _canonical = "meter/second**2"
    _label = "Acceleration"


class Force(ResourceStream):
    _canonical = "newton"
    _label = "Force"


class Pressure(ResourceStream):
    _canonical = "pascal"
    _label = "Pressure"


class Energy(ResourceStream):
    _canonical = "joule"
    _label = "Energy"


class EnergyFlowRate(ResourceStream):
    _canonical = "watt"
    _label = "Energy Flow Rate"


class Momentum(ResourceStream):
    _canonical = "kilogram*meter/second"
    _label = "Momentum"


class AngularVelocity(ResourceStream):
    _canonical = "radian/second"
    _label = "Angular Velocity"


class SpecificVolume(ResourceStream):
    _canonical = "meter**3/kilogram"
    _label = "Specific Volume"


class SurfaceTension(ResourceStream):
    _canonical = "newton/meter"
    _label = "Surface Tension"


# ============================================================================
# Derived Quantities - Thermodynamic
# ============================================================================


class Entropy(ResourceStream):
    _canonical = "joule/kelvin"
    _label = "Entropy"


class SpecificHeatCapacity(ResourceStream):
    _canonical = "joule/(kilogram*kelvin)"
    _label = "Specific Heat Capacity"


class SpecificEnergy(ResourceStream):
    _canonical = "joule/kilogram"
    _label = "Specific Energy"


class ChemicalPotential(ResourceStream):
    _canonical = "joule/mole"
    _label = "Chemical Potential"


class MolarEntropy(ResourceStream):
    _canonical = "joule/(mole*kelvin)"
    _label = "Molar Entropy"


class ThermalConductivity(ResourceStream):
    _canonical = "watt/(meter*kelvin)"
    _label = "Thermal Conductivity"


class HeatTransferCoefficient(ResourceStream):
    _canonical = "watt/(meter**2*kelvin)"
    _label = "Heat Transfer Coefficient"


class ThermalResistance(ResourceStream):
    _canonical = "kelvin/watt"
    _label = "Thermal Resistance"


class ThermalExpansionCoefficient(ResourceStream):
    _canonical = "1/kelvin"
    _label = "Thermal Expansion Coefficient"


# ============================================================================
# Derived Quantities - Fluid Mechanics
# ============================================================================


class DynamicViscosity(ResourceStream):
    _canonical = "pascal*second"
    _label = "Dynamic Viscosity"


# ============================================================================
# Derived Quantities - Radiation (Dimensionless)
# ============================================================================


class Emissivity(ResourceStream):
    _canonical = "dimensionless"
    _label = "Emissivity"


class Absorptivity(ResourceStream):
    _canonical = "dimensionless"
    _label = "Absorptivity"


class Reflectivity(ResourceStream):
    _canonical = "dimensionless"
    _label = "Reflectivity"


class Transmittance(ResourceStream):
    _canonical = "dimensionless"
    _label = "Transmittance"


# ============================================================================
# Derived Quantities - Electromagnetic
# ============================================================================


class ElectricCharge(ResourceStream):
    _canonical = "coulomb"
    _label = "Electric Charge"


class Voltage(ResourceStream):
    _canonical = "volt"
    _label = "Voltage"


class Resistance(ResourceStream):
    _canonical = "ohm"
    _label = "Resistance"


class Capacitance(ResourceStream):
    _canonical = "farad"
    _label = "Capacitance"


class MagneticFlux(ResourceStream):
    _canonical = "weber"
    _label = "Magnetic Flux"


class MagneticFluxDensity(ResourceStream):
    _canonical = "tesla"
    _label = "Magnetic Flux Density"


class Inductance(ResourceStream):
    _canonical = "henry"
    _label = "Inductance"


class ElectricalConductivity(ResourceStream):
    _canonical = "siemens/meter"
    _label = "Electrical Conductivity"


class Resistivity(ResourceStream):
    _canonical = "ohm*meter"
    _label = "Resistivity"


# ============================================================================
# Derived Quantities - Chemical & Material
# ============================================================================


class Diffusivity(ResourceStream):
    _canonical = "meter**2/second"
    _label = "Diffusivity"


class CatalyticActivity(ResourceStream):
    _canonical = "mole/second"
    _label = "Catalytic Activity"


# ============================================================================
# Derived Quantities - Transport & Flow
# ============================================================================


class Frequency(ResourceStream):
    _canonical = "hertz"
    _label = "Frequency"


class Density(ResourceStream):
    _canonical = "kilogram/meter**3"
    _label = "Density"


class MolarMass(ResourceStream):
    _canonical = "kilogram/mole"
    _label = "Molar Mass"


class Concentration(ResourceStream):
    _canonical = "mole/meter**3"
    _label = "Concentration"


class VolumetricFlowRate(ResourceStream):
    _canonical = "meter**3/second"
    _label = "Volumetric Flow Rate"


class MassFlowRate(ResourceStream):
    _canonical = "kilogram/second"
    _label = "Mass Flow Rate"


class MassFlux(ResourceStream):
    _canonical = "kilogram/(meter**2*second)"
    _label = "Mass Flux"


class EnergyFlux(ResourceStream):
    _canonical = "joule/(meter**2*second)"
    _label = "Energy Flux"


class PowerDensity(ResourceStream):
    _canonical = "watt/meter**3"
    _label = "Power Density"


class SpecificPower(ResourceStream):
    _canonical = "watt/kilogram"
    _label = "Specific Power"


class CarbonIntensity(ResourceStream):
    _canonical = "kilogram/joule"
    _label = "Carbon Intensity"


# ============================================================================
# Economic Quantities
# ============================================================================


class Currency(ResourceStream):
    _canonical = "INR"
    _label = "Currency"


class CostPerEnergy(ResourceStream):
    _canonical = "INR/joule"
    _label = "Cost per Energy"


class CostPerMass(ResourceStream):
    _canonical = "INR/kilogram"
    _label = "Cost per Mass"


class CostPerPower(ResourceStream):
    _canonical = "INR/watt"
    _label = "Cost per Power"


class CostPerVolume(ResourceStream):
    _canonical = "INR/meter**3"
    _label = "Cost per Volume"
