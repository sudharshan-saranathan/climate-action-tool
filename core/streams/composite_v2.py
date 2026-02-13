# Filename: core/streams/composite_v2.py
# Module name: core.streams.composite
# Description: Composite streams using pure composition (not inheritance)

from __future__ import annotations

# Standard
import typing
import numpy as np

# core.streams
from core.streams import (
    MassFlux,
    MassFlowRate,
    Energy,
    EnergyFlowRate,
    Currency,
    CostPerMass,
    CostPerEnergy,
    SpecificEnergy,
    Quantity,
    VolumetricFlowRate,
)


class CompositeStream:
    """
    Base class for composite streams with serialization support.
    """

    def to_dict(self) -> dict[str, typing.Any]:
        """
        Serialize the composite stream into a dictionary.
        :return: Dictionary representation of the stream.
        """

        result = {"type": self.__class__.__name__}
        for key, item in self.__dict__.items():
            result[key] = item.to_dict() if isinstance(item, ResourceStream) else item

        return result


class Material(CompositeStream):
    """
    Material stream with mass as the primary attribute.
    """

    def __init__(
        self,
        mass: typing.Union[int, float, np.ndarray],
        mass_units: str = "kilogram",
        **kwargs,
    ):
        # Primary attribute
        self.mass = MassFlowRate(mass, mass_units)

        # Secondary attributes
        self.cost = CostPerMass(
            kwargs.get("cost", 0.0),
            kwargs.get("cost_units", "INR/kilogram"),
        )


class Fuel(CompositeStream):
    """Fossil fuel stream - specialized Material with emission properties.

    Extends Material concept with energy content and emission fractions.
    """

    def __init__(
        self,
        **kwargs,
    ):
        # Primary attribute
        self.mass = MassFlowRate(
            kwargs.get("mass", "0 kg/s"),
            kwargs.get("mass_units", "kilogram/second"),
        )

        # Economic attribute
        self.cost = CostPerMass(
            kwargs.get("cost", 0.0),
            kwargs.get("cost_units", "INR/kilogram"),
        )

        # Energy content
        self.energy_content = SpecificEnergy(
            kwargs.get("energy_content", 0.0),
            kwargs.get("energy_content_units", "joule/kilogram"),
        )

        # Emission fractions
        self.carbon_fraction = ResourceStream(
            kwargs.get("carbon_fraction", 0.0),
            kwargs.get("carbon_fraction_units", "dimensionless"),
        )

        self.sulfur_fraction = ResourceStream(
            kwargs.get("sulfur_fraction", 0.0),
            kwargs.get("sulfur_fraction_units", "dimensionless"),
        )

        self.nitrogen_fraction = ResourceStream(
            kwargs.get("nitrogen_fraction", 0.0),
            kwargs.get("nitrogen_fraction_units", "dimensionless"),
        )
