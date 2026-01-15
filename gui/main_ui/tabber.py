# Filename: tabber.py
# Module name: main_ui
# Description: Tab widget for the main window.

"""
Custom tab widget for the main window.

Provides a QTabWidget subclass with custom styling and keyboard shortcuts for tab management.
Supports creating and deleting tabs with Ctrl+T and Ctrl+W respectively.
"""

import dataclasses

from PySide6 import QtGui, QtCore, QtWidgets


class TabWidget(QtWidgets.QTabWidget):
    """
    Custom tab widget with configurable appearance and keyboard shortcuts.

    Extends QTabWidget with custom styling options and keyboard shortcuts for tab
    management (create tab with Ctrl+T, delete tab with Ctrl+W).
    """

    @dataclasses.dataclass(frozen=True)
    class Options:
        """Configuration options for the tab widget."""

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

    # Create a default options instance for fallback values
    _default_opts = Options()

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
        # Initialize options before calling super class
        self._opts = TabWidget.Options(
            iconSize=kwargs.get("iconSize", self._default_opts.iconSize),
            movable=kwargs.get("movable", self._default_opts.movable),
            tabsClosable=kwargs.get("tabsClosable", self._default_opts.tabsClosable),
            tabPosition=kwargs.get("tabPosition", self._default_opts.tabPosition),
        )

        super().__init__(  # See QTabWidget documentation for keyword explanation:
            parent,
            movable=self._opts.movable,
            iconSize=self._opts.iconSize,
            tabPosition=self._opts.tabPosition,
            tabsClosable=self._opts.tabsClosable,
        )

        # Register keyboard shortcuts for tab management
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+T"), self, self.new_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.del_tab)

    def new_tab(
        self, widget: QtWidgets.QWidget, icon: QtGui.QIcon = None, label: str = None
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
        count = self.count()
        label = label or f"Tab {count + 1}"

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
