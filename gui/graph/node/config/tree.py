# Filename: form.py
# Module name: config
# Description: Three-column QTreeWidget with category headers and stream items.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
import qtawesome as qta


class StreamDelegate(QtWidgets.QStyledItemDelegate):
    """Delegate that paints a hover-revealed '+' icon on top-level column-2 cells."""

    add_clicked = QtCore.Signal(QtCore.QModelIndex)

    _ICON_SIZE = 16

    def __init__(self, icon: QtGui.QIcon, parent=None):
        super().__init__(parent)
        self._icon = icon

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        # Only paint on top-level items in the last column
        if index.parent().isValid() or index.column() != 2:
            return

        tree = self.parent()
        if tree is None or tree._hovered_top_row != index.row():
            return

        # Paint "+" icon centered in the cell
        sz = self._ICON_SIZE
        x = option.rect.center().x() - sz // 2
        y = option.rect.center().y() - sz // 2
        self._icon.paint(painter, x, y, sz, sz)

    def editorEvent(self, event, model, option, index):
        if (
            event.type() == QtCore.QEvent.Type.MouseButtonRelease
            and not index.parent().isValid()
            and index.column() == 2
        ):
            self.add_clicked.emit(index)
            return True
        return super().editorEvent(event, model, option, index)


class StreamTree(QtWidgets.QTreeWidget):

    def __init__(self, flow_classes: list, parent=None):
        super().__init__(parent, columnCount=3)

        # Customize appearance and behaviour
        self.setHeaderHidden(True)
        self.setColumnWidth(2, 40)
        self.setStyleSheet("QTreeWidget::item { height: 20px; }")
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)
        self.setMouseTracking(True)

        # Customize header
        header = self.header()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Hover state: track which top-level row is hovered (-1 = none)
        self._hovered_top_row = -1

        # Delegate for painting "+" on top-level column 2
        icon = qta.icon("mdi.plus", color="white")
        self._stream_delegate = StreamDelegate(icon, self)
        self._stream_delegate.add_clicked.connect(self._on_add_clicked)
        self.setItemDelegateForColumn(2, self._stream_delegate)

        # Add the flow classes as top-level items
        self._init_top_level_items(flow_classes)

    def _init_top_level_items(self, flow_classes: list):

        for _class in flow_classes:

            label = getattr(_class, "_label", _class.__name__)
            image = qta.icon("mdi.arrow-right-bold", color="gray")

            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, label)
            item.setIcon(0, image)
            item.setData(0, QtCore.Qt.ItemDataRole.UserRole, _class)

    @QtCore.Slot(QtCore.QModelIndex)
    def _on_add_clicked(self, index: QtCore.QModelIndex):
        item = self.itemFromIndex(index)
        if item is not None:
            self.create_row(item)

    @QtCore.Slot()
    def create_row(self, root=None):

        from gui.widgets.toolbar import ToolBar

        # Resolve the target root from the current selection if not provided
        if root is None:
            selected = self.currentItem()
            if selected is None:
                return

            root = selected
            while root.parent() is not None:
                root = root.parent()

        item = QtWidgets.QTreeWidgetItem(root)
        item.setText(0, "New Stream")
        item.setIcon(0, qta.icon("ph.warning-fill", color="#ffcb00"))

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

        self.setItemWidget(item, self.columnCount() - 1, toolbar)
        root.setExpanded(True)

    @QtCore.Slot(str)
    def filter_items(self, text: str):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            item.setHidden(text.lower() not in item.text(0).lower())

    # -- Hover tracking for delegate-painted "+" on top-level items --

    def _resolve_top_row(self, pos):
        """Return the top-level row index at *pos*, or -1."""
        item = self.itemAt(pos)
        if item is None:
            return -1
        while item.parent() is not None:
            item = item.parent()
        return self.indexOfTopLevelItem(item)

    def mouseMoveEvent(self, event):
        row = self._resolve_top_row(event.pos())
        if row != self._hovered_top_row:
            self._hovered_top_row = row
            self.viewport().update()
        super().mouseMoveEvent(event)

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        pos = self.viewport().mapFromGlobal(QtGui.QCursor.pos())
        row = self._resolve_top_row(pos)
        if row != self._hovered_top_row:
            self._hovered_top_row = row
            self.viewport().update()

    def leaveEvent(self, event):
        if self._hovered_top_row != -1:
            self._hovered_top_row = -1
            self.viewport().update()
        super().leaveEvent(event)
