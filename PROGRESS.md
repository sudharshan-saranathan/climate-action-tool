# Session Progress - Jan 9, 2026

## Completed

### 1. Sidebar Structure (`gui/sidebar/`)
- **Navigation order**: Map, Schematic, Settings, Assistant, Database
- **ComboBox dropdown** for page switching (kept current approach)
- Updated `sidebar.py` with `map_data` property accessor

### 2. MapData Page (`gui/sidebar/mapdata.py`)
- **LegendSection** - Collapsible, shows category colors + counts
- **StatisticsSection** - Collapsible, form layout with stats
- **LayersSection** - Collapsible, checkbox toggles for map layers
- All sections use `CollapsibleSection` widget

### 3. CollapsibleSection Widget (`gui/widgets/collapsible.py`)
- Reusable collapsible panel with header + content
- Uses qtawesome chevron icons (`mdi.chevron-down`/`mdi.chevron-right`)
- Methods: `add_widget()`, `set_content_layout()`, `set_expanded()`

### 4. Maps Module (`gui/maps/`)
- **Scene** - QGraphicsScene, loads India GeoJSON by default
- **Outline** - QGraphicsObject for polygon rendering (states/regions)
- **Table** - QTableWidget for pandas DataFrames
- Overlay intentionally NOT ported (per user request)
- Background: `#f5f5f5` (light gray) - fixes OpenGL ghosting

### 5. Viewer Updates (`gui/widgets/viewer.py`)
- Added `FullViewportUpdate` mode
- Added `CacheNone` - prevents OpenGL artifacts

### 6. TabView (`gui/widgets/tabview.py`)
- Default tab is now "Map" (was "Welcome")
- Uses `Viewer` + `Scene` for hardware-accelerated map display

## Remaining Tasks

### 1. Port Streams (`../climact-ai/core/stream/`)
Files to port:
- `basic.py` - Base Stream class, BasicFlows (Item, Mass, Energy, Credit)
- `combo.py` - ComboFlows (Fuel, Material, Power, Product)
- `param.py` - Parameters mixins
- Uses `pint` library for unit handling

### 2. Schematic Page (sidebar)
Design agreed:
```
┌─────────────────────────────┐
│  ▼ FLOW HUB                 │  ← Collapsible
│  ┌─────────────────────────┐│
│  │ [All ▾] ⊖ ✕ ➕         ││  ← Filter + toolbar
│  │ ◆ Item    ⚖ Mass       ││
│  │ 🔥 Energy  💰 Credit    ││  ← Draggable streams
│  │ ⛽ Fuel   🧱 Material   ││
│  └─────────────────────────┘│
├─────────────────────────────┤
│  ▼ SCHEMATIC OVERVIEW       │  ← Collapsible
│  ┌─────────────────────────┐│
│  │ ▼ Boiler_01             ││
│  │   ├─ → Steam (out)      ││  ← Hierarchical tree
│  │   └─ ← Water (in)       ││
│  └─────────────────────────┘│
└─────────────────────────────┘
```

Features planned:
- Quick filters (All | Basic | Combo | Custom)
- Drag-to-canvas from FlowHub
- Hierarchical tree (nodes with nested connections)

### 3. FlowHub Widget
Reference: `../climact-ai/gui/sidebar/flowhub.py`
- QListWidget displaying stream types
- Toolbar: Clear Selection, Delete, Create
- Custom streams can be created/edited

## File Locations Reference

```
climate-action-tool/
├── gui/
│   ├── main_ui/window.py      # Main window singleton
│   ├── sidebar/
│   │   ├── sidebar.py         # SideBar dock widget
│   │   ├── mapdata.py         # Map dashboard page
│   │   └── setting.py         # Settings page
│   ├── widgets/
│   │   ├── collapsible.py     # CollapsibleSection
│   │   ├── viewer.py          # OpenGL QGraphicsView
│   │   ├── tabview.py         # Tab widget (Map default)
│   │   └── ...
│   └── maps/
│       ├── scene.py           # Map QGraphicsScene
│       ├── outline.py         # Polygon renderer
│       └── table.py           # Data table widget
├── assets/maps/
│   └── india-state.geojson    # Default map
└── PROGRESS.md                # This file
```

## Sister Project Reference
`../climact-ai/` - Contains original implementations to reference
