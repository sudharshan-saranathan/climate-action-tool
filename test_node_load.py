#!/usr/bin/env python3
"""Test script to verify node JSON loading and deserialization."""

import json
from core.graph.node import Node
from core.streams.composite import Material, Electricity, FossilFuel

# Load the JSON file
with open("example_node.json", "r") as f:
    data = json.load(f)

# Deserialize the node
node = Node.from_dict(data)

# Verify the node was loaded correctly
print("=" * 60)
print("NODE LOADED SUCCESSFULLY")
print("=" * 60)
print(f"UID: {node.uid}")
print(f"Name: {node.meta.get('name')}")
print(f"Location: {node.meta.get('location')}")
print()

# Check technology
print("TECHNOLOGY: default")
print("-" * 60)
tech = node.tech["default"]

print("\nCONSUMED STREAMS:")
for name, stream in tech.consumed.items():
    print(f"  {name}: {stream}")
    if isinstance(stream, FossilFuel):
        print(f"    - Cost: {stream.cost}")
        print(f"    - Energy Content: {stream.energy_content}")
        print(f"    - Carbon Fraction: {stream.carbon_fraction}")

print("\nPRODUCED STREAMS:")
for name, stream in tech.produced.items():
    print(f"  {name}: {stream}")
    if isinstance(stream, Electricity):
        print(f"    - Tariff: {stream.tariff}")

print("\nEXPENSES:")
print(f"  Capital: {tech.expenses.capital}")
print(f"  Operating: {tech.expenses.operating}")

# Test serialization round-trip
print("\n" + "=" * 60)
print("TESTING ROUND-TRIP SERIALIZATION")
print("=" * 60)
serialized = node.to_dict()
print("Serialized successfully!")

# Save to file for inspection
with open("node_roundtrip.json", "w") as f:
    json.dump(serialized, f, indent=2, default=str)
print("Saved to node_roundtrip.json")

print("\n✅ All tests passed!")
