# CAT Development Schedule: Feb 9 - Mar 8, 2026
## UPDATED (Feb 16, 2026)

**Assumptions:**
- Solo developer, ~4-5 productive hours/day
- Weekends: lighter work (2-3 hrs) or rest
- Buffer days built in for debugging and unexpected issues
- **Updated Feb 16:** Backend core.graph and core.streams much further along than originally planned. Focus: stream-graph integration, GUI improvements, frontend features.

---

## Week 1: Backend - core.graph (Feb 9-15) ✅ COMPLETE

**Focus: Graph data structure and operations**

### COMPLETED
- [x] Review existing GraphCtrl implementation
- [x] Node and Edge data structures
- [x] Basic graph operations (add/remove nodes/edges)
- [x] Review and refactor GraphCtrl signal architecture
- [x] Ensure clean separation: GraphInstructions (backend) vs SceneInstructions (frontend)
- [x] GraphManager singleton with stream-matching validation
- [x] Node.Technology dataclass (consumed/produced streams, expenses, params, equations)
- [x] Edge class with proper serialization
- [x] Node/Edge JSON serialization

### NOT COMPLETED (defer to later)
- [ ] Document signal flow in core/graph/
- [ ] Write unit tests for graph operations
- [ ] Review Action base class and derived actions
- [ ] Refine undo/redo mechanism in StackManager
- [ ] Graph validation logic (prevent cycles if needed)
- [ ] Connection constraints (which nodes can connect to which)

**Week 1 Deliverable:** ✅ core.graph is stable and functional, with clean signal architecture.

---

## Week 2: Backend - core.streams (Feb 16-22) 🔄 IN PROGRESS

**Focus: Stream/flow system for edges**

### Mon Feb 16 — Stream Architecture Review ✅
- [x] Review existing core.flow/ module
- [x] Understand Composite architecture and dynamic kwargs system
- [x] Review Material, Electricity, Fuel composite classes
- [x] Understand Quantity registry pattern and dimensionality-based dispatch
- [ ] Document current architecture in docs/ARCHITECTURE_STREAMS.md

### ACTUAL IMPLEMENTATION (DIFFERS FROM ORIGINAL PLAN)
**Original Plan**: Item, Mass, Energy, Credit base classes
**Actual Implementation**: Composite-based system with dynamic attributes
- ✅ **Composite** (base): Flexible container with `attribute_groups` for GUI organization
  - `by_complexity`: simple (core essentials) / advanced (specialized)
  - `by_domain`: semantic groupings (economic, operational, emissions, etc.)
  - `custom`: user-defined attributes at runtime

- ✅ **Material**: Composite with primary attributes (mass, cost)
  - Auto-initializes MassFlowRate and CostPerMass
  - Extensible with dynamic kwargs

- ✅ **Electricity**: Composite with sophisticated operational/quality/environmental attributes
  - Power (primary), tariff, ramp_rate, capacity_factor, dispatchability
  - Voltage, power_factor, frequency, CO2_intensity, etc.
  - LCOE (levelized cost of energy)

- ✅ **Fuel**: Material + chemical composition + emissions
  - Energy content (HHV), moisture, ash content
  - Elemental composition (C, H, O, N, S fractions)
  - Emissions factors (CO2, CH4, SOx, NOx, PM2.5, PM10, CO)
  - Renewable fraction, carbon neutrality factor

### Quantity System (Registry Pattern)
- ✅ Base Quantity class with pint UnitRegistry
- ✅ 50+ physical unit types (Mass, Energy, Power, Currency, CarbonIntensity, etc.)
- ✅ Dimensionality-based automatic type dispatch
- ✅ Serialization/deserialization (to_dict/from_dict)
- ✅ Arithmetic operations with type preservation

### Tue-Thu Feb 17-19 — Stream Completion
- [x] Stream Data Model (linked to Edge objects)
- [x] Flow calculations with ResourceDictionary/ParameterDictionary
- [x] Unit conversion utilities
- [x] Stream persistence (serialization to dict/JSON)
- [x] Stream deserialization from dict/JSON

### Fri Feb 20 — Stream-Graph Integration 🔄
- [x] Streams defined in Composite classes
- [ ] When edge created → attach stream(s) from matching source/target outputs/inputs
- [ ] When edge deleted → clean up stream references
- [ ] Propagate stream changes through connected nodes
- [ ] Test: graph with nodes and streams, verify data flow

### Sat Feb 21 — Testing & Documentation
- [ ] Write comprehensive tests for core.streams (stream creation, arithmetic, serialization)
- [ ] Write tests for core.graph integration
- [ ] Document stream API (what attributes each stream has)
- [ ] Create examples/test_stream.py demo
- [ ] Create docs/ARCHITECTURE_STREAMS.md

### Sun Feb 22 — Buffer / Rest
- [ ] Fix accumulated bugs
- [ ] Review: Is stream-graph integration stable?

**Week 2 Deliverable:** core.streams + core.graph fully integrated with streams flowing through edges.

---

## Week 3: GUI Graph + Frontend Foundations (Feb 23 - Mar 1)

### Mon Feb 23 — GUI Graph Refinement
- [ ] NodeConfig dialog: use Material/Electricity/Fuel stream system
- [ ] StreamTree: display/edit composite stream attributes with proper grouping
- [ ] NodeRepr: visual feedback for node configuration state
- [ ] Test: create node → configure streams → verify in canvas

### Tue Feb 24 — Edge Representation + Stream Labels
- [ ] EdgeRepr refinement: draw stream name on edge
- [ ] Click edge → show stream details (power, mass flow, cost)
- [ ] Edge payload: store which stream(s) flow through this edge
- [ ] Hover: highlight source/target inputs/outputs matching this stream

### Wed Feb 25 — Data Model for Plants
- [ ] Define Plant dataclass (`core/models/plant.py`)
  - id, name, state, lat, lon, capacity_mtpa, pathway, year_commissioned, parameters
- [ ] Define expected Excel/SQL column schema
- [ ] Create sample data: 20 fake plants with realistic lat/lon across India

### Thu Feb 26 — Data Loader
- [ ] Implement data loader for Excel (pandas/openpyxl)
- [ ] Add SQLite reader option (sqlalchemy or sqlite3)
- [ ] Write 3-4 pytest tests for data loading
- [ ] Create `tests/core/test_data_loader.py`

### Fri Feb 27 — GeoJSON + Map Foundation
- [ ] Find/download India state boundaries geojson
- [ ] Create `gui/maps/` module
- [ ] Implement `gui/maps/map_scene.py`:
  - QGraphicsScene that loads geojson
  - Parse geojson polygons → QGraphicsPolygonItem
  - Basic rendering: state outlines in grey

### Sat Mar 1 — Buffer
- [ ] Fix bugs, catch up on missed tasks
- [ ] Or: rest

**Week 3 Deliverable:** GUI graph works with streams. Plant data model and simple map foundation ready.

---

## Week 4: Map Features + Integration (Mar 2-8)

### Mon Mar 2 — Map View + Pan/Zoom
- [ ] Implement `gui/maps/map_view.py`:
  - QGraphicsView with pan (drag) and zoom (scroll wheel)
  - Coordinate system: lat/lon → scene coordinates
  - Fit India within view on startup
- [ ] Style: state boundaries, basic aesthetics

### Tue Mar 3 — Plant Pins on Map
- [ ] Create `gui/maps/pin.py`:
  - QGraphicsEllipseItem (or custom QGraphicsItem)
  - Color by pathway: BF-BOF=red, DRI-EAF=blue, Hybrid=green
- [ ] Load 20 sample plants → plot as pins on map
- [ ] Verify: pins appear at correct geographic locations

### Wed Mar 4 — Scale + Performance
- [ ] Generate 100 fake plants (scale test)
- [ ] Performance test: does rendering 100 pins cause lag?
- [ ] If needed: implement Level-of-Detail clustering

### Thu Mar 5 — Pin Interaction
- [ ] Single-click pin → show tooltip/popup with plant summary
- [ ] Hover: highlight pin
- [ ] Double-click: placeholder for "open schematic" (future)
- [ ] Right-click: context menu (View Details, Export)

### Fri Mar 6 — Integration with Main App
- [ ] Connect map module to main_ui
- [ ] Ensure map loads on app startup as default view
- [ ] Test end-to-end: launch app → see India map → interact with pins

### Sat Mar 7 — Documentation
- [ ] Update README.md with current state
- [ ] Create docs/ARCHITECTURE_STREAMS.md
- [ ] Update MEMORY.md with lessons learned

### Sun Mar 8 — Month Review
- [ ] Review: what's done, what's not
- [ ] Plan next phase (schematic templates, save/load)
- [ ] Celebrate: working backend + frontend! 🎉

**Week 4 Deliverable:** 100+ plants on India map with click/hover interaction and main app integration.

---

## Month-End Checklist

By Mar 8, you should have:

**Backend (Weeks 1-2):**
- [x] core.graph complete with clean signal architecture
- [x] Node/Edge data structures
- [x] Stream matching validation
- [x] core.streams complete with Composite system
- [x] 50+ physical unit types with automatic dispatch
- [x] Stream persistence (serialization/deserialization)
- [ ] Stream-graph integration working (partially complete)
- [ ] Comprehensive tests for core.graph and core.streams
- [ ] Documentation of stream/graph architecture

**Frontend (Weeks 3-4):**
- [ ] GUI graph: NodeConfig + StreamTree with Composite streams
- [ ] EdgeRepr with stream labels
- [ ] Plant data model and loader
- [ ] India map rendering with state boundaries
- [ ] 100+ plant pins with pathway coloring
- [ ] Click/hover interaction on pins
- [ ] Map integration with main app
- [ ] Tests for data loading

## What's NOT in This Month

- Filter/search panel on map (Week 4 optional)
- Schematic rendering from super-templates (moved to Week 5)
- Project save/load (HDF5) (moved to Week 5)
- Optimization engine (Phase 3: April-May)
- Results visualization (Phase 4: May)
- Multiple sectors (cement, aluminum — future)
- LLM integration (future)

## Daily Routine Suggestion

```
09:00 - Review yesterday's commits, read MEMORY.md
09:15 - Code (deep work block 1)
11:15 - Break (15-20 min, walk, coffee)
11:30 - Code (deep work block 2)
13:00 - Lunch break (45 min minimum)
13:45 - Code (deep work block 3)
15:45 - Break
16:00 - Testing, bug fixes, documentation
17:00 - Commit, update MEMORY.md, plan tomorrow
17:30 - STOP. Done for the day.
```

**Total: ~6 productive hours.** That's realistic for sustained solo work.

---

## Priority Adjustments (UPDATED)

Since core.streams and core.graph are further along, priorities shift:

**MUST-HAVE for Feb:**
1. ✅ core.graph & core.streams (largely done)
2. 🔄 Stream-graph integration (edges carry streams)
3. 📋 GUI improvements (NodeConfig, StreamTree with new Composite system)
4. 📋 Plant data model + loader

**NICE-TO-HAVE:**
- Comprehensive unit tests
- Architecture documentation
- Map features beyond basic rendering

**CAN-DEFER to March:**
- Super-templates for schematics
- HDF5 save/load
- Filter panels on map

---

## Emergency Priorities

If running behind, cut in this order (last cut first):

1. ~~100+ plants scale test~~ — can test with 20 plants
2. ~~Map interaction~~ — can be minimal (click only)
3. ~~Plant data loader~~ — can hard-code sample data initially
4. **Stream-graph integration** — MUST HAVE
5. **GUI graph with streams** — MUST HAVE
6. **core.streams + core.graph** — MUST HAVE (done)

---

## Known Issues / To Investigate

1. **Stream names vs Schedule**: Schedule mentioned "Credit" class. Check if this was intentionally removed or needs to be added back.
2. **Composite flexibility**: Current system is flexible (dynamic kwargs). Verify this is the desired approach vs. fixed schema.
3. **GUI Scaling**: How does NodeConfig/StreamTree handle large attribute_groups? May need pagination/tabs.
4. **Edge Stream Payload**: How are multiple streams per edge represented? Need design spec.
