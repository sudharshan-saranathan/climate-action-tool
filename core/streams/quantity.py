#  Filename: core/streams/fundamental.py
#  Module name: core.streams.fundamental
#  Description: Fundamental stream types

from __future__ import annotations

# Standard
import uuid
import pint
import numpy as np


# Unit registry
ureg = pint.UnitRegistry()


class DimensionlessQuantity:

    _uid: str = str(uuid.uuid4())
    _label: str = "Dimensionless Quantity"
    _canonical: str = ""

    def __init__(self, data: int | float | np.ndarray, units: str = ""):

        if ureg.Unit(units).is_compatible_with(self._canonical):
            self._value = data
            self._units = ureg.Unit(units)

        else:
            raise ValueError(f"Invalid unit {units} for {self._label}")

    @property
    def value(self) -> int | float | np.ndarray:
        return self._value

    @value.setter
    def value(self, value: int | float | np.ndarray) -> None:
        if isinstance(value, (int, float, np.ndarray)):
            self._value = value

        else:
            raise TypeError(f"Invalid data type {type(value)} for {self._label}")

    @property
    def units(self) -> str:
        return str(self._units)

    @units.setter
    def units(self, _units: str) -> None:

        if ureg.Unit(_units).is_compatible_with(self._canonical):
            self._units = ureg.Unit(_units)
        else:
            raise ValueError(f"Invalid unit {_units} for {self._label}")

    @property
    def label(self) -> str:
        return self._label


class Mass(DimensionlessQuantity):
    _label: str = "Mass"
    _canonical: str = "kg"


class Length(DimensionlessQuantity):
    _label: str = "Length"
    _canonical: str = "m"


class Time(DimensionlessQuantity):
    _label: str = "Time"
    _canonical: str = "s"
