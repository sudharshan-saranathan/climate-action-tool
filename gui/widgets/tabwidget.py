#  Filename: tabs.py
#  Module name: gui.widgets
#  Description: A reusable tab widget for the main UI of Climact.

from __future__ import annotations

# Collections
from collections import namedtuple

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


# Climact modules: gui.widgets


class TabWidget(QtWidgets.QTabWidget):
    """
    Custom tab widget with configurable appearance and keyboard shortcuts.

    Extends QTabWidget with custom styling options and keyboard shortcuts:
    - Ctrl+T: Create new tab
    - Ctrl+W: Close current tab
    - Ctrl+Left: Navigate to previous tab
    - Ctrl+Right: Navigate to the next tab
    - Ctrl+R: Rename current tab
    """

    DefaultTheme = namedtuple("Theme", ["borderline", "background"])
    DefaultAttrs = namedtuple(
        "Attrs",
        [
            "iconSize",
            "position",
            "closable",
            "movable",
            "background",
        ],
    )

    # Initializer
    def __init__(self, parent=None):

        # Initialize default options, flags, and other necessary attributes before super().__init__()
        self._initialize_defaults()

        super().__init__(
            parent,
            movable=self._attrs.movable,
            tabPosition=self._attrs.position,
            tabsClosable=self._attrs.closable,
        )

        # Initialize keyboard shortcuts
        self._init_shortcuts()

    def _initialize_defaults(self) -> None:

        self._theme = self.DefaultTheme(
            borderline=QtGui.QPen(QtGui.QColor(0x363E41), 1.0),
            background=QtGui.QBrush(QtGui.QColor(0x232A2E)),
        )
        self._attrs = self.DefaultAttrs(
            iconSize=QtCore.QSize(16, 16),
            position=QtWidgets.QTabWidget.TabPosition.North,
            closable=True,
            movable=True,
            background=QtGui.QBrush(QtGui.QColor(0x232A2E)),
        )

    def _init_shortcuts(self) -> None:

        self.addAction("Ctrl+T", self.create_tab)
        self.addAction("Ctrl+W", self.remove_tab)
        self.addAction("Ctrl+Left", self.go_to_prev_tab)
        self.addAction("Ctrl+Right", self.go_to_next_tab)
        self.addAction("Ctrl+R", self.rename_tab)

    @QtCore.Slot()
    def create_tab(
        self,
        widget: QtWidgets.QWidget = QtWidgets.QWidget(),
        image: QtGui.QIcon = QtGui.QIcon(),
        label: str = str(),
    ) -> None:

        count = self.count() + 1
        label = label or f"Tab {count}"
        self.addTab(widget, image, label)

    @QtCore.Slot()
    def remove_tab(self, index: int = None):

        index = index or self.currentIndex()
        widget = self.widget(index)

        self.removeTab(index)
        widget.deleteLater()

    @QtCore.Slot()
    def go_to_prev_tab(self) -> None:
        if current := self.currentIndex():
            self.setCurrentIndex(current - 1)

    @QtCore.Slot()
    def go_to_next_tab(self) -> None:
        if current := self.currentIndex() < self.count() - 1:
            self.setCurrentIndex(current + 1)

    @QtCore.Slot()
    def rename_tab(self) -> None:

        index = self.currentIndex()
        if index < 0 or index >= self.count():
            return

        label = self.tabText(index)
        label, ok = QtWidgets.QInputDialog.getText(
            self,
            "Rename Tab",
            "Enter new tab name:",
            QtWidgets.QLineEdit.EchoMode.Normal,
            label,
        )
        if not ok or not label:
            return

        self.setTabText(index, label)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:

        indx = self.currentIndex()
        rect = self.tabBar().tabRect(indx)
        rect = rect.adjusted(0, 12, -4, 8)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0xEFEFEF)))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRect(rect)
        painter.end()
