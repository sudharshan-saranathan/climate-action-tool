# Filename: __init__.py
# Module name: config
# Description: Vertex configuration dialog.

import weakref

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets import ComboBox, HLayout
from gui.graph.vertex.config.tree import StreamTree

from core.flows import ResourceDictionary, ParameterDictionary


class VertexConfig(QtWidgets.QDialog):

    def __init__(
        self,
        vertex: QtWidgets.QGraphicsObject,
        parent: QtWidgets.QWidget = None,
    ):
        self._vertex_ref = weakref.ref(vertex)
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

    @QtCore.Slot()
    def _on_label_edited(self):
        from gui.graph.vertex.vertex import VertexItem

        string = self._label.text()
        vertex = self._vertex_ref()

        if isinstance(vertex, VertexItem):
            vertex.rename(string)

        QtCore.QTimer.singleShot(
            0, lambda: self._label.setStyleSheet("border: 1px solid green;")
        )
        QtCore.QTimer.singleShot(
            1000, lambda: self._label.setStyleSheet("border: none;")
        )
        QtCore.QTimer.singleShot(1000, lambda: self._label.clearFocus())

    def _current_form_stack(self) -> QtWidgets.QStackedWidget | None:

        page = self._dataview.currentWidget()
        if isinstance(page, QtWidgets.QSplitter) and page.count() >= 2:
            stack = page.widget(1)
            if isinstance(stack, QtWidgets.QStackedWidget):
                return stack
        return None

    @QtCore.Slot(QtWidgets.QTreeWidgetItem)
    def _on_item_selected(self, item: QtWidgets.QTreeWidgetItem):

        if not (item and item.parent()):
            return

        form = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        form_stack = self._current_form_stack()

        if form and form_stack:
            form_stack.addWidget(form)
            form_stack.setCurrentWidget(form)

    def _create_tab_widget(self, label: str) -> QtWidgets.QSplitter:

        from qtawesome import icon

        inp_tree = StreamTree(list(ResourceDictionary.values()), self)
        out_tree = StreamTree(list(ResourceDictionary.values()), self)
        par_tree = StreamTree(list(ParameterDictionary.values()), self)

        # Connect tree selection to form display
        for _tree in (inp_tree, out_tree, par_tree):
            _tree.itemClicked.connect(self._on_item_selected)

        tab = QtWidgets.QTabWidget(self)
        tab.addTab(inp_tree, icon("mdi.arrow-down-bold", color="gray"), "Inputs")
        tab.addTab(out_tree, icon("mdi.arrow-up-bold", color="gray"), "Outputs")
        tab.addTab(par_tree, icon("mdi.alpha", color="magenta"), "Parameters")
        tab.addTab(
            QtWidgets.QTextEdit(), icon("mdi.equal", color="cyan"), "Constraints"
        )

        form_stack = QtWidgets.QStackedWidget(self)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical, self)
        splitter.addWidget(tab)
        splitter.addWidget(form_stack)

        return splitter

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
