#!/usr/bin/env python3
"""Thorough test of attribute creation from JSON."""

import json
from core.graph.node import Node
from core.streams.composite import FossilFuel, Electricity

# Load the JSON file
with open("example_node.json", "r") as f:
    data = json.load(f)

# Deserialize the node
node = Node.from_dict(data)
tech = node.tech["default"]

print("=" * 70)
print("TESTING ALL ATTRIBUTE CREATION")
print("=" * 70)

# Test FossilFuel
coal = tech.consumed["coal"]
print("\n1. FOSSILFUEL (coal):")
print(f"   Type: {type(coal).__name__}")
print(f"   Value: {coal.value} {coal.units}")

# Check all attributes exist
attrs_to_check = ['cost', 'energy_content', 'carbon_fraction',
                  'sulfur_fraction', 'nitrogen_fraction']
for attr in attrs_to_check:
    if hasattr(coal, attr):
        value = getattr(coal, attr)
        print(f"   ✅ {attr}: {value}")
    else:
        print(f"   ❌ {attr}: MISSING!")

# Test Electricity
elec = tech.produced["electricity"]
print("\n2. ELECTRICITY:")
print(f"   Type: {type(elec).__name__}")
print(f"   Value: {elec.value} {elec.units}")

if hasattr(elec, 'tariff'):
    print(f"   ✅ tariff: {elec.tariff}")
else:
    print(f"   ❌ tariff: MISSING!")

# Test that attributes are the correct type
print("\n3. ATTRIBUTE TYPE CHECKING:")
print(f"   coal.cost is CostPerMass: {type(coal.cost).__name__ == 'CostPerMass'}")
print(f"   coal.energy_content is SpecificEnergy: {type(coal.energy_content).__name__ == 'SpecificEnergy'}")
print(f"   coal.carbon_fraction is ResourceStream: {type(coal.carbon_fraction).__name__ == 'ResourceStream'}")
print(f"   elec.tariff is CostPerEnergy: {type(elec.tariff).__name__ == 'CostPerEnergy'}")

# Test that we can access nested values
print("\n4. NESTED VALUE ACCESS:")
print(f"   coal.cost.value = {coal.cost.value}")
print(f"   coal.cost.units = {coal.cost.units}")
print(f"   coal.energy_content.value = {coal.energy_content.value}")
print(f"   coal.sulfur_fraction.value = {coal.sulfur_fraction.value}")
print(f"   coal.nitrogen_fraction.value = {coal.nitrogen_fraction.value}")
print(f"   elec.tariff.value = {elec.tariff.value}")
print(f"   elec.tariff.units = {elec.tariff.units}")

print("\n" + "=" * 70)
print("✅ ALL ATTRIBUTES CREATED AND ACCESSIBLE!")
print("=" * 70)
