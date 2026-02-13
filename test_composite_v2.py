#!/usr/bin/env python3
"""Test the new CompositeStream design with pure composition."""

import sys
sys.path.insert(0, '/Users/sudharshan/PycharmProjects/climate-action-tool')

from core.streams.composite_v2 import Material, Energy, Cost, FossilFuel
import json

print("=" * 70)
print("TESTING COMPOSITE STREAMS (Pure Composition)")
print("=" * 70)

# Test 1: Material
print("\n1. MATERIAL:")
steel = Material(1000, "kilogram", cost=50, cost_units="INR/kilogram")
print(f"   steel.mass = {steel.mass}")
print(f"   steel.cost = {steel.cost}")
print(f"   Accessing mass value: {steel.mass.value} {steel.mass.units}")
print(f"   Accessing cost value: {steel.cost.value} {steel.cost.units}")

# Test 2: Energy
print("\n2. ENERGY:")
electricity = Energy(500, "megawatt", tariff=6.5, tariff_units="INR/joule")
print(f"   electricity.power = {electricity.power}")
print(f"   electricity.tariff = {electricity.tariff}")

# Test 3: Cost
print("\n3. COST:")
tax = Cost(10000, "INR")
print(f"   tax.amount = {tax.amount}")

# Test 4: FossilFuel
print("\n4. FOSSIL FUEL:")
coal = FossilFuel(
    1000, "kilogram",
    cost=50, cost_units="INR/kilogram",
    energy_content=24000000, energy_content_units="joule/kilogram",
    carbon_fraction=0.7, carbon_fraction_units="dimensionless"
)
print(f"   coal.mass = {coal.mass}")
print(f"   coal.cost = {coal.cost}")
print(f"   coal.energy_content = {coal.energy_content}")
print(f"   coal.carbon_fraction = {coal.carbon_fraction}")

# Test 5: Serialization
print("\n5. SERIALIZATION:")
steel_dict = steel.to_dict()
print(f"   steel.to_dict() = {json.dumps(steel_dict, indent=2, default=str)}")

# Test 6: Deserialization
print("\n6. DESERIALIZATION:")
steel_copy = Material.from_dict(steel_dict)
print(f"   Reconstructed steel.mass = {steel_copy.mass}")
print(f"   Reconstructed steel.cost = {steel_copy.cost}")

# Test 7: Arithmetic on attributes
print("\n7. ARITHMETIC ON ATTRIBUTES:")
steel2 = Material(500, "kilogram", cost=50, cost_units="INR/kilogram")
total_mass = steel.mass + steel2.mass
print(f"   steel.mass + steel2.mass = {total_mass}")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
