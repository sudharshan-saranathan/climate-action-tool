# Filename: main_ui.py
# Module name: gui
# Description: The main User Interface.

from __future__ import annotations

from tkinter.ttk import Style

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


# Standard
from dataclasses import field
from dataclasses import dataclass


class MainWindow(QtWidgets.QMainWindow):

    @dataclass(frozen=True)
    class Style:
        """
        Border and background styling options for the main window.
        Style options:
        - border: QPen object used to draw the window's border.
        - background: QBrush object used to fill the window's background.
        """

        pen: dict = field(default_factory=lambda: {"color": 0x363E41, "width": 1.0})
        brs: dict = field(default_factory=lambda: {"color": 0x232A2E})

    @dataclass
    class Attrs:
        radius: int = 8
        rect: QtCore.QRect = field(
            default_factory=lambda: QtCore.QRect(100, 100, 1280, 960)
        )

    def __init__(self):
        super().__init__(
            parent=None,
            dockNestingEnabled=True,
        )

        # Instantiate options
        self._style = MainWindow.Style()
        self._attrs = MainWindow.Attrs()

        # Customize behaviour and attribute(s):
        self.setContentsMargins(4, 4, 4, 4)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setGeometry(self._attrs.rect)

        # UI elements:
        self._init_toolbar()
        self._init_sidebar()
        self._init_main_widget()

    def _init_toolbar(self):

        # Required
        from qtawesome import icon

        toolbar = QtWidgets.QToolBar(
            self,
            iconSize=QtCore.QSize(20, 20),
            toolButtonStyle=QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly,
            floatable=False,
            movable=False,
        )

        layout = toolbar.addAction(icon("ph.layout-fill", color="lightblue"), "Dock")
        folder = toolbar.addAction(icon("ph.folder-fill", color="#ffcb00"), "Open")
        more   = toolbar.addAction(icon('mdi.dots-horizontal', color="#efefef"), "More")

        layout.triggered.connect(self._on_action_triggered)
        folder.triggered.connect(self._on_action_triggered)

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar)

    def _init_menubar(self):

        menubar = QtWidgets.QMenuBar(self)
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

        self.setMenuBar(menubar)

    def _init_sidebar(self):

        self._dock = QtWidgets.QDockWidget(
            str(),
            self,
            features=QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar,
            floating=False,
        )

        self._dock.setTitleBarWidget(QtWidgets.QFrame(self))
        self._dock.setWidget(QtWidgets.QListWidget(self))
        self._dock.setMinimumWidth(320)

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._dock)

    def _init_main_widget(self):

        from gui.widgets.lights import TrafficLights

        lights = TrafficLights(
            self,
            on_minimize=self.showMinimized,
            on_maximize=self.showMaximized,
            on_close=self.close,
        )

        tabs = QtWidgets.QTabWidget(self)
        tabs.addTab(QtWidgets.QGraphicsView(), "Tab 1")
        tabs.addTab(QtWidgets.QGraphicsView(), "Tab 2")
        tabs.setCornerWidget(lights, QtCore.Qt.Corner.TopRightCorner)

        self.setCentralWidget(tabs)

    def _on_action_triggered(self):

        action = self.sender()
        if isinstance(action, QtGui.QAction):
            label = action.text()

            if label == "Dock":
                self._dock.setVisible(not self._dock.isVisible())

    def paintEvent(self, event: QtGui.QPaintEvent):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        brs = QtGui.QBrush(QtGui.QColor(self._style.brs["color"]))
        pen = QtGui.QPen(
            QtGui.QColor(self._style.pen["color"]), self._style.pen["width"]
        )

        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(self.rect(), self._attrs.radius, self._attrs.radius)
        painter.end()
