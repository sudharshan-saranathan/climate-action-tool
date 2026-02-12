# Filename: core/streams/composite.py
# Module name: core.streams.resources
# Description: Composite high-level resource streams for systems modeling

from __future__ import annotations

# Standard
import typing
import numpy as np

# core.streams
from core.streams import *


class Material(Mass):
    _label = "Raw Material"

    def __init__(
        self,
        data: typing.Union[int, float, np.ndarray],
        units: str = "kilogram",
        **kwargs,
    ):
        super().__init__(data, units)

        self.cost = CostPerMass(
            kwargs.get("cost", 0.0),
            kwargs.get("cost_units", "INR/kilogram"),
        )


class Electricity(Power):
    _label = "Electricity"

    def __init__(
        self,
        data: typing.Union[int, float, np.ndarray],
        units: str = "watt",
        **kwargs,
    ):
        super().__init__(data, units)

        self.cost = CostPerEnergy(
            kwargs.get("cost", 0.0),
            kwargs.get("cost_units", "INR/watt*hour"),
        )


class FossilFuel(Mass):
    _label = "Fossil Fuel"

    def __init__(
        self,
        data: typing.Union[int, float, np.ndarray],
        units: str = "kilogram",
        **kwargs,
    ):
        super().__init__(data, units)

        self.cost = CostPerMass(
            kwargs.get("cost", 0.0),
            kwargs.get("cost_units", "INR/kilogram"),
        )

        self.energy_content = SpecificEnergy(
            kwargs.get("energy_content", 0.0),
            kwargs.get("energy_content_units", "joule/kilogram"),
        )

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
