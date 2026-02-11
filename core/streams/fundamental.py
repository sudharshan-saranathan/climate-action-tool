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
    name: str = ""
    unit: str = ""
    attr: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Mass(Fundamental):
    @classmethod
    def create(cls):
        return cls(name="Mass", unit="kg", attr={})


@dataclass(frozen=True)
class Length(Fundamental):
    @classmethod
    def create(cls):
        return cls(name="Length", unit="m", attr={})


@dataclass(frozen=True)
class Time(Fundamental):
    @classmethod
    def create(cls):
        return cls(name="Time", unit="s", attr={})


@dataclass(frozen=True)
class Energy(Fundamental):
    @classmethod
    def create(cls):
        return cls(name="Energy", unit="J", attr={})


@dataclass(frozen=True)
class Temperature(Fundamental):
    @classmethod
    def create(cls):
        return cls(name="Temperature", unit="K", attr={})


@dataclass(frozen=True)
class Volume(Fundamental):
    @classmethod
    def create(cls):
        return cls(name="Volume", unit="m³", attr={})
