# Filename: combos.py
# Module name: flow
# Description: Composite flow types combining flows with parameters.

"""
Composite flow types that combine basic flows with specialized parameters.

Each composite flow extends a basic flow with domain-specific properties:
- Fuel: mass flow with energy content, emissions, cost
- Material: mass flow with cost
- Product: mass flow with revenue
- Electricity: energy flow with tariff, emissions, variability
- Fluid: mass flow with temperature and pressure
"""

from __future__ import annotations

from PySide6 import QtGui
from qtawesome import icon
from typing import ClassVar
from dataclasses import dataclass

from core.flow.flows import MassFlow, EnergyFlow
from core.flow.parameters import Ratio, TemperatureParam, PressureParam, Factor
from core.flow.dimensions import Energy, Currency, Mass, Power
from core.flow.profiles import ProfileRef, FixedProfile


class Fuel(MassFlow):
    """Fuel flow with energy content, emissions, and cost."""

    @dataclass(frozen=True)
    class Attrs(MassFlow.Attrs):
        keyID: ClassVar[str] = "fuel"
        color: ClassVar[str] = "#bd8b9c"
        label: ClassVar[str] = "Fuel"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gas-station", color="#bd8b9c")

    def __init__(self, value: float = 0.0, units: str | None = None):
        """Initialize fuel with default properties.

        Args:
            value: Fuel flow magnitude
            units: Specific unit (e.g., "kg/hr")
        """
        props = {
            "specific_energy": Ratio(Energy, Mass, label="specific_energy"),
            "emission_factor": Ratio(Mass, Mass, label="emission_factor"),
            "cost": Ratio(Currency, Mass, label="cost"),
        }
        super().__init__(value=value, units=units, props=props)


class Material(MassFlow):
    """Material flow with cost information."""

    @dataclass(frozen=True)
    class Attrs(MassFlow.Attrs):
        keyID: ClassVar[str] = "material"
        color: ClassVar[str] = "#f63c6b"
        label: ClassVar[str] = "Material"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gold", color="#f63c6b")

    def __init__(self, value: float = 0.0, units: str | None = None):
        """Initialize material with default properties.

        Args:
            value: Material flow magnitude
            units: Specific unit (e.g., "kg/hr")
        """
        props = {
            "cost": Ratio(Currency, Mass, label="cost"),
        }
        super().__init__(value=value, units=units, props=props)


class Product(MassFlow):
    """Product flow with revenue information."""

    @dataclass(frozen=True)
    class Attrs(MassFlow.Attrs):
        keyID: ClassVar[str] = "product"
        color: ClassVar[str] = "#c5ff99"
        label: ClassVar[str] = "Product"
        image: ClassVar[QtGui.QIcon] = icon("mdi.cube", color="#c5ff99")

    def __init__(self, value: float = 0.0, units: str | None = None):
        """Initialize product with default properties.

        Args:
            value: Product flow magnitude
            units: Specific unit (e.g., "kg/hr")
        """
        props = {
            "revenue": Ratio(Currency, Mass, label="revenue"),
        }
        super().__init__(value=value, units=units, props=props)


class Electricity(Power):
    """Electrical power delivery with tariff, emissions, and grid characteristics."""

    @dataclass(frozen=True)
    class Attrs(Power.Attrs):
        keyID: ClassVar[str] = "electricity"
        label: ClassVar[str] = "Electricity"

    def __init__(self, value: float = 0.0, units: str | None = None):
        """Initialize electricity with default properties.

        Args:
            value: Power magnitude
            units: Specific unit (e.g., "kW")
        """
        self._value = value
        self._units = units or "kW"

        props = {
            "tariff": Ratio(Currency, Power, label="tariff"),
            "emissions_factor": Ratio(Mass, Power, label="emissions_factor"),
            "variability": Factor("Variability", color="#daa520", icon_name="mdi.sine-wave"),
            "ramp_rate": Factor("Ramp Rate", color="#20b2aa", icon_name="mdi.speedometer"),
        }
        self._props = props

    @property
    def units(self) -> list[str]:
        """Power units (not power/time)."""
        return Power.Attrs.units

    @property
    def label(self) -> str:
        """Display label."""
        return self.Attrs.label

    @property
    def color(self) -> str:
        """Color code."""
        return self.Attrs.color

    @property
    def image(self) -> QtGui.QIcon:
        """Icon."""
        return self.Attrs.image

    @property
    def props(self) -> dict:
        """Parameter dictionary."""
        return self._props


class Fluid(MassFlow):
    """Fluid flow with thermodynamic properties."""

    @dataclass(frozen=True)
    class Attrs(MassFlow.Attrs):
        keyID: ClassVar[str] = "fluid"
        color: ClassVar[str] = "#1e90ff"
        label: ClassVar[str] = "Fluid"
        image: ClassVar[QtGui.QIcon] = icon("mdi.gas-cylinder", color="#ffd791")

    def __init__(self, value: float = 0.0, units: str | None = None):
        """Initialize fluid with default properties.

        Args:
            value: Fluid flow magnitude
            units: Specific unit (e.g., "kg/hr")
        """
        props = {
            "temperature": TemperatureParam(),
            "pressure": PressureParam(),
        }
        super().__init__(value=value, units=units, props=props)
