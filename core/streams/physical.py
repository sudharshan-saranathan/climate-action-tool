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
    _canonical = "kilogram"
    _label = "Mass"
    _keywords_alias = ["mass"]


class Length(Quantity):
    _canonical = "meter"
    _label = "Length"
    _keywords_alias = ["length", "distance"]


class Time(Quantity):
    _canonical = "second"
    _label = "Time"
    _keywords_alias = ["time", "period", "duration"]


class Temperature(Quantity):
    _canonical = "kelvin"
    _label = "Temperature"
    _keywords_alias = ["temperature", "thermodynamic_temperature"]


class ElectricCurrent(Quantity):
    _canonical = "ampere"
    _label = "Electric Current"
    _keywords_alias = ["electric_current", "current"]


class LuminousIntensity(Quantity):
    _canonical = "candela"
    _label = "Luminous Intensity"
    _keywords_alias = ["luminous_intensity", "luminous_flux", "brightness"]


class AmountOfSubstance(Quantity):
    _canonical = "mole"
    _label = "Amount of Substance"
    _keywords_alias = ["amount_of_substance", "mole"]


# ============================================================================
# Derived Quantities - Mechanical
# ============================================================================


class Area(Quantity):
    _canonical = "meter**2"
    _label = "Area"
    _keywords_alias = ["area", "size"]


class Volume(Quantity):
    _canonical = "meter**3"
    _label = "Volume"
    _keywords_alias = ["volume", "capacity"]


class Velocity(Quantity):
    _canonical = "meter/second"
    _label = "Velocity"
    _keywords_alias = ["velocity", "speed"]


class Acceleration(Quantity):
    _canonical = "meter/second**2"
    _label = "Acceleration"
    _keywords_alias = ["acceleration", "deceleration"]


class Force(Quantity):
    _canonical = "newton"
    _label = "Force"
    _keywords_alias = ["force"]


class Pressure(Quantity):
    _canonical = "pascal"
    _label = "Pressure"
    _keywords_alias = ["pressure"]


class Energy(Quantity):
    _canonical = "joule"
    _label = "Energy"
    _keywords_alias = ["energy"]


class EnergyFlowRate(Quantity):
    _canonical = "watt"
    _label = "Energy Flow Rate"
    _keywords_alias = [
        "energy_flow_rate",
        "power",
        "energy_rate",
        "energy_current",
        "energy_per_time",
    ]


class Momentum(Quantity):
    _canonical = "kilogram*meter/second"
    _label = "Momentum"
    _keywords_alias = ["momentum"]


class AngularVelocity(Quantity):
    _canonical = "radian/second"
    _label = "Angular Velocity"
    _keywords_alias = ["angular_velocity", "angular_speed"]


class SurfaceTension(Quantity):
    _canonical = "newton/meter"
    _label = "Surface Tension"
    _keywords_alias = ["surface_tension"]


# ============================================================================
# Derived Quantities - Thermodynamic
# ============================================================================


class Entropy(Quantity):
    _canonical = "joule/kelvin"
    _label = "Entropy"
    _keywords_alias = ["entropy", "thermodynamic_entropy"]


class SpecificHeatCapacity(Quantity):
    _canonical = "joule/(kilogram*kelvin)"
    _label = "Specific Heat Capacity"
    _keywords_alias = ["specific_heat_capacity", "heat_capacity"]


class SpecificEnergy(Quantity):
    _canonical = "joule/kilogram"
    _label = "Specific Energy"
    _keywords_alias = ["specific_energy"]


class ChemicalPotential(Quantity):
    _canonical = "joule/mole"
    _label = "Chemical Potential"
    _keywords_alias = ["chemical_potential"]


class MolarEntropy(Quantity):
    _canonical = "joule/(mole*kelvin)"
    _label = "Molar Entropy"
    _keywords_alias = ["molar_entropy"]


class ThermalConductivity(Quantity):
    _canonical = "watt/(meter*kelvin)"
    _label = "Thermal Conductivity"
    _keywords_alias = ["thermal_conductivity"]


class HeatTransferCoefficient(Quantity):
    _canonical = "watt/(meter**2*kelvin)"
    _label = "Heat Transfer Coefficient"
    _keywords_alias = ["heat_transfer_coefficient"]


class ThermalResistance(Quantity):
    _canonical = "kelvin/watt"
    _label = "Thermal Resistance"
    _keywords_alias = ["thermal_resistance"]


class ThermalExpansionCoefficient(Quantity):
    _canonical = "1/kelvin"
    _label = "Thermal Expansion Coefficient"
    _keywords_alias = ["thermal_expansion_coefficient"]


# ============================================================================
# Derived Quantities - Fluid Mechanics
# ============================================================================


class DynamicViscosity(Quantity):
    _canonical = "pascal*second"
    _label = "Dynamic Viscosity"
    _keywords_alias = ["dynamic_viscosity"]


# ============================================================================
# Derived Quantities - Radiation (Dimensionless)
# ============================================================================


class Emissivity(Quantity):
    _canonical = "dimensionless"
    _label = "Emissivity"
    _keywords_alias = ["emissivity"]


class Absorptivity(Quantity):
    _canonical = "dimensionless"
    _label = "Absorptivity"
    _keywords_alias = ["absorptivity"]


class Reflectivity(Quantity):
    _canonical = "dimensionless"
    _label = "Reflectivity"
    _keywords_alias = ["reflectivity"]


class Transmittance(Quantity):
    _canonical = "dimensionless"
    _label = "Transmittance"
    _keywords_alias = ["transmittance"]


# ============================================================================
# Derived Quantities - Electromagnetic
# ============================================================================


class ElectricCharge(Quantity):
    _canonical = "coulomb"
    _label = "Electric Charge"
    _keywords_alias = ["charge", "electric_charge"]


class Voltage(Quantity):
    _canonical = "volt"
    _label = "Voltage"
    _keywords_alias = ["voltage", "electric_potential", "potential_difference"]


class Resistance(Quantity):
    _canonical = "ohm"
    _label = "Resistance"
    _keywords_alias = ["resistance"]


class Capacitance(Quantity):
    _canonical = "farad"
    _label = "Capacitance"
    _keywords_alias = ["capacitance"]


class MagneticFlux(Quantity):
    _canonical = "weber"
    _label = "Magnetic Flux"
    _keywords_alias = ["magnetic_flux"]


class MagneticFluxDensity(Quantity):
    _canonical = "tesla"
    _label = "Magnetic Flux Density"
    _keywords_alias = ["magnetic_flux_density"]


class Inductance(Quantity):
    _canonical = "henry"
    _label = "Inductance"
    _keywords_alias = ["inductance"]


class ElectricalConductivity(Quantity):
    _canonical = "siemens/meter"
    _label = "Electrical Conductivity"
    _keywords_alias = ["electrical_conductivity"]


class Resistivity(Quantity):
    _canonical = "ohm*meter"
    _label = "Resistivity"
    _keywords_alias = ["resistivity"]


# ============================================================================
# Derived Quantities - Chemical & Material
# ============================================================================


class Diffusivity(Quantity):
    _canonical = "meter**2/second"
    _label = "Diffusivity"
    _keywords_alias = ["diffusivity"]


class CatalyticActivity(Quantity):
    _canonical = "mole/second"
    _label = "Catalytic Activity"
    _keywords_alias = ["catalytic_activity"]


# ============================================================================
# Derived Quantities - Transport & Flow
# ============================================================================


class Frequency(Quantity):
    _canonical = "hertz"
    _label = "Frequency"
    _keywords_alias = ["frequency"]


class Density(Quantity):
    _canonical = "kilogram/meter**3"
    _label = "Density"
    _keywords_alias = ["density"]


class MolarMass(Quantity):
    _canonical = "kilogram/mole"
    _label = "Molar Mass"
    _keywords_alias = ["molar_mass"]


class Concentration(Quantity):
    _canonical = "mole/meter**3"
    _label = "Concentration"
    _keywords_alias = ["concentration"]


class VolumetricFlowRate(Quantity):
    _canonical = "meter**3/second"
    _label = "Volumetric Flow Rate"
    _keywords_alias = ["volumetric_flow_rate"]


class MassFlowRate(Quantity):
    _canonical = "kilogram/second"
    _label = "Mass Flow Rate"
    _keywords_alias = ["mass_flow_rate"]


class MassFlux(Quantity):
    _canonical = "kilogram/(meter**2*second)"
    _label = "Mass Flux"
    _keywords_alias = ["mass_flux"]


class EnergyFlux(Quantity):
    _canonical = "joule/(meter**2*second)"
    _label = "Energy Flux"
    _keywords_alias = ["energy_flux"]


class PowerDensity(Quantity):
    _canonical = "watt/meter**3"
    _label = "Power Density"
    _keywords_alias = ["power_density"]


class SpecificPower(Quantity):
    _canonical = "watt/kilogram"
    _label = "Specific Power"
    _keywords_alias = ["specific_power"]


class CarbonIntensity(Quantity):
    _canonical = "kilogram/joule"
    _label = "Carbon Intensity"
    _keywords_alias = ["carbon_intensity"]


# ============================================================================
# Economic Quantities
# ============================================================================


class Currency(Quantity):
    _canonical = "INR"
    _label = "Currency"
    _keywords_alias = ["currency"]


class CostPerEnergy(Quantity):
    _canonical = "INR/joule"
    _label = "Cost per Energy"
    _keywords_alias = ["cost_per_energy"]


class CostPerMass(Quantity):
    _canonical = "INR/kilogram"
    _label = "Cost per Mass"
    _keywords_alias = ["cost_per_mass"]


class CostPerPower(Quantity):
    _canonical = "INR/watt"
    _label = "Cost per Power"
    _keywords_alias = ["cost_per_power"]


class CostPerVolume(Quantity):
    _canonical = "INR/meter**3"
    _label = "Cost per Volume"
    _keywords_alias = ["cost_per_volume"]
