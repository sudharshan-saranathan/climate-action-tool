# Filename: tree.py
# Module name: config
# Description: Four-column QTreeWidget with category headers and editable stream items.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets
import qtawesome as qta


# core.gui.widgets
from gui.widgets.toolbar import ToolBar


class StreamTree(QtWidgets.QTreeWidget):

    def __init__(self, _stream_list: list, parent=None):
        super().__init__(parent, columnCount=4)
        super().setEditTriggers(
            QtWidgets.QTreeWidget.EditTrigger.DoubleClicked
            | QtWidgets.QTreeWidget.EditTrigger.EditKeyPressed
        )

        # Customize appearance and behaviour
        self.setHeaderLabels(["Stream", "Value", "Units", ""])
        self.setStyleSheet("QTreeWidget::item { height: 20px; }")
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)
        self.setColumnWidth(3, 20)

        # Customize header
        header = self.header()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)

        # Add the flow classes as top-level items
        self._init_top_level_items(_stream_list)

    def _init_top_level_items(self, _stream_list: list):

        for _class in _stream_list:

            label = getattr(_class, "_label", _class.__name__)
            image = qta.icon("mdi.arrow-right-bold", color="gray")

            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, label)
            item.setIcon(0, image)
            item.setData(0, QtCore.Qt.ItemDataRole.UserRole, _class)

            toolbar = ToolBar(
                self,
                trailing=True,
                actions=[
                    (
                        qta.icon("mdi.plus", color="gray", color_active="white"),
                        "Add Stream",
                        lambda _, i=item: self.create_row(i),
                    ),
                ],
            )

            self.setItemWidget(item, 3, toolbar)

    # Override keyPressEvent to handle tab navigation
    def keyPressEvent(self, event):

        column_count = self.columnCount()

        if event.key() in (QtCore.Qt.Key.Key_Tab, QtCore.Qt.Key.Key_Backtab):

            if item := self.currentItem():
                col = self.currentColumn()
                new_col = (
                    (col + 1) % column_count
                    if event.key() == QtCore.Qt.Key.Key_Tab
                    else (col - 1) % 4
                )
                if new_col != 3:  # Skip toolbar column
                    self.setCurrentItem(item, new_col)
                    if (
                        self.editTriggers()
                        & QtWidgets.QAbstractItemView.EditTrigger.AnyKeyPressed
                    ):
                        self.editItem(item, new_col)
                event.accept()
            return
        super().keyPressEvent(event)

    @QtCore.Slot()
    def create_row(self, root=None, name="", value="", units=""):

        # Resolve the target root from the current selection if not provided
        if root is None:
            selected = self.currentItem()
            if selected is None:
                return None

            root = selected
            while root.parent() is not None:
                root = root.parent()

        item = QtWidgets.QTreeWidgetItem([name or "New Stream", str(value), str(units)])
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
        root.addChild(item)

        # Column 3: Delete button
        toolbar = ToolBar(
            self,
            trailing=True,
            actions=[
                (
                    qta.icon("mdi.delete", color="red"),
                    "Delete",
                    lambda _, r=root, i=item: r.removeChild(i),
                ),
            ],
        )

        self.setItemWidget(item, 3, toolbar)
        self.editItem(item, 0)
        root.setExpanded(True)
        return item
