# Filename: core/graph/node.py
# Module name: core.graph
# Description: A backend data-structure for bi-directional, multi-graphs

from __future__ import annotations
from typing import Dict, Type, Any
from types import SimpleNamespace
import json

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# core.streams
from core.streams.quantity import ResourceStream
from core.signals import SignalBus


@dataclass
class Technology:
    consumed: dict[str, ResourceStream] = field(default_factory=dict)
    produced: dict[str, ResourceStream] = field(default_factory=dict)
    expenses: SimpleNamespace = field(
        default_factory=lambda: SimpleNamespace(
            capital=0,
            operating=0,
        )
    )

    params: dict[str, ResourceStream] = field(default_factory=dict)
    equations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "consumed": {
                name: stream.to_dict() for name, stream in self.consumed.items()
            },
            "produced": {
                name: stream.to_dict() for name, stream in self.produced.items()
            },
            "expenses": {
                "capital": self.expenses.capital,
                "operating": self.expenses.operating,
            },
            "params": self.params,
            "equations": self.equations,
        }


# Dataclass
@dataclass(frozen=True)
class Node:

    uid: str
    meta: Dict[str, Any]
    tech: dict[str, Technology] = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.uid)

    def __eq__(self, other) -> bool:

        if not isinstance(other, Node):
            return False

        return self.uid == other.uid

    @classmethod
    def from_dict(cls: Type[Node], data: dict) -> Node:
        """Reconstruct Node from the dictionary with full Technology deserialization."""

        # Deserialize tech dictionary
        tech_dict = {}
        for tech_name, tech_data in data.get("tech", {}).items():
            # Deserialize consumed streams
            consumed = {
                name: ResourceStream.from_dict(stream_data)
                for name, stream_data in tech_data.get("consumed", {}).items()
            }
            # Deserialize produced streams
            produced = {
                name: ResourceStream.from_dict(stream_data)
                for name, stream_data in tech_data.get("produced", {}).items()
            }
            # Deserialize expenses
            expenses_data = tech_data.get("expenses", {})
            expenses = SimpleNamespace(
                capital=expenses_data.get("capital", 0),
                operating=expenses_data.get("operating", 0),
            )

            # Create a new technology branch
            tech_dict[tech_name] = Technology(
                consumed=consumed,
                produced=produced,
                expenses=expenses,
                params=tech_data.get("params", {}),
                equations=tech_data.get("equations", []),
            )

        return cls(
            uid=data.get("uid", ""),
            meta=data.get("meta", {}),
            tech=tech_dict,
        )

    @classmethod
    def from_json(cls: Type[Node], jstr: str) -> Node:
        return cls.from_dict(json.loads(jstr))

    def to_dict(self) -> dict[str, Any]:

        return {
            "uid": self.uid,
            "meta": self.meta,
            "tech": {
                tech_name: tech.to_dict() for tech_name, tech in self.tech.items()
            },
        }

    def get_produced(self) -> set[str]:
        """
        Return this node's output streams as a set.
        :return: Set of produced stream names.
        """
        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.produced.keys()
        )

    def get_consumed(self) -> set[str]:
        """
        Return this node's input streams as a set.
        :return: Set of consumed stream names.
        """
        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.consumed.keys()
        )

    def set_consumed(
        self,
        path: str,
        value: str,
        units: str = None,
        create_if_missing: bool = False,
        stream_class: str = "ResourceStream",
    ) -> None:
        """Set or update a consumed stream.

        Args:
            path: Path like "SteamTurbine.steam.enthalpy.units"
            value: Value to set (for creating streams or updating value)
            units: Units to set (optional)
            create_if_missing: If True, create stream/pathway if it doesn't exist (like 'mkdir -p')
            stream_class: Type of stream to create if it doesn't exist (default: ResourceStream)
        """

        words = path.strip(".").split(".")
        if len(words) < 3:
            bus = SignalBus()
            bus.ui.notify.emit(
                self.uid,
                f"Invalid path: {path}. Expected: pathway.stream_name.property",
            )
            return

        branch = words[0]
        stream = words[1]

    def set_produced(
        self,
        path: str,
        value=None,
        units: str = None,
        stream_type: str = "ResourceStream",
        create: bool = False,
    ) -> None:
        """Set or update a produced stream parameter.

        Args:
            path: Path like "blastfurnace.moltenslag.rich_slag.silica_content.units"
            value: Value to set (for creating streams or updating value)
            units: Units to set (optional)
            stream_type: Type of stream to create if it doesn't exist (default: ResourceStream)
            create: If True, create stream/pathway if it doesn't exist (like 'mkdir -p')

        Examples:
            # Update existing stream
            node.set_produced("blastfurnace.steel.value", 100, "kg/s")

            # Create new stream (requires create=True)
            node.set_produced("blastfurnace.newstream.value", 50, "kg/s", create=True)
        """
        parts = path.strip(".").split(".")
        if len(parts) < 3:
            raise ValueError(
                f"Invalid path: {path}. Expected: pathway.stream_name.property"
            )

        pathway = parts[0]
        stream_name = parts[1]
        property_path = parts[2:]  # Remaining path to navigate

        # Check if pathway exists
        if pathway not in self.tech:
            if not create:
                raise ValueError(
                    f"Pathway '{pathway}' not found. Use create=True to create it."
                )
            self.tech[pathway] = Technology()
        tech = self.tech[pathway]

        # Check if stream exists
        if stream_name not in tech.produced:
            if not create:
                raise ValueError(
                    f"Stream '{stream_name}' not found in pathway '{pathway}'. Use create=True to create it."
                )
            if value is None:
                raise ValueError(
                    f"Must provide 'value' to create new stream '{stream_name}'."
                )
            from core.streams import CLASS_REGISTRY

            stream_class = CLASS_REGISTRY.get(stream_type, ResourceStream)
            tech.produced[stream_name] = stream_class(value, units or "")

        # Navigate to target attribute
        target = tech.produced[stream_name]
        for attr in property_path[:-1]:
            if not hasattr(target, attr):
                raise ValueError(f"No attribute '{attr}' on {type(target).__name__}")
            target = getattr(target, attr)

        # Set final property
        final_prop = property_path[-1]
        if final_prop == "value":
            if value is None:
                raise ValueError("Must provide 'value' parameter")
            target.value = value
        elif final_prop == "units":
            if units is None:
                raise ValueError("Must provide 'units' parameter")
            target._q = target._q.__class__(target.value, units)
        else:
            raise ValueError(f"Unknown property: {final_prop}. Use 'value' or 'units'")

    def set_parameter(
        self,
        path: str,
        value=None,
        units: str = None,
        param_type: str = "ResourceStream",
        create: bool = False,
    ) -> None:
        """Set or update a technology parameter.

        Args:
            path: Path like "steamturbine.efficiency.value"
            value: Value to set
            units: Units to set (optional)
            param_type: Type of parameter to create if it doesn't exist
            create: If True, create parameter/pathway if it doesn't exist (like 'mkdir -p')

        Examples:
            # Update existing parameter
            node.set_parameter("steamturbine.efficiency.value", 0.85)

            # Create new parameter (requires create=True)
            node.set_parameter("steamturbine.max_temp.value", 1200, "celsius", create=True)
        """
        parts = path.strip(".").split(".")
        if len(parts) < 3:
            raise ValueError(
                f"Invalid path: {path}. Expected: pathway.param_name.property"
            )

        pathway = parts[0]
        param_name = parts[1]
        property_path = parts[2:]

        # Check if pathway exists
        if pathway not in self.tech:
            if not create:
                raise ValueError(
                    f"Pathway '{pathway}' not found. Use create=True to create it."
                )
            self.tech[pathway] = Technology()
        tech = self.tech[pathway]

        # Check if parameter exists
        if param_name not in tech.params:
            if not create:
                raise ValueError(
                    f"Parameter '{param_name}' not found in pathway '{pathway}'. Use create=True to create it."
                )
            if value is None:
                raise ValueError(
                    f"Must provide 'value' to create new parameter '{param_name}'."
                )
            from core.streams import CLASS_REGISTRY

            param_class = CLASS_REGISTRY.get(param_type, ResourceStream)
            tech.params[param_name] = param_class(value, units or "")

        # Navigate to target attribute
        target = tech.params[param_name]
        for attr in property_path[:-1]:
            if not hasattr(target, attr):
                raise ValueError(f"No attribute '{attr}' on {type(target).__name__}")
            target = getattr(target, attr)

        # Set final property
        final_prop = property_path[-1]
        if final_prop == "value":
            if value is None:
                raise ValueError("Must provide 'value' parameter")
            target.value = value
        elif final_prop == "units":
            if units is None:
                raise ValueError("Must provide 'units' parameter")
            target._q = target._q.__class__(target.value, units)
        else:
            raise ValueError(f"Unknown property: {final_prop}. Use 'value' or 'units'")

    def set_equation(self, pathway: str, equation: str) -> None:
        """Add an equation to a technology pathway.

        Args:
            pathway: Technology pathway name (e.g., "BF", "EAF", "steamturbine")
            equation: Equation string to add

        Examples:
            node.set_equation("BF", "steel_output = iron_ore_input * efficiency")
            node.set_equation("steamturbine", "power = steam_flow * enthalpy_drop")
        """
        # Create technology if it doesn't exist
        if pathway not in self.tech:
            self.tech[pathway] = Technology()

        tech = self.tech[pathway]

        # Add equation if not already present
        if equation not in tech.equations:
            tech.equations.append(equation)
