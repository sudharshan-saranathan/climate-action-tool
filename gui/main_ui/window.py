from __future__ import annotations

import dataclasses

from PySide6 import QtCore, QtGui, QtWidgets
from qtawesome import icon as qta_icon

from gui.sidebar import SideBar
from gui.widgets import TabView, ToolBar


class MainWindow(QtWidgets.QMainWindow):
    """
    The main user interface (UI) of Climate Action Tool (subclassed from QMainWindow). This class initializes the UI's
    components, child widgets, a left-aligned vertical toolbar, a dock widget, a menubar, and a status bar. Further,
    only one instance of this class can exist at any given time.
    """

    @dataclasses.dataclass  # Options
    class Options:
        border: QtGui.QPen = dataclasses.field(default_factory=QtGui.QPen)
        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(QtGui.QColor(0x232A2E))
        )

    # Singleton pattern instance:
    _instance: MainWindow | None = None

    # Singleton pattern adopted:
    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        # Prevent reinitialization for singleton pattern:
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
        self._init_sidebar()
        self._init_tabview()

        self._options = MainWindow.Options()
        self._initialized = True

    def _init_menubar(self) -> None:
        """
        Adds menus to the main window's menubar.
        """

        # QMainWindow already instantiates a menubar. So we retrieve and modify it instead of instantiating a new one:
        menubar = self.menuBar()
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

        menubar.setNativeMenuBar(
            False
        )  # On macOS, native placement of the menubar (top of the desktop) will be ignored.

    def _init_toolbar(self) -> None:
        """
        Instantiates ToolBar (a subclass of QToolBar) and adds it to the left-aligned toolbar area.
        Actions include Open, Save, Optimize, and Results.
        """

        # By default, ToolBar is non-floatable and non-movable:
        toolbar = ToolBar(
            self,
            style="QToolBar QToolButton {margin: 1px 2px 2px 2px;}",
            orientation=QtCore.Qt.Orientation.Vertical,
            iconSize=QtCore.QSize(24, 24),  # TODO: Replace this magic number.
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
        Instantiates SideBar (a subclass of QDockWidget) and adds it as a left-aligned dock widget to the main window.
        The dock houses a ComboBox in its title, and a QStackedWidget as the main widget.
        """

        sidebar = SideBar(self)
        sidebar.hide()

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, sidebar)

    def _init_tabview(self) -> None:
        """
        Instantiates TabView (a subclass of QTabWidget) and adds it as the central widget of the main window.
        """

        tabs = TabView(
            self,
            tabsClosable=True,
            tabPosition=QtWidgets.QTabWidget.TabPosition.North,
            movable=True,
        )

        self.setCentralWidget(tabs)

    @QtCore.Slot()
    def _on_action_triggered(self):
        """
        This slot is invoked when an action from the toolbar is either triggered programmatically or when the user
        explicitly clicks the toolbar's buttons. The method retrieves the triggered action, using its string label to
        call additional methods or propagate new signals.
        """
        pass

    def paintEvent(self, event):
        """
        Reimplements paintEvent to draw the application's background.
        """

        painter = QtGui.QPainter(self)
        painter.setPen(self._options.border)
        painter.setBrush(self._options.background)
        painter.drawRoundedRect(self.rect(), 8, 8)
        painter.end()

        super().paintEvent(event)
