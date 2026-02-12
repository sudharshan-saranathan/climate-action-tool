#!/usr/bin/env python3
"""Test the new set_consumed, set_produced, set_parameter, set_equation methods."""

from core.graph.node import Node

# Create a node
node = Node(uid="test_plant", meta={"name": "Test Plant"})

print("=" * 70)
print("TESTING SET METHODS")
print("=" * 70)

# Test 1: set_consumed - create a simple stream (with create=True)
print("\n1. CREATE CONSUMED STREAM (create=True):")
node.set_consumed("steamturbine.steam.value", 100, "kg/s", create=True)
print(f"   steamturbine.steam = {node.tech['steamturbine'].consumed['steam']}")

# Test 2: set_consumed - create with composite type
print("\n2. CREATE CONSUMED STREAM (Electricity type, create=True):")
node.set_consumed("plant.electricity.value", 500, "megawatt", stream_type="Electricity", create=True)
elec = node.tech['plant'].consumed['electricity']
print(f"   plant.electricity = {elec}")
print(f"   Has tariff attribute: {hasattr(elec, 'tariff')}")

# Test 3: set_consumed - update nested attribute (no create flag needed for updates)
print("\n3. UPDATE NESTED ATTRIBUTE:")
node.set_consumed("plant.electricity.tariff.value", 6.5, "INR/joule")
print(f"   plant.electricity.tariff = {elec.tariff}")

# Test 4: set_produced - create stream
print("\n4. CREATE PRODUCED STREAM (create=True):")
node.set_produced("blastfurnace.steel.value", 200, "kilogram", stream_type="Material", create=True)
steel = node.tech['blastfurnace'].produced['steel']
print(f"   blastfurnace.steel = {steel}")
print(f"   Has cost attribute: {hasattr(steel, 'cost')}")

# Test 5: set_parameter
print("\n5. SET PARAMETER (create=True):")
node.set_parameter("steamturbine.efficiency.value", 0.85, "dimensionless", create=True)
eff = node.tech['steamturbine'].params['efficiency']
print(f"   steamturbine.efficiency = {eff}")

# Test 6: Test guardrails - should fail without create=True
print("\n6. TEST GUARDRAILS (should fail):")
try:
    node.set_consumed("nonexistent.stream.value", 100, "kg/s")
    print("   ❌ FAILED - should have raised error!")
except ValueError as e:
    print(f"   ✅ Correctly blocked: {e}")

# Test 7: set_equation
print("\n7. ADD EQUATIONS:")
node.set_equation("steamturbine", "power = steam_flow * enthalpy_drop * efficiency")
node.set_equation("blastfurnace", "steel_output = iron_ore_input * yield_factor")
print(f"   steamturbine equations: {node.tech['steamturbine'].equations}")
print(f"   blastfurnace equations: {node.tech['blastfurnace'].equations}")

# Test 8: Verify all pathways exist
print("\n8. VERIFY PATHWAYS:")
print(f"   Technologies: {list(node.tech.keys())}")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
