# Filename: tree.py
# Module name: vertex
# Description: Two-column QTreeWidget with category headers and stream items.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

import qtawesome as qta


class StreamTree(QtWidgets.QTreeWidget):
    """
    A two-column tree widget for managing flow streams by category.

    Column 0: Icon + Label
    Column 1: Action buttons (+ for categories, gear/delete for streams)

    Signals:
        add_requested: Emitted when a category's + button is clicked. Passes the category key.
        stream_selected: Emitted when a stream item is clicked. Passes (item, flow).
        delete_requested: Emitted when a stream's delete button is clicked. Passes the stream item.
    """

    # Data role for storing flow on items
    FLOW_ROLE = QtCore.Qt.ItemDataRole.UserRole + 1

    add_requested = QtCore.Signal(str)
    stream_selected = QtCore.Signal(QtWidgets.QTreeWidgetItem, object)
    configure_requested = QtCore.Signal(QtWidgets.QTreeWidgetItem, object)
    delete_requested = QtCore.Signal(QtWidgets.QTreeWidgetItem)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setIndentation(16)
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        # Stretch column 0, fixed size for column 1 (action buttons)
        header = self.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(1, 56)

        self._categories: dict[str, QtWidgets.QTreeWidgetItem] = {}

        # Emit stream_selected when a stream item is clicked
        self.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item: QtWidgets.QTreeWidgetItem, column: int) -> None:
        """Emit stream_selected if a stream item (not category) is clicked."""
        flow = item.data(0, self.FLOW_ROLE)
        if flow is not None:
            self.stream_selected.emit(item, flow)

    def add_category(self, key: str, icon, label: str) -> QtWidgets.QTreeWidgetItem:
        """
        Add a top-level category with a + button.

        Args:
            key: Unique identifier for this category.
            icon: QIcon for the category.
            label: Display label.

        Returns:
            The category QTreeWidgetItem.
        """
        item = QtWidgets.QTreeWidgetItem(self)
        item.setText(0, label)
        item.setIcon(0, icon)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        item.setData(0, QtCore.Qt.ItemDataRole.UserRole, key)

        # Add button in column 1
        add_btn = QtWidgets.QToolButton()
        add_btn.setIcon(qta.icon("mdi.plus"))
        add_btn.setAutoRaise(True)
        add_btn.setToolTip(f"Add {label}")
        add_btn.clicked.connect(lambda: self.add_requested.emit(key))
        self.setItemWidget(item, 1, add_btn)

        item.setExpanded(True)
        self._categories[key] = item
        return item

    def add_stream(
        self,
        category_key: str,
        label: str,
        flow=None,
    ) -> QtWidgets.QTreeWidgetItem | None:
        """
        Add a stream item under a category.

        Args:
            category_key: The key of the parent category.
            label: Display label for the stream.
            flow: Optional flow instance to associate with this stream.

        Returns:
            The stream QTreeWidgetItem, or None if category not found.
        """

        # Required
        from gui.widgets.toolbar import ToolBar

        category = self._categories.get(category_key)
        if not category:
            return None

        item = QtWidgets.QTreeWidgetItem(category)
        item.setText(0, label)
        item.setIcon(0, qta.icon("mdi.circle-small"))
        if flow is not None:
            item.setData(0, self.FLOW_ROLE, flow)

        # Action buttons container
        actions = ToolBar(
            self,
            trailing=False,
            actions=[
                (
                    qta.icon("mdi.cog-outline"),
                    "Configure",
                    lambda: self.configure_requested.emit(
                        item, item.data(0, self.FLOW_ROLE)
                    ),
                ),
                (
                    qta.icon("mdi.trash-can-outline", color="red"),
                    "Delete",
                    lambda: self.delete_requested.emit(item),
                ),
            ],
        )

        self.setItemWidget(item, 1, actions)
        return item

    def remove_stream(self, item: QtWidgets.QTreeWidgetItem) -> None:
        """Remove a stream item from its parent category."""
        parent = item.parent()
        if parent:
            parent.removeChild(item)

    def category(self, key: str) -> QtWidgets.QTreeWidgetItem | None:
        """Get a category item by key."""
        return self._categories.get(key)
