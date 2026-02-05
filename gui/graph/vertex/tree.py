# Filename: tree.py
# Module name: vertex
# Description: Single-column QTreeWidget where each top-level item is a collapsible flow header
#              with an embedded stream form widget as its child.


# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets


class StreamTree(QtWidgets.QTreeWidget):
    """
    A single-column tree widget for managing flow streams.

    Each top-level item is a collapsible header (icon + label).
    Its single child embeds a form widget via setItemWidget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setIndentation(16)
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.NoSelection)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

    def add_item(self, icon, label, widget) -> QtWidgets.QTreeWidgetItem:
        """
        Add a collapsible top-level item with an embedded child widget.

        Args:
            icon: QIcon for the header row.
            label: Text label for the header row.
            widget: The widget to embed in the child row.

        Returns:
            The top-level QTreeWidgetItem.
        """

        # Top-level header item
        item = QtWidgets.QTreeWidgetItem(self)
        item.setText(0, label)
        item.setIcon(0, icon)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        # Single child item that hosts the widget
        child = QtWidgets.QTreeWidgetItem(item)
        child.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)

        hint = widget.sizeHint()
        if hint.isValid():
            child.setSizeHint(0, hint)

        self.setItemWidget(child, 0, widget)
        item.setExpanded(False)

        return item

    def remove_item(self, item: QtWidgets.QTreeWidgetItem) -> None:
        """Remove a top-level item and its child widget."""

        index = self.indexOfTopLevelItem(item)
        if index >= 0:
            self.takeTopLevelItem(index)
