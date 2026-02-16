#  Filename: config.py
#  Module name: config
#  Description: Configuration widget for a graph node.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass


class NodeConfigWidget(QtWidgets.QMainWindow):

    @dataclass
    class Appearance:
        """Default appearance options for the node configuration widget.

        Attributes:
            background: The widget's default background color.
        """

        border: QtGui.QBrush = field(
            default_factory=lambda: QtGui.QBrush(QtGui.QColor(0x363E41))
        )
        background: QtGui.QBrush = field(
            default_factory=lambda: QtGui.QBrush(QtGui.QColor(0x232A2E))
        )

    @dataclass(frozen=True)
    class Geometric:
        """Default geometric options.

        Attributes:
            border_radius: Radius of the node's rounded corners.
            padding: The node's default padding.
            dimensions: The node's default dimensions when created (fixed).
        """

        border_radius: int = 4
        padding: int = 4
        dimensions: QtCore.QSize = field(
            default_factory=lambda: QtCore.QSize(1200, 720)
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        # Make window transparent and frameless
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setContentsMargins(4, 4, 4, 4)

        # Instantiate dataclasses
        self._appearance = NodeConfigWidget.Appearance()
        self._geometric = NodeConfigWidget.Geometric()
        self.resize(
            self._geometric.dimensions.width(),
            self._geometric.dimensions.height(),
        )

        # UI components
        self._pane = self._init_dock()
        self._tabs = self._init_tabs()

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._pane)
        self.setCentralWidget(self._tabs)

    def _init_dock(self) -> QtWidgets.QDockWidget:

        from gui.widgets import TrafficLights
        from qtawesome import icon as qta_icon

        frame = QtWidgets.QFrame(self)
        frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        form = QtWidgets.QFormLayout(
            frame,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            verticalSpacing=4,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )

        form.addRow("Process:", QtWidgets.QLineEdit(frame))
        form.addRow("Tech/Type:", QtWidgets.QComboBox(frame))
        form.addRow("Primary Unit:", QtWidgets.QComboBox(frame))

        dock = QtWidgets.QDockWidget("Node Config", self, floating=False)
        dock.setTitleBarWidget(QtWidgets.QFrame(self))
        dock.setWidget(frame)

        return dock

    def _init_tabs(self):

        from gui.widgets import TrafficLights
        from gui.graph.node.tree import StreamTree
        from qtawesome import icon as qta_icon

        traffic = TrafficLights(self)
        traffic.close_clicked.connect(self.close)

        self._inp_tree = StreamTree()
        self._out_tree = StreamTree()

        tabs = QtWidgets.QTabWidget(self)
        tabs.addTab(
            self._inp_tree,
            qta_icon("mdi.arrow-down-bold", color="gray"),
            "In",
        )
        tabs.addTab(
            self._out_tree,
            qta_icon("mdi.arrow-up-bold", color="gray"),
            "Out",
        )
        tabs.addTab(
            QtWidgets.QGraphicsView(self),
            qta_icon("mdi.alpha", color="gray"),
            "Params",
        )
        tabs.addTab(
            QtWidgets.QGraphicsView(self),
            qta_icon("mdi.equal", color="gray"),
            "Equations",
        )

        tabs.setCornerWidget(traffic)
        return tabs

    def paintEvent(self, event, /):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor(0x232A2E))
        painter.drawRoundedRect(self.rect(), 8, 8)

        super().paintEvent(event)
