# CAT Development Schedule: Feb 9 - Mar 8, 2026

**Assumptions:**
- Solo developer, ~4-5 productive hours/day
- Weekends: lighter work (2-3 hrs) or rest
- Buffer days built in for debugging and unexpected issues
- Goal: Complete Phase 1 (Maps) + begin Phase 2 (Schematic)

---

## Week 1: Data & Foundations (Feb 9-15)

### Mon Feb 9 — REST DAY
- No coding
- Read MVP_ROADMAP.md with fresh eyes
- Sketch the data flow on paper: Excel → Plant objects → Map pins

### Tue Feb 10 — Data Schema Design
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
  - Read Excel with pandas/openpyxl
  - Return list of Plant objects
- [ ] Create sample data: 20 fake plants with realistic lat/lon across India

### Wed Feb 11 — Data Loader + Tests
- [ ] Finish data loader for Excel
- [ ] Add SQLite reader option (sqlalchemy or sqlite3)
- [ ] Write 3-4 pytest tests for data loading
  - Test: loads correct number of plants
  - Test: lat/lon are valid (within India bounds)
  - Test: pathway is one of known types
  - Test: handles missing data gracefully
- [ ] Create `tests/core/test_data_loader.py`

### Thu Feb 12 — GeoJSON + Map Foundation
- [ ] Find/download India state boundaries geojson
  - Source: Natural Earth or DataMeet India
- [ ] Create `gui/maps/` module
- [ ] Implement `gui/maps/map_scene.py`:
  - QGraphicsScene that loads geojson
  - Parse geojson polygons → QGraphicsPolygonItem
  - Basic rendering: state outlines in grey
- [ ] Test: India map renders in a standalone window

### Fri Feb 13 — Map View + Pan/Zoom
- [ ] Implement `gui/maps/map_view.py`:
  - QGraphicsView with pan (drag) and zoom (scroll wheel)
  - Coordinate system: lat/lon → scene coordinates
  - Fit India within view on startup
- [ ] Style: state boundaries, water color, basic aesthetics
- [ ] Test: can pan across India, zoom in/out smoothly

### Sat Feb 14 — Buffer / Light Work
- [ ] Fix any issues from the week
- [ ] Polish map rendering if needed
- [ ] Or: rest

### Sun Feb 15 — Rest or Light Planning
- [ ] Plan Week 2 tasks
- [ ] Review: "Can I load data and see a map?"

**Week 1 Deliverable:** Data loader works. India map renders with pan/zoom.

---

## Week 2: Map Pins + Interaction (Feb 16-22)

### Mon Feb 16 — Plant Pins on Map
- [ ] Create `gui/maps/pin.py`:
  - QGraphicsEllipseItem (or custom QGraphicsItem)
  - Color by pathway: BF-BOF=red, DRI-EAF=blue, Hybrid=green
  - Size by capacity (optional, or fixed size)
- [ ] Load 20 sample plants → plot as pins on map
- [ ] Verify: pins appear at correct geographic locations

### Tue Feb 17 — Scale to 5000 Plants
- [ ] Generate 5000 fake plants (or use real dataset if available)
  - Distribute across Indian states with realistic density
  - Mix of pathways: ~80% BF-BOF, ~15% DRI-EAF, ~5% Hybrid
- [ ] Performance test: does rendering 5000 pins cause lag?
  - If yes: implement Level-of-Detail (cluster pins when zoomed out)
  - If no: proceed
- [ ] Add state labels on map

### Wed Feb 18 — Pin Interaction
- [ ] Single-click pin → show tooltip/popup with plant summary:
  - Name, State, Capacity, Pathway
- [ ] Hover: highlight pin (glow or size increase)
- [ ] Double-click: placeholder for "open schematic" (Phase 2)
  - For now: print to console or show message box
- [ ] Right-click: context menu (View Details, Open Schematic, Export)

### Thu Feb 19 — Sidebar / Filter Panel
- [ ] Add filter panel to map view:
  - Filter by pathway (checkboxes: BF-BOF, DRI-EAF, Hybrid)
  - Filter by state (dropdown)
  - Filter by capacity range (slider)
- [ ] Filtered pins update in real-time
- [ ] Show count: "Showing 4200 of 5000 plants"

### Fri Feb 20 — Legend + Map Polish
- [ ] Add map legend:
  - Color key for pathways
  - Size key for capacity (if using variable sizes)
- [ ] Add scale bar (approximate)
- [ ] Add summary statistics panel:
  - Total plants: 5000
  - By pathway: BF-BOF: 4000, DRI: 750, Hybrid: 250
  - Total capacity: X MT/yr
- [ ] Polish aesthetics: fonts, colors, spacing

### Sat Feb 21 — Integration with Main App
- [ ] Connect map module to main_ui
  - Map should be the default view when app opens
  - Or: accessible via tab/button from main window
- [ ] Ensure map loads on app startup
- [ ] Test end-to-end: launch app → see India map → see pins

### Sun Feb 22 — Buffer / Rest
- [ ] Fix accumulated bugs
- [ ] Or: rest and plan Week 3

**Week 2 Deliverable:** 5000 plants on India map. Click for details. Filter by pathway/state.

---

## Week 3: Save/Load + Schematic Foundation (Feb 23 - Mar 1)

### Mon Feb 23 — Project Save/Load
- [ ] Define project file format:
  - Option A: SQLite database (recommended for 5000 plants)
  - Option B: JSON + Excel bundle
- [ ] Implement `core/project.py`:
  ```python
  class Project:
      name: str
      description: str
      plants: List[Plant]
      sector: str  # "steel", "cement", etc.

      def save(self, path: str): ...
      def load(cls, path: str) -> Project: ...
  ```
- [ ] Save: serialize plants + parameters to file
- [ ] Load: deserialize and reconstruct Plant objects

### Tue Feb 24 — Save/Load Testing
- [ ] Test round-trip: save → load → verify identical data
- [ ] Test: save 5000 plants, load time < 2 seconds
- [ ] Add "File > Save" and "File > Open" to main menu
- [ ] Recent projects list (optional)

### Wed Feb 25 — Super-Template Design (Paper First!)
- [ ] NO CODING TODAY
- [ ] Design the steel super-template on paper/whiteboard:
  - What are ALL possible nodes (unit operations)?
    - Iron ore preparation
    - Blast furnace / DRI shaft furnace
    - BOF / EAF
    - Casting
    - Rolling
    - CCUS module (optional)
    - Hydrogen injection (optional, future)
  - What are ALL possible edges (streams)?
    - Iron ore, coal/gas, electricity, heat, steel, slag, CO2
  - Which nodes are active for each pathway?
    - BF-BOF: ore prep → BF → BOF → cast → roll
    - DRI-EAF: ore prep → DRI → EAF → cast → roll
  - How do optional modules (CCUS) attach?
- [ ] Document in `docs/super_template_design.md`

### Thu Feb 26 — Super-Template Data Structure
- [ ] Implement template as a graph data structure:
  ```python
  class SuperTemplate:
      nodes: Dict[str, Node]  # all possible nodes
      edges: List[Edge]       # all possible connections
      pathways: Dict[str, List[str]]  # pathway → active node IDs

      def instantiate(self, pathway: str, params: dict) -> PlantSchematic:
          """Create a plant-specific schematic from template."""
  ```
- [ ] Define Node and Edge classes (may reuse existing vertex/edge)
- [ ] Hard-code steel super-template as first example

### Fri Feb 27 — Schematic Rendering
- [ ] Render super-template in QGraphicsScene:
  - Active nodes: full color, connected
  - Inactive nodes: grey, dashed edges
- [ ] Use existing vertex rendering code where possible
- [ ] Test: render BF-BOF pathway, see correct nodes highlighted

### Sat Mar 1 — Buffer
- [ ] Fix bugs, catch up on missed tasks
- [ ] Or: rest

**Week 3 Deliverable:** Save/load works. Super-template designed and rendering.

---

## Week 4: Schematic Interaction + Integration (Mar 2-8)

### Mon Mar 2 — Schematic ↔ Vertex Config
- [ ] Double-click map pin → opens schematic view for that plant
- [ ] Click schematic node → opens vertex-config (StreamForm!)
  - Reuse existing StreamForm + parameter editing
  - Shows input/output streams for that unit operation
  - Fixed params (specific_energy) show as read-only
  - Variable params (cost) show with profile editor

### Tue Mar 3 — Parameter Flow Through Schematic
- [ ] When user edits a parameter:
  - Update the Plant's parameter in memory
  - Recalculate downstream values (if simple calculation exists)
  - Visual feedback: updated values shown on edges
- [ ] Example: change electricity consumption of EAF → total energy changes

### Wed Mar 4 — Map ↔ Schematic Navigation
- [ ] Implement navigation flow:
  - Map view (default) → double-click pin → Schematic view
  - Schematic view → "Back to Map" button → Map view
  - Breadcrumb: "India > Maharashtra > Tata Steel Jamshedpur"
- [ ] State preserved: returning to map keeps zoom/position

### Thu Mar 5 — Polish + Bug Fixes
- [ ] End-to-end test:
  1. Open app → see India map with 5000 pins
  2. Filter by state (Maharashtra)
  3. Double-click a plant → see schematic
  4. Click a node → edit parameters
  5. Back to map → pin still selected
- [ ] Fix any issues found
- [ ] Performance profiling: is anything slow?

### Fri Mar 6 — Export + Summary
- [ ] Export plant data to CSV
- [ ] Export current view as PNG (map screenshot)
- [ ] Add "About" dialog with project description

### Sat Mar 7 — Documentation
- [ ] Update README.md with current state
- [ ] Document how to:
  - Load plant data (Excel format)
  - Use the map
  - Open schematics
  - Edit parameters
- [ ] Update MEMORY.md with lessons learned

### Sun Mar 8 — Month Review
- [ ] Review: what's done, what's not
- [ ] Plan March schedule (Phase 3: Optimization)
- [ ] Celebrate: you have a working map + schematic tool! 🎉

**Week 4 Deliverable:** Map → Schematic → Parameter editing. Full navigation loop.

---

## Month-End Checklist

By Mar 8, you should have:

- [  ] India map rendering with state boundaries
- [  ] 5000 plant pins with pathway coloring
- [  ] Click/hover interaction on pins
- [  ] Filter by pathway, state, capacity
- [  ] Project save/load (SQLite or JSON)
- [  ] Steel super-template designed and documented
- [  ] Schematic rendering (active/inactive nodes)
- [  ] Map → Schematic navigation (double-click)
- [  ] Parameter editing via StreamForm (reusing existing code)
- [  ] Back navigation (Schematic → Map)
- [  ] Basic export (CSV, PNG)
- [  ] Tests for data loading and save/load

## What's NOT in This Month

- Optimization engine (Phase 3: March-April)
- Results visualization (Phase 4: April)
- Multiple sectors (cement, aluminum — future)
- Collaboration features (future)
- Cloud deployment (future)

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

1. ~~Export (CSV/PNG)~~ — nice to have
2. ~~Filter panel~~ — nice to have
3. ~~Legend/statistics~~ — nice to have
4. ~~Polish/aesthetics~~ — nice to have
5. Save/load — important but can use JSON hack
6. **Schematic rendering** — MUST HAVE
7. **Map with pins** — MUST HAVE
8. **Data loader** — MUST HAVE

If you only get items 6-8 done, **that's still a successful month.**
