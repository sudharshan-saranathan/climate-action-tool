# CAT Development Schedule: Feb 9 - Mar 8, 2026

**Assumptions:**
- Solo developer, ~4-5 productive hours/day
- Weekends: lighter work (2-3 hrs) or rest
- Buffer days built in for debugging and unexpected issues
- **Updated Feb 11:** Focusing on backend (core.graph, core.streams) for next 2 weeks before returning to maps

---

## Week 1: Backend - core.graph (Feb 9-15)
**Focus: Graph data structure and operations**

### Mon Feb 9 — REST DAY
- No coding
- Review existing core.graph implementation
- Sketch graph architecture on paper: Node/Edge relationships, signal flow

### Tue Feb 10 — Core Graph Structure
- [x] Review existing GraphCtrl implementation
- [x] Node and Edge data structures
- [x] Basic graph operations (add/remove nodes/edges)

### Wed Feb 11 — Graph Controller Refinement
- [x] Review and refactor GraphCtrl signal architecture
- [x] Ensure clean separation: GraphInstructions (backend) vs SceneInstructions (frontend)
- [ ] Document signal flow in core/graph/
- [ ] Write unit tests for graph operations

### Thu Feb 12 — Action System
- [ ] Review Action base class and derived actions
- [ ] Refine undo/redo mechanism in StackManager
- [ ] Test: create node → undo → redo cycle works correctly
- [ ] Ensure actions handle both backend state AND frontend repr references

### Fri Feb 13 — Graph Validation & Constraints
- [ ] Add graph validation logic (prevent cycles if needed, enforce rules)
- [ ] Add connection constraints (which nodes can connect to which)
- [ ] Edge validation (source/target compatibility)
- [ ] Write tests for validation logic

### Sat Feb 14 — Buffer / Light Work
- [ ] Fix any issues from the week
- [ ] Polish graph API
- [ ] Or: rest

### Sun Feb 15 — Rest or Light Planning
- [ ] Plan Week 2 tasks (core.streams)
- [ ] Review: "Is core.graph stable and well-tested?"

**Week 1 Deliverable:** core.graph is stable, well-tested, with clean signal architecture.

---

## Week 2: Backend - core.streams (Feb 16-22)
**Focus: Stream/flow system for edges**

### Mon Feb 16 — Stream Architecture Review
- [x] Review existing core.flow/ module
- [x] Understand Item, Mass, Energy, Credit base classes
- [x] Review Fuel, Material, Electricity, Product combo classes
- [ ] Document current architecture in core/flow/

### Tue Feb 17 — Stream Data Model
- [x] Define Stream class (data flowing through edges)
- [x] Link Stream to Edge objects
- [x] Implement ResourceDictionary usage
- [x] Implement ParameterDictionary usage
- [ ] Write basic tests for stream creation

### Wed Feb 18 — Stream Calculations
- [x] Implement flow calculations (input → output)
- [x] Add unit conversion utilities
- [ ] Add validation for stream data (no negative mass/energy)
- [ ] Test: create stream, modify values, verify calculations

### Thu Feb 19 — Stream Persistence
- [x] Implement stream serialization (to dict/JSON)
- [x] Implement stream deserialization (from dict/JSON)
- [ ] Add versioning for backward compatibility
- [ ] Test: save → load → verify identical stream data

### Fri Feb 20 — Stream-Graph Integration
- [x] Connect streams to graph edges
- [ ] When edge created → attach empty stream
- [ ] When edge deleted → clean up stream
- [ ] Propagate stream changes through connected nodes
- [ ] Test: graph with nodes and streams, verify data flow

### Sat Feb 21 — Testing & Documentation
- [ ] Write comprehensive tests for core.streams
- [ ] Document stream API in docstrings
- [ ] Create examples/test_stream.py demo
- [ ] Or: rest

### Sun Feb 22 — Buffer / Rest
- [ ] Fix accumulated bugs from Week 2
- [ ] Review both core.graph and core.streams
- [ ] Plan transition back to frontend work (Week 3+)

**Week 2 Deliverable:** core.streams is complete with calculation, persistence, and graph integration.

---

## Week 3: Data & Map Foundations (Feb 23 - Mar 1)
**Resuming frontend work - originally Week 1**

### Mon Feb 23 — Data Schema Design
- [ ] Define Plant data model (`core/models/plant.py`)
  ```python
  @dataclass
  class Plant:
      id: str
      name: str
      state: str
      lat: float
      lon: float
      capacity_mtpa: float  # million tons per annum
      pathway: str           # "BF-BOF", "DRI-EAF", "Hybrid"
      year_commissioned: int
      parameters: dict       # links to core.flow parameters
  ```
- [ ] Define expected Excel/SQL column schema
- [ ] Write a data loader: `core/data/loader.py`
- [ ] Create sample data: 20 fake plants with realistic lat/lon across India

### Tue Feb 24 — Data Loader + Tests
- [ ] Finish data loader for Excel (pandas/openpyxl)
- [ ] Add SQLite reader option (sqlalchemy or sqlite3)
- [ ] Write 3-4 pytest tests for data loading
- [ ] Create `tests/core/test_data_loader.py`

### Wed Feb 25 — GeoJSON + Map Foundation
- [ ] Find/download India state boundaries geojson
- [ ] Create `gui/maps/` module
- [ ] Implement `gui/maps/map_scene.py`:
  - QGraphicsScene that loads geojson
  - Parse geojson polygons → QGraphicsPolygonItem
  - Basic rendering: state outlines in grey

### Thu Feb 26 — Map View + Pan/Zoom
- [ ] Implement `gui/maps/map_view.py`:
  - QGraphicsView with pan (drag) and zoom (scroll wheel)
  - Coordinate system: lat/lon → scene coordinates
  - Fit India within view on startup
- [ ] Style: state boundaries, basic aesthetics

### Fri Feb 27 — Plant Pins on Map
- [ ] Create `gui/maps/pin.py`:
  - QGraphicsEllipseItem (or custom QGraphicsItem)
  - Color by pathway: BF-BOF=red, DRI-EAF=blue, Hybrid=green
- [ ] Load 20 sample plants → plot as pins on map
- [ ] Verify: pins appear at correct geographic locations

### Sat Mar 1 — Buffer
- [ ] Fix bugs, catch up on missed tasks
- [ ] Or: rest

**Week 3 Deliverable:** Data loader works. India map renders with pins and pan/zoom.

---

## Week 4: Map Interaction + Polish (Mar 2-8)
**Resuming frontend work - originally Week 2**

### Mon Mar 2 — Scale to 5000 Plants
- [ ] Generate 5000 fake plants (or use real dataset if available)
  - Distribute across Indian states with realistic density
  - Mix of pathways: ~80% BF-BOF, ~15% DRI-EAF, ~5% Hybrid
- [ ] Performance test: does rendering 5000 pins cause lag?
  - If yes: implement Level-of-Detail (cluster pins when zoomed out)

### Tue Mar 3 — Pin Interaction
- [ ] Single-click pin → show tooltip/popup with plant summary
- [ ] Hover: highlight pin (glow or size increase)
- [ ] Double-click: placeholder for "open schematic" (future)
- [ ] Right-click: context menu (View Details, Export)

### Wed Mar 4 — Filter Panel
- [ ] Add filter panel to map view:
  - Filter by pathway (checkboxes: BF-BOF, DRI-EAF, Hybrid)
  - Filter by state (dropdown)
  - Filter by capacity range (slider)
- [ ] Filtered pins update in real-time
- [ ] Show count: "Showing 4200 of 5000 plants"

### Thu Mar 5 — Legend + Statistics
- [ ] Add map legend (color key for pathways)
- [ ] Add summary statistics panel:
  - Total plants, by pathway breakdown
  - Total capacity: X MT/yr
- [ ] Polish aesthetics: fonts, colors, spacing

### Fri Mar 6 — Integration with Main App
- [ ] Connect map module to main_ui
- [ ] Ensure map loads on app startup
- [ ] Test end-to-end: launch app → see India map → interact with pins

### Sat Mar 7 — Documentation
- [ ] Update README.md with current state
- [ ] Document how to load plant data (Excel format)
- [ ] Update MEMORY.md with lessons learned

### Sun Mar 8 — Month Review
- [ ] Review: what's done, what's not
- [ ] Plan next phase (schematic views, save/load)
- [ ] Celebrate: you have working backend + frontend! 🎉

**Week 4 Deliverable:** 5000 plants on India map with filters and interaction.

---

## Month-End Checklist

By Mar 8, you should have:

**Backend (Weeks 1-2):**
- [x] core.graph complete with clean signal architecture
- [ ] Graph validation and constraints
- [ ] Action system (undo/redo) stable and tested
- [x] core.streams complete with calculation engine
- [x] Stream persistence (serialization/deserialization)
- [~] Stream-graph integration working (partially complete)
- [ ] Comprehensive tests for core.graph and core.streams

**Frontend (Weeks 3-4):**
- [  ] Data loader for plant data (Excel/SQLite)
- [  ] India map rendering with state boundaries
- [  ] 5000 plant pins with pathway coloring
- [  ] Click/hover interaction on pins
- [  ] Filter by pathway, state, capacity
- [  ] Map integration with main app
- [  ] Tests for data loading

## What's NOT in This Month

- Schematic rendering and navigation (moved to April)
- Project save/load (moved to April)
- Super-template design (moved to April)
- Optimization engine (Phase 3: April-May)
- Results visualization (Phase 4: May)
- Multiple sectors (cement, aluminum — future)
- Collaboration features (future)

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
Don't try to do 10-hour days. You'll burn out by Week 2.

---

## Emergency Priorities

If you're running behind, cut in this order (last cut first):

1. ~~Filter panel~~ — nice to have
2. ~~Legend/statistics~~ — nice to have
3. ~~Polish/aesthetics~~ — nice to have
4. ~~5000 plants scale test~~ — can test with 100 plants
5. Map with pins — important but can defer
6. Data loader — important but can defer
7. **Stream-graph integration** — MUST HAVE
8. **core.streams** — MUST HAVE
9. **core.graph** — MUST HAVE

If you only get items 7-9 done, **that's still a successful month.** Backend is the priority.
