# Filename: time.py
# Module name: flow
# Description: Time dimension and FlowMixin for flow rate semantics.

"""
Time dimension and FlowMixin class.

Time represents a time dimension with units like hours, days, years.
FlowMixin provides the behavior for "dimension per time" (flow rate).

A flow class combines a physical dimension with FlowMixin:
    class MassFlow(Mass, FlowMixin):
        pass

This creates a "mass per time" type with units like "kg/hr", "g/s", etc.
"""

from __future__ import annotations

from PySide6 import QtGui
from qtawesome import icon
from typing import ClassVar, Optional, Any
from dataclasses import dataclass

from core.flow.dimensions import Dimension


class Time(Dimension):
    """Time dimension with units for duration."""

    @dataclass(frozen=True)
    class Attrs(Dimension.Attrs):
        keyID: ClassVar[str] = "time"
        color: ClassVar[str] = "#808080"
        label: ClassVar[str] = "Time"
        units: ClassVar[list[str]] = ["s", "min", "hr", "day", "yr"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.clock", color="#808080")


class FlowMixin:
    """Mixin providing flow rate semantics (dimension per time).

    Classes using FlowMixin should also inherit from a Dimension class.
    Multiple inheritance: class MassFlow(Mass, FlowMixin)

    Provides:
    - value: the magnitude of the flow
    - units: combined dimension/time units
    - props: dictionary of parameter instances
    """

    def __init__(self, value: float = 0.0, units: Optional[str] = None, props: Optional[dict[str, Any]] = None):
        """Initialize a flow.

        Args:
            value: The flow magnitude (default 0.0)
            units: The specific unit to use (if None, uses first available from Attrs)
            props: Dictionary of Parameter instances describing flow properties
        """
        self._value = value
        self._units = units
        self._props = props if props is not None else {}

    @property
    def value(self) -> float:
        """The magnitude of this flow."""
        return self._value

    @value.setter
    def value(self, val: float):
        """Set the magnitude of this flow."""
        self._value = val

    @property
    def units(self) -> list[str]:
        """Available units for this flow (dimension/time)."""
        # Generate all combinations of dimension and time units
        # Get dimension units from parent Dimension class
        if hasattr(self, 'Attrs'):
            dim_units = self.Attrs.units
        else:
            dim_units = ["?"]

        time_units = Time.Attrs.units

        # Combine dimension and time units
        return [f"{d}/{t}" for d in dim_units for t in time_units]

    @property
    def props(self) -> dict[str, Any]:
        """Dictionary of parameters describing flow properties."""
        return self._props

    @property
    def label(self) -> str:
        """Display label from Attrs."""
        if hasattr(self, 'Attrs'):
            return self.Attrs.label
        return "Flow"

    @property
    def image(self) -> QtGui.QIcon:
        """Icon from Attrs."""
        if hasattr(self, 'Attrs'):
            return self.Attrs.image
        return icon("mdi.help-circle")

    @property
    def color(self) -> str:
        """Color from Attrs."""
        if hasattr(self, 'Attrs'):
            return self.Attrs.color
        return "#ffffff"
