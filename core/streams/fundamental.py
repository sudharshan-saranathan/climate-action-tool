#  Filename: core/streams/fundamental.py
#  Module name: core.streams.fundamental
#  Description: Fundamental stream types

# Standard
import uuid
import logging
from typing import Dict, Any


# Dataclass
from dataclasses import field
from dataclasses import dataclass


@dataclass(frozen=True)
class Fundamental:
    label: str = "Fundamental"
    units: list[str] = field(default_factory=list)
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Mass(Fundamental):
    @classmethod
    def create(cls):
        return cls(label="Mass", units=["g", "kg", "ton", "MT"], attrs={})


@dataclass(frozen=True)
class Length(Fundamental):
    @classmethod
    def create(cls):
        return cls(label="Length", units=["cm", "m", "km", "mi"], attrs={})


@dataclass(frozen=True)
class Time(Fundamental):
    @classmethod
    def create(cls):
        return cls(label="Time", units=["s", "min", "h", "d"], attrs={})


@dataclass(frozen=True)
class Energy(Fundamental):
    @classmethod
    def create(cls):
        return cls(label="Energy", units=["J", "KJ", "MJ", "GJ", "TJ"], attrs={})


@dataclass(frozen=True)
class Temperature(Fundamental):
    @classmethod
    def create(cls):
        return cls(label="Temperature", units=["°C", "°F", "K"], attrs={})


@dataclass(frozen=True)
class Volume(Fundamental):
    @classmethod
    def create(cls):
        return cls(label="Volume", units=["cm³", "m³", "L", "mL"], attrs={})
