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

from gui.widgets.traffic import TrafficLights


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
        self.setContentsMargins(4, 8, 8, 8)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setGeometry(self._attrs.rect)

        # UI components
        self._init_toolbar()
        self._init_dock()
        self._init_tabs()

    def _init_toolbar(self):

        # Required
        from gui.widgets.toolbar import ToolBar
        from qtawesome import icon

        toolbar = ToolBar(
            self,
            trailing=False,
            iconSize=QtCore.QSize(18, 18),
            actions=[
                (icon("ph.layout-fill", color="darkcyan"), "Dock", self._execute),
                (icon("ph.folder-fill", color="#ffcb00"), "Open", self._execute),
                (icon("ph.play-fill", color="green"), "Run", self._execute),
                (icon("ph.dots-three", color="#efefef"), "More", self._execute),
            ],
        )

        toolbar.addAction(icon("ph.keyboard", color="white"), "Keys", self._execute)
        toolbar.addAction(icon("ph.question", color="white"), "Help", self._execute)
        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar)

    def _init_dock(self):

        # Required
        from gui.widgets.dock import DockWidget

        lower_title = str()
        upper_title = (
            "<span style='font-family: Bitcount; font-size: 16pt'>Clim</span>"
            "<span style='font-family: Bitcount; font-size: 16pt; color:darkcyan'>Act</span>"
        )

        self._u_dock = DockWidget(upper_title, QtWidgets.QTableWidget())
        self._l_dock = DockWidget(lower_title, QtWidgets.QTextEdit())

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._u_dock)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._l_dock)

    def _init_tabs(self):

        # Required
        from gui.main_ui.tabber import Tabber
        from qtawesome import icon

        # UI components
        map_viewer = QtWidgets.QGraphicsView()  # Map viewer.
        sch_viewer = QtWidgets.QGraphicsView()  # Scene viewer.
        traffic = TrafficLights(  # Traffic lights (corner widget).
            self,
            on_minimize=self.showMinimized,
            on_maximize=self.showMaximized,
            on_close=self.close,
        )

        tabs = Tabber(self)
        tabs.addTab(map_viewer, icon("ph.map-trifold-fill", color="#4a556d"), "Map")
        tabs.addTab(sch_viewer, icon("mdi.draw", color="red"), "Schematic")
        tabs.setCornerWidget(traffic)

        self.setCentralWidget(tabs)

    @QtCore.Slot()
    def _execute(self):

        action = self.sender()
        string = action.text() if isinstance(action, QtGui.QAction) else str()

        if string.lower() == "dock":
            self._u_dock.setVisible(not self._u_dock.isVisible())
            self._l_dock.setVisible(not self._l_dock.isVisible())

    def paintEvent(self, event: QtGui.QPaintEvent):

        pen_color = self._style.pen["color"]
        pen_width = self._style.pen["width"]
        brs_color = self._style.brs["color"]

        brs = QtGui.QBrush(QtGui.QColor(brs_color))
        pen = QtGui.QPen(QtGui.QColor(pen_color), pen_width)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(self.rect(), self._attrs.radius, self._attrs.radius)
        painter.end()
