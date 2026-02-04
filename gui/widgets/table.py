# Filename: table.py
# Module name: widgets
# Description: Custom table widget for managing data streams (inputs/outputs).


# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass
from qtawesome import icon as qta_icon

from gui.widgets.combobox import ComboBox
from gui.widgets.toolbar import ToolBar


class DataIOTable(QtWidgets.QTableWidget):
    """
    A custom table widget for managing data streams with comprehensive properties.

    Columns:
    1. Stream Type
    2. Custom Label
    3. Description
    4. Units (combo box)
    5. Minimum Value
    6. Value
    7. Maximum Value
    8. Time-Series (checkbox)
    9. Formula
    10. Actions (delete, edit)
    """

    sig_delete_stream = QtCore.Signal(int)  # Emitted when delete is clicked
    sig_edit_stream = QtCore.Signal(int)  # Emitted when edit is clicked

    @dataclass(frozen=True)
    class Attrs:
        """Configuration options for the data IO table.

        Attributes:
            row_height: Row height in pixels.
            columns: Table column labels.
        """

        selectionMode: QtWidgets.QTableWidget.SelectionMode = (
            QtWidgets.QTableWidget.SelectionMode.MultiSelection
        )

        selectionBehavior: QtWidgets.QTableWidget.SelectionBehavior = (
            QtWidgets.QTableWidget.SelectionBehavior.SelectRows
        )

        row_height: int = 24
        columns: list[str] = field(
            default_factory=lambda: [
                "Flow",
                "Unit",
                "Name",
                "Symbol",
                "Minimum",
                "Maximum",
                "Value",
                "Formula",
                "Actions",
            ]
        )

    def __init__(self, parent=None):
        """
        Initialize the data IO table widget.
        """

        # Instantiate dataclass
        self._attrs = DataIOTable.Attrs()

        # Initialize super class
        super().__init__(
            parent,
            columnCount=len(self._attrs.columns),
        )

        # Configure table appearance
        self.setShowGrid(False)
        self.setHorizontalHeaderLabels(self._attrs.columns)
        self.setSelectionBehavior(self._attrs.selectionBehavior)
        self.setSelectionMode(self._attrs.selectionMode)
        self.verticalHeader().setVisible(False)

        _fixed = QtWidgets.QHeaderView.ResizeMode.Fixed
        _resize = QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        _stretch = QtWidgets.QHeaderView.ResizeMode.Stretch

        # Configure column resizing
        header = self.horizontalHeader()
        header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(0, _fixed)  # Flow Type
        header.setSectionResizeMode(1, _fixed)  # Units
        header.setSectionResizeMode(2, _fixed)  # Name
        header.setSectionResizeMode(3, _fixed)  # Symbol
        header.setSectionResizeMode(4, _fixed)  # Minimum
        header.setSectionResizeMode(5, _fixed)  # Maximum
        header.setSectionResizeMode(6, _fixed)  # Value
        header.setSectionResizeMode(7, _fixed)  # Formula
        header.setSectionResizeMode(8, _stretch)

    def add_stream(
        self,
        flow: str = "",
        name: str = "",
        symbol: str = "",
        minimum: str = "",
        current: str = "",
        maximum: str = "",
        formula: str = "",
        units_list: list = None,
    ) -> int:
        """
        Add a new stream row to the table.

        Args:
            flow: Type of stream (e.g., flow class label).
            name: Custom label for the stream.
            symbol: Symbol of this input.
            minimum: Minimum value.
            current: Current value.
            maximum: Maximum value.
            formula: Formula or calculation.
            units_list: List of available units for this flow (overrides default units).

        Returns:
            The row index of the new stream.
        """

        row = self.rowCount()
        self.insertRow(row)
        self.setRowHeight(row, self._attrs.row_height)

        # 1. Flow Type (read-only text with icon)
        from core.flow import AllFlows

        flow_item = QtWidgets.QTableWidgetItem(flow)
        flow_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        flow_item.setFlags(flow_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

        # Set the flow icon
        for flow_class in AllFlows.values():
            if flow_class.LABEL == flow:
                icon = qta_icon(flow_class.ICON, color=flow_class.COLOR)
                flow_item.setIcon(icon)
                break

        self.setItem(row, 0, flow_item)

        # 4. Units (combo box)
        units_combo = ComboBox(items=units_list)
        self.setCellWidget(row, 1, units_combo)

        # 2. Custom Label (editable text)
        name_item = QtWidgets.QTableWidgetItem(name)
        name_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 2, name_item)

        # 3. Symbol (editable text)
        symb_item = QtWidgets.QTableWidgetItem(symbol)
        symb_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 3, symb_item)

        # 5. Minimum Value (editable text)
        min_item = QtWidgets.QTableWidgetItem(minimum)
        min_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 4, min_item)

        # 6. Value (editable text)
        val_item = QtWidgets.QTableWidgetItem(current)
        val_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 5, val_item)

        # 7. Maximum Value (editable text)
        max_item = QtWidgets.QTableWidgetItem(maximum)
        max_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 6, max_item)

        # 8. Formula (editable text)
        formula_item = QtWidgets.QTableWidgetItem(formula)
        formula_item.setTextAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.setItem(row, 7, formula_item)

        # 9. Actions (delete and edit buttons)
        style = """
        QToolBar {
            margin: 0px;
            padding: 0px;
        }
        
        QToolButton, QToolButton:hovered, QToolButton:selected {
            background: transparent;
            margin: 0px;
            padding: 0px;
        }
        """

        actions_toolbar = ToolBar(
            style=style,
            iconSize=QtCore.QSize(16, 16),
            actions=[
                (
                    qta_icon("ph.trend-up", color="orange", color_active="#ffcb00"),
                    "Plot",
                    lambda: print(f"Plotting entity"),
                ),
                (
                    qta_icon("mdi.pencil", color="darkcyan", color_active="cyan"),
                    "Edit",
                    lambda r=row: self.sig_edit_stream.emit(r),
                ),
                (
                    qta_icon("mdi.delete", color="darkred", color_active="red"),
                    "Delete",
                    lambda r=row: self.sig_delete_stream.emit(r),
                ),
            ],
        )
        self.setCellWidget(row, 8, actions_toolbar)

        return row

    def get_stream(self, row: int) -> dict:
        """
        Get stream data from a specific row.
        """

        if row < 0 or row >= self.rowCount():
            return {}

        stream_type = self.item(row, 0).text() if self.item(row, 0) else ""
        label = self.item(row, 1).text() if self.item(row, 1) else ""
        description = self.item(row, 2).text() if self.item(row, 2) else ""
        min_value = self.item(row, 4).text() if self.item(row, 4) else ""
        value = self.item(row, 5).text() if self.item(row, 5) else ""
        max_value = self.item(row, 6).text() if self.item(row, 6) else ""
        formula = self.item(row, 8).text() if self.item(row, 8) else ""

        # Get units from combo box
        units_widget = self.cellWidget(row, 3)
        units = ""
        if units_widget:
            combo = units_widget.findChild(QtWidgets.QComboBox)
            if combo:
                units = combo.currentText()

        # Get time-series checkbox state
        ts_widget = self.cellWidget(row, 7)
        time_series = False
        if ts_widget:
            checkbox = ts_widget.findChild(QtWidgets.QCheckBox)
            if checkbox:
                time_series = checkbox.isChecked()

        return {
            "stream_type": stream_type,
            "label": label,
            "description": description,
            "units": units,
            "min_value": min_value,
            "value": value,
            "max_value": max_value,
            "time_series": time_series,
            "formula": formula,
        }

    def remove_stream(self, row: int) -> None:
        """
        Remove a stream row from the table.

        Args:
            row: The row index to remove.
        """

        if 0 <= row < self.rowCount():
            self.removeRow(row)
