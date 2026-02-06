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
from gui.widgets.layouts import HLayout
from gui.graph.vertex.tree import StreamTree
from core.flow import Fuel, Material, Electricity

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
        bounds: QtCore.QSize = field(default_factory=lambda: QtCore.QSize(900, 640))
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

        HLayout(self, margins=(4, 4, 4, 4), widgets=[self._splitter])

    def _init_overview(self) -> QtWidgets.QFrame:

        container = QtWidgets.QFrame(self)
        container.setFixedWidth(240)

        self._combo = ComboBox(editable=True)
        self._label = QtWidgets.QLineEdit("Vertex", self)
        self._label.returnPressed.connect(self._on_label_edited)

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

        dummy = self._create_stack_page("")
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

    def _create_stack_page(self, label: str) -> QtWidgets.QFrame:

        # Required
        from gui.widgets.layouts import VLayout
        from gui.graph.vertex.config.stream import StreamDialog

        # Page components
        tab = self._create_tab_widget(label)

        # Arrange in a grid
        frame = QtWidgets.QFrame(self)
        VLayout(frame, margins=(0, 0, 0, 0), spacing=4, widgets=[tab])

        # Connect each StreamTree's configure_requested signal to show dialog
        for i in range(tab.count()):
            tree = tab.widget(i)
            if isinstance(tree, StreamTree):
                tree.configure_requested.connect(
                    lambda item, flow: StreamDialog(item, flow, self).exec()
                )

        return frame

    def _create_flow_menu(self) -> QtWidgets.QMenu:

        # Required
        from core.flow import AllFlows

        # Create a menu and add actions
        menu = QtWidgets.QMenu(self)
        for flow_class in AllFlows.values():

            action = menu.addAction(flow_class.Attrs.image, flow_class.Attrs.label)
            action.setShortcutVisibleInContextMenu(True)
            action.setIconVisibleInMenu(True)
            action.triggered.connect(
                lambda checked=False, cls=flow_class: self._on_add_flow(cls)
            )

        return menu

    def _init_toolbar(self) -> QtWidgets.QToolBar:

        # Required
        from gui.widgets.toolbar import ToolBar
        from core.flow import ComboFlows, Parameters

        left_align = QtCore.Qt.AlignmentFlag.AlignLeft
        vert_align = QtCore.Qt.AlignmentFlag.AlignVCenter
        label = QtWidgets.QLabel("Click to add", alignment=left_align | vert_align)

        # Instantiate toolbar
        button_style = QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly
        toolbar = ToolBar(
            self,
            toolButtonStyle=button_style,
            iconSize=QtCore.QSize(20, 20),
        )
        toolbar.addWidget(label)
        toolbar.setStyleSheet("QToolButton {padding: 0px; margin: 0px;}")
        toolbar.addSeparator()
        for _class in ComboFlows.values():
            action = toolbar.addAction(_class.Attrs.image, _class.Attrs.label)
            action.triggered.connect(
                lambda checked=False, cls=_class: self._on_add_flow(cls)
            )

        toolbar.addSeparator()
        for _class in Parameters.values():
            action = toolbar.addAction(_class.Attrs.image, _class.Attrs.label)
            action.triggered.connect(
                lambda checked=False, cls=_class: self._on_add_flow(cls)
            )

        return toolbar

    @QtCore.Slot()
    def _on_add_flow(self, flow_class) -> None:

        # Retrieve the current page and find the tab widget inside it
        page = self._dataview.currentWidget()
        tab = page.findChild(QtWidgets.QTabWidget)
        if tab is None:
            return

        tree = tab.currentWidget()
        if isinstance(tree, StreamTree):
            flow = flow_class()
            tree.add_stream(flow.key, flow.label, flow)

    @QtCore.Slot()
    def _on_tech_added(self, label: str) -> None:

        # Instantiate a new page and add it to the stack
        page = self._create_stack_page(label)
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

    @QtCore.Slot()
    def _on_label_edited(self):

        # Required
        from gui.graph.vertex.vertex import VertexItem

        string = self._label.text()
        vertex = self._vertex()

        if isinstance(vertex, VertexItem):
            vertex.rename(string)

        # Provide a visual confirmation
        QtCore.QTimer.singleShot(
            0, lambda: self._label.setStyleSheet("border: 1px solid green;")
        )
        QtCore.QTimer.singleShot(
            1000, lambda: self._label.setStyleSheet("border: none;")
        )
        QtCore.QTimer.singleShot(1000, lambda: self._label.clearFocus())

    def _create_tab_widget(self, label: str) -> QtWidgets.QTabWidget:

        # Required
        from qtawesome import icon

        # Instantiate a tab-widget
        tab = QtWidgets.QTabWidget(self)

        # Create a StreamTree per tab with predefined categories
        categories = [
            ("fuel", Fuel),
            ("material", Material),
            ("electricity", Electricity),
        ]

        # Map category key to flow class for add_requested handler
        category_map = {key: cls for key, cls in categories}

        for tab_icon, tab_label, tab_color in [
            ("mdi.arrow-down", "Inputs", "gray"),
            ("mdi.arrow-up", "Outputs", "gray"),
            ("mdi.alpha", "Parameters", "#ef6fc6"),
            ("mdi.equal", "Equations", "cyan"),
        ]:
            tree = StreamTree(self)
            for key, flow_cls in categories:
                flow = flow_cls()
                tree.add_category(key, flow.image, flow.label)

            # Connect add_requested to create a new stream
            def on_add(cat_key, t=tree):
                flow_cls = category_map.get(cat_key)
                if flow_cls:
                    flow = flow_cls()
                    t.add_stream(cat_key, flow.label, flow)

            tree.add_requested.connect(on_add)
            tab.addTab(tree, icon(tab_icon, color=tab_color), tab_label)

        return tab

    @QtCore.Slot(str)
    def set_label_text(self, text):
        self._label.setText(text)

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pen = QtGui.QPen(self._style.border["color"], self._style.border["width"])
        brs = QtGui.QBrush(self._style.background["color"])
        brs.setTexture(QtGui.QPixmap(self._style.mosaic))

        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(
            self.rect(),
            self._attrs.radius,
            self._attrs.radius,
        )

        super().paintEvent(event)
