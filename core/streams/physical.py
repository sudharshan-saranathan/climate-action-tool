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
    _keywords_alias = ["length", "distance"]


class Time(Quantity):
    canonical = "second"
    label = "Time"
    _keywords_alias = ["time", "period", "duration"]


class Temperature(Quantity):
    canonical = "kelvin"
    label = "Temperature"
    _keywords_alias = ["temperature", "thermodynamic_temperature"]


class ElectricCurrent(Quantity):
    canonical = "ampere"
    label = "Electric Current"
    _keywords_alias = [
        "electrical_current",
        "electric_current",
        "current",
    ]


class LuminousIntensity(Quantity):
    canonical = "candela"
    label = "Luminous Intensity"
    _keywords_alias = [
        "luminous_intensity",
        "luminous_flux",
        "brightness",
    ]


class AmountOfSubstance(Quantity):
    canonical = "mole"
    label = "Amount of Substance"
    _keywords_alias = ["amount_of_substance", "mole"]


# ============================================================================
# Derived Quantities - Mechanical
# ============================================================================


class Area(Quantity):
    canonical = "meter**2"
    label = "Area"
    _keywords_alias = ["area", "size"]


class Volume(Quantity):
    canonical = "meter**3"
    label = "Volume"
    _keywords_alias = ["volume", "capacity"]


class Velocity(Quantity):
    canonical = "meter/second"
    label = "Velocity"
    _keywords_alias = ["velocity", "speed"]


class Acceleration(Quantity):
    canonical = "meter/second**2"
    label = "Acceleration"
    _keywords_alias = ["acceleration", "deceleration"]


class Force(Quantity):
    canonical = "newton"
    label = "Force"
    _keywords_alias = ["force"]


class Pressure(Quantity):
    canonical = "pascal"
    label = "Pressure"
    _keywords_alias = ["pressure"]


class Energy(Quantity):
    canonical = "joule"
    label = "Energy"
    _keywords_alias = ["energy"]


class EnergyFlowRate(Quantity):
    canonical = "watt"
    label = "Energy Flow Rate"
    _keywords_alias = [
        "energy_flow_rate",
        "power",
        "energy_rate",
        "energy_current",
        "energy_per_time",
    ]


class Momentum(Quantity):
    canonical = "kilogram*meter/second"
    label = "Momentum"
    _keywords_alias = ["momentum"]


class AngularVelocity(Quantity):
    canonical = "radian/second"
    label = "Angular Velocity"
    _keywords_alias = ["angular_velocity", "angular_speed"]


class SurfaceTension(Quantity):
    canonical = "newton/meter"
    label = "Surface Tension"
    _keywords_alias = ["surface_tension"]


# ============================================================================
# Derived Quantities - Thermodynamic
# ============================================================================


class Entropy(Quantity):
    canonical = "joule/kelvin"
    label = "Entropy"
    _keywords_alias = ["entropy", "thermodynamic_entropy"]


class SpecificHeatCapacity(Quantity):
    canonical = "joule/(kilogram*kelvin)"
    label = "Specific Heat Capacity"
    _keywords_alias = ["specific_heat_capacity", "heat_capacity"]


class SpecificEnergy(Quantity):
    canonical = "joule/kilogram"
    label = "Specific Energy"
    _keywords_alias = ["specific_energy"]


class ChemicalPotential(Quantity):
    canonical = "joule/mole"
    label = "Chemical Potential"
    _keywords_alias = ["chemical_potential"]


class MolarEntropy(Quantity):
    canonical = "joule/(mole*kelvin)"
    label = "Molar Entropy"
    _keywords_alias = ["molar_entropy"]


class ThermalConductivity(Quantity):
    canonical = "watt/(meter*kelvin)"
    label = "Thermal Conductivity"
    _keywords_alias = ["thermal_conductivity"]


class HeatTransferCoefficient(Quantity):
    canonical = "watt/(meter**2*kelvin)"
    label = "Heat Transfer Coefficient"
    _keywords_alias = ["heat_transfer_coefficient"]


class ThermalResistance(Quantity):
    canonical = "kelvin/watt"
    label = "Thermal Resistance"
    _keywords_alias = ["thermal_resistance"]


class ThermalExpansionCoefficient(Quantity):
    canonical = "1/kelvin"
    label = "Thermal Expansion Coefficient"
    _keywords_alias = ["thermal_expansion_coefficient"]


# ============================================================================
# Derived Quantities - Fluid Mechanics
# ============================================================================


class DynamicViscosity(Quantity):
    canonical = "pascal*second"
    label = "Dynamic Viscosity"
    _keywords_alias = ["dynamic_viscosity"]


# ============================================================================
# Derived Quantities - Radiation (Dimensionless)
# ============================================================================


class Emissivity(Quantity):
    canonical = "dimensionless"
    label = "Emissivity"
    _keywords_alias = ["emissivity"]


class Absorptivity(Quantity):
    canonical = "dimensionless"
    label = "Absorptivity"
    _keywords_alias = ["absorptivity"]


class Reflectivity(Quantity):
    canonical = "dimensionless"
    label = "Reflectivity"
    _keywords_alias = ["reflectivity"]


class Transmittance(Quantity):
    canonical = "dimensionless"
    label = "Transmittance"
    _keywords_alias = ["transmittance"]


# ============================================================================
# Derived Quantities - Electromagnetic
# ============================================================================


class ElectricCharge(Quantity):
    canonical = "coulomb"
    label = "Electric Charge"
    _keywords_alias = ["charge", "electric_charge"]


class Voltage(Quantity):
    canonical = "volt"
    label = "Voltage"
    _keywords_alias = ["voltage", "electric_potential", "potential_difference"]


class Resistance(Quantity):
    canonical = "ohm"
    label = "Resistance"
    _keywords_alias = ["resistance"]


class Capacitance(Quantity):
    canonical = "farad"
    label = "Capacitance"
    _keywords_alias = ["capacitance"]


class MagneticFlux(Quantity):
    canonical = "weber"
    label = "Magnetic Flux"
    _keywords_alias = ["magnetic_flux"]


class MagneticFluxDensity(Quantity):
    canonical = "tesla"
    label = "Magnetic Flux Density"
    _keywords_alias = ["magnetic_flux_density"]


class Inductance(Quantity):
    canonical = "henry"
    label = "Inductance"
    _keywords_alias = ["inductance"]


class ElectricalConductivity(Quantity):
    canonical = "siemens/meter"
    label = "Electrical Conductivity"
    _keywords_alias = ["electrical_conductivity"]


class Resistivity(Quantity):
    canonical = "ohm*meter"
    label = "Resistivity"
    _keywords_alias = ["resistivity"]


# ============================================================================
# Derived Quantities - Chemical & Material
# ============================================================================


class Diffusivity(Quantity):
    canonical = "meter**2/second"
    label = "Diffusivity"
    _keywords_alias = ["diffusivity"]


class CatalyticActivity(Quantity):
    canonical = "mole/second"
    label = "Catalytic Activity"
    _keywords_alias = ["catalytic_activity"]


# ============================================================================
# Derived Quantities - Transport & Flow
# ============================================================================


class Frequency(Quantity):
    canonical = "hertz"
    label = "Frequency"
    _keywords_alias = ["frequency"]


class Density(Quantity):
    canonical = "kilogram/meter**3"
    label = "Density"
    _keywords_alias = ["density"]


class MolarMass(Quantity):
    canonical = "kilogram/mole"
    label = "Molar Mass"
    _keywords_alias = ["molar_mass"]


class Concentration(Quantity):
    canonical = "mole/meter**3"
    label = "Concentration"
    _keywords_alias = ["concentration"]


class VolumetricFlowRate(Quantity):
    canonical = "meter**3/second"
    label = "Volumetric Flow Rate"
    _keywords_alias = ["volumetric_flow_rate"]


class MassFlowRate(Quantity):
    canonical = "kilogram/second"
    label = "Mass Flow Rate"
    _keywords_alias = ["mass_flow_rate"]


class MassFlux(Quantity):
    canonical = "kilogram/(meter**2*second)"
    label = "Mass Flux"
    _keywords_alias = ["mass_flux"]


class EnergyFlux(Quantity):
    canonical = "joule/(meter**2*second)"
    label = "Energy Flux"
    _keywords_alias = ["energy_flux"]


class PowerDensity(Quantity):
    canonical = "watt/meter**3"
    label = "Power Density"
    _keywords_alias = ["power_density"]


class SpecificPower(Quantity):
    canonical = "watt/kilogram"
    label = "Specific Power"
    _keywords_alias = ["specific_power"]


class CarbonIntensity(Quantity):
    canonical = "kilogram/joule"
    label = "Carbon Intensity"
    _keywords_alias = ["carbon_intensity"]


class RampRate(Quantity):
    canonical = "watt/second"
    label = "Ramp Rate"
    _keywords_alias = ["ramp_rate", "power_ramp", "ramping_rate"]


# ============================================================================
# Economic Quantities
# ============================================================================


class Currency(Quantity):
    canonical = "INR"
    label = "Currency"
    _keywords_alias = ["currency"]


class CostPerEnergy(Quantity):
    canonical = "INR/joule"
    label = "Cost per Energy"
    _keywords_alias = ["cost_per_energy"]


class CostPerMass(Quantity):
    canonical = "INR/kilogram"
    label = "Cost per Mass"
    _keywords_alias = ["cost_per_mass"]


class CostPerPower(Quantity):
    canonical = "INR/watt"
    label = "Cost per Power"
    _keywords_alias = ["cost_per_power"]


class CostPerVolume(Quantity):
    canonical = "INR/meter**3"
    label = "Cost per Volume"
    _keywords_alias = ["cost_per_volume"]
