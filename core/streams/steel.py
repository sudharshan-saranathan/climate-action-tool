# Filename: core/streams/steel.py
# Module name: core.streams.steel
# Description: Steel resource streams for systems modeling

from __future__ import annotations

# Standard
import typing
import numpy as np

# core.streams
from core.streams import *


class Steel(Mass):
    _label = "Steel"

    def __init__(self, data: typing.Union[int, float, np.ndarray], **kwargs):
        super().__init__(data, "kilogram")

        self._cost = CostPerMass(
            kwargs.get("cost", 0.0),
            kwargs.get("cost_units", "INR/kilogram"),
        )

        self._carbon_fraction = ResourceStream(
            kwargs.get("carbon_fraction", 0.0),
            kwargs.get("carbon_fraction_units", "dimensionless"),
        )

        self._chromium_fraction = ResourceStream(
            kwargs.get("chromium_fraction", 0.0),
            kwargs.get("chromium_fraction_units", "dimensionless"),
        )

        self._manganese_fraction = ResourceStream(
            kwargs.get("manganese_fraction", 0.0),
            kwargs.get("manganese_fraction_units", "dimensionless"),
        )

        self._nickel_fraction = ResourceStream(
            kwargs.get("nickel_fraction", 0.0),
            kwargs.get("nickel_fraction_units", "dimensionless"),
        )

        self._vanadium_fraction = ResourceStream(
            kwargs.get("vanadium_fraction", 0.0),
            kwargs.get("vanadium_fraction_units", "dimensionless"),
        )

        self._tungsten_fraction = ResourceStream(
            kwargs.get("tungsten_fraction", 0.0),
            kwargs.get("tungsten_fraction_units", "dimensionless"),
        )

        self._other_fraction = ResourceStream(
            kwargs.get("other_fraction", 0.0),
            kwargs.get("other_fraction_units", "dimensionless"),
        )
