# Filename: basic.py
# Module name: flow
# Description: Basic flow types.

"""
Basic stream/flow type definitions.
"""

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from qtawesome import icon

import types
from typing import ClassVar
from dataclasses import dataclass


class Flow:
    """Base class representing a stream/flow type in the graph."""

    @dataclass(frozen=True)
    class Attrs:
        keyID: ClassVar[str] = "flow"
        color: ClassVar[str] = "#ffffff"
        label: ClassVar[str] = "Flow"
        units: ClassVar[list[str]] = []
        image: ClassVar[QtGui.QIcon] = icon("mdi.minus", color="#ffffff")

    def __init__(self, units: list[str] = None, props: list = None):
        props = {p.label: p for p in props} if props else dict()

        self._value = 0.0
        self._units = units
        self._attrs = types.SimpleNamespace(props=props)

    @property
    def label(self) -> str:
        return self.Attrs.label

    @property
    def image(self) -> QtGui.QIcon:
        return self.Attrs.image

    @property
    def color(self) -> str:
        return self.Attrs.color

    @property
    def units(self) -> list[str]:
        return self._units if self._units is not None else self.Attrs.units

    @property
    def props(self) -> dict:
        return self._attrs.props


class Item(Flow):
    """Flow of countable items."""

    @dataclass(frozen=True)
    class Attrs(Flow.Attrs):
        keyID: ClassVar[str] = "item"
        color: ClassVar[str] = "#8a8a8a"
        label: ClassVar[str] = "Item"
        units: ClassVar[list[str]] = ["count"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.package", color="#8a8a8a")


class Mass(Flow):
    """Flow of mass (weight)."""

    @dataclass(frozen=True)
    class Attrs(Flow.Attrs):
        keyID: ClassVar[str] = "mass"
        color: ClassVar[str] = "#78cad2"
        label: ClassVar[str] = "Mass"
        units: ClassVar[list[str]] = ["gms", "kgs", "tons", "MTs"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.weight-gram", color="#78cad2")


class Energy(Flow):
    """Flow of energy."""

    @dataclass(frozen=True)
    class Attrs(Flow.Attrs):
        keyID: ClassVar[str] = "energy"
        color: ClassVar[str] = "#ffa500"
        label: ClassVar[str] = "Energy"
        units: ClassVar[list[str]] = ["J", "kJ", "MJ", "GJ"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.fire", color="#ffa500")


class Credit(Flow):
    """Flow of currency/credits."""

    @dataclass(frozen=True)
    class Attrs(Flow.Attrs):
        keyID: ClassVar[str] = "credit"
        color: ClassVar[str] = "#5eb616"
        label: ClassVar[str] = "Credit"
        units: ClassVar[list[str]] = ["INR", "USD"]
        image: ClassVar[QtGui.QIcon] = icon("mdi.cash-multiple", color="#5eb616")
