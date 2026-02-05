# Filename: table.py
# Module name: widgets
# Description: Custom tree widget for managing data streams (inputs/outputs).


# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass
from qtawesome import icon as qta_icon

from gui.widgets.combobox import ComboBox
from gui.widgets.toolbar import ToolBar


# Column indices
COL_FLOW = 0
COL_UNIT = 1
COL_NAME = 2
COL_SYMBOL = 3
COL_ACTIONS = 4


class DataTree(QtWidgets.QTreeWidget):
    """
    A tree widget for managing data streams with expandable parameter children.

    Columns:
        Flow | Unit | Name | Symbol | Actions
    """

    sig_delete_stream = QtCore.Signal(int)
    sig_edit_stream = QtCore.Signal(int)

    @dataclass(frozen=True)
    class Attrs:
        row_height: int = 24
        columns: list[str] = field(
            default_factory=lambda: [
                "Flow",
                "Unit",
                "Name",
                "Symbol",
                "Actions",
            ]
        )

    def __init__(self, parent=None):

        # Instantiate dataclass
        self._attrs = DataTree.Attrs()

        # Initialize super class
        super().__init__(parent)

        # Configure tree appearance
        self.setColumnCount(len(self._attrs.columns))
        self.setHeaderLabels(self._attrs.columns)
        self.setRootIsDecorated(True)
        self.setUniformRowHeights(True)
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QTreeWidget.SelectionBehavior.SelectRows)

        _fixed = QtWidgets.QHeaderView.ResizeMode.Fixed
        _stretch = QtWidgets.QHeaderView.ResizeMode.Stretch

        # Configure column resizing
        header = self.header()
        header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(COL_FLOW, _stretch)
        header.setSectionResizeMode(COL_UNIT, _fixed)
        header.setSectionResizeMode(COL_NAME, _fixed)
        header.setSectionResizeMode(COL_SYMBOL, _fixed)
        header.setSectionResizeMode(COL_ACTIONS, _fixed)

    def add_stream(
        self,
        flow=None,
        name: str = "",
        symbol: str = "",
    ) -> QtWidgets.QTreeWidgetItem:
        """
        Add a new stream to the tree.

        Args:
            flow: A Flow instance (carries label, image, units, params).
            name: Custom label for the stream.
            symbol: Symbol for this input.

        Returns:
            The top-level QTreeWidgetItem.
        """

        if flow is None:
            return None

        # -- Top-level item --
        item = QtWidgets.QTreeWidgetItem(self)
        item.setText(COL_FLOW, flow.label)
        item.setIcon(COL_FLOW, flow.image)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        # Unit combo box
        units_combo = ComboBox(items=flow.units)
        self.setItemWidget(item, COL_UNIT, units_combo)

        # Editable text columns
        for col, text in [(COL_NAME, name), (COL_SYMBOL, symbol)]:
            item.setText(col, text)
            item.setTextAlignment(col, QtCore.Qt.AlignmentFlag.AlignCenter)

        # Actions toolbar
        index = self.indexOfTopLevelItem(item)
        self._add_actions_toolbar(item, index)

        # -- Child items for parameters --
        for key, param in flow.params.items():
            child = QtWidgets.QTreeWidgetItem(item)
            child.setText(COL_FLOW, param.label)
            child.setIcon(COL_FLOW, param.image)
            child.setFlags(child.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            # Parameter unit combo box
            param_combo = ComboBox(items=param.units)
            self.setItemWidget(child, COL_UNIT, param_combo)

        return item

    def get_stream(self, index: int) -> dict:
        """
        Get stream data from a top-level item by index.

        Returns:
            Dict with flow data and nested params list.
        """

        item = self.topLevelItem(index)
        if item is None:
            return {}

        # Get unit from combo widget
        unit_widget = self.itemWidget(item, COL_UNIT)
        unit = unit_widget.currentText() if unit_widget else ""

        result = {
            "flow": item.text(COL_FLOW),
            "unit": unit,
            "name": item.text(COL_NAME),
            "symbol": item.text(COL_SYMBOL),
            "params": [],
        }

        # Collect child parameter data
        for i in range(item.childCount()):
            child = item.child(i)
            child_unit_widget = self.itemWidget(child, COL_UNIT)
            child_unit = child_unit_widget.currentText() if child_unit_widget else ""

            result["params"].append(
                {
                    "flow": child.text(COL_FLOW),
                    "unit": child_unit,
                }
            )

        return result

    def remove_stream(self, index: int) -> None:
        """Remove a top-level stream and all its children."""

        if 0 <= index < self.topLevelItemCount():
            self.takeTopLevelItem(index)

    def _add_actions_toolbar(self, item, index: int) -> None:
        """Attach the actions toolbar to a top-level item."""

        style = """
        QToolBar {
            margin: 0px;
            padding: 0px;
        }

        QToolButton, QToolButton:hovered, QToolButton:selected {
            background: transparent;
            margin: 0px;
            padding: 0px;
        }
        """

        actions_toolbar = ToolBar(
            style=style,
            iconSize=QtCore.QSize(16, 16),
            actions=[
                (
                    qta_icon("ph.trend-up", color="orange", color_active="#ffcb00"),
                    "Plot",
                    lambda: print("Plotting entity"),
                ),
                (
                    qta_icon("mdi.pencil", color="darkcyan", color_active="cyan"),
                    "Edit",
                    lambda idx=index: self.sig_edit_stream.emit(idx),
                ),
                (
                    qta_icon("mdi.delete", color="darkred", color_active="red"),
                    "Delete",
                    lambda idx=index: self.sig_delete_stream.emit(idx),
                ),
            ],
        )
        self.setItemWidget(item, COL_ACTIONS, actions_toolbar)
