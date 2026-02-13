# Filename: core/streams/composite.py
# Module name: core.streams.composite
# Description: Composite high-level resource streams for systems modeling

from __future__ import annotations

# Standard
import typing
import logging


class Composite:
    label = "Composite"
    image = "mdi.set-center"
    color = "#FFD700"

    # Attribute grouping for GUI display
    attribute_groups = {
        "core": [],  # No predefined attributes - all dynamic
        "advanced": [],
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
    color = "#FFD700"

    # Attribute grouping for GUI display
    attribute_groups = {
        "core": [
            "mass",
            "cost",
        ],
        "advanced": [],
    }

    def __init__(
        self,
        **kwargs,
    ):
        # Import MassFlowRate from core.streams.physical
        from core.streams.physical import MassFlowRate
        from core.streams.physical import CostPerMass

        # For a Material stream, mass and cost are auto-defined.
        self.mass = MassFlowRate("0 kg/s")
        self.cost = CostPerMass("0 INR/kg")

        # Initialize other attributes based on kwargs
        kwargs.pop("mass", None)
        kwargs.pop("cost", None)
        super().__init__(**kwargs)


class Electricity(Composite):
    label = "Electricity"
    image = "mdi.lightning-bolt"
    color = "#4A90E2"

    # Attribute grouping for GUI display
    attribute_groups = {
        "core": [
            "power",
            "tariff",
            "capacity_factor",
            "dispatchability",
            "CO2_intensity",
        ],
        "advanced": [
            "ramp_rate",
            "variability",
            "minimum_stable_generation",
            "start_up_time",
            "shut_down_time",
            "voltage",
            "power_factor",
            "frequency",
            "SOx_intensity",
            "NOx_intensity",
            "PM2_5_intensity",
            "PM10_intensity",
            "LCOE",
        ],
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


class Fuel(Material):
    label = "Fuel"
    image = "mdi.fire"
    color = "#FF6B35"

    # Attribute grouping for GUI display
    # Note: 'mass' and 'cost' are inherited from Material and always shown
    attribute_groups = {
        "core": [
            "energy_content",
            "carbon_fraction",
            "CO2_emissions",
        ],
        "advanced": [
            "moisture_content",
            "ash_content",
            "hydrogen_fraction",
            "oxygen_fraction",
            "nitrogen_fraction",
            "sulfur_fraction",
            "CH4_emissions",
            "SOx_emissions",
            "NOx_emissions",
            "PM2_5_emissions",
            "PM10_emissions",
            "CO_emissions",
            "renewable_fraction",
            "carbon_neutrality_factor",
        ],
    }

    def __init__(
        self,
        **kwargs,
    ):
        # Import required classes
        from core.streams.physical import SpecificEnergy
        from core.streams.quantity import Quantity

        # Physical/Chemical properties
        self.energy_content = SpecificEnergy("0 joule/kg")  # Higher heating value
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

        # Sustainability attributes
        self.renewable_fraction = Quantity("0 dimensionless")  # 0=fossil, 1=biomass
        self.carbon_neutrality_factor = Quantity(
            "0 dimensionless"
        )  # For carbon accounting

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
