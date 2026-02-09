#  Filename: gui/graph/vertex/config/tree.py
#  Module Name: VertexConfigTree
#  Description: Tree widget for VertexConfigDialog.

# Standard
import weakref
from typing import Any

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact

from qtawesome import icon
from gui.widgets.toolbar import ToolBar


class StreamTree(QtWidgets.QTreeWidget):
    """Tree widget for VertexConfigDialog."""

    def __init__(self, parent=None):
        super().__init__(parent, columnCount=3)

        # Customize appearance and behaviour
        self.setHeaderHidden(True)
        self.setMouseTracking(True)
        self.setColumnWidth(2, 140)
        self.setStyleSheet("QTreeWidget::item { height: 20px; }")
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)

        # Customize header
        header = self.header()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Strong references to prevent GC of StreamForm instances
        self._flow_to_item_map: dict[str, QtWidgets.QTreeWidgetItem] = {}
        self._item_to_form_map: dict[QtWidgets.QTreeWidgetItem, object] = {}

    def _init_top_level_items(self, resources: dict[str, Any]):

        # Import toolbar
        from gui.widgets.toolbar import ToolBar

        # Create a row for each flow class
        for label, flow_class in resources.items():

            item = QtWidgets.QTreeWidgetItem(self, [flow_class.Attrs.label])
            item.setIcon(0, flow_class.Attrs.image)

            toolbar = ToolBar(self)
            toggle = toolbar.addAction(
                icon("mdi.check-bold", color_off="gray", color_on="cyan"),
                "Toggle auto-balance",
            )
            create = toolbar.addAction(
                icon("mdi.plus", color="gray", color_active="white"), "Create Entity"
            )

            toggle.setCheckable(True)
            create.setData(item)
            create.triggered.connect(self._on_item_created)

            self.setItemWidget(item, self.columnCount() - 1, toolbar)
            self._flow_to_item_map[label] = item

    @QtCore.Slot()
    def _on_item_created(self):

        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return

        root = action.data()
        self.create_entity(root.text(0))

    @QtCore.Slot()
    def _on_item_deleted(self):

        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return

        item = action.data()
        root = item.parent()
        self.delete_entity(root.text(0), item.text(0))

    # Method to add a resource-class to the tree
    def add_top_level_item(self, flow_class):

        item = QtWidgets.QTreeWidgetItem([flow_class.Attrs.label])
        item.setIcon(0, flow_class.Attrs.image)

        widget = ToolBar(self, trailing=True)
        toggle = widget.addAction(
            icon("mdi.check-bold", color_off="gray", color_on="cyan"),
            "Toggle auto-balance",
        )
        create = widget.addAction(
            icon("mdi.plus", color="gray", color_active="white"),
            "Create Entity",
            self._on_item_created,
        )

        toggle.setCheckable(True)
        create.setData(item)
        self.addTopLevelItem(item)
        self.setItemWidget(item, self.columnCount() - 1, widget)
        self._flow_to_item_map[item.text(0)] = item

    # Method to create a new entity under the specified parent
    def create_entity(self, flow_id: str):
        """Create a new entity and display it under the specified flow class.

        :param flow_id: The string ID of the entity's flow class (e.g., Mass, Energy, Currency)
        """

        root = self._flow_to_item_map.get(flow_id, None)
        if not root:
            return None

        root.setExpanded(True)
        root.setFirstColumnSpanned(True)
        root.setToolTip(0, f"Click + to add a new {root.text(0)} entity")

        item = QtWidgets.QTreeWidgetItem(root, [f"Entity {root.childCount() + 1}"])
        item.setIcon(0, icon("ph.warning-fill", color="#ffcb00"))
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        widget = ToolBar(
            self,
            trailing=True,
        )

        as_inp = widget.addAction(
            icon("mdi.arrow-down-bold", color_off="gray", color_on="white"),
            "Mark as Input",
            lambda: print(f"Mark as input"),
        )

        as_out = widget.addAction(
            icon("mdi.arrow-up-bold", color_off="gray", color_on="white"),
            "Mark as Output",
            lambda: print(f"Mark as output"),
        )

        delete = widget.addAction(
            icon("mdi.delete", color="red"),
            "Delete",
            self._on_item_deleted,
        )

        as_inp.setCheckable(True)
        as_out.setCheckable(True)
        delete.setData(item)

        self.setItemWidget(item, self.columnCount() - 1, widget)
        self.editItem(item, 0)
        return item

    def delete_entity(self, flow_id: str, entity: str):

        root = self._flow_to_item_map.get(flow_id, None)
        if not root:
            return

        item = next(
            (
                root.child(index)
                for index in range(root.childCount())
                if root.child(index).text(0) == entity
            )
        )

        root.removeChild(item)
