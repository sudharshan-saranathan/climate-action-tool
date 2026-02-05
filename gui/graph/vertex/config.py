# Filename: config.py
# Module name: vertex
# Description: Vertex configuration dialog.

# Python
import weakref


# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact
from gui.widgets.combobox import ComboBox
from gui.widgets.layouts import GLayout, HLayout
from gui.graph.vertex.tree import DataTree

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
        bounds: QtCore.QSize = field(default_factory=lambda: QtCore.QSize(900, 720))
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
        super().__init__(parent, modal=True)

        # Customize appearance and behaviour
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(self._attrs.bounds)

        # Interface components
        self._overview = self._init_overview()
        self._dataview = self._init_dataview()
        self._splitter = self._init_splitter()

        HLayout(self, margins=(8, 8, 8, 8), widgets=[self._splitter])

    def _init_overview(self) -> QtWidgets.QFrame:

        container = QtWidgets.QFrame(self)
        container.setFixedWidth(240)

        self._label = QtWidgets.QLineEdit("Vertex", self)
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

    def _init_dataview(self) -> QtWidgets.QStackedWidget:

        dummy = self._create_page("")
        dummy.setObjectName("dummy-page")
        dummy.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect(dummy, blurRadius=5))

        stack = QtWidgets.QStackedWidget(self)
        stack.addWidget(dummy)
        return stack

    def _init_splitter(self) -> QtWidgets.QSplitter:

        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        splitter.addWidget(self._overview)
        splitter.addWidget(self._dataview)

        return splitter

    def _create_page(self, label: str) -> QtWidgets.QFrame:
        """Create a blurred placeholder tab widget shown before any tech is added."""

        # Layout
        from gui.widgets.layouts import VLayout

        # Page components
        tab = self._create_tab_widget(label)
        cnf = QtWidgets.QTableWidget()
        cnf.setMinimumHeight(180)

        # Adjust relative sizing
        cnf.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        # Arrange in a grid
        frame = QtWidgets.QFrame(self)
        VLayout(
            frame,
            margins=(0, 0, 0, 0),
            spacing=4,
            widgets=[tab, cnf],
        )

        return frame

    def _create_flow_menu(self) -> QtWidgets.QMenu:

        # Required
        from core.flow import AllFlows

        # Create a menu and add actions
        menu = QtWidgets.QMenu(self)
        for flow_class in AllFlows.values():

            instance = flow_class()
            action = menu.addAction(instance.image, instance.label)
            action.setShortcutVisibleInContextMenu(True)
            action.setIconVisibleInMenu(True)
            action.triggered.connect(
                lambda checked=False, cls=flow_class: self._on_add_flow(cls)
            )

        return menu

    @QtCore.Slot()
    def _on_add_flow(self, flow_class) -> None:

        # Retrieve the current page and find the tab widget inside it
        page = self._dataview.currentWidget()
        tab = page.findChild(QtWidgets.QTabWidget)
        if tab is None:
            return

        tree = tab.currentWidget()
        if isinstance(tree, DataTree):
            flow = flow_class()
            tree.add_stream(flow=flow)

    @QtCore.Slot()
    def _on_tech_added(self, label: str) -> None:

        # Instantiate a new page and add it to the stack
        page = self._create_page(label)
        self._dataview.addWidget(page)
        self._dataview.setCurrentWidget(page)

        # Store reference in the dictionary
        self._dicts.tab_map[label] = page

    @QtCore.Slot()
    def _on_tech_changed(self, index: int) -> None:

        label = self._combo.currentText()
        page = self._dicts.tab_map.get(label, None)

        if page:
            self._dataview.setCurrentWidget(page)

    def _create_tab_widget(self, label: str) -> QtWidgets.QTabWidget:

        # Required
        from qtawesome import icon

        # Instantiate a tab-widget
        tab = QtWidgets.QTabWidget(self)

        # Create config trees for this tech
        inp_data = DataTree(self)
        out_data = DataTree(self)
        par_data = DataTree(self)

        tab.addTab(inp_data, icon("mdi.arrow-down", color="gray"), "Inputs")
        tab.addTab(out_data, icon("mdi.arrow-up", color="gray"), "Outputs")
        tab.addTab(par_data, icon("mdi.alpha", color="#ef6fc6"), "Parameters")

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
        """
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
        """

        super().paintEvent(event)
