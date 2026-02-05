# Filename: stream.py
# Module name: config
# Description: StreamTree-based widget for managing streams (one collapsible item per flow).


# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


from gui.widgets.combobox import ComboBox
from gui.widgets.layouts import VLayout
from gui.graph.vertex.tree import StreamTree


class Stream(StreamTree):
    """
    A tree widget where each top-level item represents a single flow/stream.

    Adding a flow creates a collapsible item containing:
        - Name, Symbol, Extrema, Quantity fields
        - Per-parameter unit selectors
        - Time evolution controls
        - Delete button
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def add_flow(self, flow, name: str = "", symbol: str = "") -> QtWidgets.QTreeWidgetItem:
        """
        Add a new collapsible item for the given flow.

        Args:
            flow: A Flow instance.
            name: Custom label for the stream.
            symbol: Symbol for this stream.

        Returns:
            The top-level QTreeWidgetItem.
        """

        container = QtWidgets.QFrame()
        p_form = self._init_primary_form(flow, name)
        s_form = self._init_secondary_form(flow)
        t_form = self._init_temporal_form()
        delete = self._init_delete_button()

        fixed_width = 400
        p_form.setFixedWidth(fixed_width)
        s_form.setFixedWidth(fixed_width)
        t_form.setFixedWidth(fixed_width)

        alignment = QtCore.Qt.AlignmentFlag.AlignHCenter
        layout = VLayout(container, spacing=12)
        layout.addWidget(p_form, alignment=alignment)
        layout.addWidget(s_form, alignment=alignment)
        layout.addWidget(t_form, alignment=alignment)
        layout.addWidget(delete, alignment=alignment)
        layout.addStretch(1)

        item = self.add_item(flow.image, flow.label, container)
        delete.clicked.connect(lambda: self._remove_flow(item))

        return item

    def _remove_flow(self, item: QtWidgets.QTreeWidgetItem) -> None:
        """Remove a flow item from the tree."""
        self.remove_item(item)

    def paintEvent(self, event):
        """Draw placeholder text when no flows have been added."""

        if self.topLevelItemCount() == 0:
            painter = QtGui.QPainter(self.viewport())
            painter.setOpacity(0.5)
            icon = QtGui.QIcon(":/png/empty.png")
            icon.paint(painter, self.viewport().rect())

            painter.setPen(QtGui.QColor("gray"))
            painter.drawText(
                self.viewport().rect(),
                QtCore.Qt.AlignmentFlag.AlignCenter,
                "Use the toolbar to add flows",
            )
            painter.end()
        else:
            super().paintEvent(event)

    @staticmethod
    def _init_primary_form(flow, name: str) -> QtWidgets.QGroupBox:
        """Create the Primary Attributes group box."""

        group = QtWidgets.QGroupBox("Primary Attributes")
        form = QtWidgets.QFormLayout(
            group,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        form.setContentsMargins(8, 8, 8, 8)

        name_edit = QtWidgets.QLineEdit(name or flow.label)
        symb_edit = QtWidgets.QLineEdit(flow.label.lower(), readOnly=True)

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
        primary_combo = ComboBox(items=flow.units)
        primary_row = QtWidgets.QHBoxLayout()
        primary_row.addWidget(primary_value)
        primary_row.addWidget(primary_combo)

        form.addRow("Name:", name_edit)
        form.addRow("Symbol:", symb_edit)
        form.addRow("Extrema:", extrema_row)
        form.addRow("Quantity:", primary_row)

        return group

    @staticmethod
    def _init_secondary_form(flow) -> QtWidgets.QGroupBox:
        """Create the Secondary Attributes group box."""

        group = QtWidgets.QGroupBox("Secondary Attributes")
        form = QtWidgets.QFormLayout(
            group,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        form.setContentsMargins(8, 8, 8, 8)

        for key, param in flow.props.items():
            value = QtWidgets.QLineEdit(placeholderText="e.g. 4")
            combo = ComboBox(items=param.units)
            row = QtWidgets.QHBoxLayout()
            row.addWidget(value)
            row.addWidget(combo)
            form.addRow(f"{param.label}:", row)

        return group

    @staticmethod
    def _init_temporal_form() -> QtWidgets.QGroupBox:
        """Create the Time Evolution group box."""

        group = QtWidgets.QGroupBox("Time Evolution")
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

        coeff_s = QtWidgets.QLineEdit(placeholderText="volatility")
        coeff_a = QtWidgets.QLineEdit(placeholderText="slope / amplitude")
        coeff_b = QtWidgets.QLineEdit(placeholderText="intercept / rate")
        coeff_c = QtWidgets.QLineEdit(placeholderText="offset")

        form.addRow("Mode:", mode_combo)
        form.addRow("\u03c3:", coeff_s)
        form.addRow("a:", coeff_a)
        form.addRow("b:", coeff_b)
        form.addRow("c:", coeff_c)

        all_fields = [coeff_s, coeff_a, coeff_b, coeff_c]
        mode_fields = {
            "Constant": [],
            "Linear": [coeff_a, coeff_b],
            "Exponential": [coeff_a, coeff_b, coeff_c],
            "Linear-Markov": [coeff_s, coeff_a, coeff_b],
        }

        def on_mode_changed(text):
            visible = mode_fields.get(text, [])
            for field in all_fields:
                form.setRowVisible(field, field in visible)

        mode_combo.currentTextChanged.connect(on_mode_changed)
        on_mode_changed("Constant")

        return group

    @staticmethod
    def _init_delete_button() -> QtWidgets.QPushButton:

        delete = QtWidgets.QPushButton("Delete")
        delete.setStyleSheet("background: #FF5F57; color: white;")
        return delete
