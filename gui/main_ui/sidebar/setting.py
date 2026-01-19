# Filename: setting.py
# Module name: setting
# Description: Settings/preferences widget for the sidebar.

"""
Settings and preferences panel for the sidebar.

Provides a form-based interface for configuring application settings including
project name, version, description, and epoch parameters.
"""

from __future__ import annotations

from PySide6 import QtCore
from PySide6 import QtWidgets

from gui.widgets.layouts import HLayout


class Preferences(QtWidgets.QWidget):
    """
    Settings and preferences panel widget.

    Displays a form with fields for project configuration and epoch settings,
    with apply and reset buttons for managing changes.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._init_buttons()

        # Set up form fields
        name_edit = QtWidgets.QLineEdit(self)
        text_edit = QtWidgets.QTextEdit()
        combo_box = QtWidgets.QComboBox()
        spin_start = QtWidgets.QSpinBox()
        spin_final = QtWidgets.QSpinBox()

        # Configure form layout
        self._form = QtWidgets.QFormLayout(self)
        self._form.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        self._form.setContentsMargins(4, 0, 0, 4)
        self._form.setSpacing(2)

        # Add form rows
        self._form.addRow("Project:", name_edit)
        self._form.addRow("Version:", combo_box)
        self._form.addRow("Description:", text_edit)
        self._form.addRow("Start Epoch:", spin_start)
        self._form.addRow("Final Epoch:", spin_final)

        # Configure widget values
        text_edit.setMaximumHeight(160)
        spin_start.setRange(-100, 100)
        spin_final.setRange(-100, 100)
        spin_final.setValue(50)

    def _init_buttons(self) -> None:
        """Initialize the settings control buttons (Apply, Reset)."""

        self._buttons = HLayout(None, spacing=4)
        self._buttons.addStretch(10)
        self._buttons.addWidget(
            reset := QtWidgets.QPushButton("Reset"),
            0,
            QtCore.Qt.AlignmentFlag.AlignRight,
        )
        self._buttons.addWidget(
            apply := QtWidgets.QPushButton("Apply"),
            0,
            QtCore.Qt.AlignmentFlag.AlignRight,
        )

        reset.setObjectName("Reset Button")
        apply.setObjectName("Apply Button")
        apply.pressed.connect(self._on_save_settings)

    def _on_save_settings(self) -> None:
        """Handle the apply button click to save settings."""

        apply = self.findChild(QtWidgets.QPushButton, "Apply Button")
        apply.setText("Apply")

    def _on_settings_changed(self) -> None:
        """Handle changes to any settings field."""

        apply = self.findChild(QtWidgets.QPushButton, "Apply Button")
        apply.setText("Apply")
