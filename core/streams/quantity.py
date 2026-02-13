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
    _registry: dict = {}  # Dimensionality-based registry for arithmetic operations

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        # Register by dimensionality for arithmetic operations
        # Only register classes that explicitly declare _canonical (not inherited)
        if "_canonical" in cls.__dict__:
            dims = ureg.parse_units(cls._canonical).dimensionality
            ResourceStream._registry[dims] = cls

    def __init__(
        self,
        data: typing.Union[int, float, np.ndarray],
        units: typing.Optional[str] = None,
    ):

        if not isinstance(data, (int, float, np.ndarray)):
            raise TypeError(f"Invalid data type: {type(data)}")

        # Default to canonical SI unit if not specified (or empty string)
        if not units:
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
            "value": (
                self.value.tolist()
                if isinstance(self.value, np.ndarray)
                else self.value
            ),
            "units": str(self.units),
        }

        for key, item in self.__dict__.items():
            if isinstance(item, ResourceStream):
                result[key] = item.to_dict()  # type: ignore

        return result

    def dimensionality(self) -> "ureg.Dimensionality":
        return self._q.dimensionality

    @classmethod
    def from_dict(cls, data: dict) -> "ResourceStream":
        """Factory method to reconstruct ResourceStream from the given dictionary.

        Uses the 'type' field to instantiate the correct subclass and
        recursively deserialize nested ResourceStream objects.
        """

        # Import CLASS_REGISTRY from core.streams
        from core.streams import CLASS_REGISTRY

        # Get the target class from CLASS_REGISTRY
        class_name = data.get("type", "ResourceStream")
        target_class = CLASS_REGISTRY.get(class_name, cls)

        # Extract main attributes and convert lists to np.ndarray
        value = data.get("value", 0)
        if isinstance(value, list):
            value = np.array(value)
        units = data.get("units", "")

        # Build kwargs by flattening nested ResourceStreams
        kwargs = {}
        for key, val in data.items():
            if key in ("type", "value", "units", "_q"):
                continue
            # Check if this is a nested ResourceStream dict
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
