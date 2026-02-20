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
from gui.widgets.toolbar import ToolBar


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

        # Define a widget factory list
        self._widget_factory: dict[str, tuple] = {}

        # Initialize corner toolbar
        self._corner_toolbar = ToolBar(
            parent=self,
            trailing=True,
            iconSize=QtCore.QSize(16, 16),
        )

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

    @QtCore.Slot()
    def _add_tab_from_factory(self):

        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return

        image = action.icon()
        label = action.text()
        widget = self._widget_factory.get(label, None)

        if widget:
            super().addTab(widget[1](), image, label)

    @QtCore.Slot()
    def _go_to_previous_tab(self) -> None:
        """Navigate to the previous tab."""

        current = self.currentIndex()
        if current > 0:
            self.setCurrentIndex(current - 1)

    @QtCore.Slot()
    def _go_to_next_tab(self) -> None:
        """Navigate to the next tab."""

        current = self.currentIndex()
        if current < self.count() - 1:
            self.setCurrentIndex(current + 1)

    @QtCore.Slot()
    def _rename_tab(self) -> None:

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

    def register_widget(
        self,
        widget: type,
        label: str,
        image: QtGui.QIcon = QtGui.QIcon(),
    ):

        action = QtGui.QAction(label, icon=image, parent=self._corner_toolbar)
        action.triggered.connect(self._add_tab_from_factory)

        self._widget_factory[label] = (image, widget)
        self._corner_toolbar.addAction(action)

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
