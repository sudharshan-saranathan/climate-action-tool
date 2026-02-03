# Filename: main_ui.py
# Module name: gui
# Description: The main User Interface.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


# Standard
from dataclasses import field
from dataclasses import dataclass

from gui.reusable.dock import DockWidget
from gui.reusable.toolbar import ToolBar


# ----------------------------------------------------------------------------------------------------------------------
# Class Name: `MainWindow`
# Class Info: CAT's main top-level user interface (UI)
# Qt website: https://doc.qt.io/qtforpython-6/index.html


class MainWindow(QtWidgets.QMainWindow):

    @dataclass(frozen=True)
    class Style:
        """
        Border and background styling options for the main window.

        - border: QPen object used to draw the window's border.
        - background: QBrush object used to fill the window's background.
        """

        pen: dict = field(default_factory=lambda: {"color": 0x363E41, "width": 1.0})
        brs: dict = field(default_factory=lambda: {"color": 0x232A2E})

    @dataclass
    class Attrs:
        radius: int = 8
        rect: QtCore.QRect = field(
            default_factory=lambda: QtCore.QRect(100, 100, 1600, 900)
        )

    def __init__(self):
        super().__init__(parent=None)  # Top-level window must have no parent.

        # Define style and attribute(s)
        self._style = MainWindow.Style()
        self._attrs = MainWindow.Attrs()

        # Customize appearance and behaviour
        self.setContentsMargins(4, 4, 4, 4)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setGeometry(self._attrs.rect)

        # UI components
        self._init_dock()
        self._init_tabs()
        self._init_toolbar()

    def _init_dock(self):

        from gui.reusable.dock import DockWidget

        upper = DockWidget("Climate Action Tool", QtWidgets.QTableWidget())
        lower = DockWidget("", QtWidgets.QTableWidget())

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, upper)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, lower)

    def _init_tabs(self):

        tabs = QtWidgets.QTabWidget(
            self,
            tabsClosable=True,
            tabBarAutoHide=True,
            tabShape=QtWidgets.QTabWidget.TabShape.Rounded,
        )

        self.setCentralWidget(tabs)

    def _init_toolbar(self):

        # Required
        from gui.reusable.toolbar import ToolBar
        from qtawesome import icon

        toolbar_one = ToolBar(
            self,
            iconSize=QtCore.QSize(18, 18),
            actions=[
                (icon("ph.layout-fill", color_active="#f2d3aa"), "Dock", self._execute),
                (icon("ph.folder-fill", color_active="#ffcb00"), "open", self._execute),
            ],
        )

        toolbar_two = ToolBar(
            self,
            iconSize=QtCore.QSize(18, 18),
            actions=[
                (icon("ph.gear", color_active="#ababab"), "Settings", self._execute),
            ],
        )

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar_one)
        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar_two)

    def _execute(self):
        pass

    def paintEvent(self, event: QtGui.QPaintEvent):

        pen_color = self._style.pen["color"]
        pen_width = self._style.pen["width"]
        brs_color = self._style.brs["color"]

        brs = QtGui.QBrush(QtGui.QColor(brs_color))
        pen = QtGui.QPen(QtGui.QColor(pen_color), pen_width)

        painter = QtGui.QPainter(self)
        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(self.rect(), self._attrs.radius, self._attrs.radius)
        painter.end()
