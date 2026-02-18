#  Filename: core/streams/physical.py
#  Module name: core.streams.fundamental
#  Description: SI base units (7 fundamental physical quantities)

from __future__ import annotations
from core.streams.quantity import Quantity


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
    "RampRate",
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


class Mass(Quantity):
    canonical = "kilogram"
    label = "Mass"
    _attr = "mass"


class Length(Quantity):
    canonical = "meter"
    label = "Length"


class Time(Quantity):
    canonical = "second"
    label = "Time"


class Temperature(Quantity):
    canonical = "kelvin"
    label = "Temperature"


class ElectricCurrent(Quantity):
    canonical = "ampere"
    label = "Electric Current"


class LuminousIntensity(Quantity):
    canonical = "candela"
    label = "Luminous Intensity"


class AmountOfSubstance(Quantity):
    canonical = "mole"
    label = "Amount of Substance"


# ============================================================================
# Derived Quantities - Mechanical
# ============================================================================


class Area(Quantity):
    canonical = "meter**2"
    label = "Area"


class Volume(Quantity):
    canonical = "meter**3"
    label = "Volume"


class Velocity(Quantity):
    canonical = "meter/second"
    label = "Velocity"


class Acceleration(Quantity):
    canonical = "meter/second**2"
    label = "Acceleration"


class Force(Quantity):
    canonical = "newton"
    label = "Force"


class Pressure(Quantity):
    canonical = "pascal"
    label = "Pressure"


class Energy(Quantity):
    canonical = "joule"
    label = "Energy"


class EnergyFlowRate(Quantity):
    canonical = "watt"
    label = "Energy Flow Rate"


class Momentum(Quantity):
    canonical = "kilogram*meter/second"
    label = "Momentum"


class AngularVelocity(Quantity):
    canonical = "radian/second"
    label = "Angular Velocity"


class SurfaceTension(Quantity):
    canonical = "newton/meter"
    label = "Surface Tension"


# ============================================================================
# Derived Quantities - Thermodynamic
# ============================================================================


class Entropy(Quantity):
    canonical = "joule/kelvin"
    label = "Entropy"


class SpecificHeatCapacity(Quantity):
    canonical = "joule/(kilogram*kelvin)"
    label = "Specific Heat Capacity"


class SpecificEnergy(Quantity):
    canonical = "joule/kilogram"
    label = "Specific Energy"


class ChemicalPotential(Quantity):
    canonical = "joule/mole"
    label = "Chemical Potential"


class MolarEntropy(Quantity):
    canonical = "joule/(mole*kelvin)"
    label = "Molar Entropy"


class ThermalConductivity(Quantity):
    canonical = "watt/(meter*kelvin)"
    label = "Thermal Conductivity"


class HeatTransferCoefficient(Quantity):
    canonical = "watt/(meter**2*kelvin)"
    label = "Heat Transfer Coefficient"


class ThermalResistance(Quantity):
    canonical = "kelvin/watt"
    label = "Thermal Resistance"


class ThermalExpansionCoefficient(Quantity):
    canonical = "1/kelvin"
    label = "Thermal Expansion Coefficient"


# ============================================================================
# Derived Quantities - Fluid Mechanics
# ============================================================================


class DynamicViscosity(Quantity):
    canonical = "pascal*second"
    label = "Dynamic Viscosity"


# ============================================================================
# Derived Quantities - Radiation (Dimensionless)
# ============================================================================


class Emissivity(Quantity):
    canonical = "dimensionless"
    label = "Emissivity"


class Absorptivity(Quantity):
    canonical = "dimensionless"
    label = "Absorptivity"


class Reflectivity(Quantity):
    canonical = "dimensionless"
    label = "Reflectivity"


class Transmittance(Quantity):
    canonical = "dimensionless"
    label = "Transmittance"


# ============================================================================
# Derived Quantities - Electromagnetic
# ============================================================================


class ElectricCharge(Quantity):
    canonical = "coulomb"
    label = "Electric Charge"


class Voltage(Quantity):
    canonical = "volt"
    label = "Voltage"


class Resistance(Quantity):
    canonical = "ohm"
    label = "Resistance"


class Capacitance(Quantity):
    canonical = "farad"
    label = "Capacitance"


class MagneticFlux(Quantity):
    canonical = "weber"
    label = "Magnetic Flux"


class MagneticFluxDensity(Quantity):
    canonical = "tesla"
    label = "Magnetic Flux Density"


class Inductance(Quantity):
    canonical = "henry"
    label = "Inductance"


class ElectricalConductivity(Quantity):
    canonical = "siemens/meter"
    label = "Electrical Conductivity"


class Resistivity(Quantity):
    canonical = "ohm*meter"
    label = "Resistivity"


# ============================================================================
# Derived Quantities - Chemical & Material
# ============================================================================


class Diffusivity(Quantity):
    canonical = "meter**2/second"
    label = "Diffusivity"


class CatalyticActivity(Quantity):
    canonical = "mole/second"
    label = "Catalytic Activity"


# ============================================================================
# Derived Quantities - Transport & Flow
# ============================================================================


class Frequency(Quantity):
    canonical = "hertz"
    label = "Frequency"


class Density(Quantity):
    canonical = "kilogram/meter**3"
    label = "Density"


class MolarMass(Quantity):
    canonical = "kilogram/mole"
    label = "Molar Mass"


class Concentration(Quantity):
    canonical = "mole/meter**3"
    label = "Concentration"


class VolumetricFlowRate(Quantity):
    canonical = "meter**3/second"
    label = "Volumetric Flow Rate"


class MassFlowRate(Quantity):
    canonical = "kilogram/second"
    label = "Mass Flow Rate"


class MassFlux(Quantity):
    canonical = "kilogram/(meter**2*second)"
    label = "Mass Flux"


class EnergyFlux(Quantity):
    canonical = "joule/(meter**2*second)"
    label = "Energy Flux"


class PowerDensity(Quantity):
    canonical = "watt/meter**3"
    label = "Power Density"


class SpecificPower(Quantity):
    canonical = "watt/kilogram"
    label = "Specific Power"


class CarbonIntensity(Quantity):
    canonical = "kilogram/joule"
    label = "Carbon Intensity"


class RampRate(Quantity):
    canonical = "watt/second"
    label = "Ramp Rate"


# ============================================================================
# Economic Quantities
# ============================================================================


class Currency(Quantity):
    canonical = "INR"
    label = "Currency"


class CostPerEnergy(Quantity):
    canonical = "INR/joule"
    label = "Cost per Energy"


class CostPerMass(Quantity):
    canonical = "INR/kilogram"
    label = "Cost per Mass"


class CostPerPower(Quantity):
    canonical = "INR/watt"
    label = "Cost per Power"


class CostPerVolume(Quantity):
    canonical = "INR/meter**3"
    label = "Cost per Volume"
