# Filename: form.py
# Module name: vertex
# Description: Three-column QTreeWidget with category headers and stream items.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets
import qtawesome as qta

from .form import StreamForm


class StreamTree(QtWidgets.QTreeWidget):

    def __init__(self, flow_classes: list, parent=None):
        super().__init__(parent, columnCount=3)

        # Customize appearance and behaviour
        self.setHeaderHidden(True)
        self.setColumnWidth(2, 60)
        self.setStyleSheet("QTreeWidget::item { height: 20px; }")
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)

        # Customize header
        header = self.header()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Add the flow classes as top-level items
        self._init_top_level_items(flow_classes)

    def _init_top_level_items(self, flow_classes: list):

        # Import toolbar
        from gui.widgets.toolbar import ToolBar

        # Create a row for each flow class
        for _class in flow_classes:

            label = _class.Attrs.label
            image = _class.Attrs.image

            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, label)
            item.setIcon(0, image)

            toolbar = ToolBar(
                self,
                iconSize=QtCore.QSize(16, 16),
                actions=[
                    (qta.icon("mdi.plus"), "Add", lambda _, l=label: self.create_row(l))
                ],
            )

            self.setItemWidget(item, 2, toolbar)

    @QtCore.Slot()
    def create_row(self, label: str):

        # Import toolbar
        from gui.widgets.toolbar import ToolBar

        root = self.findItems(label, QtCore.Qt.MatchFlag.MatchExactly, column=0)
        if root:
            root = root[0]
            item = QtWidgets.QTreeWidgetItem(root)
            item.setText(0, "New Stream")
            item.setText(1, "Not configured")
            item.setIcon(0, qta.icon("ph.warning-fill", color="#ffcb00"))

            # Find the flow class associated with this item

            toolbar = ToolBar(
                self,
                trailing=True,
                iconSize=QtCore.QSize(14, 14),
                actions=[
                    (
                        qta.icon("mdi.cog", color="gray", color_active="white"),
                        "Configure",
                        lambda: print(f"Configuring"),
                    ),
                    (
                        qta.icon("mdi.delete", color="red"),
                        "Delete",
                        lambda _, r=root, i=item: r.removeChild(i),
                    ),
                ],
            )

            self.setItemWidget(item, 2, toolbar)
            root.setExpanded(True)

    @staticmethod
    def _create_primary() -> QtWidgets.QFrame:
        pass

    @staticmethod
    def _create_secondary() -> QtWidgets.QFrame:
        pass

    @staticmethod
    def _create_temporal() -> QtWidgets.QFrame:
        pass
