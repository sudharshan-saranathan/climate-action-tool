# Filename: __init__.py
# Module name: config
# Description: Node configuration dialog.

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets import ComboBox, HLayout
from gui.graph.node.config.tree import StreamTree

from core.streams import CLASS_REGISTRY


class NodeConfig(QtWidgets.QDialog):

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        self._widget_map = dict()
        super().__init__(parent)

        # Customize appearance and behaviour:
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(900, 720)

        self._overview = self._init_overview()
        self._dataview = self._init_dataview()

        HLayout(
            self,
            spacing=4,
            margins=(4, 4, 4, 4),
            widgets=[self._overview, self._dataview],
        )

    def _init_overview(self) -> QtWidgets.QFrame:

        container = QtWidgets.QFrame(self)
        container.setFixedWidth(240)

        self._combo = ComboBox(editable=True)
        self._label = QtWidgets.QLineEdit("Node", self)

        layout = QtWidgets.QFormLayout(
            container,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignVCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )

        layout.addRow("Entity:", self._label)
        layout.addRow("Type/Tech:", self._combo)

        self._combo.sig_item_added.connect(self._on_tech_added)
        self._combo.currentIndexChanged.connect(self._on_tech_changed)

        return container

    def _init_dataview(self) -> QtWidgets.QStackedWidget:
        dummy = self._create_tab_widget("")
        dummy.setObjectName("dummy-page")
        dummy.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect(dummy, blurRadius=5))

        stack = QtWidgets.QStackedWidget(self)
        stack.addWidget(dummy)
        return stack

    @QtCore.Slot()
    def _on_tech_added(self, label: str) -> None:
        page = self._create_tab_widget(label)
        self._dataview.addWidget(page)
        self._dataview.setCurrentWidget(page)

        self._widget_map[label] = page

    @QtCore.Slot()
    def _on_tech_changed(self, index: int) -> None:
        label = self._combo.currentText()
        page = self._widget_map.get(label, None)

        if page:
            self._dataview.setCurrentWidget(page)

    def _create_tab_widget(self, label: str) -> QtWidgets.QTabWidget:

        from qtawesome import icon

        stream_classes = list(CLASS_REGISTRY.values())
        inp_tree = StreamTree(stream_classes, self)
        out_tree = StreamTree(stream_classes, self)
        par_tree = StreamTree(stream_classes, self)

        tab = QtWidgets.QTabWidget(self)
        tab.addTab(inp_tree, icon("mdi.arrow-down-bold", color="gray"), "Consumed")
        tab.addTab(out_tree, icon("mdi.arrow-up-bold", color="gray"), "Produced")
        tab.addTab(par_tree, icon("mdi.alpha", color="magenta"), "Parameters")
        tab.addTab(
            QtWidgets.QTextEdit(), icon("mdi.equal", color="cyan"), "Constraints"
        )

        # Corner widget: search filter
        search = QtWidgets.QLineEdit(placeholderText="Filter...")
        search.setClearButtonEnabled(True)
        search.setFixedWidth(160)
        tab.setCornerWidget(search, QtCore.Qt.Corner.TopRightCorner)

        # Connect search to the active tab's filter
        search.textChanged.connect(lambda text: self._on_filter(tab, text))
        tab.currentChanged.connect(lambda: search.clear())

        return tab

    def _on_filter(self, tab: QtWidgets.QTabWidget, text: str):
        tree = tab.currentWidget()
        if isinstance(tree, StreamTree):
            tree.filter_items(text)

    def paintEvent(self, event, /):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor(0x232A2E))
        painter.drawRoundedRect(self.rect(), 8, 8)

        super().paintEvent(event)

    @property
    def overview(self) -> QtWidgets.QFrame:
        return self._overview

    @property
    def dataview(self) -> QtWidgets.QStackedWidget:
        return self._dataview

    @QtCore.Slot(str)
    def set_label_text(self, text):
        self._label.setText(text)
