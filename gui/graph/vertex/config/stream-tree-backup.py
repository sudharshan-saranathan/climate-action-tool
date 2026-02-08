# Filename: __init__.py
# Module Name: StreamTree
# Description: Stream tree widget for vertex configuration.

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact
import qtawesome as qta
from gui.widgets import ToolBar
from core.flow import ResourceDictionary, ParameterDictionary


class StreamTree(QtWidgets.QTreeWidget):

    def __init__(self, flow_classes: list, parent=None):
        super().__init__(parent, columnCount=3)

        # Customize appearance and behaviour
        self.setHeaderHidden(True)
        self.setStyleSheet("QTreeWidget::item { height: 20px; }")
        self.setColumnWidth(2, 60)
        self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.SingleSelection)

        # Customize header
        header = self.header()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self._init_top_level_items()

    def _init_top_level_items(self):

        self._iroot = QtWidgets.QTreeWidgetItem(self, ["Inputs"])
        self._oroot = QtWidgets.QTreeWidgetItem(self, ["Outputs"])
        self._param = QtWidgets.QTreeWidgetItem(self, ["Parameters"])

        inp_actions = self._create_toolbar(ResourceDictionary, self._iroot)
        out_actions = self._create_toolbar(ResourceDictionary, self._oroot)
        par_actions = self._create_toolbar(ParameterDictionary, self._param)

        inp_actions.setObjectName(self._iroot.text(0))
        out_actions.setObjectName(self._oroot.text(0))
        par_actions.setObjectName(self._param.text(0))

        self.setItemWidget(self._iroot, 2, inp_actions)
        self.setItemWidget(self._oroot, 2, out_actions)
        self.setItemWidget(self._param, 2, par_actions)

    def _create_toolbar(
        self,
        resources: dict[str, type],
        root_item: QtWidgets.QTreeWidgetItem,
    ):
        toolbar = ToolBar(self, trailing=True)
        for key, _class in resources.items():

            _label = _class.Attrs.label
            _image = _class.Attrs.image

            action = toolbar.addAction(_image, _label, self._on_item_created)
            action.setData(root_item)

        return toolbar

    @QtCore.Slot()
    def _on_item_created(self):

        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return

        root = action.data().text(0)
        name = action.text()

        self.create_item(root, name)

    @QtCore.Slot()
    def _on_item_deleted(
        self,
        root: QtWidgets.QTreeWidgetItem,
        item: QtWidgets.QTreeWidgetItem,
    ):
        root.removeChild(item)

    def create_item(self, section: str, label: str):

        root = self.findItems(section, QtCore.Qt.MatchFlag.MatchExactly)
        if not root or not isinstance(root[0], QtWidgets.QTreeWidgetItem):
            return

        root = root[0]
        root.setExpanded(True)

        dictionary = (
            ParameterDictionary if section == "Parameters" else ResourceDictionary
        )
        icon = dictionary[label.lower()].Attrs.image
        text = dictionary[label.lower()].Attrs.label

        item = QtWidgets.QTreeWidgetItem(root)
        item.setIcon(0, icon)
        item.setText(0, text)
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        actions = ToolBar(
            self,
            trailing=True,
            actions=[
                (
                    qta.icon("mdi.delete", color="red"),
                    "Delete",
                    lambda _, i=item: self._on_item_deleted(root, i),
                ),
            ],
        )

        self.setItemWidget(item, 2, actions)
