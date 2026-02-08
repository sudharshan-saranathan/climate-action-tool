#  Filename: gui/graph/vertex/config/tree.py
#  Module Name: VertexConfigTree
#  Description: Tree widget for VertexConfigDialog.

from typing import Any, Literal
from PySide6 import QtCore
from PySide6 import QtWidgets
import qtawesome as qta


class StreamTree(QtWidgets.QTreeWidget):
    """Tree widget for VertexConfigDialog."""

    def __init__(self, parent=None, resources: dict[str, Any] = None):
        super().__init__(parent, columnCount=3)

        # Customize appearance and behaviour
        self.setHeaderHidden(True)
        self.setColumnWidth(2, 40)
        self.setStyleSheet("QTreeWidget::item { height: 20px; }")
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)

        # Customize header
        header = self.header()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Strong references to prevent GC of StreamForm instances
        self.item_to_form_map: dict[QtWidgets.QTreeWidgetItem, object] = {}

        # If top-level items are provided, initialize them
        if resources:
            self._init_top_level_items(resources)

    def _init_top_level_items(self, resources: dict[str, Any]):

        # Import toolbar
        from gui.widgets.toolbar import ToolBar

        # Create a row for each flow class
        for label, flow_class in resources.items():
            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, flow_class.Attrs.label)
            item.setIcon(0, flow_class.Attrs.image)
            item.setData(0, QtCore.Qt.ItemDataRole.UserRole, flow_class)

            toolbar = ToolBar(
                self,
                iconSize=QtCore.QSize(16, 16),
                actions=[
                    (
                        qta.icon("mdi.plus"),
                        "Add",
                        lambda _, l=label: self.create_entity(l),
                    )
                ],
            )

            self.setItemWidget(item, self.columnCount() - 1, toolbar)

    # Method to create a new entity under the specified parent
    def create_entity(self, key: str):
        """Create a new entity under the specified parent."""

        print(f"Creating entity for {key}")

        root = self.findItems(key, QtCore.Qt.MatchFlag.MatchCaseSensitive, column=0)
        if root:
            root = root[0]
            item = QtWidgets.QTreeWidgetItem(root)
            item.setText(0, "New Entity")
            item.setIcon(0, qta.icon("ph.warning-fill", color="#ffcb00"))
            return item

        return None
