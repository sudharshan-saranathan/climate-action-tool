# CAT: Complete Feature Registry

**Last Updated**: 2026-02-08
**Purpose**: Single source of truth for ALL features — major and minor, done and planned.

---

## Status Legend
- ✅ DONE
- 🔨 IN PROGRESS
- 📋 PLANNED
- 💡 FUTURE

---

## MAJOR FEATURES

### M1. Core/Flow Module ✅
**Status**: Complete
**Description**: Dimension-based flow architecture with time-varying profiles.

| Component | Status | Notes |
|-----------|--------|-------|
| Dimensions (Mass, Energy, Power, Currency, ...) | ✅ | 7 dimensions |
| FlowMixin + basic flows (MassFlow, EnergyFlow, ...) | ✅ | 4 basic flows |
| Composite flows (Fuel, Electricity, Fluid, ...) | ✅ | 5 composite flows |
| Profile system (Fixed, Linear, Stepped) | ✅ | ProfileRef wrapping |
| Fixed vs Variable parameters | ✅ | UI reflects distinction |
| Power as first-class dimension | ✅ | Electricity uses Power directly |
| Parameter classes (Ratio, Factor, Temp, Pressure) | ✅ | With profile support |

**Files**: `core/flow/dimensions.py`, `time.py`, `flows.py`, `profiles.py`, `parameters.py`, `combos.py`

---

### M2. Maps Module 📋
**Status**: Planned (Schedule: Week 1-2)
**Description**: India map with geo-tagged plant pins. Default view on app launch.

| Component | Status | Notes |
|-----------|--------|-------|
| GeoJSON loader (India state boundaries) | 📋 | Natural Earth or DataMeet |
| QGraphicsScene map rendering | 📋 | State polygons, water, borders |
| QGraphicsView with pan/zoom | 📋 | Scroll=zoom, drag=pan |
| Plant pins (color by pathway) | 📋 | BF-BOF=red, DRI=blue, Hybrid=green |
| Pin interaction (click, hover, double-click) | 📋 | Tooltip, highlight, open schematic |
| Filter panel (pathway, state, capacity) | 📋 | Real-time filtering |
| Legend + statistics summary | 📋 | Count by pathway, total capacity |
| Map ↔ Schematic navigation | 📋 | Double-click pin → schematic |

**Planned files**: `gui/maps/map_scene.py`, `map_view.py`, `pin.py`, `filters.py`

---

### M3. Data Import/Export (HDF5) 📋
**Status**: Planned (Schedule: Week 3)
**Description**: Project persistence using HDF5 (.h5) files. Schematics stored as JSON within HDF5.

| Component | Status | Notes |
|-----------|--------|-------|
| Plant data model | 📋 | `core/models/plant.py` |
| Excel/SQL import | 📋 | Read plant tables (lat, lon, pathway, params) |
| Schematic → JSON serialization | 📋 | Graph nodes + edges + params → JSON |
| JSON → HDF5 storage | 📋 | h5py or PyTables |
| HDF5 → JSON → Schematic deserialization | 📋 | Round-trip fidelity |
| Project save/load | 📋 | File > Save / File > Open |
| Export to CSV/Excel | 📋 | Plant-level data export |

**Key decisions**:
- HDF5 chosen for: large datasets (5000 plants), hierarchical structure, fast I/O
- JSON intermediate: schematics serialized to JSON, then stored as HDF5 datasets
- Structure:
  ```
  project.h5
  ├── /metadata          (project name, sector, date, version)
  ├── /plants/           (plant data table: id, lat, lon, capacity, pathway)
  ├── /schematics/       (per-plant JSON blobs of graph structure)
  │   ├── plant_001.json
  │   ├── plant_002.json
  │   └── ...
  ├── /parameters/       (parameter values, profiles)
  ├── /templates/        (super-template definitions)
  └── /results/          (optimization outputs, if any)
  ```

**Planned files**: `core/data/loader.py`, `core/data/hdf5.py`, `core/project.py`

---

### M4. Schematic Module 📋
**Status**: Planned (Schedule: Week 3-4)
**Description**: Plant-level process flow diagram. Instantiated from super-template.

| Component | Status | Notes |
|-----------|--------|-------|
| Super-template definition | 📋 | All possible nodes/edges for a sector |
| Template instantiation per plant | 📋 | Activate pathway-specific nodes |
| Active pathway rendering (full color) | 📋 | Connected, interactive |
| Inactive pathway rendering (greyed out) | 📋 | Dashed, opacity 0.3 |
| Node ↔ vertex-config integration | 📋 | Click node → StreamForm |
| Parameter editing in schematic context | 📋 | Reuse existing forms |
| Stream labels on edges | 📋 | Show flow values |

**Architecture**:
```
SuperTemplate (sector-level, e.g., "Steel")
  ├── All possible nodes (BF, BOF, DRI, EAF, CCUS, H2, ...)
  ├── All possible edges (ore, coal, electricity, CO2, steel, ...)
  └── Pathway definitions:
      ├── "BF-BOF": [ore_prep, BF, BOF, cast, roll]
      ├── "DRI-EAF": [ore_prep, DRI, EAF, cast, roll]
      └── "BF-BOF+CCUS": [ore_prep, BF, BOF, cast, roll, CCUS]

PlantSchematic = SuperTemplate.instantiate(pathway="BF-BOF", params={...})
```

**Planned files**: `core/models/template.py`, `gui/schematic/`

---

### M5. Stream Editor 📋
**Status**: Planned
**Description**: Users can define custom stream types derived from fundamental streams.

| Component | Status | Notes |
|-----------|--------|-------|
| Custom stream definition UI | 📋 | Name, base type, additional params |
| Derive from fundamental streams | 📋 | e.g., "Syngas" from MassFlow with composition params |
| Save custom streams to project | 📋 | Persist in HDF5 |
| Use custom streams in schematic | 📋 | Available in StreamTree |

**Example**:
```python
# User defines "Syngas" stream
Syngas = derive_from(MassFlow,
    name="Syngas",
    additional_params={
        "H2_fraction": Ratio(Mass, Mass, is_variable=False),
        "CO_fraction": Ratio(Mass, Mass, is_variable=False),
        "temperature": TemperatureParam(),
    }
)
# Syngas now available in StreamTree alongside Fuel, Material, etc.
```

**Key**: Must integrate with the existing flow architecture (dimensions, parameters, profiles)

**Planned files**: `gui/editors/stream_editor.py`, `core/flow/custom.py`

---

### M6. Optimization (AMPL Translation) 📋
**Status**: Planned (Schedule: Month 2-3)
**Description**: Translate schematic graph → AMPL script. This is the **hardest** component.

| Component | Status | Notes |
|-----------|--------|-------|
| Schematic graph → intermediate representation | 📋 | Flatten graph to sets, params, vars |
| IR → AMPL .mod file generation | 📋 | Sets, parameters, variables, constraints, objective |
| IR → AMPL .dat file generation | 📋 | Data instantiation from plant parameters |
| AMPL solver interface | 📋 | Call AMPL with .mod + .dat, parse results |
| Objective configuration UI | 📋 | Min cost, max efficiency, emission target |
| Constraint configuration UI | 📋 | Capacity bounds, emission limits, budget |
| Solver selection | 📋 | CPLEX, Gurobi, GLPK, HiGHS |

**AMPL Translation Architecture**:
```
Schematic (Graph)
    │
    ▼
Intermediate Representation (IR)
    ├── Sets: PLANTS, PATHWAYS, TIME_PERIODS, RESOURCES
    ├── Parameters: cost[p,t], emissions[p,t], capacity[p]
    ├── Variables: x[p,pathway] (binary), production[p,t]
    ├── Constraints: demand, capacity, emissions_target
    └── Objective: minimize total_cost
    │
    ▼
AMPL Script (.mod + .dat)
    │
    ▼
Solver (CPLEX/Gurobi/HiGHS)
    │
    ▼
Results (parsed back into Plant objects)
```

**Example AMPL output** (generated from schematic):
```ampl
# Generated by CAT from Steel sector schematic
# Date: 2026-03-15

set PLANTS := 1..5000;
set PATHWAYS := {BF_BOF, DRI_EAF, BF_BOF_CCUS, DRI_EAF_CCUS};
set TIME_PERIODS := 2025 2030 2035 2040 2045 2050;

param current_pathway {PLANTS} symbolic;
param capacity {PLANTS} >= 0;
param emission_factor {PATHWAYS, TIME_PERIODS} >= 0;
param conversion_cost {PLANTS, PATHWAYS} >= 0;
param operating_cost {PLANTS, PATHWAYS, TIME_PERIODS} >= 0;

var select {PLANTS, PATHWAYS} binary;
var production {PLANTS, TIME_PERIODS} >= 0;

minimize TotalCost:
    sum {p in PLANTS, pw in PATHWAYS}
        conversion_cost[p,pw] * select[p,pw]
    + sum {p in PLANTS, pw in PATHWAYS, t in TIME_PERIODS}
        operating_cost[p,pw,t] * production[p,t];

subject to OnePathway {p in PLANTS}:
    sum {pw in PATHWAYS} select[p,pw] = 1;

subject to EmissionTarget {t in TIME_PERIODS}:
    sum {p in PLANTS, pw in PATHWAYS}
        emission_factor[pw,t] * production[p,t] * select[p,pw]
    <= 0.5 * sum {p in PLANTS} production[p,t];

subject to CapacityLimit {p in PLANTS, t in TIME_PERIODS}:
    production[p,t] <= capacity[p];
```

**Critical path**: This translation is essentially a **domain-specific compiler**.
- Input: visual schematic (graph)
- Output: algebraic optimization model (AMPL)
- Complexity: must handle arbitrary topologies, not just hard-coded steel

**Planned files**: `core/optimization/ir.py`, `core/optimization/ampl_writer.py`, `core/optimization/solver.py`

---

### M7. Results Visualization 📋
**Status**: Planned (Schedule: Month 3)
**Description**: Dedicated results page with plotting and analysis widgets.

| Component | Status | Notes |
|-----------|--------|-------|
| Results data model | 📋 | Parse AMPL solution → structured results |
| Results page/tab in main UI | 📋 | Separate from map/schematic |
| Time series plots | 📋 | Emissions evolution 2025-2050 |
| Pathway distribution (pie/bar) | 📋 | % plants by pathway per year |
| Cost breakdown chart | 📋 | Capex vs Opex vs Carbon cost |
| Map overlay (color by decision) | 📋 | Stay=grey, Convert=green, CCUS=blue |
| Sensitivity analysis | 📋 | Tornado diagram: which param matters most? |
| Plant-level result table | 📋 | Sortable, filterable |
| Export results (CSV, PDF, PNG) | 📋 | Publication-ready |

**Plotting**: Use matplotlib embedded in Qt (FigureCanvasQTAgg) or pyqtgraph for interactivity

**Planned files**: `gui/results/results_page.py`, `gui/results/charts.py`, `core/results/`

---

### M8. LLM Integration 💡
**Status**: Future
**Description**: Programmatic access to all CAT functionality via function-calling for LLM agents.

| Component | Status | Notes |
|-----------|--------|-------|
| Stringified method registry | 💡 | All public methods → JSON schema |
| Function-calling API | 💡 | LLM can: load project, query plants, run optimization |
| Natural language queries | 💡 | "Which plants should convert to DRI first?" |
| Programmatic schematic modification | 💡 | LLM can add/remove nodes, change params |
| Robust data model (SQL/HDF5) | 💡 | Required for programmatic access |

**Architecture Implication**:
```
Two access paths to the same data model:

GUI (Human)                    LLM (Agent)
    │                              │
    ▼                              ▼
 Qt Widgets                   Function Calls
    │                              │
    ▼                              ▼
 ┌─────────────────────────────────────┐
 │        Core Data Model              │
 │  (Plants, Schematics, Parameters)   │
 │                                     │
 │  Every mutation is an API call:     │
 │  - plant.set_parameter(key, value)  │
 │  - schematic.add_node(node)         │
 │  - project.run_optimization(...)    │
 │                                     │
 │  Every query is an API call:        │
 │  - project.get_plants(filter=...)   │
 │  - plant.get_emissions()            │
 │  - results.get_optimal_pathway()    │
 └─────────────────────────────────────┘
```

**Design Principle**: GUI widgets should call the same API that LLMs will call.
Don't build GUI-only logic. Every action must be expressible as a function call.

**This means**:
- `core/` modules must have clean, documented public APIs
- All methods must accept/return serializable types (no Qt objects in core)
- Callbacks should be registerable (observer pattern or signals)
- Method signatures must be convertible to JSON schema for function-calling

---

## MINOR FEATURES

### m1. Startup Dialog 🔨
**Status**: Partially implemented (many button stubs)
**Description**: App launch dialog with project options.

| Component | Status | Notes |
|-----------|--------|-------|
| New Project | 📋 | Create blank project, choose sector |
| Open Project | 📋 | File picker → load .h5 |
| Recent Projects | 📋 | List of recently opened files |
| Templates | 📋 | Pre-built sector templates (Steel, Cement, ...) |
| Button stubs | 🔨 | Many buttons exist but aren't connected |

**Planned files**: `gui/startup/` (existing, needs completion)

---

### m2. Menubar 📋
**Status**: Planned
**Description**: Complete File, Edit, View, Tools, Help menus.

| Menu | Items | Status |
|------|-------|--------|
| File | New, Open, Save, Save As, Export, Recent, Quit | 📋 |
| Edit | Undo, Redo, Cut, Copy, Paste, Preferences | 📋 |
| View | Map, Schematic, Results, Toggle Sidebar, Zoom | 📋 |
| Tools | Run Optimization, Validate Schematic, Stream Editor | 📋 |
| Help | Documentation, About, Report Bug | 📋 |

---

### m3. Main Window Toolbar 📋
**Status**: Planned
**Description**: Toolbar buttons connected to major pages/actions.

| Button | Action | Status |
|--------|--------|--------|
| Map | Switch to map view | 📋 |
| Schematic | Switch to schematic view | 📋 |
| Optimize | Open optimization page | 📋 |
| Results | Open results page | 📋 |
| Save | Quick save project | 📋 |
| Export | Export dialog | 📋 |

---

### m4. Welcome Tab 📋
**Status**: Planned
**Description**: Landing page with shortcuts and getting-started info.

| Component | Status | Notes |
|-----------|--------|-------|
| Quick action buttons | 📋 | New Project, Open Project, Recent |
| Keyboard shortcuts reference | 📋 | Common shortcuts table |
| Getting started guide | 📋 | 3-step workflow overview |
| Sector templates | 📋 | "Start with Steel", "Start with Cement" |
| Version info | 📋 | App version, last update |

---

## DEPENDENCY MAP

```
M1 (Core/Flow) ✅
 │
 ├──► M5 (Stream Editor)
 │     Custom streams extend the flow system
 │
 ├──► M4 (Schematic)
 │     Nodes use flows, edges use streams
 │     │
 │     ├──► M3 (HDF5 Save/Load)
 │     │     Schematics serialized to JSON → HDF5
 │     │
 │     ├──► M6 (AMPL Translation) ← CRITICAL PATH
 │     │     Schematic graph → AMPL script
 │     │     │
 │     │     └──► M7 (Results)
 │     │           Parse AMPL output → visualize
 │     │
 │     └──► M8 (LLM Integration)
 │           Programmatic access to schematic + optimization
 │
 └──► M2 (Maps)
       Plant pins on India map
       Double-click → opens M4 (Schematic)

Minor features (m1-m4) can be done incrementally alongside major features.
```

---

## CRITICAL ARCHITECTURAL DECISIONS

### 1. HDF5 for Storage (not SQLite)
**Rationale**:
- Hierarchical: maps to project/plant/schematic structure
- Handles large arrays (5000 plants × parameters × time steps)
- Single file: easy to share, backup, version
- JSON schematics stored as string datasets within HDF5
- Libraries: h5py (simple) or PyTables (advanced queries)

### 2. AMPL for Optimization (not scipy/CVXPY)
**Rationale**:
- Industry standard for large-scale optimization
- Supports MILP (mixed-integer linear programming) — needed for pathway selection
- Solver-independent: can swap CPLEX ↔ Gurobi ↔ HiGHS
- 5000 binary variables (pathway selection) + continuous variables = needs commercial solver
- Schematic → AMPL translation is a compiler problem

### 3. Dual Access: GUI + LLM
**Rationale**:
- Every core operation must be a callable function (not GUI-only)
- Enables future LLM agent: "Optimize Maharashtra plants for <0.5 target"
- Forces clean separation: `core/` (logic) vs `gui/` (presentation)
- Method signatures → JSON schema → function-calling tools

### 4. Super-Template Pattern for Schematics
**Rationale**:
- One template per sector (Steel, Cement, Aluminum)
- All possible pathways in one graph
- Per-plant instantiation activates relevant subset
- Avoids: 5000 unique schematics (unmaintainable)
- Enables: consistent parameter structure across plants

---

## EFFORT ESTIMATES (ROUGH)

| Feature | Effort | Complexity | Dependencies |
|---------|--------|------------|--------------|
| M1 Core/Flow | ✅ Done | High | None |
| M2 Maps | 2-3 weeks | Medium | GeoJSON, plant data |
| M3 HDF5 I/O | 1-2 weeks | Medium | Schematic serialization |
| M4 Schematic | 3-4 weeks | High | Super-template design |
| M5 Stream Editor | 1-2 weeks | Medium | Core/Flow module |
| M6 AMPL Translation | 4-6 weeks | **Very High** | Schematic + IR design |
| M7 Results | 2-3 weeks | Medium | AMPL output parsing |
| M8 LLM Integration | 3-4 weeks | High | Clean core API |
| m1-m4 Minor features | 1-2 weeks total | Low | Can be done incrementally |

**Total estimated**: 4-6 months for full MVP (solo developer)

---

## RISK REGISTER

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| AMPL translation too complex | High | Medium | Start with hard-coded steel model, generalize later |
| 5000 pins cause rendering lag | Medium | Medium | Spatial indexing, level-of-detail clustering |
| HDF5 schema changes break old files | Medium | High | Version field in metadata, migration scripts |
| Super-template too rigid | High | Medium | Allow per-plant node additions/overrides |
| AMPL license cost | Medium | Low | Use HiGHS (open source) as default solver |
| LLM integration scope creep | High | High | Defer to after optimization works |
| Solo developer burnout | High | Medium | Sustainable pace, phase-based delivery |
