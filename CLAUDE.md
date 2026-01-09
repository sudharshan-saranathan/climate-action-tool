# Climate Action Tool

## Project Overview
Climate Action Tool is a GUI platform for climate modeling, built with PySide6 and Python.

This project is a refactoring of `../climact-ai`. Reference that project for existing implementations when needed.

## Project Structure
- `gui/main_ui/` - Main window interface (QMainWindow singleton)
- `gui/sidebar/` - Sidebar dock widget with settings panel
- `gui/widgets/` - Reusable custom widgets (ToolBar, ComboBox, layouts)
- `gui/startup/` - Startup dialogs and widgets

## Key Dependencies
- PySide6 - Qt bindings for Python
- qtawesome - Icon library (using `mdi.*` and `ph.*` icon sets)

## Related Project
- `../climact-ai/` - Sister project with shared UI patterns
