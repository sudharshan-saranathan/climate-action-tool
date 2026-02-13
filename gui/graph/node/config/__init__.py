# Filename: __init__.py
# Module name: config
# Description: Node configuration dialog.

import json
import logging

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets import ComboBox, Field, HLayout
from gui.graph.node.config.tree import StreamTree

from core.streams import (
    CLASS_REGISTRY,
    Electricity,
    Material,
    Fuel,
)

# Flow types for input/output streams (quantities that enter/exit a node)
_FLOW_CLASSES = [Electricity, Material, Fuel]
_FLOW_NAMES = {cls.__name__ for cls in _FLOW_CLASSES}

# Parameter types: everything except flows
_PARAM_CLASSES = [
    cls for name, cls in CLASS_REGISTRY.items() if name not in _FLOW_NAMES
]


class NodeConfig(QtWidgets.QDialog):

    sig_save = QtCore.Signal(str)  # Emits serialized JSON on Save

    _logger = logging.getLogger("NodeConfig")

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ):
        self._widget_map = dict()
        self._nuid = None
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
        self._label = Field(self, placeholderText="Node")

        self._save_btn = QtWidgets.QPushButton("Save", self)
        self._save_btn.setAutoDefault(False)
        self._save_btn.setDefault(False)
        self._save_btn.clicked.connect(self._on_save_clicked)

        layout = QtWidgets.QFormLayout(
            container,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignVCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )

        layout.addRow("Entity:", self._label)
        layout.addRow("Type/Tech:", self._combo)
        layout.addRow("", self._save_btn)

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

        inp_tree = StreamTree(_FLOW_CLASSES, self)
        out_tree = StreamTree(_FLOW_CLASSES, self)
        par_tree = StreamTree(_PARAM_CLASSES, self)

        tab = QtWidgets.QTabWidget(self)
        tab.addTab(inp_tree, icon("mdi.arrow-down-bold", color="gray"), "In")
        tab.addTab(out_tree, icon("mdi.arrow-up-bold", color="gray"), "Out")
        tab.addTab(par_tree, icon("mdi.alpha", color="magenta"), "Params")
        tab.addTab(QtWidgets.QTextEdit(), icon("mdi.equal", color="cyan"), "Rules")

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

    def populate(self, data: dict) -> None:
        """Populate dialog from backend node data.

        Expected format:
        {
            "uid": "...",
            "meta": {"name": "...", ...},
            "tech": {
                "tech_name": {
                    "consumed": {"coal": {"type": "Mass", "value": 100, "units": "kg"}, ...},
                    "produced": {...},
                    "params": {...},
                    "equations": [...],
                    ...
                },
                ...
            }
        }
        """
        self._nuid = data.get("uid", self._nuid)

        # Set entity name from meta
        meta = data.get("meta", {})
        name = meta.get("name", meta.get("label", ""))
        if name:
            self._label.setText(name)

        # Clear existing tech pages
        for label, page in list(self._widget_map.items()):
            self._dataview.removeWidget(page)
            page.deleteLater()
        self._widget_map.clear()

        # Clear combo items (skip programmatic signal emission)
        self._combo.blockSignals(True)
        self._combo.clear()
        self._combo._item_count = 0
        self._combo.blockSignals(False)

        # Rebuild tech pages from data
        tech_dict = data.get("tech", {})
        for tech_name, tech_data in tech_dict.items():
            # Add to combo
            self._combo.addItem(tech_name)
            self._combo._item_count = self._combo.count()

            # Create tab page
            page = self._create_tab_widget(tech_name)
            self._dataview.addWidget(page)
            self._widget_map[tech_name] = page

            # Populate consumed (tab 0)
            consumed_tree = page.widget(0)
            if isinstance(consumed_tree, StreamTree):
                consumed_tree.populate(tech_data.get("consumed", {}))

            # Populate produced (tab 1)
            produced_tree = page.widget(1)
            if isinstance(produced_tree, StreamTree):
                produced_tree.populate(tech_data.get("produced", {}))

            # Populate params (tab 2)
            params_tree = page.widget(2)
            if isinstance(params_tree, StreamTree):
                params_tree.populate(tech_data.get("params", {}))

            # Populate equations (tab 3) — QTextEdit
            equations_widget = page.widget(3)
            if isinstance(equations_widget, QtWidgets.QTextEdit):
                equations = tech_data.get("equations", [])
                equations_widget.setPlainText("\n".join(equations))

        # Select first tech in combo
        if self._combo.count() > 0:
            self._combo.setCurrentIndex(0)
            first_label = self._combo.currentText()
            page = self._widget_map.get(first_label)
            if page:
                self._dataview.setCurrentWidget(page)

    def to_dict(self) -> dict:
        """Serialize all tech pages into the Node data format."""
        tech = {}
        for tech_name, page in self._widget_map.items():
            consumed_tree = page.widget(0)
            produced_tree = page.widget(1)
            params_tree = page.widget(2)
            equations_widget = page.widget(3)

            consumed = (
                consumed_tree.to_dict() if isinstance(consumed_tree, StreamTree) else {}
            )
            produced = (
                produced_tree.to_dict() if isinstance(produced_tree, StreamTree) else {}
            )
            params = (
                params_tree.to_dict() if isinstance(params_tree, StreamTree) else {}
            )

            equations = []
            if isinstance(equations_widget, QtWidgets.QTextEdit):
                text = equations_widget.toPlainText().strip()
                if text:
                    equations = [line for line in text.split("\n") if line.strip()]

            tech[tech_name] = {
                "consumed": consumed,
                "produced": produced,
                "params": params,
                "equations": equations,
            }

        return {
            "meta": {"name": self._label.text()},
            "tech": tech,
        }

    @QtCore.Slot()
    def _on_save_clicked(self) -> None:
        data = self.to_dict()
        jstr = json.dumps(data)
        self._logger.info(f"Saving node config: {jstr}")
        self.sig_save.emit(jstr)

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
