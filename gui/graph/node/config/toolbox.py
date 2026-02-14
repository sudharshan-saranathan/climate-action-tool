# Filename: toolbox.py
# Module name: gui.graph.node.config.toolbox
# Description: Tree widget for browsing named streams grouped by composite type.
#
# Layout:
#   ┌──────────────────────────────────────────┐
#   │  ▼ ⚡ Electricity                    [+] │
#   │      ● Grid                          [x] │
#   │      ● Solar                         [x] │
#   │      ● Nuclear                       [x] │
#   │  ▶ ⛽ Fuel                           [+] │
#   │  ▶ 🪙 Material                      [+] │
#   └──────────────────────────────────────────┘
#
# Emits `stream_selected(stream_name, class_name)` when a child stream
# is clicked. The parent widget is responsible for displaying attribute
# forms in response.

from __future__ import annotations

from PySide6 import QtCore
from PySide6 import QtWidgets
import qtawesome as qta

from core.streams.composite import Composite
from gui.widgets.toolbar import ToolBar


class StreamTree(QtWidgets.QTreeWidget):
    """Tree of composite stream categories with user-added named streams.

    Signals:
        stream_selected(str, str): (stream_name, class_name)
            Emitted when the user selects a child stream item.
        stream_removed(str, str): (stream_name, class_name)
            Emitted when a child stream is deleted.
    """

    stream_selected = QtCore.Signal(str, str)  # (stream_name, class_name)
    stream_removed = QtCore.Signal(str, str)   # (stream_name, class_name)

    def __init__(self, stream_classes: list[type], parent=None):
        super().__init__(parent, columnCount=2)
        self.setHeaderLabels(["Stream", ""])
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Fixed
        )
        self.setColumnWidth(1, 32)
        self.setRootIsDecorated(True)
        self.setSelectionMode(
            QtWidgets.QTreeWidget.SelectionMode.SingleSelection
        )

        self._cls_map: dict[str, type] = {}
        self._roots: dict[str, QtWidgets.QTreeWidgetItem] = {}

        for cls in stream_classes:
            if issubclass(cls, Composite):
                self._add_category(cls)

        self.currentItemChanged.connect(self._on_current_changed)

    def _add_category(self, cls: type):
        root = QtWidgets.QTreeWidgetItem(self)
        root.setText(0, cls.label)
        root.setIcon(0, qta.icon(cls.image, color=cls.color))
        root.setFlags(
            QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
        )

        toolbar = ToolBar(
            self,
            trailing=True,
            actions=[
                (
                    qta.icon("mdi.plus", color="gray", color_active="white"),
                    f"Add {cls.label}",
                    lambda _, c=cls: self._on_add_stream(c),
                ),
            ],
        )
        self.setItemWidget(root, 1, toolbar)

        self._roots[cls.label] = root
        self._cls_map[cls.label] = cls

    def _on_add_stream(self, cls: type):
        name, ok = QtWidgets.QInputDialog.getText(
            self, f"New {cls.label}", "Name:"
        )
        if not ok or not name.strip():
            return

        name = name.strip()
        root = self._roots[cls.label]

        # Prevent duplicates
        for i in range(root.childCount()):
            if root.child(i).text(0) == name:
                return

        self.add_stream(cls.label, name)

    def add_stream(self, category_label: str, name: str):
        """Programmatically add a named stream under a category."""
        root = self._roots.get(category_label)
        cls = self._cls_map.get(category_label)
        if root is None or cls is None:
            return

        child = QtWidgets.QTreeWidgetItem(root)
        child.setText(0, name)
        child.setIcon(0, qta.icon(cls.image, color=cls.color))

        toolbar = ToolBar(
            self,
            trailing=True,
            actions=[
                (
                    qta.icon("mdi.delete", color="red"),
                    "Remove",
                    lambda _, r=root, c=child, cl=cls: self._on_remove_stream(r, c, cl),
                ),
            ],
        )
        self.setItemWidget(child, 1, toolbar)

        root.setExpanded(True)
        self.setCurrentItem(child)

    def _on_remove_stream(self, root, child, cls):
        name = child.text(0)
        root.removeChild(child)
        self.stream_removed.emit(name, cls.__name__)

    def _on_current_changed(self, current, _previous):
        if current is None or current.parent() is None:
            return

        root = current.parent()
        cls = self._cls_map.get(root.text(0))
        if cls is None:
            return

        self.stream_selected.emit(current.text(0), cls.__name__)

    def cls_for(self, class_name: str) -> type | None:
        """Look up the composite class by its __name__."""
        for cls in self._cls_map.values():
            if cls.__name__ == class_name:
                return cls
        return None
