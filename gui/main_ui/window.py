# Filename: window.py
# Module name: main_ui
# Description: Main window interface for the Climate Action Tool.

"""
Main window interface for the Climate Action Tool.

Provides the primary window with toolbar, menubar, statusbar, and dock widgets.
Implemented as a singleton to ensure only one window instance exists.
"""

from __future__ import annotations

import dataclasses

from qtawesome import icon as qta_icon
from PySide6 import QtCore, QtGui, QtWidgets

from gui.widgets import ToolBar


class MainWindow(QtWidgets.QMainWindow):
    """
    Main application window for the Climate Action Tool.

    Initializes and manages the primary UI components including menubar, toolbar, dock widgets,
    and statusbar. Implemented as a singleton to ensure only one window instance exists at any time.
    """

    @dataclasses.dataclass
    class Options:
        """Configuration options for the main window."""
        border: QtGui.QPen = dataclasses.field(default_factory=QtGui.QPen)
        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(
                QtGui.QColor(0x232A2E),
                QtCore.Qt.BrushStyle.SolidPattern,  # Plain color, no texture.
            )
        )

    # Singleton instance:
    _instance: MainWindow | None = None

    def __new__(cls, **kwargs):
        """Enforce singleton pattern by returning the same instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        """
        Initialize the main window.

        Prevents reinitialization by checking the _initialized flag.
        """
        # Prevent reinitialization of the singleton instance:
        if hasattr(self, "_initialized"):
            return

        super().__init__()
        super().setObjectName("main-window")  # Qt property

        # Frameless window with a transparent background for custom styling.
        # Note: Window dragging and traffic lights must be implemented manually.
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        self._init_menubar()
        self._init_toolbar()
        # self._init_sidebar()
        # self._init_tabview()
        self._init_status()

        self._options = MainWindow.Options()
        self._initialized = True

    def _init_menubar(self) -> None:
        """
        Initialize the menubar with File, Edit, View, and Help menus.

        Sets the menubar to use the application's custom menu bar instead of the system's native one.
        """
        menubar = self.menuBar()
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

        # Use the application's custom menu bar instead of the system's native menu bar:
        menubar.setNativeMenuBar(False)

    def _init_toolbar(self) -> None:
        """
        Initialize the left-aligned toolbar with action buttons.

        Creates a vertical toolbar with action buttons for Dock, Open, Save, Optimize, and Results.
        The toolbar is non-floatable and non-movable by default.
        """
        toolbar = ToolBar(
            self,
            style="QToolBar QToolButton {margin: 1px 2px 2px 2px;}",
            orientation=QtCore.Qt.Orientation.Vertical,
            iconSize=QtCore.QSize(24, 24),
            trailing=False,
            actions=[
                (
                    qta_icon("ph.layout-fill", color="#efefef"),
                    "Dock",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.folder-plus", color="#ffcb00"),
                    "Open",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.floppy", color="#59bff2"),
                    "Save",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.language-python", color="#967ab8"),
                    "Optimize",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.chart-box", color="#ffcb00"),
                    "Results",
                    self._on_action_triggered,
                ),
            ],
        )

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar)

    def _init_sidebar(self) -> None:
        """
        Initialize the sidebar dock widget.

        Creates a SideBar (QDockWidget subclass) with a ComboBox in the title and QStackedWidget
        as the main content. Adds it as a left-aligned dock widget and hides it by default.
        """
        from .sidebar.sidebar import SideBar

        sidebar = SideBar(self)
        sidebar.hide()

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, sidebar)

    def _init_tabview(self) -> None:
        """
        Initialize the tab view as the central widget.

        Creates a QTabWidget with closable, movable tabs positioned at the top.
        Sets it as the central widget of the main window.
        """
        tabs = QtWidgets.QTabWidget(
            self,
            tabsClosable=True,
            tabPosition=QtWidgets.QTabWidget.TabPosition.North,
            movable=True,
        )

        self.setCentralWidget(tabs)

    def _init_status(self) -> None:
        """Initialize the status bar at the bottom of the main window."""
        self._status = QtWidgets.QStatusBar()
        self.setStatusBar(self._status)

    @QtCore.Slot()
    def _on_action_triggered(self) -> None:
        """
        Handle toolbar action button clicks.

        This slot is invoked when an action from the toolbar is triggered either programmatically
        or by user interaction. Implement specific behavior based on the triggered action.
        """
        pass

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """
        Paint the main window with a rounded rectangle background.

        Args:
            event: The paint event.
        """
        painter = QtGui.QPainter(self)
        painter.setPen(self._options.border)
        painter.setBrush(self._options.background)
        painter.drawRoundedRect(self.rect(), 8, 8)
        painter.end()

        super().paintEvent(event)
