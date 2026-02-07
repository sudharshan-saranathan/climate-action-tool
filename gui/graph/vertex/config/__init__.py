# Filename: __init__.py
# Module name: config
# Description: Vertex configuration dialog.

import weakref

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets.combobox import ComboBox
from gui.widgets.layouts import HLayout
from gui.graph.vertex.config.tree import StreamTree
from gui.graph.vertex.config.form import StreamForm

from core.flow import ResourceDictionary, ParameterDictionary

from dataclasses import field
from dataclasses import dataclass


class VertexConfig(QtWidgets.QDialog):

    @dataclass(frozen=True)
    class Style:
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

    def __init__(
        self,
        vertex: QtWidgets.QGraphicsObject,
        parent: QtWidgets.QDialog = None,
    ):
        self._vertex = weakref.ref(vertex)

        self._attrs = VertexConfig.Attrs()
        self._style = VertexConfig.Style()
        self._dicts = dict()

        super().__init__(parent, modal=True)

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(self._attrs.bounds)

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

    def _create_stack_page(self, label: str) -> QtWidgets.QSplitter:

        _tabs = self._create_tab_widget(label)
        _form = StreamForm(self)
        _form.setDisabled(True)
        _form.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect(_form, blurRadius=5))

        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        splitter.setContentsMargins(4, 0, 4, 0)
        splitter.addWidget(_tabs)
        splitter.addWidget(_form)

        return splitter

    @QtCore.Slot()
    def _on_tech_added(self, label: str) -> None:
        page = self._create_stack_page(label)
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
