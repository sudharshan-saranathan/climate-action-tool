# Filename: config.py
# Module name: vertex
# Description: Vertex configuration dialog.

# Python
import logging
import weakref


# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact
from gui.widgets.combobox import ComboBox
from gui.widgets.layouts import HLayout
from gui.widgets.table import ConfigWidget
from qtawesome import icon as qta_icon

# Dataclass
from dataclasses import field
from dataclasses import dataclass


class VertexConfig(QtWidgets.QDialog):
    """A dialog window for configuring vertex inputs, outputs, parameters, and equations."""

    @dataclass(frozen=True)
    class Style:
        """Default vertex styling options.

        Attributes:
            mosaic: Path to the background texture (default: ":/theme/pattern.png").
            border: Default border styling.
            background: Default background style.
        """

        mosaic: str = ":/theme/pattern.png"
        border: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x393E41),
                "width": 0.0,
            }
        )
        background: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x232A2E),
                "brush": QtCore.Qt.BrushStyle.SolidPattern,
            }
        )

    @dataclass(frozen=True)
    class Attrs:
        bounds: QtCore.QSize = field(default_factory=lambda: QtCore.QSize(1200, 720))
        radius: int = 8

    @dataclass(frozen=True)
    class Dicts:
        tab_map: dict[str, QtWidgets.QWidget] = field(default_factory=dict)

    def __init__(
        self,
        vertex: QtWidgets.QGraphicsObject,
        parent: QtWidgets.QDialog = None,
    ):

        # Store weak reference to the vertex
        self._vertex = weakref.ref(vertex)

        # Instantiate dataclasses
        self._attrs = VertexConfig.Attrs()
        self._style = VertexConfig.Style()
        self._dicts = VertexConfig.Dicts()

        # Initialize super class
        super().__init__(parent)

        # Customize appearance and behaviour
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(self._attrs.bounds)

        # UI components
        self._stack = QtWidgets.QStackedWidget()  # Stacked widget.

        # Add placeholder widget
        self._dummy = self._create_placeholder()
        self._stack.addWidget(self._dummy)

        self._forms = self._init_forms()  # Form layout on the left-hand side.

        # Simple horizontal layout
        HLayout(
            self,
            margins=(8, 4, 8, 8),
            widgets=[self._forms, self._stack],
        )

    def _init_forms(self) -> QtWidgets.QFrame:

        container = QtWidgets.QFrame(self)
        container.setFixedWidth(240)

        self._label = QtWidgets.QLabel("Vertex", self)
        self._combo = ComboBox(editable=True)

        layout = QtWidgets.QFormLayout(
            container,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignVCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )

        layout.addRow("Entity:", self._label)
        layout.addRow("Type/Tech:", self._combo)

        # Connect combo signals
        self._combo.sig_item_added.connect(self._on_tech_added)
        self._combo.currentIndexChanged.connect(self._on_tech_changed)

        return container

    def _create_placeholder(self) -> QtWidgets.QTabWidget:
        """Create a blurred placeholder tab widget shown before any tech is added."""

        # Create using the same structure as real tab widgets
        tab = self.create_tab_widget("")
        tab.setDisabled(True)

        # Apply a blur-effect to indicate it's inactive
        blur_effect = QtWidgets.QGraphicsBlurEffect(tab)
        blur_effect.setBlurRadius(5)
        tab.setGraphicsEffect(blur_effect)
        return tab

    def _create_flow_menu(self) -> QtWidgets.QMenu:

        # Required
        from core.flow import AllFlows

        # Create a menu and add actions
        menu = QtWidgets.QMenu(self)
        for flow_class in AllFlows.values():
            instance = flow_class()
            action = menu.addAction(instance.image, instance.label)
            action.triggered.connect(
                lambda checked=False, cls=flow_class: self._on_add_flow(cls)
            )

        return menu

    def _on_add_flow(self, flow_class) -> None:
        """Handle adding a new flow stream to the current tab."""

        # Get the currently active tech page (QTabWidget)
        current_page_idx = self._stack.currentIndex()
        tab_widget = self._stack.widget(current_page_idx)

        # Get the currently active tab index in the tab widget
        current_tab_index = tab_widget.currentIndex()

        # Get the corresponding ConfigWidget (Inputs or Outputs)
        # Tab 0 = Inputs, Tab 1 = Outputs
        if current_tab_index == 0:
            table = tab_widget.widget(0)  # Inputs table
        elif current_tab_index == 1:
            table = tab_widget.widget(1)  # Outputs table
        else:
            return  # Don't add to other tabs

        # Instantiate the flow and add it to the table
        flow = flow_class()
        table.add_stream(flow=flow)

    def _on_tech_added(self, tech_name: str) -> None:

        if tech_name not in self._dicts.tab_map:
            # Remove placeholder if this is the first tech
            if len(self._dicts.tab_map) == 0:
                self._stack.removeWidget(self._dummy)
                self._dummy.deleteLater()

            # Create a new configuration widget for the new tech
            tab_widget = self.create_tab_widget(tech_name)
            self._dicts.tab_map[tech_name] = tab_widget
            self._stack.addWidget(tab_widget)

            # Switch to the newly added tech page
            self._stack.setCurrentWidget(tab_widget)

    def _on_tech_changed(self, index: int) -> None:
        """Handle switching between technology types."""

        if index < 0:
            return

        # Get the tech name from combo and switch the stack
        technology = self._combo.itemText(index)
        tab_widget = self._dicts.tab_map.get(technology, None)

        if tab_widget:
            self._stack.setCurrentWidget(tab_widget)

    def create_tab_widget(self, label: str) -> QtWidgets.QTabWidget:

        # Required
        from qtawesome import icon
        from pyqtgraph import PlotWidget

        # Instantiate a tab-widget
        tab = QtWidgets.QTabWidget(self)

        # Create data IO tables for this tech
        inp_data = ConfigWidget(self)
        out_data = ConfigWidget(self)
        par_data = ConfigWidget(self)
        equation = QtWidgets.QTextEdit(self)
        plotting = PlotWidget(self, background=QtGui.QColor(0xEFEFEF))

        tab.addTab(inp_data, icon("mdi.arrow-down", color="gray"), "Inputs")
        tab.addTab(out_data, icon("mdi.arrow-up", color="gray"), "Outputs")
        tab.addTab(par_data, icon("mdi.alpha", color="#ef6fc6"), "Parameters")
        tab.addTab(equation, icon("mdi.equal", color="darkcyan"), "Equations")
        tab.addTab(plotting, icon("mdi.chart-line", color="pink"), "Plotting")

        # Create a tech name label for top-left corner
        tech_label = QtWidgets.QLabel(f"<b>{label}</b>")
        tech_label.setStyleSheet("color: gray; padding: 4px;")
        tab.setCornerWidget(tech_label, QtCore.Qt.Corner.TopLeftCorner)

        # Create an `Add` button with the flows as menu items
        menu = self._create_flow_menu()
        button = QtWidgets.QToolButton(self)
        button.setIconSize(QtCore.QSize(20, 20))
        button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        button.setIcon(icon("mdi.plus", color="lightblue", color_active="white"))
        button.setMenu(menu)

        tab.setCornerWidget(button, QtCore.Qt.Corner.TopRightCorner)
        return tab

    @QtCore.Slot(str)
    def set_label_text(self, text):
        self._label.setText(text)

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pen = QtGui.QPen(self._style.border["color"], self._style.border["width"])
        brs = QtGui.QBrush(self._style.background["color"])

        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(
            self.rect(),
            self._attrs.radius,
            self._attrs.radius,
        )
