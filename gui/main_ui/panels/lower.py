# Filename: lower.py
# Module name: panels
# Description: Lower panel to be shown within a dock

"""
Lower panel widget containing the FlowHub.

Displays available stream/flow types for use in the graph editor.
"""

# Pyside6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass


# Climact
from qtawesome import icon as qta_icon
from core.flows import ResourceDictionary


class LowerPanel(QtWidgets.QListWidget):
    """Lower panel containing the FlowHub widget."""

    @dataclass
    class Style:
        border: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x40474D),
                "width": 1.0,
            }
        )

        background: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x40474D),
                "brush": QtCore.Qt.BrushStyle.SolidPattern,
            }
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        # Instantiate dataclasses
        self._style = LowerPanel.Style()

        # Built-in streams
        self._first_header = self._create_first_header_item()
        self.add_items(ResourceDictionary)

        # User-defined
        self._second_header = self._create_second_header_item()

    def _execute(self):
        pass

    def _create_first_header_item(self):

        icon = qta_icon("ph.list-fill", color="white")
        header_item = QtWidgets.QListWidgetItem(icon, "Built-in Resources", self)
        header_item.setFlags(header_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        header_item.setFlags(header_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        header_item.setSizeHint(QtCore.QSize(0, 28))

        return header_item

    def _create_second_header_item(self):

        # Required
        from gui.widgets.toolbar import ToolBar

        icon = qta_icon("ph.list-fill", color="white")
        header_item = QtWidgets.QListWidgetItem(icon, "Custom Resources", self)
        header_item.setFlags(header_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        header_item.setFlags(header_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        header_item.setSizeHint(QtCore.QSize(0, 28))

        toolbar = ToolBar(
            self,
            trailing=True,
            actions=[
                (
                    qta_icon("mdi.minus", color="gray", active_color="white"),
                    "Delete",
                    self._execute,
                ),
                (
                    qta_icon("mdi.plus", color="gray", active_color="white"),
                    "Add",
                    self._execute,
                ),
            ],
        )

        self.setItemWidget(header_item, toolbar)
        return header_item

    def add_items(self, flows: dict, editable=False, selectable=False):

        # Add flows
        for flow, _class in flows.items():

            item = QtWidgets.QListWidgetItem(
                _class.Attrs.image, _class.Attrs.label, self
            )
            item.setSizeHint(QtCore.QSize(0, 28))

            if not editable:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            if not selectable:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)

    def paintEvent(self, event):

        painter = QtGui.QPainter(self.viewport())
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        first_section_bl = self.visualItemRect(self._first_header).bottomLeft()
        first_section_br = self.visualItemRect(self._first_header).bottomRight()
        second_section_tl = self.visualItemRect(self._second_header).topLeft()
        second_section_tr = self.visualItemRect(self._second_header).topRight()

        separator_pen = QtGui.QPen(QtGui.QColor(0xFFFFFF), 1.0)
        painter.setPen(separator_pen)
        painter.drawLine(first_section_bl, first_section_br)
        painter.drawLine(second_section_tl, second_section_tr)
        painter.end()

        super().paintEvent(event)
