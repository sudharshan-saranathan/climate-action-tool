# Filename: tree.py
# Module name: config
# Description: Four-column QTreeWidget with category headers and editable stream items.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets
import qtawesome as qta


# core.gui.widgets
from gui.widgets.toolbar import ToolBar
from core.streams.composite import Composite


class StreamTree(QtWidgets.QTreeWidget):

    def __init__(self, _stream_list: list, parent=None):
        super().__init__(parent, columnCount=3)
        super().setEditTriggers(
            QtWidgets.QTreeWidget.EditTrigger.DoubleClicked
            | QtWidgets.QTreeWidget.EditTrigger.EditKeyPressed
        )

        # Customize appearance and behaviour
        self.setHeaderLabels(["Stream", "Value", ""])
        self.setStyleSheet("QTreeWidget::item { height: 28px; padding: 2px;}")
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)

        # Customize header
        header = self.header()
        header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 160)

        # Add the flow classes as top-level items
        self._init_top_level_items(_stream_list)

    def _init_top_level_items(self, _stream_list: list):

        for _class in _stream_list:

            image = "mdi.arrow-right-bold"
            color = "gray"
            if issubclass(_class, Composite):
                image = _class.image
                color = _class.color

            label = getattr(_class, "_label", _class.__name__)
            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, label)
            item.setIcon(0, qta.icon(image, color=color))
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

            self.setItemWidget(item, 2, toolbar)

    def _get_root_from_selection(self) -> QtWidgets.QTreeWidgetItem | None:

        if selected := self.currentItem():
            while selected.parent():
                selected = selected.parent()

            return selected

        return None

    def _add_grouped_attributes(
        self,
        root: QtWidgets.QTreeWidgetItem,
        composite_cls: type,
    ) -> None:

        # Import the ComboBox widget from gui.widgets
        from gui.widgets import ComboBox

        groups = getattr(composite_cls, "attribute_groups", {})
        select = ComboBox(items=groups.keys())
        parent = root.parent()

        for key in groups[select.currentText()]:

            section = QtWidgets.QTreeWidgetItem([key.capitalize()])
            section.setIcon(0, qta.icon("mdi.circle-small", color="white"))

            icon = "mdi.numeric-" + str(parent.childCount())
            root.setIcon(0, qta.icon(icon, color="white"))
            root.addChild(section)

            for attr in groups[select.currentText()][key]:

                label = groups[select.currentText()][key][attr]
                field = QtWidgets.QTreeWidgetItem(section)
                field.setText(0, label)
                field.setTextAlignment(
                    0,
                    QtCore.Qt.AlignmentFlag.AlignVCenter
                    | QtCore.Qt.AlignmentFlag.AlignRight,
                )

        # self.setItemWidget(root, 1, select)

    @QtCore.Slot()
    def create_row(self, root, name="", value="", units=""):

        # Resolve the target root from the current selection if not provided
        root = root or self._get_root_from_selection()
        if root is None:
            return None

        # Merge value and units into a single field
        value_with_units = f"{value} {units}".strip() if units else str(value)
        item = QtWidgets.QTreeWidgetItem([name, value_with_units])
        item.setText(0, f"Resource {root.childCount() + 1}")
        root.addChild(item)
        self._add_grouped_attributes(
            item, root.data(0, QtCore.Qt.ItemDataRole.UserRole)
        )

        # Column 2: Toolbar
        toolbar = ToolBar(
            self,
            trailing=True,
            iconSize=QtCore.QSize(18, 18),
        )
        toolbar.addAction(qta.icon("mdi.cursor-text", color="cyan"), "Rename")
        toolbar.addAction(qta.icon("mdi.check-all", color="lightgray"), "Check")
        toolbar.addAction(qta.icon("mdi.eraser", color="lightgray"), "Erase")
        toolbar.addAction(qta.icon("mdi.delete", color="red"), "Delete")

        # Set widgets
        self.setItemWidget(item, 2, toolbar)
        self.editItem(item, 0)
        root.setExpanded(True)
        return item
