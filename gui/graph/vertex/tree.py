# Filename: tree.py
# Module name: vertex
# Description: Two-column QTreeWidget where each top-level item is a collapsible flow header
#              with an embedded stream form widget as its child.


# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets


class _ResizeWatcher(QtCore.QObject):
    """Event filter that updates a QTreeWidgetItem's size hint when its widget resizes."""

    def __init__(self, item, tree):
        super().__init__(tree)
        self._item = item
        self._tree = tree

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.Resize:
            parent = self._item.parent()
            if parent and parent.isExpanded():
                self._item.setSizeHint(0, obj.sizeHint())
                parent.setExpanded(False)
                parent.setExpanded(True)
        return False


class StreamTree(QtWidgets.QTreeWidget):
    """
    A two-column tree widget for managing flow streams.

    Each top-level item is a collapsible header (icon + label + action widget).
    Its single child embeds a form widget via setItemWidget spanning both columns.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setIndentation(16)
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.NoSelection)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        # Stretch column 0, fixed size for column 1 (action button)
        header = self.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def add_item(
        self, icon, label, widget, action: QtWidgets.QWidget = None
    ) -> QtWidgets.QTreeWidgetItem:
        """
        Add a collapsible top-level item with an embedded child widget.

        Args:
            icon: QIcon for the header row.
            label: Text label for the header row.
            widget: The widget to embed in the child row.
            action: Optional widget (e.g., delete button) for the header's second column.

        Returns:
            The top-level QTreeWidgetItem.
        """

        # Top-level header item
        item = QtWidgets.QTreeWidgetItem(self)
        item.setText(0, label)
        item.setIcon(0, icon)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        # Action widget in column 1
        if action:
            self.setItemWidget(item, 1, action)

        # Single child item that hosts the widget (spans both columns visually)
        child = QtWidgets.QTreeWidgetItem(item)
        child.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        child.setFirstColumnSpanned(True)

        hint = widget.sizeHint()
        if hint.isValid():
            child.setSizeHint(0, hint)

        self.setItemWidget(child, 0, widget)
        widget.installEventFilter(_ResizeWatcher(child, self))
        item.setExpanded(False)

        return item

    def remove_item(self, item: QtWidgets.QTreeWidgetItem) -> None:
        """Remove a top-level item and its child widget."""

        index = self.indexOfTopLevelItem(item)
        if index >= 0:
            self.takeTopLevelItem(index)
