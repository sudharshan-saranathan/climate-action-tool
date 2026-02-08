# Climate Action Tool (CAT): MVP Roadmap

## Project Vision

**Climate Action Tool** is a decision-support system for analyzing sector-level decarbonization pathways at plant granularity.

**Use Case**: "What's a cost-efficient and low-carbon pathway for Emission-Factor < 0.5 by 2050, given 5000+ steel plants in India with 80% BF-BOF, 20% DRI, 5% CCUS penetration?"

---

## Core Architecture (DONE ✅)

The foundation built so far is **exactly right for this domain**:

### 1. Dimension-Based Flow System ✅
**Why this matters for CAT:**
- Steel plants consume Mass flows (iron ore), Energy flows (electricity), and emit emissions
- Each plant has multiple pathways: BF-BOF, DRI-EAF, with different parameter profiles
- Profiles let you model time-evolution: "CCUS adoption increases 0-50% by 2050"

**Implementation:**
- `dimensions.py`: Mass, Energy, Power, Currency, Temperature, Pressure
- `flows.py`: MassFlow, EnergyFlow, PowerFlow, CurrencyFlow
- `combos.py`: Fuel, Electricity, Material, Product, Fluid
- **Key**: Each flow can have fixed (specific_energy) and variable (cost) parameters

### 2. Time-Varying Profiles ✅
**Why this matters for CAT:**
- Parameters change over time: costs evolve, efficiency improves, CCUS costs decline
- Profiles enable: "Electricity tariff = $50/MWh in 2024, $30/MWh by 2050"
- Three profile types: Fixed, Linear, Stepped (matches reality)

**Use in CAT:**
```
BF-BOF pathway:
  - specific_energy: Fixed(12 GJ/ton) ← unchanged
  - emissions_factor: Stepped([2024, 2030, 2050] → [1.8, 1.6, 1.2]) ← CCUS effect
  - cost: Linear([2024, 2050] → [$80/ton, $120/ton]) ← inflation
```

### 3. Fixed vs Variable Parameters ✅
**Why this matters for CAT:**
- Physical constants (specific energy of a process) → Fixed
- Market variables (electricity cost, CCUS penetration) → Variable
- UI reflects this: users can't accidentally change fundamental physics

**Use in CAT:**
```
Plant parameters:
  ├─ specific_energy (BF-BOF) → FIXED: 12 GJ/ton
  ├─ CCUS_penetration → VARIABLE: can explore 0-100%
  ├─ Electricity_tariff → VARIABLE: market-driven
  └─ CO2_capture_cost → VARIABLE: technology improvement
```

---

## MVP Phases

### Phase 1: Data & Mapping (2-3 weeks) 🗺️

**Goal**: "Open India's map, see 5000+ plants"

**Tasks**:
1. **GeoJSON India Boundary**
   - Load state boundaries from geojson file
   - Display in QGraphicsView/QGraphicsScene
   - Pan/zoom working

2. **Plant Data Model**
   ```python
   class Plant:
       id: str
       name: str
       state: str
       lat: float
       lon: float
       capacity: float  # tons/year
       pathway: str  # "BF-BOF", "DRI-EAF", "Hybrid"
       parameters: Dict[str, Parameter]  # from core.flow
   ```

3. **Data Loading**
   - Read Excel/SQL with plant data
   - Parse lat-lon
   - Create Plant instances
   - Plot as pins on map (color by pathway: BF-BOF=red, DRI=blue, Hybrid=yellow)

4. **Map Interaction**
   - Single-click: show plant summary (tooltip)
   - Double-click: open Plant Schematic (Phase 2)
   - Legend: show pathway types and filter by state

**Deliverable**: Map with 5000+ pins, clickable, plant data loaded

---

### Phase 2: Plant Schematic (3-4 weeks) 📊

**Goal**: "Double-click a pin → see plant's process flow"

**Architecture**:
```
SuperTemplate (all possible pathways)
  ├─ BF-BOF pathway
  │  ├─ Iron Ore Reduction
  │  ├─ Blast Furnace
  │  ├─ BOF Converter
  │  └─ CCUS (optional)
  ├─ DRI-EAF pathway
  │  ├─ DRI Shaft Furnace
  │  ├─ EAF
  │  └─ CCUS (optional)
  └─ Hybrid pathway
     ├─ ...
```

**Tasks**:
1. **Super-Template Design**
   - Define all possible nodes (unit operations)
   - Define all possible edges (streams)
   - Store in Python or JSON

2. **Instantiation**
   ```python
   plant = plants_db["plant_id_123"]
   schematic = SuperTemplate.instantiate(
       pathway=plant.pathway,
       parameters=plant.parameters
   )
   ```

3. **Visualization**
   - Active pathway: normal colors, fully connected
   - Inactive pathway: greyed out (opacity 0.3)
   - Streams show: mass flow, energy flow, emissions

4. **Parameter Display** (integrate with vertex-config)
   - Click a node → right panel shows StreamForm (already built!)
   - Shows all input/output streams
   - Allow parameter editing (cost, tariff, CCUS penetration, etc.)

5. **Real-time Calculation**
   - As user changes parameter → recalculate downstream impacts
   - "If I increase CCUS penetration 0% → 50%, emissions drop from 1.8 → 1.2 t CO2/ton"

**Deliverable**: Plant schematic with interactive parameter editing

---

### Phase 3: Optimization Engine (4-6 weeks) ⚡

**Goal**: "Find optimal pathways across 5000+ plants given constraints"

**Core Question**:
```
Given:
  - 5000 plants with current pathways
  - Cost budget constraints
  - Emission targets (< 0.5 by 2050)
  - Technology options (CCUS, efficiency, fuel switching)
  - Market dynamics (electricity tariff evolution)

Find:
  - Optimal % of plants converting to DRI
  - Optimal CCUS penetration
  - Optimal operational parameters
  - Minimum cost to achieve target
```

**Tasks**:
1. **Optimization Framework**
   - Use scipy.optimize or specialized solver (CVXPY for convex problems)
   - Objective: minimize cost subject to emission constraint
   - Variables: pathway selection, CCUS %, efficiency improvements

2. **Problem Formulation**
   ```python
   # Pseudocode
   def formulate_steel_optimization():
       # Decision variables
       x_bfbof = IntVar(0, 5000)  # plants staying BF-BOF
       x_dri = IntVar(0, 5000)    # plants converting to DRI
       ccus_penetration = FloatVar(0, 1)

       # Objective
       minimize(total_cost(x_bfbof, x_dri, ccus_penetration))

       # Constraints
       x_bfbof + x_dri == 5000  # all plants assigned
       avg_emissions(x_bfbof, x_dri, ccus_penetration) <= 0.5  # 2050 target
       capacity(x_bfbof, x_dri) >= production_demand

       return solve()
   ```

3. **UI**
   - "Set Objectives" panel:
     - Emission target (slider: 0.5-2.5 t CO2/ton)
     - Cost budget (slider: $0-100B)
   - "Run Optimization" button
   - Progress indicator (optimization can take time)

**Deliverable**: Optimization solver finds pathways that satisfy constraints

---

### Phase 4: Results Visualization (2-3 weeks) 📈

**Goal**: "Plot and analyze outcomes"

**Tasks**:
1. **Results Object**
   ```python
   class OptimizationResult:
       pathway_mix: Dict[str, int]  # {"BF-BOF": 4000, "DRI": 1000}
       total_cost: float
       avg_emissions: float
       ccus_penetration: float
       by_plant: List[PlantDecision]  # which plants should convert
   ```

2. **Visualization Widgets**
   - **Pie chart**: % of plants by pathway
   - **Time series**: emissions evolution 2024-2050
   - **Cost breakdown**: capex vs opex vs carbon cost
   - **Map overlay**: color plants by suggested action (stay/convert/upgrade)
   - **Sensitivity analysis**: how does result change if cost ±10%?

3. **Export**
   - CSV: plant-level decisions
   - PDF: summary report
   - JSON: full solution for re-analysis

**Deliverable**: Rich visualization of optimization results

---

## Implementation Order

### Week 1-2: Phase 1 (Maps)
```
Priority:
1. GeoJSON loader, QGraphicsScene setup
2. Plant data model + SQL/Excel reader
3. Map pins + click handlers
4. State-level filtering
```

### Week 3-5: Phase 2 (Schematic)
```
Priority:
1. Super-template design (what are the nodes/edges?)
2. Instantiation logic (which nodes active for BF-BOF?)
3. Schematic rendering (connect to existing graph UI)
4. Parameter editing (reuse StreamForm from vertex-config)
5. Real-time recalculation
```

### Week 6-10: Phase 3 (Optimization)
```
Priority:
1. Formulate steel optimization problem (math model)
2. Integrate solver (scipy.optimize)
3. Optimization UI (set constraints, run)
4. Validation (does solution satisfy constraints?)
```

### Week 11-13: Phase 4 (Results)
```
Priority:
1. Results data structure
2. Visualization widgets (pie, time series, map)
3. Export (CSV, PDF, JSON)
4. Sensitivity analysis
```

---

## What You've Already Built (Don't Redo!)

### ✅ Core/Flow Module
- You have dimension-based architecture perfect for industrial processes
- Profiles enable temporal evolution of parameters
- Fixed vs Variable distinction matches plant optimization reality
- **Don't refactor this. Extend it.**

### ✅ GUI Foundation
- StreamForm: shows parameters, allows editing ← reuse for plant schematic
- ProfileEditorDialog: edit time-varying parameters ← reuse for sector scenarios
- QGraphicsView-based vertex editing ← foundation for schematic visualization
- **Don't rebuild. Integrate.**

### ✅ Data Model
- Parameter system: Cost, Tariff, Emissions, Efficiency
- Flow types: Fuel, Electricity, Material, Product
- **Don't extend. Use for plant modeling.**

---

## Next Steps

### If starting Phase 1 immediately:

1. **Define Plant Data Schema**
   ```python
   # What columns do your Excel files have?
   # lat, lon, capacity, pathway_type, ...?
   ```

2. **Get Sample Data**
   - Even 10 real plants (or fake data) to test with
   - 1 geojson file of India boundaries

3. **Start with Single Plant**
   - Load it, plot it on map
   - Verify coordinates are correct
   - Then scale to 5000+

4. **Optimization Research**
   - Study the steel decarbonization problem
   - What are actual constraints?
   - What are real costs/emissions by pathway?
   - This will drive optimization formulation

---

## Architecture Notes for Future Self

### Why this design works:

1. **Modular Phases**: Each phase produces a working deliverable
   - Phase 1: Map works without schematic
   - Phase 2: Schematic works without optimization
   - Phase 3: Optimization works without visualization
   - Phase 4: Visualization is polishing

2. **Reuse Foundation**: The core/flow module scales
   - Single plant schematic? Use flows + parameters
   - 5000-plant optimization? Same flows, aggregated

3. **UI Pattern Consistency**:
   - Map pins → Schematic nodes → Optimization variables
   - Parameter editing → always uses StreamForm
   - Results → flows through pipeline

4. **Performance Planning**:
   - Phase 1: Rendering 5000 map pins (may need spatial indexing)
   - Phase 2: Single plant schematic (probably fine)
   - Phase 3: Optimization solver (may need parallelization)
   - Phase 4: Visualization (use matplotlib/plotly, not custom)

---

## Success Criteria

**Phase 1 MVP**:
- Open India map
- Load plant data
- Plot 5000+ pins
- Double-click shows plant details

**Phase 2 MVP**:
- Plant schematic shows correct pathway
- Parameter editing updates schematic
- Can modify key variables (CCUS %, efficiency, cost)

**Phase 3 MVP**:
- Set emission target (e.g., < 0.5 by 2050)
- Run optimization
- Get feasible solution

**Phase 4 MVP**:
- Visualize solution
- Export results
- Answer original question: "What's optimal pathway given constraints?"

---

## Why This Works

You built the **right abstraction first**:
- Dimensions ← physical quantities (Mass, Energy, Emissions)
- Flows ← how quantities move (pathways, conversions)
- Parameters ← what varies (cost, efficiency, carbon intensity)
- Profiles ← how they change over time

This is **exactly the model** for industrial decarbonization:
- Plants consume inputs (Fuel, Electricity, Material)
- Follow pathways (BF-BOF, DRI-EAF)
- Produce outputs (Steel, Emissions)
- Costs and efficiencies change over time

**You didn't overthink it. You got the model right.** Now you just need to:
1. Add geography (lat/lon)
2. Add aggregation (5000 plants)
3. Add optimization (find best mix)
4. Add visualization (show results)

That's the MVP. Everything else is scaling and polish.

---

**Last thought**: This is a genuinely significant project. The work you've done in the core/flow module is foundational and well-designed. You're not starting from scratch on Phase 1—you have the right abstractions to build on.

Take a break. When you come back, focus only on Phase 1. Get the map working. Everything else follows from there.
