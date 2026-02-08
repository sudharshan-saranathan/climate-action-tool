# Filename: form.py
# Module name: config
# Description: Stream configuration widget with primary attributes and secondary properties table.

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets import ToolBar
from gui.widgets import GLayout
from gui.widgets import ComboBox

import qtawesome as qta

# Secondary table column indices
COL_NAME = 0
COL_UNIT = 1
COL_VALUE = 2
COL_PROFILE = 3
COL_ACTIONS = 4
SECONDARY_HEADERS = ["Name", "Unit", "Value", "Profile", "Actions"]


class StreamForm(QtWidgets.QFrame):
    """Form for configuring a single stream."""

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setStyleSheet("QFrame {border-radius: 4px; background: #40474d;}")

        # Customize appearance and behaviour:
        self.setMinimumHeight(360)

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
        self._save_btn.setMaximumWidth(100)
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

            # Value field: show value_at(0.0) from profile
            value_edit = QtWidgets.QLineEdit()
            value_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            try:
                current_value = param.value_at(0.0)
                value_edit.setText(str(current_value))
            except:
                value_edit.setText("0.0")
            self._table.setCellWidget(row, COL_VALUE, value_edit)

            # Profile type combo and edit button: ONLY for variable parameters
            is_variable = getattr(
                param, "is_variable", True
            )  # Default to True for backwards compat

            if is_variable:
                # Profile type combo: show profile type from parameter
                profile_type = "Fixed"
                try:
                    if hasattr(param, "profile_ref") and param.profile_ref:
                        profile_class_name = (
                            param.profile_ref.profile.__class__.__name__
                        )
                        if "Linear" in profile_class_name:
                            profile_type = "Linear"
                        elif "Stepped" in profile_class_name:
                            profile_type = "Stepped"
                except:
                    pass

                profile_combo = ComboBox(items=["Fixed", "Linear", "Stepped"])
                profile_combo.setCurrentText(profile_type)
                self._table.setCellWidget(row, COL_PROFILE, profile_combo)

                # Actions: Edit and Delete buttons (for variable params)
                actions = ToolBar(
                    self,
                    trailing=True,
                    actions=[
                        (
                            qta.icon("mdi.pencil", color="#4da6ff"),
                            "Edit",
                            lambda _, r=row, p=param, k=key: self._on_edit_profile(
                                k, p
                            ),
                        ),
                        (
                            qta.icon("mdi.delete", color="red"),
                            "Delete",
                            lambda _, r=self._table, i=row: r.removeRow(i),
                        ),
                    ],
                )
            else:
                # Fixed parameter: show "Fixed" label, no editing
                fixed_label = QtWidgets.QLabel("Fixed")
                fixed_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self._table.setCellWidget(row, COL_PROFILE, fixed_label)

                # No actions for fixed parameters
                actions = ToolBar(self, trailing=True, actions=[])

            self._table.setCellWidget(row, COL_ACTIONS, actions)

    @QtCore.Slot(str, object)
    def _on_edit_profile(self, param_key: str, param):
        """Open a dialog to edit the parameter's profile.

        Args:
            param_key: Key of the parameter in props
            param: The Parameter instance to edit
        """
        # Create profile editor dialog
        dialog = ProfileEditorDialog(param, parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # Profile was updated in-place
            pass

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

        # Customize header
        header = self._table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self._table.horizontalHeader().setStretchLastSection(False)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)

        layout.addWidget(self._table)
        return group


class ProfileEditorDialog(QtWidgets.QDialog):
    """Dialog for editing parameter profile time points and values."""

    def __init__(self, param, parent=None):
        """Initialize profile editor dialog.

        Args:
            param: Parameter instance with profile_ref
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(f"Edit {param.label} Profile")
        self.setMinimumSize(500, 300)

        self._param = param
        self._profile_ref = param.profile_ref

        # Main layout
        layout = QtWidgets.QVBoxLayout(self)

        # Profile type selector
        type_layout = QtWidgets.QHBoxLayout()
        type_layout.addWidget(QtWidgets.QLabel("Profile Type:"))
        self._type_combo = ComboBox(items=["Fixed", "Linear", "Stepped"])
        try:
            profile_class_name = self._profile_ref.profile.__class__.__name__
            if "Linear" in profile_class_name:
                self._type_combo.setCurrentText("Linear")
            elif "Stepped" in profile_class_name:
                self._type_combo.setCurrentText("Stepped")
        except:
            pass
        type_layout.addWidget(self._type_combo)
        type_layout.addStretch()
        layout.addLayout(type_layout)

        # Time points and values table
        self._table = QtWidgets.QTableWidget(0, 2)
        self._table.setHorizontalHeaderLabels(["Time", "Value"])
        self._table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self._table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        # Populate from current profile
        self._populate_from_profile()

        layout.addWidget(QtWidgets.QLabel("Time Points & Values:"))
        layout.addWidget(self._table)

        # Add/Remove row buttons
        button_layout = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Add Row")
        add_btn.clicked.connect(self._add_row)
        remove_btn = QtWidgets.QPushButton("Remove Row")
        remove_btn.clicked.connect(self._remove_row)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(remove_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # OK/Cancel buttons
        dialog_buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        layout.addWidget(dialog_buttons)

    def _populate_from_profile(self):
        """Populate table from current profile."""
        try:
            profile = self._profile_ref.profile
            if hasattr(profile, "time_points"):
                self._table.setRowCount(len(profile.time_points))
                for i, (t, v) in enumerate(zip(profile.time_points, profile.values)):
                    t_item = QtWidgets.QTableWidgetItem(str(t))
                    v_item = QtWidgets.QTableWidgetItem(str(v))
                    self._table.setItem(i, 0, t_item)
                    self._table.setItem(i, 1, v_item)
            else:
                # Fixed profile
                self._table.setRowCount(1)
                self._table.setItem(0, 0, QtWidgets.QTableWidgetItem("0"))
                self._table.setItem(
                    0, 1, QtWidgets.QTableWidgetItem(str(profile.value))
                )
        except Exception:
            # Default: one row with 0, 0
            self._table.setRowCount(1)
            self._table.setItem(0, 0, QtWidgets.QTableWidgetItem("0"))
            self._table.setItem(0, 1, QtWidgets.QTableWidgetItem("0"))

    def _add_row(self):
        """Add a new row to the table."""
        row = self._table.rowCount()
        self._table.insertRow(row)
        self._table.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
        self._table.setItem(row, 1, QtWidgets.QTableWidgetItem(""))

    def _remove_row(self):
        """Remove the selected row from the table."""
        current_row = self._table.currentRow()
        if current_row >= 0:
            self._table.removeRow(current_row)

    def accept(self):
        """Update the parameter's profile and close dialog."""
        try:
            from core.flow.profiles import FixedProfile, LinearProfile, SteppedProfile

            profile_type = self._type_combo.currentText()
            time_points = []
            values = []

            for row in range(self._table.rowCount()):
                t_item = self._table.item(row, 0)
                v_item = self._table.item(row, 1)
                if t_item and v_item and t_item.text() and v_item.text():
                    try:
                        time_points.append(float(t_item.text()))
                        values.append(float(v_item.text()))
                    except ValueError:
                        continue

            if profile_type == "Fixed":
                if values:
                    profile = FixedProfile(values[0])
                else:
                    profile = FixedProfile(0.0)
            elif profile_type == "Linear":
                if len(time_points) >= 2:
                    profile = LinearProfile(time_points, values)
                else:
                    profile = FixedProfile(values[0] if values else 0.0)
            elif profile_type == "Stepped":
                if time_points:
                    profile = SteppedProfile(time_points, values)
                else:
                    profile = FixedProfile(values[0] if values else 0.0)
            else:
                profile = FixedProfile(0.0)

            # Update parameter's profile_ref
            self._profile_ref.profile = profile

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Failed to update profile: {e}"
            )
            return

        super().accept()
