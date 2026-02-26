# Filename: main_ui.py
# Module name: main_ui
# Description: The main UI of Climact.

"""
Main User Interface (UI) of the application. The main window displays a toolbar, menubar, statusbar, and dock widgets.
Implemented as a singleton to ensure only one main-window instance exists.
"""

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact module: gui.widgets
from gui.widgets import ToolBar
from gui.widgets.window import FramelessWindow
from gui.main_ui.tabber import TabWidget


# MainUI: Main UI of Climact
class MainUI(FramelessWindow):

    # Constructor
    def __init__(self, **kwargs):

        # Initialize super class
        super().__init__()
        self.setObjectName("main-window")

        # Configure menubar with application-specific menus
        menubar = self.menuBar()
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

        # Initialize UI components
        self._init_toolbar()
        self._init_docks()
        self._init_tabs()

    def _init_toolbar(self) -> None:

        # Import QtAwesome (Python/Qt)
        import qtawesome as qta

        # Create toolbar with custom actions
        toolbar = ToolBar(
            self,
            style="QToolBar QToolButton {margin: 2px 2px 4px 2px;}",
            orientation=QtCore.Qt.Orientation.Vertical,
            iconSize=QtCore.QSize(24, 24),
            trailing=False,
            actions=[
                (qta.icon("ph.layout-fill", color="#fef9ef"), "Dock", self._execute),
                (qta.icon("ph.folder-fill", color="#ffcb77"), "Open", self._execute),
                (qta.icon("mdi.function", color="cyan"), "Optimize", self._execute),
                (qta.icon("mdi.chart-box", color="#fe6d73"), "Results", self._execute),
                (qta.icon("ph.dots-three", color="#efefef"), "More", self._execute),
            ],
        )

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar)

    def _init_docks(self):

        # Required
        from gui.widgets.dock import Dock
        from gui.main_ui.lower import LowerPanel
        from gui.main_ui.upper import UpperPanel

        lower_title = QtWidgets.QFrame()
        upper_title = QtWidgets.QLabel(
            """
        <span style='font-family: Bitcount; font-size: 30pt'>Clim</span>
        <span style='font-family: Bitcount; font-size: 30pt; color: darkcyan'>Act</span>
        """,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        upper_panel = UpperPanel(self)
        lower_panel = LowerPanel(self)

        upper_dock = Dock(upper_title, upper_panel, parent=self)
        lower_dock = Dock(lower_title, lower_panel, parent=self)

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, upper_dock)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, lower_dock)

        # Store dock reference(s)
        self._docks = {"upper": upper_dock, "lower": lower_dock}

    def _init_tabs(self) -> None:

        # Required
        from PySide6 import QtGui
        from qtawesome import icon
        from gui.widgets.viewer import Viewer

        # Show a permanent map tab and make it unclosable:
        tab_icon = icon("mdi.map", color="#4a556d")
        position = QtWidgets.QTabBar.ButtonPosition.RightSide

        map_canvas = QtWidgets.QGraphicsScene()
        map_viewer = Viewer(
            sceneRect=QtCore.QRectF(0, 0, 5000.0, 5000.0),
            backgroundBrush=QtGui.QBrush(QtGui.QColor(0xEFEFEF)),
        )
        map_viewer.setScene(map_canvas)

        self._tabs = TabWidget(self)
        self._tabs.addTab(map_viewer, tab_icon, "Map")
        self._tabs.tabBar().setTabButton(0, position, None)
        self.setCentralWidget(self._tabs)

    @QtCore.Slot()
    def _execute(self) -> None:
        """
        Handle toolbar action button clicks.

        This slot is invoked when an action from the toolbar is triggered either programmatically
        or by user interaction. Implement specific behavior based on the triggered action.
        """
        pass
