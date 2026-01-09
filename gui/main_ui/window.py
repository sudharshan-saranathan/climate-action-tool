# Encoding: utf-8
# Filename: window
# Description: The main graphical user interface of this application (subclassed from QMainWindow)

# Imports (standard):
from __future__ import annotations

from threading import active_count

# Imports (3rd party):
from PySide6 import QtCore, QtWidgets


# Class MainWindow:
class MainWindow(QtWidgets.QMainWindow):
    """
    The main user interface (UI) of Climate Action Tool (subclassed from QMainWindow). This class initializes the UI's
    components, child widgets, a left-aligned vertical toolbar, a dock widget, a menubar, and a status bar. Further,
    only one instance of this class can exist at any given time.
    """

    # The singleton instance:
    _instance = None

    # Implementation of `__new__` to enforce the singleton pattern:
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # The class's constructor:
    def __init__(self):
        super().__init__()

        # Add child widgets, toolbars, etc. to the GUI:
        self._init_menubar()
        self._init_toolbar()
        self._init_sidebar()

    # Invoked by the class's constructor:
    def _init_menubar(self) -> None:
        """
        Initializes the window's menubar.

        :return: None
        """

        # Menubar (located at the top of the window):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

    # Invoked by the class's constructor:
    def _init_toolbar(self) -> None:
        """
        Initializes the window's toolbar with a custom QToolbar subclass. The toolbar includes actions related to
        modeling, optimization, import/export, and visualization.

        :return: None
        """

        # Import the custom toolbar:
        from qtawesome import icon as qta_icon
        from gui.widgets.toolbar import ToolBar

        toolbar = ToolBar(
            self,
            style='QToolBar QToolButton {margin: 2px;}',
            orientation=QtCore.Qt.Orientation.Vertical, # Vertical toolbar
            iconSize=QtCore.QSize(20, 20),
            trailing=False,
            actions=[
                (qta_icon('mdi.folder-plus', color='#ffcb00'), "Open", self._on_action_triggered),
                (qta_icon('mdi.floppy', color='#59bff2'), "Save", self._on_action_triggered)
            ]
        )

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar)


    # Invoked by the class's constructor:
    def _init_sidebar(self) -> None:
        pass


    # Toolbar action handler:
    @QtCore.Slot()
    def _on_action_triggered(self):
        """
        This slot is invoked when an action from the toolbar is either triggered programmatically or when the user
        explicitly clicks the toolbar's buttons. The method retrieves the triggered action, using its string label to
        call additional methods or propagate new signals. Essentially, this handler is an interchange.

        :return: None
        """