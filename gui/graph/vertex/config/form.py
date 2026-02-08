# Filename: form.py
# Module name: config
# Description: Stream configuration widget with primary attributes and secondary properties table.

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets.combobox import ComboBox
from gui.widgets.layouts import GLayout

import qtawesome as qta

# Secondary table column indices
COL_NAME = 0
COL_UNIT = 1
COL_CONSTANT = 2
COL_SLOPE = 3
COL_INTERCEPT = 4
COL_VOLATILITY = 5
SECONDARY_HEADERS = ["Name", "Unit", "Constant", "Slope", "Intercept", "Volatility"]


class StreamForm(QtWidgets.QFrame):
    """Form for configuring a single stream."""

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setStyleSheet("QFrame {border-radius: 4px; background: #40474d;}")

        # Customize appearance and behaviour:
        self.setMinimumWidth(420)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )

        # Reference(s)
        self._item = None
        self._flow = None

        # UI components
        self._cat_form = self._init_categorical_form()
        self._num_form = self._init_numerical_form()
        self._sec_form = self._init_secondary_table()

        # Save button
        self._save_btn = QtWidgets.QPushButton(
            qta.icon("mdi.content-save", color="#efefef"), "Save"
        )
        self._save_btn.clicked.connect(self._on_save)

        layout = GLayout(self, margins=(4, 4, 4, 4), spacing=4)
        layout.addWidget(self._cat_form, 0, 0)
        layout.addWidget(self._num_form, 0, 1)
        layout.addWidget(self._sec_form, 1, 0, 1, 2)
        layout.addWidget(self._save_btn, 2, 0, 1, 2)

    def set_item(self, item: QtWidgets.QTreeWidgetItem):
        """Associate this form with a tree item."""
        self._item = item

    def configure_flow(self, flow):
        """Populate form fields with flow data."""
        self._flow = flow
        if not flow:
            return

        # Primary — set the type label and available units
        self._type_label.setText(flow.label)
        self._unit_combo.clear()
        self._unit_combo.addItems(flow.units)

        # Secondary — populate table with flow's props
        self._table.setRowCount(0)
        for key, param in flow.props.items():
            row = self._table.rowCount()
            self._table.insertRow(row)

            # Name (read-only)
            name_item = QtWidgets.QTableWidgetItem(param.label)
            name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self._table.setItem(row, COL_NAME, name_item)

            # Unit combo
            unit_combo = ComboBox(items=param.units)
            self._table.setCellWidget(row, COL_UNIT, unit_combo)

            # Coefficient columns (editable, default "0.0")
            for col in (COL_CONSTANT, COL_SLOPE, COL_INTERCEPT, COL_VOLATILITY):
                self._table.setItem(row, col, QtWidgets.QTableWidgetItem("0.0"))

    @QtCore.Slot()
    def _on_save(self):
        """Push form data back to the associated QTreeWidgetItem."""
        if not self._item:
            return

        name = self._name_edit.text().strip()
        if name:
            self._item.setText(0, name)
            self._item.setIcon(0, qta.icon("ph.check-circle-fill", color="#5eb616"))

            quantity = "Variable" if self._var_radio.isChecked() else "Fixed"
            self._item.setText(1, f"{quantity} ({self._type_label.text()})")

    def _init_categorical_form(self) -> QtWidgets.QGroupBox:
        """Create the Categorical group box (Type, Name, Symbol, Unit)."""

        group = QtWidgets.QGroupBox("Categorical")
        form = QtWidgets.QFormLayout(
            group,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        form.setContentsMargins(8, 8, 8, 8)

        self._type_label = QtWidgets.QLabel("—")
        self._name_edit = QtWidgets.QLineEdit()
        self._symb_edit = QtWidgets.QLineEdit(readOnly=True)
        self._unit_combo = ComboBox()

        self._name_edit.textChanged.connect(
            lambda text: self._symb_edit.setText("_".join(text.strip().lower().split()))
        )

        form.addRow("Type:", self._type_label)
        form.addRow("Name:", self._name_edit)
        form.addRow("Symbol:", self._symb_edit)
        form.addRow("Unit:", self._unit_combo)

        return group

    def _init_numerical_form(self) -> QtWidgets.QGroupBox:
        """Create the Numerical group box (Quantity toggle + Fixed/Variable fields)."""

        group = QtWidgets.QGroupBox("Numerical")
        self._n_layout = QtWidgets.QFormLayout(
            group,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        self._n_layout.setContentsMargins(8, 8, 8, 8)

        # Quantity: Variable or Fixed
        self._var_radio = QtWidgets.QRadioButton("Variable")
        self._fixed_radio = QtWidgets.QRadioButton("Fixed")
        self._var_radio.setChecked(True)
        quantity_row = QtWidgets.QHBoxLayout()
        quantity_row.addWidget(self._var_radio)
        quantity_row.addWidget(self._fixed_radio)

        # Fixed fields: temporal coefficients
        self._constant_edit = QtWidgets.QLineEdit(placeholderText="0.0")
        self._slope_edit = QtWidgets.QLineEdit(placeholderText="0.0")

        # Variable fields: bounds + initial guess
        self._min_edit = QtWidgets.QLineEdit(placeholderText="0.0")
        self._max_edit = QtWidgets.QLineEdit(placeholderText="100.0")

        self._n_layout.addRow("Quantity:", quantity_row)
        self._n_layout.addRow("Constant:", self._constant_edit)
        self._n_layout.addRow("Slope:", self._slope_edit)
        self._n_layout.addRow("Min:", self._min_edit)
        self._n_layout.addRow("Max:", self._max_edit)
        self._n_layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Toggle visibility based on radio selection
        self._fixed_radio.toggled.connect(self._on_quantity_toggled)
        self._on_quantity_toggled(False)

        return group

    @QtCore.Slot(bool)
    def _on_quantity_toggled(self, fixed: bool):

        for w in (self._constant_edit, self._slope_edit):
            self._n_layout.setRowVisible(w, fixed)

        for w in (self._min_edit, self._max_edit):
            self._n_layout.setRowVisible(w, not fixed)

    def _init_secondary_table(self) -> QtWidgets.QGroupBox:

        group = QtWidgets.QGroupBox("Secondary")
        layout = QtWidgets.QVBoxLayout(group)
        layout.setContentsMargins(4, 4, 4, 4)

        self._table = QtWidgets.QTableWidget(0, len(SECONDARY_HEADERS))
        self._table.setHorizontalHeaderLabels(SECONDARY_HEADERS)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.verticalHeader().setVisible(False)
        self._table.setAlternatingRowColors(True)

        layout.addWidget(self._table)
        return group
