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
from gui.widgets import Lights
from gui.widgets import Viewer


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
        """Enforce singleton design by returning the same instance."""

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
        super().setObjectName("main-window")

        # Frameless window with a transparent background for explicit background control:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        # Window dragging properties
        self.setProperty("dragged_via_menubar", False)
        self.setProperty("mouse_press_pos", QtCore.QPointF())

        self._init_menubar()
        self._init_toolbar()
        self._init_tabview()
        self._init_status()
        self._init_shortcuts()

        self._options = MainWindow.Options()
        self._lights = None  # Will be set in _init_menubar
        self._initialized = True

    def _init_menubar(self) -> None:
        """
        Initialize the menubar with File, Edit, View, and Help menus and traffic light controls.

        Sets the menubar to use the application's custom menu bar instead of the system's native one.
        Adds traffic light buttons (minimize, maximize, close) as a corner widget.
        Installs event filter for window dragging via the menubar.
        """
        # Create and configure the traffic lights widget
        self._lights = Lights(self)
        self._lights.sig_minimize_clicked.connect(self.showMinimized)
        self._lights.sig_maximize_clicked.connect(self._on_maximize)
        self._lights.sig_close_clicked.connect(self.close)

        # Configure menubar
        menubar = self.menuBar()
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

        # Use application's custom menu bar and set traffic lights as corner widget
        menubar.setNativeMenuBar(False)
        menubar.setCornerWidget(self._lights)

        # Install event filter for window dragging via menubar
        menubar.installEventFilter(self)
        self._lights.installEventFilter(self)

    def _init_toolbar(self) -> None:
        """
        Initialize the left-aligned toolbar with action buttons.

        Creates a vertical toolbar with action buttons for Dock, Open, Save, Optimize, and Results.
        The toolbar is non-floatable and non-movable by default.
        """

        toolbar = ToolBar(
            self,
            style="QToolBar QToolButton {margin: 1px 1px 2px 1px;}",
            orientation=QtCore.Qt.Orientation.Vertical,
            iconSize=QtCore.QSize(24, 24),
            trailing=False,
            actions=[
                (
                    qta_icon("ph.layout-fill", color="#fef9ef"),
                    "Dock",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.folder-plus", color="#ffcb77"),
                    "Open",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.floppy", color="#17c3b2"),
                    "Save",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.language-python", color="#227c9d"),
                    "Optimize",
                    self._on_action_triggered,
                ),
                (
                    qta_icon("mdi.chart-box", color="#fe6d73", color_active="#ff3d44"),
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
        from sidebar.sidebar import SideBar

        sidebar = SideBar(self)
        sidebar.hide()

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, sidebar)

    def _init_tabview(self) -> None:
        """
        Initialize the tab view as the central widget.

        Creates a QTabWidget with closable, movable tabs positioned at the top.
        Sets it as the central widget of the main window.
        """

        # Required:
        from gui.main_ui.tabber import TabWidget

        self._tabs = TabWidget(
            self,
            tabsClosable=True,
            tabPosition=QtWidgets.QTabWidget.TabPosition.North,
            movable=True,
        )

        self.setCentralWidget(self._tabs)

        # Show a permanent map tab and make it unclosable:
        self._tabs.new_tab(
            QtWidgets.QFrame(), icon=qta_icon("mdi.map", color="lightblue"), label="Map"
        )

        self._tabs.tabBar().setTabButton(
            0, QtWidgets.QTabBar.ButtonPosition.RightSide, None
        )

    def _init_status(self) -> None:
        """Initialize the status bar at the bottom of the main window."""
        self._status = QtWidgets.QStatusBar()
        self.setStatusBar(self._status)

    def _init_shortcuts(self) -> None:
        """Initialize keyboard shortcuts for the main window."""

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+T"), self, self._on_new_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self._on_del_tab)

    @QtCore.Slot()
    def _on_action_triggered(self) -> None:
        """
        Handle toolbar action button clicks.

        This slot is invoked when an action from the toolbar is triggered either programmatically
        or by user interaction. Implement specific behavior based on the triggered action.
        """
        pass

    @QtCore.Slot()
    def _on_maximize(self) -> None:
        """Toggle the window between normal and maximized states."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    @QtCore.Slot()
    def _on_new_tab(self) -> None:
        """
        Create a new tab with a graphics view and scene.

        Creates a QGraphicsScene with a dark gray background and adds it to a QGraphicsView.
        The view is configured for drag-based panning.
        """

        # Create the graphics scene with background color
        scene = QtWidgets.QGraphicsScene(self)

        # Create the graphics view and set the scene
        viewer = Viewer(
            scene,
            viewportUpdateMode=QtWidgets.QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate,
            renderHints=QtGui.QPainter.RenderHint.Antialiasing,
            dragMode=QtWidgets.QGraphicsView.DragMode.ScrollHandDrag,
            cacheMode=QtWidgets.QGraphicsView.CacheModeFlag.CacheBackground,
            optimizationFlags=QtWidgets.QGraphicsView.OptimizationFlag.DontSavePainterState,
            sceneRect=QtCore.QRectF(0, 0, 10000.0, 10000.0),
            backgroundBrush=QtGui.QBrush(QtGui.QColor(0x393e41))
        )

        viewer.setViewportMargins(2, 2, 2, 2)
        viewer.setCornerWidget(QtWidgets.QFrame())

        self._tabs.new_tab(
            viewer,
            qta_icon("mdi.sitemap", color="#efefef"),
            "Schematic",
        )

    @QtCore.Slot()
    def _on_del_tab(self):
        pass

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        Handle mouse press events for window dragging.

        Stores the initial left-button click position for use in window dragging via the menubar.

        Args:
            event: The mouse press event.
        """
        super().mousePressEvent(event)
        if event.isAccepted():
            return

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.setProperty("mouse_press_pos", event.position())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        Handle mouse move events for window dragging.

        Moves the window by calculating the delta between the current and initial mouse positions
        when dragged via the menubar with the left button pressed.

        Args:
            event: The mouse move event.
        """
        if event.buttons() & QtCore.Qt.MouseButton.LeftButton and self.property(
            "dragged_via_menubar"
        ):
            if click_position := self.property("mouse_press_pos"):
                delta = event.position() - click_position
                delta_point = delta.toPoint()
                self.move(self.pos() + delta_point)

        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        Handle double-click events on the menubar to toggle maximize.

        Double-clicking a blank area of the menubar toggles the window between normal and
        maximized states, similar to native window manager behavior.

        Args:
            event: The double-click event.
        """
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return super().mouseDoubleClickEvent(event)

        self._on_maximize()
        return super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        Handle mouse release events to end window dragging.

        Clears the window dragging state when the left mouse button is released, stopping
        any active window drag operation.

        Args:
            event: The mouse release event.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.setProperty("dragged_via_menubar", False)
            self.setProperty("mouse_press_pos", None)

        super().mouseReleaseEvent(event)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
        Filter events from the menubar to enable window dragging.

        Intercepts mouse events on blank areas of the menubar to allow window dragging and
        maximize toggling. Events that occur over menu items are allowed to pass through normally.

        Args:
            watched: The object being watched.
            event: The event to filter.

        Returns:
            True if the event was handled, False otherwise.
        """
        if not isinstance(event, QtGui.QMouseEvent):
            return super().eventFilter(watched, event)

        event_type = event.type()
        if event_type not in (
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseMove,
            QtCore.QEvent.Type.MouseButtonDblClick,
            QtCore.QEvent.Type.MouseButtonRelease,
        ):
            return super().eventFilter(watched, event)

        menubar = self.menuBar()
        if menubar is None:
            return super().eventFilter(watched, event)

        # Use global coordinates for consistent hit-testing:
        global_pos_f = event.globalPosition()
        global_pos = global_pos_f.toPoint()

        # Always clear menubar drag on release:
        if event_type == QtCore.QEvent.Type.MouseButtonRelease and self.property(
            "dragged_via_menubar"
        ):
            local_window = QtCore.QPointF(self.mapFromGlobal(global_pos))
            forwarded = QtGui.QMouseEvent(
                event_type,
                local_window,
                local_window,
                global_pos_f,
                event.button(),
                event.buttons(),
                event.modifiers(),
            )
            self.mouseReleaseEvent(forwarded)
            self.setProperty("dragged_via_menubar", False)
            self.setProperty("mouse_press_pos", None)
            return True

        # Only intercept events over blank areas of the menubar:
        action = menubar.actionAt(menubar.mapFromGlobal(global_pos))
        if action is None:
            local_window = QtCore.QPointF(self.mapFromGlobal(global_pos))
            forwarded = QtGui.QMouseEvent(
                event_type,
                local_window,
                local_window,
                global_pos_f,
                event.button(),
                event.buttons(),
                event.modifiers(),
            )

            if event_type == QtCore.QEvent.Type.MouseButtonPress:
                self.setProperty("dragged_via_menubar", True)
                self.setProperty("mouse_press_pos", local_window)
                self.mousePressEvent(forwarded)
                return True

            if event_type == QtCore.QEvent.Type.MouseMove:
                if self.property("dragged_via_menubar"):
                    self.mouseMoveEvent(forwarded)
                    return True
                return super().eventFilter(watched, event)

            if event_type == QtCore.QEvent.Type.MouseButtonDblClick:
                self.mouseDoubleClickEvent(forwarded)

        return super().eventFilter(watched, event)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """
        Paint the main window with a rounded rectangle background.

        Args:
            event: The paint event.
        """
        painter = QtGui.QPainter(self)
        painter.save()

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self._options.background)
        painter.drawRoundedRect(self.rect(), 8, 8)

        painter.restore()
        super().paintEvent(event)
