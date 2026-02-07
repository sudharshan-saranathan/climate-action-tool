# Filename: form.py
# Module name: config
# Description: Stream configuration widget with category tree and form panel.

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets.combobox import ComboBox
from gui.widgets.layouts import VLayout


class StreamForm(QtWidgets.QFrame):
    """Dialog for configuring a single stream."""

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setStyleSheet("QFrame {border-radius: 4px; background: #40474d;}")

        # Customize appearance and behaviour:
        self.setMinimumWidth(320)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )

        # Reference(s)
        self._item = None
        self._flow = None

        # UI components
        self._p_form = self._init_primary_form()
        self._s_form = self._init_secondary_form()
        self._t_form = self._init_temporal_form()

        VLayout(
            self,
            margins=(0, 12, 0, 12),
            spacing=4,
            widgets=[self._p_form, self._s_form, self._t_form],
        )

    def configure_item(self, item: QtWidgets.QTreeWidgetItem):
        """Configure this form with a flow instance from the tree item."""
        self._item = item
        self._flow = item.data(0, QtCore.Qt.ItemDataRole.UserRole)

        self.setWindowTitle(f"Configure: {item.text(0)}")
        self.configure_flow(self._flow)

    def configure_flow(self, flow):
        """Populate form fields with flow data."""
        if not flow:
            return

        # Secondary form — clear and repopulate with flow's props
        secondary_group = self._s_form
        secondary_layout = secondary_group.layout()
        if isinstance(secondary_layout, QtWidgets.QFormLayout):
            # Remove all rows
            while secondary_layout.rowCount() > 0:
                secondary_layout.removeRow(0)

            # Add rows for flow's props
            for key, param in flow.props.items():
                value_edit = QtWidgets.QLineEdit(placeholderText="0.0")
                unit_combo = ComboBox(items=param.units)
                row = QtWidgets.QHBoxLayout()
                row.addWidget(value_edit)
                row.addWidget(unit_combo)
                secondary_layout.addRow(f"{param.label}:", row)

    @staticmethod
    def _init_primary_form() -> QtWidgets.QGroupBox:
        """Create the Primary Attributes group box (empty)."""

        group = QtWidgets.QGroupBox("Primary")
        form = QtWidgets.QFormLayout(
            group,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        form.setContentsMargins(8, 8, 8, 8)

        name_edit = QtWidgets.QLineEdit()
        symb_edit = QtWidgets.QLineEdit(readOnly=True)

        name_edit.textChanged.connect(
            lambda text: symb_edit.setText("_".join(text.strip().lower().split()))
        )

        min_edit = QtWidgets.QLineEdit()
        max_edit = QtWidgets.QLineEdit()
        min_edit.setPlaceholderText("Min (e.g. 0)")
        max_edit.setPlaceholderText("Max (e.g. 100)")
        extrema_row = QtWidgets.QHBoxLayout()
        extrema_row.addWidget(min_edit)
        extrema_row.addWidget(max_edit)

        primary_value = QtWidgets.QLineEdit(placeholderText="e.g. 25")
        primary_combo = ComboBox()
        primary_row = QtWidgets.QHBoxLayout()
        primary_row.addWidget(primary_value)
        primary_row.addWidget(primary_combo)

        form.addRow("Name:", name_edit)
        form.addRow("Symbol:", symb_edit)
        form.addRow("Extrema:", extrema_row)
        form.addRow("Quantity:", primary_row)

        return group

    @staticmethod
    def _init_secondary_form() -> QtWidgets.QGroupBox:
        """Create the Secondary Attributes group box (empty)."""

        group = QtWidgets.QGroupBox("Secondary")
        form = QtWidgets.QFormLayout(
            group,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        form.setContentsMargins(8, 8, 8, 8)
        return group

    @staticmethod
    def _init_temporal_form() -> QtWidgets.QGroupBox:
        """Create the Time Evolution group box."""

        def on_mode_changed(text):
            visible = mode_fields.get(text, [])
            for field in all_fields:
                form.setRowVisible(field, field in visible)

        group = QtWidgets.QGroupBox("Temporal")
        form = QtWidgets.QFormLayout(
            group,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        form.setContentsMargins(8, 8, 8, 8)

        mode_combo = ComboBox(
            items=["Constant", "Linear", "Exponential", "Linear-Markov"]
        )

        cfs = QtWidgets.QLineEdit(placeholderText="volatility")
        cfa = QtWidgets.QLineEdit(placeholderText="slope / amplitude")
        cfb = QtWidgets.QLineEdit(placeholderText="intercept / rate")
        cfc = QtWidgets.QLineEdit(placeholderText="offset")

        form.addRow("Mode:", mode_combo)
        form.addRow("\u03c3:", cfs)
        form.addRow("a:", cfa)
        form.addRow("b:", cfb)
        form.addRow("c:", cfc)

        all_fields = [cfs, cfa, cfb, cfc]
        mode_fields = {
            "Constant": [],
            "Linear": [cfa, cfb],
            "Exponential": [cfa, cfb, cfc],
            "Linear-Markov": [cfs, cfa, cfb],
        }

        mode_combo.currentTextChanged.connect(on_mode_changed)
        on_mode_changed("Constant")

        return group
