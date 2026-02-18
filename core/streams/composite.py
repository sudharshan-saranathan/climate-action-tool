# Filename: core/streams/composite.py
# Module name: core.streams.composite
# Description: Composite high-level resource streams for systems modeling

from __future__ import annotations

# Standard
import typing
import logging


# core.streams
from core.streams.physical import MassFlowRate
from core.streams.physical import CostPerMass


class Composite:
    label = "Composite"
    image = "mdi.set-center"
    color = "#FFD700"

    # Attribute dictionary for GUI
    attribute_hierarchy = {
        "Primary": {},
    }

    def __init__(
        self,
        **kwargs,
    ):
        # Lazy import Quantity from core.streams
        from core.streams import Quantity

        # Create dynamic attributes based on the given keyword and units.
        # Example: Composite(mass='10 kg', speed='25 m/s') will create two attributes: mass and speed.
        # The attributes' classes are determined from the given units via Quantity.registry lookup.
        # If the class cannot be found, `Quantity` is used as a fallback.
        # NOTE: Pre-existing attributes with the same name will not be overwritten.

        for attr, value in kwargs.items():
            if not hasattr(self, attr):
                setattr(
                    self,
                    attr,
                    Quantity.registry.get(
                        Quantity(value).dimensionality(),
                        Quantity,
                    )(value),
                )

            else:
                logging.warning(f"Attribute {attr} already exists. Skipping.")


class Material(Composite):
    label = "Material"
    image = "mdi.gold"
    color = "#f63c6b"

    # Attribute dictionary for GUI
    attribute_hierarchy = {
        "Primary": {
            "mass": "Mass [kg/s]",
            "cost": "Cost [INR/kg]",
        },
    }

    def __init__(self, **kwargs):

        # For a Material stream, mass and cost are auto-defined.
        self.mass = MassFlowRate("0 kg/s")
        self.cost = CostPerMass("0 INR/kg")

        # Initialize other attributes based on kwargs
        kwargs.pop("mass", None)
        kwargs.pop("cost", None)
        super().__init__(**kwargs)


class Electricity(Composite):
    label = "Electricity"
    image = "mdi.flash"
    color = "#8491a3"

    attribute_hierarchy = {
        "Primary": {
            "power": "Power [kW]",
            "tariff": "Tariff [INR/kWh]",
        },
        "Cycle": {
            "start_up_time": "Start-up time [s]",
            "shut_down_time": "Shut-down time [s]",
        },
        "Quality": {
            "voltage": "Voltage [V]",
            "power_factor": "Power factor [dimensionless]",
            "frequency": "Frequency [Hz]",
        },
        "Emissions": {
            "CO2_intensity": "CO2 intensity [kg/J]",
            "SOx_intensity": "SOx intensity [kg/J]",
            "NOx_intensity": "NOx intensity [kg/J]",
            "PM2_5_intensity": "PM2.5 intensity [kg/J]",
            "PM10_intensity": "PM10 intensity [kg/J]",
        },
        "Operational": {
            "ramp_rate": "Ramp Rate [kW/s]",
            "capacity_factor": "Capacity Factor [dimensionless]",
            "dispatchability": "Dispatchability [dimensionless]",
            "variability": "Variability [dimensionless]",
            "minimum_stable_generation": "Minimum Stable Generation [dimensionless]",
        },
    }

    def __init__(
        self,
        **kwargs,
    ):
        # Import required classes
        from core.streams.physical import EnergyFlowRate
        from core.streams.physical import CostPerEnergy
        from core.streams.physical import RampRate
        from core.streams.physical import Time
        from core.streams.physical import Voltage
        from core.streams.physical import Frequency
        from core.streams.physical import CarbonIntensity
        from core.streams.quantity import Quantity

        # Power and cost
        self.power = EnergyFlowRate("0 W")
        self.tariff = CostPerEnergy("0 INR/kWh")

        # Operational characteristics
        self.ramp_rate = RampRate("0 W/s")  # How fast power output can change
        self.capacity_factor = Quantity("0 dimensionless")  # Actual/nameplate (0-1)
        self.dispatchability = Quantity("0 dimensionless")  # Controllability (0-1)
        self.variability = Quantity("0 dimensionless")  # Coefficient of variation
        self.minimum_stable_generation = Quantity("0 dimensionless")  # Fraction of max
        self.start_up_time = Time("0 s")  # Time to start generation
        self.shut_down_time = Time("0 s")  # Time to stop generation

        # Grid/electrical quality
        self.voltage = Voltage("0 V")  # Operating voltage
        self.power_factor = Quantity("1 dimensionless")  # AC power quality (0-1)
        self.frequency = Frequency("50 Hz")  # Grid frequency (50 or 60 Hz)

        # Environmental - emissions intensity (per kWh or per joule)
        self.CO2_intensity = CarbonIntensity("0 kg/J")  # Can also use kg/kWh
        self.SOx_intensity = Quantity("0 kg/J")
        self.NOx_intensity = Quantity("0 kg/J")
        self.PM2_5_intensity = Quantity("0 kg/J")
        self.PM10_intensity = Quantity("0 kg/J")

        # Economic
        self.LCOE = CostPerEnergy("0 INR/kWh")  # Levelized cost of energy

        # Remove from kwargs before passing to parent
        kwargs.pop("power", None)
        kwargs.pop("tariff", None)
        kwargs.pop("ramp_rate", None)
        kwargs.pop("capacity_factor", None)
        kwargs.pop("dispatchability", None)
        kwargs.pop("variability", None)
        kwargs.pop("minimum_stable_generation", None)
        kwargs.pop("start_up_time", None)
        kwargs.pop("shut_down_time", None)
        kwargs.pop("voltage", None)
        kwargs.pop("power_factor", None)
        kwargs.pop("frequency", None)
        kwargs.pop("CO2_intensity", None)
        kwargs.pop("SOx_intensity", None)
        kwargs.pop("NOx_intensity", None)
        kwargs.pop("PM2_5_intensity", None)
        kwargs.pop("PM10_intensity", None)
        kwargs.pop("LCOE", None)
        super().__init__(**kwargs)


class Fluid(Composite):
    label = "Fluid"
    image = "mdi.gas-cylinder"
    color = "darkcyan"

    attribute_hierarchy = {
        "Primary": {
            "mass": "Mass [kg/s]",
            "cost": "Cost [INR/kg]",
        },
        "Thermodynamic": {
            "vapor_fraction": "Vapor Fraction [dimensionless]",
            "temperature": "Temperature [°C]",
            "pressure": "Pressure [bar]",
        },
    }

    def __init__(self, **kwargs):

        # Import required classes
        from core.streams.quantity import Quantity
        from core.streams.physical import (
            MassFlowRate,
            CostPerMass,
            Temperature,
            Pressure,
        )

        # Primary attributes
        self.mass = MassFlowRate("0 kg/s")
        self.cost = CostPerMass("0 INR/kg")

        # Thermodynamic attributes
        self.vapor_fraction = Quantity("0 dimensionless")
        self.temperature = Temperature("0 °C")
        self.pressure = Pressure("0 bar")

        # Remove from kwargs before passing to parent
        kwargs.pop("mass", None)
        kwargs.pop("cost", None)
        kwargs.pop("vapor_fraction", None)
        kwargs.pop("temperature", None)
        kwargs.pop("pressure", None)
        super().__init__(**kwargs)


class Fuel(Material):
    label = "Fuel"
    image = "mdi.gas-station"
    color = "#bd8b9c"

    attribute_hierarchy = {
        "Primary": {
            "ash_content": "Ash Content [dimensionless]",
            "energy_content": "Energy Content [kJ/kg]",
            "moisture_content": "Moisture Content [dimensionless]",
        },
        "Chemical": {
            "carbon_fraction": "Carbon Fraction [dimensionless]",
            "sulfur_fraction": "Sulfur Fraction [dimensionless]",
            "oxygen_fraction": "Oxygen Fraction [dimensionless]",
            "hydrogen_fraction": "Hydrogen Fraction [dimensionless]",
            "nitrogen_fraction": "Nitrogen Fraction [dimensionless]",
        },
        "Emissions": {
            "CO2_emissions": "CO2 Emissions [kg/kg]",
            "CH4_emissions": "CH4 Emissions [kg/kg]",
            "SOx_emissions": "SOx Emissions [kg/kg]",
            "NOx_emissions": "NOx Emissions [kg/kg]",
            "PM2_5_emissions": "PM2.5 Emissions [kg/kg]",
            "PM10_emissions": "PM10 Emissions [kg/kg]",
            "CO_emissions": "CO Emissions [kg/kg]",
        },
    }

    def __init__(
        self,
        **kwargs,
    ):
        # Import required classes
        from core.streams.physical import MassFlowRate, CostPerMass, SpecificEnergy
        from core.streams.quantity import Quantity

        # Primary attributes
        self.mass = MassFlowRate("0 kg/s")
        self.cost = CostPerMass("0 INR/kg")
        self.energy_content = SpecificEnergy("0 joule/kg")  # Higher heating value

        # Additional chemical properties
        self.moisture_content = Quantity("0 dimensionless")
        self.ash_content = Quantity("0 dimensionless")

        # Elemental composition (mass fractions)
        self.carbon_fraction = Quantity("0 dimensionless")
        self.sulfur_fraction = Quantity("0 dimensionless")
        self.oxygen_fraction = Quantity("0 dimensionless")
        self.hydrogen_fraction = Quantity("0 dimensionless")
        self.nitrogen_fraction = Quantity("0 dimensionless")

        # Emissions factors (kg pollutant per kg fuel)
        self.CO2_emissions = Quantity("0 dimensionless")
        self.CH4_emissions = Quantity("0 dimensionless")
        self.SOx_emissions = Quantity("0 dimensionless")
        self.NOx_emissions = Quantity("0 dimensionless")
        self.PM2_5_emissions = Quantity("0 dimensionless")
        self.PM10_emissions = Quantity("0 dimensionless")
        self.CO_emissions = Quantity("0 dimensionless")

        # Remove from kwargs before passing to parent
        kwargs.pop("energy_content", None)
        kwargs.pop("moisture_content", None)
        kwargs.pop("ash_content", None)
        kwargs.pop("carbon_fraction", None)
        kwargs.pop("hydrogen_fraction", None)
        kwargs.pop("oxygen_fraction", None)
        kwargs.pop("nitrogen_fraction", None)
        kwargs.pop("sulfur_fraction", None)
        kwargs.pop("CO2_emissions", None)
        kwargs.pop("CH4_emissions", None)
        kwargs.pop("SOx_emissions", None)
        kwargs.pop("NOx_emissions", None)
        kwargs.pop("PM2_5_emissions", None)
        kwargs.pop("PM10_emissions", None)
        kwargs.pop("CO_emissions", None)
        kwargs.pop("renewable_fraction", None)
        kwargs.pop("carbon_neutrality_factor", None)
        super().__init__(**kwargs)
