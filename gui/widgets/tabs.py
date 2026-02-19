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
        self._widget_factory: dict[type, tuple] = {}

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

    def register_widget(self, _widget: type, _icon: QtGui.QIcon, _label: str):

        action = QtGui.QAction(_label, icon=_icon, parent=self._corner_toolbar)
        action.triggered.connect(lambda: self.addTab(_widget()))
        action.setObjectName(_label)

        self._widget_factory[_widget] = (_icon, _label)
        self._corner_toolbar.addAction(action)

    def addTab(
        self,
        widget: QtWidgets.QWidget = QtWidgets.QWidget(),
        image: QtGui.QIcon = QtGui.QIcon(),
        label: str = str(),
    ):
        super().addTab(widget, image, label)
