#  Filename: core/streams/quantity.py
#  Module name: core.streams.quantity
#  Description: Base ResourceStream class with the registry pattern

from __future__ import annotations

# Standard
import pint
import numpy as np
import typing


__all__ = ["ResourceStream", "ureg"]


# Unit registry
ureg = pint.UnitRegistry()
ureg.define("INR = [currency]")


class ResourceStream:
    _label: str = "Generic Stream"
    _registry: dict = {}

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        if hasattr(cls, "_canonical"):
            dims = ureg.parse_units(cls._canonical).dimensionality
            ResourceStream._registry[dims] = cls

    def __init__(
        self,
        data: typing.Union[int, float, np.ndarray],
        units: typing.Optional[str] = None,
    ):

        if not isinstance(data, (int, float, np.ndarray)):
            raise TypeError(f"Invalid data type: {type(data)}")

        # Default to canonical SI unit if not specified
        if units is None:
            units = getattr(self, "_canonical", "")

        # Validate dimensionality if canonical is defined
        if hasattr(self, "_canonical"):
            dims = ureg.parse_units(self._canonical).dimensionality
            if ureg.parse_units(units).dimensionality != dims:
                raise ValueError(
                    f"Units {units} are not compatible with {self._canonical} "
                    f"(expected {dims})"
                )

        self._q = ureg.Quantity(data, units)  # type: ignore

    @classmethod
    def _from_quantity(cls, q: "ureg.Quantity") -> ResourceStream:
        target_cls = cls._registry.get(q.dimensionality, ResourceStream)
        return target_cls(q.magnitude, str(q.units))

    def __add__(self, other: ResourceStream) -> ResourceStream:
        return self._from_quantity(self._q + other._q)

    def __sub__(self, other: ResourceStream) -> ResourceStream:
        return self._from_quantity(self._q - other._q)

    def __mul__(self, other: ResourceStream) -> ResourceStream:
        return self._from_quantity(self._q * other._q)

    def __truediv__(self, other: ResourceStream) -> ResourceStream:
        return self._from_quantity(self._q / other._q)

    def __eq__(self, other: ResourceStream) -> bool:
        return self._q == other._q

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>: {self._q}"

    @property
    def value(self) -> typing.Union[int, float, np.ndarray]:
        return self._q.magnitude

    @value.setter
    def value(self, value: typing.Union[int, float, np.ndarray]) -> None:
        self._q = ureg.Quantity(value, self._q.units)  # type: ignore

    @property
    def units(self) -> str:
        return self._q.units

    @property
    def label(self) -> str:
        return self._label

    @property
    def quantity(self) -> "ureg.Quantity":
        return self._q.copy()

    def to(self, units: str) -> ResourceStream:

        new_quantity = self._q.to(units)
        return self._from_quantity(new_quantity)

    def to_dict(self) -> dict[str, typing.Any]:

        result = {
            "type": self.__class__.__name__,
            "value": self.value.tolist() if isinstance(self.value, np.ndarray) else self.value,
            "units": str(self.units),
        }

        for key, item in self.__dict__.items():
            if isinstance(item, ResourceStream):
                result[key] = item.to_dict()  # type: ignore

        return result

    def dimensionality(self) -> "ureg.Dimensionality":
        return self._q.dimensionality
