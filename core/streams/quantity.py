#  Filename: core/streams/quantity.py
#  Module name: core.streams.quantity
#  Description: Base Quantity class with the registry pattern

from __future__ import annotations

# Standard
import pint
import typing
import numpy as np


__all__ = ["Quantity", "ureg"]


# Unit registry
ureg = pint.UnitRegistry()
ureg.define("INR = [currency]")


class Quantity:
    """
    Base class for all resource streams. Uses the registry pattern for dimensionality-based dispatch.
    """

    label: str = "Generic"
    registry: dict = {}  # A registry for dimensionality-to-type mapping.

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)

        # Register by dimensionality for arithmetic operations
        # Only register classes that explicitly declare canonical (not inherited)
        if "canonical" in cls.__dict__:
            dims = ureg.parse_units(cls.canonical).dimensionality
            Quantity.registry[dims] = cls

    def __init__(
        self,
        *args,
    ):

        # Pass args to the pint constructor first
        self._q = ureg.Quantity(*args)  # type: ignore

        # Validate dimensionality if canonical is defined
        self._validate_units(str(self._q.units))

    def _validate_units(self, units: str) -> None:

        if hasattr(self, "canonical"):
            dims = ureg.parse_units(self.canonical).dimensionality
            if ureg.parse_units(units).dimensionality != dims:
                raise ValueError(
                    f"Units {units} are not compatible with {self.canonical} "
                    f"(expected {dims})"
                )

    @classmethod
    def _from_quantity(cls, q: "ureg.Quantity") -> Quantity:
        target_cls = cls.registry.get(q.dimensionality, Quantity)
        return target_cls(q.magnitude, str(q.units))

    def __add__(self, other: Quantity) -> Quantity:
        return self._from_quantity(self._q + other._q)

    def __sub__(self, other: Quantity) -> Quantity:
        return self._from_quantity(self._q - other._q)

    def __mul__(self, other: Quantity) -> Quantity:
        return self._from_quantity(self._q * other._q)

    def __truediv__(self, other: Quantity) -> Quantity:
        return self._from_quantity(self._q / other._q)

    def __eq__(self, other: Quantity) -> bool:
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
    def quantity(self) -> "ureg.Quantity":
        return self._q.copy()

    def to(self, units: str) -> Quantity:

        new_quantity = self._q.to(units)
        return self._from_quantity(new_quantity)

    def to_dict(self) -> dict[str, typing.Any]:

        result = {
            "type": self.__class__.__name__,
            "value": (
                self.value.tolist()
                if isinstance(self.value, np.ndarray)
                else self.value
            ),
            "units": str(self.units),
        }

        for key, item in self.__dict__.items():
            if isinstance(item, Quantity):
                result[key] = item.to_dict()  # type: ignore

        return result

    def dimensionality(self) -> "ureg.Dimensionality":
        return self._q.dimensionality

    @classmethod
    def from_dict(cls, data: dict) -> "Quantity":
        """
        Factory method to reconstruct Quantity from the given dictionary.
        """

        # Import CLASS_REGISTRY from core.streams
        from core.streams import CLASS_REGISTRY

        # Get the target class from CLASS_REGISTRY
        class_name = data.get("type", "Quantity")
        target_class = CLASS_REGISTRY.get(class_name, cls)

        # Extract main attributes and convert lists to np.ndarray
        value = data.get("value", 0)
        if isinstance(value, list):
            value = np.array(value)

        units = data.get("units", "")

        # Build kwargs by flattening nested quantities
        kwargs = {}
        for key, val in data.items():
            if key in ("type", "value", "units", "_q"):
                continue

            # Check if this is a nested Quantity dict
            if isinstance(val, dict) and "type" in val:

                # Extract the nested stream's value and units directly as kwargs
                nested_value = val.get("value", 0)
                if isinstance(nested_value, list):
                    nested_value = np.array(nested_value)

                nested_units = val.get("units", "")
                kwargs[key] = nested_value
                kwargs[f"{key}_units"] = nested_units
            else:
                kwargs[key] = val

        # Instantiate the correct class
        return target_class(value, units, **kwargs)
