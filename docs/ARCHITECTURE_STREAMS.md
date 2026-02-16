# Core Streams Architecture

**Last Updated**: Feb 16, 2026
**Module**: `core/streams/`

---

## Overview

The `core.streams` module provides a flexible, physically-sound system for representing material, energy, and economic flows in climate action models. It's built on three core pillars:

1. **Quantity System**: Unit-aware numbers with automatic type dispatch
2. **Composite Streams**: Domain-specific bundle types (Material, Electricity, Fuel)
3. **Attribute Grouping**: Organize stream properties for GUI and programmatic access

---

## Architecture

```
Quantity (pint UnitRegistry)
  ├── Base class for all physical quantities
  ├── Dimensionality-based type registry
  ├── Automatic arithmetic with type preservation
  └── Serialization/deserialization (to_dict/from_dict)

Physical Units (50+ types)
  ├── Fundamental: Mass, Length, Time, Temperature, ElectricCurrent, etc.
  ├── Derived: Energy, Power, Force, Pressure, etc.
  ├── Domain-specific: CarbonIntensity, Currency, CostPerEnergy, etc.
  └── Registered in Quantity.registry by dimensionality

Composite (dynamic container)
  ├── Base class for high-level stream types
  ├── Flexible kwargs system (auto-instantiates quantities from unit strings)
  ├── attribute_groups: hierarchical organization for GUI display
  └── Extensible via subclassing

Stream Types (Composite subclasses)
  ├── Material: mass, cost (generic solid/liquid)
  ├── Electricity: power, tariff, ramp_rate, grid quality, emissions
  ├── Fuel: mass, energy_content, composition, emissions, sustainability
  └── (Future) Custom streams via user-defined Composite subclasses
```

---

## Quantity System

### Base Class: `Quantity`

```python
from core.streams import Quantity, ureg

# Create quantities with unit strings
mass = Mass("100 kg")
power = EnergyFlowRate("500 kW")
cost = Currency("50000 INR")

# Arithmetic operations preserve type
total_mass = mass + mass  # Returns Mass, not Quantity
power_per_day = power * Time("1 day")  # Returns correct type based on dimensionality

# Unit conversion
mass_in_tons = mass.to("metric_ton")

# Serialization
data = mass.to_dict()  # {"type": "Mass", "value": 100, "units": "kg"}
mass_restored = Quantity.from_dict(data)

# Access underlying pint Quantity
pint_q = mass.quantity  # <Quantity(100, 'kilogram')>
```

### Registry Pattern

Quantities register themselves by dimensionality:

```python
# When Mass subclass is defined with canonical="kg":
# → Quantity.registry[Mass dimensionality] = Mass

# On arithmetic, the result type is auto-selected:
result = mass + energy  # Different dimensionalities
# → result type depends on computed dimensionality
# → If no specific type, defaults to Quantity
```

### Available Physical Units

**Fundamental (SI base)**
- Mass, Length, Time, Temperature, ElectricCurrent, LuminousIntensity, AmountOfSubstance

**Mechanical**
- Area, Volume, Velocity, Acceleration, Force, Pressure
- Energy, EnergyFlowRate (Power), Momentum, AngularVelocity, SurfaceTension

**Thermodynamic**
- Entropy, SpecificHeatCapacity, SpecificEnergy, ChemicalPotential
- MolarEntropy, ThermalConductivity, HeatTransferCoefficient, ThermalResistance, ThermalExpansionCoefficient

**Fluid Mechanics**
- DynamicViscosity

**Radiation**
- Emissivity, Absorptivity, Reflectivity, Transmittance

**Electromagnetic**
- ElectricCharge, Voltage, Resistance, Capacitance, MagneticFlux, MagneticFluxDensity
- Inductance, ElectricalConductivity, Resistivity

**Chemical & Material**
- Diffusivity, CatalyticActivity

**Transport & Flow**
- Frequency, Density, MolarMass, Concentration
- VolumetricFlowRate, MassFlowRate, MassFlux, EnergyFlux
- PowerDensity, SpecificPower, CarbonIntensity

**Economic**
- Currency, CostPerEnergy, CostPerMass, CostPerPower, CostPerVolume

---

## Composite Streams

### Base: `Composite`

A flexible container for bundles of quantities:

```python
from core.streams import Composite

# Create a composite with arbitrary kwargs
my_stream = Composite(
    mass="100 kg",
    cost="500 INR",
    temperature="300 K"
)

# Each kwarg is auto-converted to appropriate Quantity type
assert isinstance(my_stream.mass, Mass)
assert isinstance(my_stream.cost, Currency)
assert isinstance(my_stream.temperature, Temperature)
```

**Key Features:**
- **Dynamic instantiation**: Pass any `name="value units"` pair; quantity type is auto-selected based on dimensionality
- **Attribute groups**: Organize properties for UI display via `attribute_groups` dict
- **Extensibility**: Subclass Composite to create domain-specific stream types

### Attribute Groups

Each Composite subclass defines `attribute_groups` for GUI organization:

```python
class Material(Composite):
    display_hierarchy = {
        "primary": {
            "mass": "Mass",
            "cost": "Cost",
        },
    }

# GUI can use this to show Material attributes in two categories:
# - Primary: [mass, cost]
```

View modes supported:
- **by_complexity**: `simple` (core essentials), `advanced` (specialized)
- **by_domain**: `primary`, `operational`, `environmental`, `economic`, etc.
- **custom**: User-added attributes at runtime

---

## Stream Types

### Material

Generic solid/liquid streams (ore, slag, water, etc.).

```python
from core.streams import Material

ore = Material(
    mass="1000 kg/s",
    cost="500 INR/kg"
)

# Auto-initialized with MassFlowRate and CostPerMass
assert isinstance(ore.mass, MassFlowRate)
assert isinstance(ore.cost, CostPerMass)

# Extensible with custom attributes
iron_ore = Material(
    mass="1000 kg/s",
    cost="500 INR/kg",
    iron_content="0.65 dimensionless",  # 65% Fe
    silica_content="0.15 dimensionless",
)
```

**Attributes:**
- `mass` (MassFlowRate): Flow rate in kg/s
- `cost` (CostPerMass): Cost per unit mass in INR/kg
- Any additional kwargs auto-converted to Quantities

**Use Cases:** Ore, coal, water, slag, steel, cement, etc.

---

### Electricity

Power/grid streams with operational and environmental characteristics.

```python
from core.streams import Electricity

coal_power = Electricity(
    power="1000 MW",
    tariff="4.5 INR/kWh"
)

# Auto-initialized attributes:
assert isinstance(coal_power.power, EnergyFlowRate)  # MW
assert isinstance(coal_power.tariff, CostPerEnergy)  # INR/kWh
assert isinstance(coal_power.ramp_rate, RampRate)  # MW/s
assert isinstance(coal_power.capacity_factor, Quantity)  # dimensionless
```

**Attributes (organized by category):**

**Primary:**
- `power`: EnergyFlowRate (MW, kW, etc.)
- `tariff`: CostPerEnergy (INR/kWh)

**Operational:**
- `ramp_rate`: RampRate (MW/s — how fast power changes)
- `capacity_factor`: Quantity (0-1, actual/nameplate)
- `dispatchability`: Quantity (0-1, controllability)
- `variability`: Quantity (0-1, coefficient of variation)
- `minimum_stable_generation`: Quantity (0-1, minimum stable output)

**Cycle:**
- `start_up_time`: Time (s)
- `shut_down_time`: Time (s)

**Quality (Grid):**
- `voltage`: Voltage (V)
- `power_factor`: Quantity (0-1)
- `frequency`: Frequency (50 or 60 Hz)

**Environmental:**
- `CO2_intensity`: CarbonIntensity (kg CO2/kWh)
- `SOx_intensity`, `NOx_intensity`, `PM2_5_intensity`, `PM10_intensity`: Quantity (kg/kWh)

**Economic:**
- `LCOE`: CostPerEnergy (levelized cost of energy in INR/kWh)

**Use Cases:** Coal power, gas power, solar, wind, grid, CHP, etc.

---

### Fuel

Energy-dense material with composition and emissions.

```python
from core.streams import Fuel

coal = Fuel(
    mass="100 kg/s",
    cost="300 INR/kg",
    energy_content="24 MJ/kg"  # Higher heating value
)

# Inherited from Material:
assert isinstance(coal.mass, MassFlowRate)
assert isinstance(coal.cost, CostPerMass)

# New to Fuel:
assert isinstance(coal.energy_content, SpecificEnergy)
```

**Attributes (organized by category):**

**Primary:**
- `mass`: MassFlowRate (kg/s)
- `cost`: CostPerMass (INR/kg)
- `energy_content`: SpecificEnergy (MJ/kg, HHV)

**Chemical:**
- `moisture_content`: Quantity (dimensionless, 0-1)
- `ash_content`: Quantity (dimensionless, 0-1)

**Composition (elemental mass fractions):**
- `carbon_fraction`: Quantity (0-1)
- `hydrogen_fraction`: Quantity (0-1)
- `oxygen_fraction`: Quantity (0-1)
- `nitrogen_fraction`: Quantity (0-1)
- `sulfur_fraction`: Quantity (0-1)

**Emissions (factors per kg fuel burned):**
- `CO2_emissions`: Quantity (kg CO2/kg fuel)
- `CH4_emissions`: Quantity (kg CH4/kg fuel)
- `SOx_emissions`, `NOx_emissions`: Quantity
- `PM2_5_emissions`, `PM10_emissions`: Quantity
- `CO_emissions`: Quantity

**Sustainability:**
- `renewable_fraction`: Quantity (0-1, 0=fossil, 1=biomass)
- `carbon_neutrality_factor`: Quantity (0-1, for carbon accounting)

**Use Cases:** Coal, natural gas, biomass, hydrogen, syngas, etc.

---

## Serialization

### to_dict() and from_dict()

All Quantities and Composites support round-trip serialization:

```python
coal = Fuel(
    mass="100 kg/s",
    cost="300 INR/kg",
    energy_content="24 MJ/kg"
)

# Serialize
data = coal.to_dict()
# {
#     "type": "Fuel",
#     "mass": {"type": "MassFlowRate", "value": 100, "units": "kg/s"},
#     "cost": {"type": "CostPerMass", "value": 300, "units": "INR/kg"},
#     "energy_content": {"type": "SpecificEnergy", "value": 24, "units": "MJ/kg"},
#     ...
# }

# Deserialize
import json
json_str = json.dumps(data)
coal_restored = Quantity.from_dict(json.loads(json_str))
assert coal_restored.mass.value == 100
```

This enables:
- Saving/loading schematics to JSON
- Storing in HDF5
- Transmitting over APIs
- Version control friendly

---

## Integration with core.graph

### Nodes: Technology.consumed / Technology.produced

Each node has two dictionaries mapping stream names to Quantity types:

```python
# In core/graph/node.py
@dataclass
class Technology:
    consumed: dict[str, Quantity]  # Input streams (e.g., {"coal": Fuel, "air": Material})
    produced: dict[str, Quantity]  # Output streams (e.g., {"steam": Material, "power": Electricity})
```

### Edges: Stream Matching

When connecting nodes, `GraphManager._verify_stream_matching()` checks that at least one output stream type from the source matches an input stream type in the target:

```python
source_produced = {"coal": Fuel, "power": Electricity}
target_consumed = {"fuel": Material, "power": Electricity}

# Matching streams: "power" (both have Electricity/EnergyFlowRate)
# → Connection allowed
```

### Edge Payload

Edges carry metadata about which stream(s) flow through them:

```python
@dataclass
class Edge:
    payload: Dict[str, str]  # e.g., {"stream": "power", "value": "1000 MW"}
```

---

## Design Decisions

### 1. Composite vs Fixed Schema

**Decision**: Flexible Composite with dynamic kwargs instead of fixed property schema.

**Rationale**:
- Allows arbitrary custom streams without modifying base classes
- Users can extend Material/Electricity/Fuel with domain-specific properties
- Attribute groups allow UI to organize properties semantically

**Trade-off**: Less type safety at definition time; reliance on string-based kwargs.

---

### 2. Registry Pattern for Type Dispatch

**Decision**: Quantity types self-register by dimensionality.

**Rationale**:
- Arithmetic operations (`mass + mass`) return the correct type without manual casting
- Extensible: new Quantity subclasses register automatically
- Dimensionality is unambiguous physical truth

**Trade-off**: Requires `canonical` declaration on each Quantity subclass.

---

### 3. No "Credit" or Generic Currency Stream

**Decision**: Removed "Credit" base class; Currency is a Quantity type, not a Composite.

**Rationale**:
- Currency is a dimension like Mass/Energy, not a bundle of properties
- Economic streams (cost, revenue) are attributes of Material/Electricity/Fuel, not separate types
- Avoids class explosion and conceptual confusion

**Example**: Instead of `Credit("500 INR")`, use `Material(..., cost="500 INR/kg")`

---

### 4. No Profiles in Core Streams

**Note**: Original design mentioned time-varying profiles. This is **deferred** to:
- `core/data/`: Plant parameter definitions
- `core/optimization/`: Time-parameterized variables

Streams themselves are point-in-time quantities; time-varying behavior is handled at the schematic/optimization layer.

---

## Testing

Located in `tests/core/test_streams.py` (to be created):

```python
import pytest
from core.streams import Mass, Electricity, Fuel, Quantity

def test_mass_arithmetic():
    """Test that Mass + Mass returns Mass."""
    m1 = Mass("100 kg")
    m2 = Mass("50 kg")
    result = m1 + m2
    assert isinstance(result, Mass)
    assert result.value == 150

def test_fuel_serialization():
    """Test round-trip serialization of Fuel."""
    fuel = Fuel(mass="100 kg/s", energy_content="24 MJ/kg")
    data = fuel.to_dict()
    restored = Quantity.from_dict(data)
    assert isinstance(restored, Fuel)
    assert restored.mass.value == 100

def test_electricity_attributes():
    """Test that Electricity has expected attributes."""
    elec = Electricity(power="1000 MW")
    assert hasattr(elec, 'power')
    assert hasattr(elec, 'tariff')
    assert hasattr(elec, 'ramp_rate')
    assert hasattr(elec, 'CO2_intensity')

def test_custom_material():
    """Test extending Material with custom attributes."""
    ore = Material(
        mass="1000 kg/s",
        iron_content="0.65 dimensionless"
    )
    assert hasattr(ore, 'iron_content')
    assert ore.iron_content.value == 0.65
```

---

## Future Extensions

1. **Custom Streams**: Allow users to define new Composite subclasses in the UI
2. **Profiles**: Time-varying stream values (deferred to optimization layer)
3. **Stream Validation**: Constraints (e.g., "mass must be positive")
4. **Conversion Efficiency**: Track losses when streams transform (e.g., fuel → power)
5. **Causal Reasoning**: Propagate stream changes through the graph

---

## References

- **Module**: `core/streams/`
  - `quantity.py`: Base Quantity class and registry
  - `physical.py`: 50+ physical unit types
  - `composite.py`: Composite, Material, Electricity, Fuel

- **Integration**: `core/graph/node.py` (Technology.consumed/produced)

- **GUI**: `gui/graph/node/tree.py` (StreamTree for editing)
