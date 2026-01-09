# Encoding: utf-8
# Filename: window
# Description: The main graphical user interface of this application (subclassed from QMainWindow)

# Imports (standard):
from __future__ import annotations

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
        self._setup_ui()

    # Set up the UI:
    def _setup_ui(self):
        """
        Invoked by the class's constructor to initialize the UI's components.
        :return:
        """

        # Menubar (located at the top of the window):
        menubar = self.menuBar()

        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")
