# Filename: __init__.py
# Module name: config
# Description: Vertex configuration dialog.

import weakref

from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets.combobox import ComboBox
from gui.graph.vertex.config.tree import StreamTree
from gui.graph.vertex.config.form import StreamForm

from core.flow import ResourceDictionary, ParameterDictionary



class VertexConfig(QtWidgets.QFrame):

    def __init__(
        self,
        vertex: QtWidgets.QGraphicsObject,
        parent: QtWidgets.QWidget = None,
    ):
        self._vertex = weakref.ref(vertex)
        self._dicts = dict()

        super().__init__(parent)

        self._overview = self._init_overview()
        self._dataview = self._init_dataview()
        self._form = StreamForm(self)
        self._form.setDisabled(True)
        self._form.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect(self._form, blurRadius=5))

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

        self._dicts[label] = page

    @QtCore.Slot()
    def _on_tech_changed(self, index: int) -> None:
        label = self._combo.currentText()
        page = self._dicts.get(label, None)

        if page:
            self._dataview.setCurrentWidget(page)

    @QtCore.Slot()
    def _on_label_edited(self):
        from gui.graph.vertex import VertexItem

        string = self._label.text()
        vertex = self._vertex()

        if isinstance(vertex, VertexItem):
            vertex.rename(string)

        QtCore.QTimer.singleShot(
            0, lambda: self._label.setStyleSheet("border: 1px solid green;")
        )
        QtCore.QTimer.singleShot(
            1000, lambda: self._label.setStyleSheet("border: none;")
        )
        QtCore.QTimer.singleShot(1000, lambda: self._label.clearFocus())

    def _create_tab_widget(self, label: str) -> QtWidgets.QTabWidget:

        from qtawesome import icon

        inp_tree = StreamTree(list(ResourceDictionary.values()), self)
        out_tree = StreamTree(list(ResourceDictionary.values()), self)
        par_tree = StreamTree(list(ParameterDictionary.values()), self)

        tab = QtWidgets.QTabWidget(self)
        tab.addTab(inp_tree, icon("mdi.arrow-down-bold", color="#efefef"), "Inputs")
        tab.addTab(out_tree, icon("mdi.arrow-up-bold", color="#efefef"), "Outputs")
        tab.addTab(par_tree, icon("mdi.alpha", color="pink"), "Parameters")
        tab.addTab(QtWidgets.QTextEdit(), icon("mdi.equal", color="cyan"), "Equations")

        return tab

    @property
    def overview(self) -> QtWidgets.QFrame:
        return self._overview

    @property
    def dataview(self) -> QtWidgets.QStackedWidget:
        return self._dataview

    @property
    def form(self) -> StreamForm:
        return self._form

    @QtCore.Slot(str)
    def set_label_text(self, text):
        self._label.setText(text)
