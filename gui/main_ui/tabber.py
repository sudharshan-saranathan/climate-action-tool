# Filename: tabber.py
# Module name: main_ui
# Description: Tab widget for the main window.

"""
Custom tab widget for the main window.

Provides a QTabWidget subclass with custom styling and keyboard shortcuts for tab management.
Shortcuts: Ctrl+T (new tab), Ctrl+W (close tab), Ctrl+Left/Right (navigate), Ctrl+R (rename).
"""

import dataclasses
from qtawesome import icon as qta_icon
from PySide6 import QtGui, QtCore, QtWidgets
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

    @dataclasses.dataclass(frozen=True)
    class Options:
        """
        Configuration options for the tab widget.

        Attributes:
            iconSize: QSize for tab icons (default: 16x16).
            tabPosition: Tab position in the widget (default: North/top).
            tabsClosable: Whether tabs display close buttons (default: True).
            movable: Whether tabs can be reordered (default: True).
            background: QBrush for tab background color (default: dark gray).
        """

        iconSize: QtCore.QSize = dataclasses.field(
            default_factory=lambda: QtCore.QSize(16, 16)
        )
        tabPosition: QtWidgets.QTabWidget.TabPosition = (
            QtWidgets.QTabWidget.TabPosition.North
        )
        tabsClosable: bool = True
        movable: bool = True
        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(
                QtGui.QColor(0x393E41), QtCore.Qt.BrushStyle.SolidPattern
            )
        )

    def __init__(self, parent=None, **kwargs):
        """
        Initialize the tab widget with optional configuration.

        Args:
            parent: Parent widget (optional).
            **kwargs: Configuration options:
                - iconSize: QSize for tab icons (default: 16x16)
                - tabPosition: Tab position (default: North)
                - tabsClosable: Whether tabs can be closed (default: True)
                - movable: Whether tabs can be moved (default: True)
        """
        # Initialize options before calling super class with literal default values
        self._opts = TabWidget.Options(
            iconSize=kwargs.get("iconSize", QtCore.QSize(16, 16)),
            movable=kwargs.get("movable", True),
            tabsClosable=kwargs.get("tabsClosable", True),
            tabPosition=kwargs.get(
                "tabPosition", QtWidgets.QTabWidget.TabPosition.North
            ),
        )

        super().__init__(
            parent,
            movable=self._opts.movable,
            iconSize=self._opts.iconSize,
            tabPosition=self._opts.tabPosition,
            tabsClosable=self._opts.tabsClosable,
        )

        # Set up keyboard shortcuts for tab management
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+T"), self, self.new_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.del_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Left"), self, self._go_to_previous_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Right"), self, self._go_to_next_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, self.rename_tab)

        self._setup_corner_toolbar()

    def new_tab(
        self,
        widget: QtWidgets.QWidget = None,
        icon: QtGui.QIcon = qta_icon("mdi.tab", color="#efefef"),
        label: str = None,
    ) -> None:
        """
        Create a new tab with the given widget.

        Adds a new tab to the tab widget with the specified content, icon, and label.
        If no label is provided, a default label is generated based on the tab count.

        Args:
            widget: The widget to display in the new tab.
            icon: The icon to display in the tab (optional).
            label: The label text for the tab (optional, default: "Tab N").
        """
        from gui.widgets.viewer import Viewer
        from gui.graph.canvas import Canvas

        count = self.count()
        label = label or f"Tab {count + 1}"

        if not widget:
            canvas = Canvas()
            widget = Viewer(
                canvas,
                parent=self,
                dragMode=QtWidgets.QGraphicsView.DragMode.NoDrag,
                viewportUpdateMode=QtWidgets.QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate,
                renderHints=QtGui.QPainter.RenderHint.Antialiasing,
                backgroundBrush=QtGui.QBrush(QtGui.QColor(0xEFEFEF)),
                sceneRect=QtCore.QRectF(0, 0, 5000, 5000),
            )

        self.addTab(widget, icon, label)
        self.setTabIcon(count, icon)

    def del_tab(self, index: int = None) -> None:
        """
        Delete the tab at the specified index.

        Removes a tab from the tab widget. If no index is provided, the currently active tab is deleted.

        Args:
            index: The index of the tab to delete (optional, default: current tab).
        """
        index = index or self.currentIndex()
        self.removeTab(index)

    def rename_tab(self, index: int = None, label: str = None) -> None:
        """
        Rename the tab at the specified index.

        Changes the label of a tab. If no label is provided, a dialog is shown to prompt the user
        for a new name. If no index is provided, the currently active tab is renamed.

        Args:
            index: The index of the tab to rename (optional, default: current tab).
            label: The new label for the tab (optional, default: prompt user with dialog).
        """
        index = index or self.currentIndex()

        if index < 0 or index >= self.count():
            return

        if label is None:
            current_label = self.tabText(index)
            label, ok = QtWidgets.QInputDialog.getText(
                self,
                "Rename Tab",
                "Enter new tab name:",
                QtWidgets.QLineEdit.EchoMode.Normal,
                current_label,
            )
            if not ok or not label:
                return

        self.setTabText(index, label)

    def _setup_corner_toolbar(self) -> None:
        """
        Create and configure the corner toolbar.

        Adds a toolbar to the top-right corner with a "New Tab" action button.
        The toolbar is non-floatable and non-movable.
        """
        actions = [
            (
                qta_icon("mdi.plus", color="gray", color_active="white"),
                "New Tab",
                lambda: self.new_tab(QtWidgets.QWidget()),
            ),
        ]

        toolbar = ToolBar(
            parent=self,
            actions=actions,
            trailing=True,
            floatable=False,
            movable=False,
        )
        self.setCornerWidget(toolbar, QtCore.Qt.Corner.TopRightCorner)

    def _go_to_previous_tab(self) -> None:
        """Navigate to the previous tab."""
        current = self.currentIndex()
        if current > 0:
            self.setCurrentIndex(current - 1)

    def _go_to_next_tab(self) -> None:
        """Navigate to the next tab."""
        current = self.currentIndex()
        if current < self.count() - 1:
            self.setCurrentIndex(current + 1)
