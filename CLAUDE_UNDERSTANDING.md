# Bidirectional Signal-Based Architecture

## Overview

The Climate Action Tool uses a **signal-based bidirectional communication system** to decouple the frontend (GUI) from the backend (graph data structure). This architecture allows the same operations to be triggered from multiple sources (user UI interactions, programmatic calls from LLM, etc.) while maintaining a single source of truth in the backend.

## Core Components

### 1. Application Signal Bus (main.py)

The `ClimateActionTool` (QApplication subclass) acts as the central message broker, hosting two signal instruction classes:

#### GraphInstructions
Signals for **backend-level graph operations**:
- `create_item(str, dict)` - Request to create a node/edge in the graph
- `delete_item(str, dict)` - Request to delete a node/edge from the graph
- `undo_action()` - Request to undo the most recent backend action
- `redo_action()` - Request to redo the most recent backend action

#### SceneInstructions
Signals for **frontend-level visual operations**:
- `create_repr(str, dict)` - Request to create a visual representation (NodeRepr, EdgeRepr) on the Canvas
- `delete_repr(str, dict)` - Request to delete a visual representation from the Canvas
- `undo_action()` - Request to undo frontend state (hiding reprs, reverting visual changes)
- `redo_action()` - Request to redo frontend state

These are **class variables** on the application, accessible anywhere via:
```python
app = QtWidgets.QApplication.instance()
app.graph_ctrl.create_item.emit(key, data)
```

### 2. Frontend Components (gui/graph/)

#### Canvas (QGraphicsScene)
- **Role**: Manages all visual representations of graph items
- **Signal Emission**: When user interacts with the UI (right-click menu, keyboard shortcuts), Canvas emits `graph_ctrl` signals
- **Signal Reception**: Listens to `scene_ctrl` signals to create/delete/modify visual representations
- **Example**: User clicks "Create Node" → Canvas.`_raise_create_request()` → `graph_ctrl.create_item.emit()`

#### VertexItem (NodeRepr)
- **Role**: Visual representation of a graph node
- **Local Signals**: Emits local signals like `item_clicked`, `item_shifted` to Canvas (not app-level signals)
- **Registration**: These local signals are registered with Canvas via `register_signals()`, which connects them to Canvas slots

### 3. Backend Components (core/graph/)

#### GraphCtrl
- **Role**: Manages the authoritative graph data structure (nodes and edges)
- **Signal Reception**: Listens to `graph_ctrl` signals from the application bus
- **Signal Emission**: After processing, emits `scene_ctrl` signals to request frontend updates
- **Data Storage**: Maintains `self.nodes` and `self.edges` as the source of truth

## Bidirectional Signal Flow

### Scenario 1: User Creates a Node via UI

```
User clicks "Create Node" in context menu
        ↓
Canvas._raise_create_request("NodeRepr") is called
        ↓
Canvas emits: app.graph_ctrl.create_item.emit("NodeRepr", {"pos": pos_data})
        ↓
GraphCtrl._init_() has connected to this signal: self._app.graph_ctrl.create_item.connect(self.create_item)
        ↓
GraphCtrl.create_item() receives the signal
        ↓
GraphCtrl processes and creates Node in backend: self.nodes[uid] = Node(...)
        ↓
GraphCtrl emits: app.scene_ctrl.create_repr.emit("NodeRepr", {...backend_node_data...})
        ↓
Canvas._init_controllers() has connected: scc.create_repr.connect(self.create_item)
        ↓
Canvas.create_item() receives the signal
        ↓
Canvas creates NodeRepr visual object: repr = NodeRepr(pos=pos)
        ↓
Canvas adds to scene: self.addItem(repr)
```

**Result**: Both backend and frontend are updated in sync, single source of truth maintained.

### Scenario 2: LLM Creates a Node Programmatically

```
LLM code calls (same entry point):
app.graph_ctrl.create_item.emit("NodeRepr", {...node_data...})
        ↓
(Flow continues identically to Scenario 1)
```

**Key Insight**: The origin of the signal is irrelevant. Whether from user UI or programmatic call, the same bidirectional flow occurs.

## Design Principles

### 1. Decoupling
- Canvas never directly modifies the backend graph
- GraphCtrl never directly creates visual representations
- All communication is through signals
- Allows independent testing and modification

### 2. Single Source of Truth
- Backend (GraphCtrl) is the authoritative state
- Frontend (Canvas) is a reflection of backend state
- Frontend changes may be "hidden" but backend is always the truth

### 3. Symmetry
- GraphInstructions and SceneInstructions have parallel signal structures (create/delete/undo/redo)
- Both users and LLM can trigger the same flows

### 4. Unidirectional Causality
- Flow direction: Frontend request → Backend processing → Frontend response
- Backend never initiates frontend changes unprompted
- All changes originate from a request signal

## Undo/Redo Considerations

The signal-based architecture must support undo/redo uniformly:

### Current State
- **Frontend (Canvas)**: Has `StackManager` managing visual state changes
- **Backend (GraphCtrl)**: Will need to track backend state changes (nodes being hidden via state flag)

### Architectural Question
- Should there be **one unified StackManager** tracking both frontend and backend changes?
- Or **two separate StackManagers** (one frontend, one backend) that stay in sync?

**Implication**:
- If unified: One Action object handles both frontend and backend undo/redo atomically
- If separate: Risk of desynchronization and complex coordination

## Signal Parameters

Note on signal signatures:

- **create/delete signals**: Pass `(str, dict)` - a key identifying what to create/delete and data with parameters
- **undo/redo signals**: Currently `()` - no parameters, acts as simple "do undo" command
  - Could be extended to pass action indices or specific action identifiers if needed

## Access Pattern

Anywhere in the code:
```python
from PySide6 import QtWidgets

app = QtWidgets.QApplication.instance()

# Emit a create request
app.graph_ctrl.create_item.emit("NodeRepr", {"pos": QPointF(100, 100)})

# Emit an undo request
app.graph_ctrl.undo_action.emit()
```

This works because the app instance holds the signal definitions, making them globally accessible.
