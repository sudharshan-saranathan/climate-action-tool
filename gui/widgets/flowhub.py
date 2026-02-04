# Filename: flowhub.py
# Module name: widgets
# Description: Flow hub widget displaying available stream types.

"""
Flow hub widget for displaying and managing stream types.

Provides a QListWidget showing available flow types (BasicFlows and ComboFlows)
with toolbar actions for creating, deleting, and managing custom streams.
"""

from __future__ import annotations

from qtawesome import icon as qta_icon
from PySide6 import QtCore, QtWidgets

from core.flow import BasicFlows, ComboFlows
from gui.widgets.toolbar import ToolBar
from gui.widgets.layouts import HLayout


class FlowHub(QtWidgets.QListWidget):
    """
    List widget displaying available flow/stream types.

    Shows predefined flow types from BasicFlows and ComboFlows,
    and allows creating custom user-defined streams.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        super().setUniformItemSizes(True)

        # Header with toolbar
        header = QtWidgets.QFrame()
        tools = ToolBar(
            self,
            actions=[
                (
                    qta_icon("ph.selection-slash", color="gray", color_active="white"),
                    "Clear Selection",
                    None,
                ),
                (
                    qta_icon("mdi.minus", color="gray", color_active="white"),
                    "Delete",
                    None,
                ),
                (
                    qta_icon("mdi.plus", color="gray", color_active="white"),
                    "Create",
                    None,
                ),
            ],
        )

        layout = HLayout(self, widgets=[tools])
        layout.addWidget(tools)

        # Add header as first item (non-selectable)
        item = QtWidgets.QListWidgetItem(self)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)

        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.setItemWidget(item, header)
        self.addItem(item)

        # Add predefined flow types
        for key, cls in (BasicFlows | ComboFlows).items():
            item = QtWidgets.QListWidgetItem(cls.LABEL, self)
            item.setIcon(qta_icon(cls.ICON, color=cls.COLOR))
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
            item.setSizeHint(QtCore.QSize(0, 28))
            self.addItem(item)

        # Connect toolbar signals
        tools.sig_action_triggered.connect(self._on_tool_action_triggered)

    def _on_tool_action_triggered(self, action: str) -> None:
        """Handle toolbar action clicks."""

        if action == "Create":
            item = QtWidgets.QListWidgetItem("New Stream", self)
            item.setIcon(qta_icon("ph.flow-arrow", color="cyan"))
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
            item.setSizeHint(QtCore.QSize(0, 28))
            self.editItem(item)

        elif action == "Delete":
            for item in self.selectedItems():
                self.takeItem(self.row(item))

        elif action == "Clear Selection":
            self.clearSelection()
