# Filename: core/graph/node.py
# Module name: core.graph
# Description: A backend data-structure for bi-directional, multi-graphs

from __future__ import annotations

# Standard Library
import logging
import typing
import json
# Dataclass
from dataclasses import field
from dataclasses import dataclass

# core.streams
from core.streams.quantity import Quantity


@dataclass
class Technology:
    inp: dict[str, Quantity] = field(default_factory=dict)
    out: dict[str, Quantity] = field(default_factory=dict)
    par: dict[str, Quantity] = field(default_factory=dict)
    eqn: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, typing.Any]:

        return {
            "inp": {key: value.to_dict() for key, value in self.inp.items()},
            "out": {key: value.to_dict() for key, value in self.out.items()},
            "par": {key: value.to_dict() for key, value in self.par.items()},
            "eqn": {key: value for key, value in self.eqn.items()},
        }

    def to_json(self) -> str:

        try:
            return json.dumps(self.to_dict())

        except Exception as e:
            logging.warning(f"Error converting Technology to JSON: {e}")
            return "{}"

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Technology:

        inp = data.get("inp", {})
        out = data.get("out", {})
        par = data.get("par", {})
        eqn = data.get("eqn", {})

        return cls(
            inp={key: value for key, value in inp.items()},
            out={key: value for key, value in out.items()},
            par={key: value for key, value in par.items()},
            eqn={key: value for key, value in eqn.items()},
        )

    def from_json(self, jstr: str) -> Technology:

        try:
            return self.from_dict(json.loads(jstr))

        except Exception as e:
            logging.warning(f"Invalid JSON for Technology.from_json: {e}")
            return self.from_dict({})


# Dataclass
@dataclass(frozen=True)
class Node:

    nuid: str
    meta: dict[str, typing.Any]
    tech: dict[str, Technology] = field(default_factory=dict)

    # Return a dictionary representation of the node
    def to_dict(self) -> dict[str, typing.Any]:

        return {
            "nuid": self.nuid,
            "meta": self.meta,
            "tech": {
                tech_name: tech.to_dict() for tech_name, tech in self.tech.items()
            },
        }

    # Return a JSON representation of the node
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    # Create a Node instance from a dictionary
    @classmethod
    def from_dict(cls: typing.Type[Node], data: dict[str, typing.Any]) -> Node:

        # Deserialize tech dictionary
        technology = {
            key: Technology.from_dict(value)
            for key, value in data.get("tech", {}).items()
        }

        return cls(
            nuid=data.get("nuid", ""),
            meta=data.get("meta", {}),
            tech=technology,
        )

    # Create a Node instance from a JSON string
    @classmethod
    def from_json(cls: typing.Type[Node], jstr: str) -> Node:
        return cls.from_dict(json.loads(jstr))

    def get_out_streams(self) -> set[str]:
        """
        Return this node's output streams as a set.
        :return: Set of produced stream names.
        """

        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.out.keys()
        )

    def get_inp_streams(self) -> set[str]:
        """
        Return this node's input streams as a set.
        :return: Set of consumed stream names.
        """

        return set(
            stream_name
            for tech in self.tech.values()
            for stream_name in tech.inp.keys()
        )

    # Create a new technology branch for this node with the given JSON string
    def create_tech_branch(self, branch: str, jstr: str) -> None:

        # Import SignalBus
        from core.signals import SignalBus

        try:
            dictionary = json.loads(jstr)
            self.tech[branch] = Technology.from_dict(dictionary)

        except json.JSONDecodeError as e:
            logging.warning(f"Invalid JSON for set_branch: {e}")
            bus = SignalBus()
            bus.ui.notify.emit(
                self.nuid,
                f"ERROR: Invalid JSON for set_branch: {e}",
            )

    # Return a hash of the node's unique identifier
    def __hash__(self) -> int:
        return hash(self.nuid)

    # Check if two nodes are equal based on their unique identifiers
    def __eq__(self, other) -> bool:
        return self.nuid == other.nuid if isinstance(other, Node) else False
