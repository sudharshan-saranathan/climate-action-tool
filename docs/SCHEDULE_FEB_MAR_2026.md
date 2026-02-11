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
- [ ] Review and refactor GraphCtrl signal architecture
- [ ] Ensure clean separation: GraphInstructions (backend) vs SceneInstructions (frontend)
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
- [ ] Review existing core.flow/ module
- [ ] Understand Item, Mass, Energy, Credit base classes
- [ ] Review Fuel, Material, Electricity, Product combo classes
- [ ] Document current architecture in core/flow/

### Tue Feb 17 — Stream Data Model
- [ ] Define Stream class (data flowing through edges)
- [ ] Link Stream to Edge objects
- [ ] Implement ResourceDictionary usage
- [ ] Implement ParameterDictionary usage
- [ ] Write basic tests for stream creation

### Wed Feb 18 — Stream Calculations
- [ ] Implement flow calculations (input → output)
- [ ] Add unit conversion utilities
- [ ] Add validation for stream data (no negative mass/energy)
- [ ] Test: create stream, modify values, verify calculations

### Thu Feb 19 — Stream Persistence
- [ ] Implement stream serialization (to dict/JSON)
- [ ] Implement stream deserialization (from dict/JSON)
- [ ] Add versioning for backward compatibility
- [ ] Test: save → load → verify identical stream data

### Fri Feb 20 — Stream-Graph Integration
- [ ] Connect streams to graph edges
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
