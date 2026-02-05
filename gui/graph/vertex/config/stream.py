# Filename: stream.py
# Module name: config
# Description: QToolBox-based widget for managing streams (one section per flow).


# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

from core.flow.basic import Flow
from gui.widgets.combobox import ComboBox


class Stream(QtWidgets.QToolBox):
    """
    A toolbox where each section represents a single flow/stream.

    Adding a flow creates a collapsible section containing:
        - Name, Symbol, Minimum fields
        - Primary attribute unit selector
        - Per-parameter unit selectors
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def add_flow(self, flow, name: str = "", symbol: str = "") -> int:
        """
        Add a new section for the given flow.

        Args:
            flow: A Flow instance.
            name: Custom label for the stream.
            symbol: Symbol for this stream.

        Returns:
            The index of the newly added section.
        """

        # -- Section content --
        page = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(page)

        name_edit = QtWidgets.QLineEdit(name or flow.label)
        symbol_edit = QtWidgets.QLineEdit(symbol)
        min_edit = QtWidgets.QLineEdit()
        max_edit = QtWidgets.QLineEdit()
        min_edit.setPlaceholderText("<")
        max_edit.setPlaceholderText(">")

        extrema_row = QtWidgets.QHBoxLayout()
        extrema_row.addWidget(min_edit)
        extrema_row.addWidget(max_edit)

        form.addRow("Name:", name_edit)
        form.addRow("Symbol:", symbol_edit)
        form.addRow("Extrema:", extrema_row)

        # Primary attribute (units from base flow class)
        primary_value = QtWidgets.QLineEdit("0.0")
        primary_combo = ComboBox(items=flow.units)
        primary_row = QtWidgets.QHBoxLayout()
        primary_row.addWidget(primary_value)
        primary_row.addWidget(primary_combo)
        form.addRow("Quantity:", primary_row)

        # Parameter value + units
        for key, param in flow.props.items():
            value = QtWidgets.QLineEdit("0.0")
            combo = ComboBox(items=param.units)
            row = QtWidgets.QHBoxLayout()
            row.addWidget(value)
            row.addWidget(combo)
            form.addRow(f"{param.label}:", row)

        return self.addItem(page, flow.image, flow.label)
