# Filename: parameters.py
# Module name: flow
# Description: Parameter classes for flow properties.

"""
Parameter system for flow properties with profile support.

Parameters represent properties of flows that can vary over time:
- TemperatureParam: Temperature with time-varying profiles
- PressureParam: Pressure with time-varying profiles
- Factor: Dimensionless 0-1 factor (efficiency, variability, etc.)
- Ratio: Ratio of two dimensions (cost per mass, emissions per energy, etc.)

All parameters support ProfileRef for time-varying behavior.
"""

from __future__ import annotations

from abc import ABC
from PySide6 import QtGui
from qtawesome import icon
from typing import ClassVar, Optional, Any
from dataclasses import dataclass

from core.flow.dimensions import Dimension, Temperature, Pressure
from core.flow.profiles import ProfileRef, FixedProfile


class Parameter(ABC):
    """Base class for flow parameters with profile support."""

    @dataclass(frozen=True)
    class Attrs:
        """Metadata for a parameter."""
        keyID: ClassVar[str] = "parameter"
        color: ClassVar[str] = "#8b0000"
        label: ClassVar[str] = "Parameter"
        units: ClassVar[list[str]] = []
        image: ClassVar[QtGui.QIcon] = icon("mdi.pound", color="#8b0000")
        is_variable: ClassVar[bool] = False  # Whether this parameter can vary with time

    def __init__(self, profile_ref: Optional[ProfileRef] = None):
        """Initialize with a profile reference.

        Args:
            profile_ref: ProfileRef wrapping a Profile. If None, defaults to FixedProfile(0.0)
        """
        if profile_ref is None:
            profile_ref = ProfileRef(
                profile=FixedProfile(0.0),
                units=self.Attrs.units[0] if self.Attrs.units else "",
                description=""
            )
        self.profile_ref = profile_ref

    @property
    def is_variable(self) -> bool:
        """Whether this parameter can vary with time."""
        return self.Attrs.is_variable

    @property
    def label(self) -> str:
        """Display label."""
        return self.Attrs.label

    @property
    def image(self) -> QtGui.QIcon:
        """Icon for this parameter."""
        return self.Attrs.image

    @property
    def color(self) -> str:
        """Color for this parameter."""
        return self.Attrs.color

    @property
    def units(self) -> list[str]:
        """Available units."""
        return self.Attrs.units

    def value_at(self, time: float) -> float:
        """Get the parameter value at a specific time.

        Args:
            time: Time at which to evaluate

        Returns:
            The parameter value at the given time
        """
        return self.profile_ref.value_at(time)


class FixedParameter(Parameter):
    """Parameter that is fixed and cannot vary with time.

    Examples: specific energy of a fuel, carbon content, physical properties.
    The UI will not show profile editing options for these.
    """

    @dataclass(frozen=True)
    class Attrs(Parameter.Attrs):
        is_variable: ClassVar[bool] = False


class VariableParameter(Parameter):
    """Parameter that can vary over time with profiles.

    Examples: cost, tariff, market prices, efficiency that changes seasonally.
    The UI will show profile type selector and editing options for these.
    """

    @dataclass(frozen=True)
    class Attrs(Parameter.Attrs):
        is_variable: ClassVar[bool] = True


class TemperatureParam(VariableParameter):
    """Temperature parameter with profile support."""

    @dataclass(frozen=True)
    class Attrs(Parameter.Attrs):
        keyID: ClassVar[str] = "temperature_param"
        color: ClassVar[str] = "#ff6347"
        label: ClassVar[str] = "Temperature"
        units: ClassVar[list[str]] = ["K", "°C", "°F"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.thermometer", color="#ff6347")


class PressureParam(VariableParameter):
    """Pressure parameter with profile support."""

    @dataclass(frozen=True)
    class Attrs(VariableParameter.Attrs):
        keyID: ClassVar[str] = "pressure_param"
        color: ClassVar[str] = "#4682b4"
        label: ClassVar[str] = "Pressure"
        units: ClassVar[list[str]] = ["Pa", "kPa", "MPa", "bar", "atm"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.gauge", color="#4682b4")
        is_variable: ClassVar[bool] = True


class Factor(VariableParameter):
    """Dimensionless factor parameter (typically 0-1 range).

    Used for efficiency, variability, ramp rates, and other
    dimensionless properties that can vary with time.
    """

    def __init__(self, label: str = "Factor", color: str = "#808080", icon_name: str = "mdi.percent", profile_ref: Optional[ProfileRef] = None):
        """Initialize a factor parameter.

        Args:
            label: Display label
            color: Color code
            icon_name: Icon name from qtawesome
            profile_ref: ProfileRef for time-varying values
        """
        super().__init__(profile_ref)
        self._label = label
        self._color = color
        self._icon_name = icon_name

    @property
    def label(self) -> str:
        return self._label

    @property
    def image(self) -> QtGui.QIcon:
        return icon(self._icon_name, color=self._color)

    @property
    def color(self) -> str:
        return self._color

    @property
    def units(self) -> list[str]:
        return ["0-1"]


class Ratio(Parameter):
    """Ratio parameter derived from two dimensions (numerator/denominator).

    Units are the cross-product of numerator and denominator units.
    Can be either fixed (for physical properties) or variable (for market prices).

    Examples:
        Ratio(Currency, Mass, is_variable=True): Cost (can vary) - USD/kg
        Ratio(Energy, Mass, is_variable=False): Specific energy (fixed) - MJ/kg
        Ratio(Mass, Mass, is_variable=False): Emission factor (fixed) - dimensionless
    """

    def __init__(self, numerator: type, denominator: type, label: Optional[str] = None,
                 profile_ref: Optional[ProfileRef] = None, is_variable: bool = True):
        """Initialize a ratio parameter.

        Args:
            numerator: Dimension class for numerator (e.g., Currency)
            denominator: Dimension class for denominator (e.g., Mass)
            label: Optional custom label. If None, auto-generated.
            profile_ref: ProfileRef for time-varying values
            is_variable: Whether this ratio can vary with time (default: True for costs)
        """
        super().__init__(profile_ref)
        self._numerator = numerator
        self._denominator = denominator
        self._custom_label = label
        self._is_variable = is_variable

    @property
    def is_variable(self) -> bool:
        """Whether this parameter can vary with time."""
        return self._is_variable

    @property
    def label(self) -> str:
        """Auto-generated or custom label."""
        if self._custom_label:
            return self._custom_label
        num_label = self._numerator.Attrs.label.lower()
        den_label = self._denominator.Attrs.label.lower()
        return f"{num_label}_per_{den_label}"

    @property
    def image(self) -> QtGui.QIcon:
        """Use numerator's icon."""
        return self._numerator.Attrs.image

    @property
    def color(self) -> str:
        """Use numerator's color."""
        return self._numerator.Attrs.color

    @property
    def units(self) -> list[str]:
        """Cross-product of numerator and denominator units."""
        num_units = self._numerator.Attrs.units
        den_units = self._denominator.Attrs.units

        # If same dimension, return dimensionless
        if self._numerator == self._denominator:
            return ["-"]

        # Generate all combinations
        return [f"{n}/{d}" for n in num_units for d in den_units]
