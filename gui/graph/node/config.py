#  Filename: config.py
#  Module name: config
#  Description: Configuration widget for a graph node.

from __future__ import annotations

# Standard
import typing

# Dataclass
from dataclasses import field
from dataclasses import dataclass

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact
from gui.widgets import Field, HLayout
from gui.widgets import ComboBox
from gui.widgets import TabWidget


class NodeConfigWidget(QtWidgets.QDialog):

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

    @dataclass
    class Dictionary:
        """Default dictionary options.

        Attributes:
            consumed: The node's default consumed streams.
            produced: The node's default produced streams.
            parameters: The node's default parameters.
            equations: The node's default equations.
        """

        consumed: dict[str, typing.Any] = field(default_factory=dict)
        produced: dict[str, typing.Any] = field(default_factory=dict)
        parameters: dict[str, typing.Any] = field(default_factory=dict)
        equations: dict[str, typing.Any] = field(default_factory=dict)

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
        self._info = self._init_dock()
        self._tabs = self._init_tabs()

        layout = HLayout(self, spacing=4)
        layout.addWidget(self._info)
        layout.addWidget(self._tabs)

    def _init_dock(self) -> QtWidgets.QDockWidget:

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

        name_field = Field(frame, readOnly=True)
        type_combo = ComboBox(frame)
        flow_combo = ComboBox(frame)

        form.addRow("Process:", name_field)
        form.addRow("Tech/Type:", type_combo)
        form.addRow("Primary Stream:", flow_combo)

        dock = QtWidgets.QDockWidget("Node Config", self, floating=False)
        dock.setTitleBarWidget(QtWidgets.QFrame(self))
        dock.setWidget(frame)
        dock.setFixedWidth(280)

        return dock

    def _init_tabs(self) -> QtWidgets.QTabWidget:

        self._default_tab = QtWidgets.QLabel(
            "Click + on the top-right corner to define a new technology.",
            self,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        tech_tabs = TabWidget(self)
        tech_tabs.addTab(self._default_tab, "Default")

        return tech_tabs

    def _create_tab_widget(self):

        from gui.graph.node.tree import StreamTree
        from qtawesome import icon as qta_icon

        inp = StreamTree()
        out = StreamTree()
        par = StreamTree()
        eqn = QtWidgets.QTextEdit()

        tabs = QtWidgets.QTabWidget(self)
        tabs.addTab(inp, qta_icon("mdi.arrow-down-bold", color="gray"), "In")
        tabs.addTab(out, qta_icon("mdi.arrow-up-bold", color="gray"), "Out")
        tabs.addTab(par, qta_icon("mdi.alpha", color="gray"), "Params")
        tabs.addTab(eqn, qta_icon("mdi.equal", color="gray"), "Equations")

        return tabs

    def from_data(self, data: dict[str, typing.Any]) -> None:

        # Metadata
        meta = data.get("meta", {})

        # Set the node's label
        name_field = self._info.findChild(Field)
        name_field.setText(meta.get("label", "Process"))
        name_field.clearFocus()

        # Load the node's technical details
        # self._inp_tree.from_dict(data.get("consumed", {}))
        # self._out_tree.from_dict(data.get("produced", {}))

    def paintEvent(self, event, /):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor(0x232A2E))
        painter.drawRoundedRect(self.rect(), 8, 8)

        super().paintEvent(event)
