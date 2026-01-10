# Encoding: utf-8
# Filename: collapsible.py
# Description: A collapsible section widget for the Climate Action Tool

# Imports (compatibility):
from __future__ import annotations

# Imports (third party)
from PySide6 import QtCore, QtWidgets
from qtawesome import icon as qta_icon

# Imports (local):
from gui.widgets import HLayout, VLayout


# Class CollapsibleSection:
class CollapsibleSection(QtWidgets.QFrame):
    """
    A collapsible section with a clickable header and expandable content.
    """

    # Signal emitted when the section is toggled:
    toggled = QtCore.Signal(bool)

    # Initializer:
    def __init__(
        self,
        title: str,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)

        # Store section title:
        self._title = title

        # Instantiate UI components:
        layout = VLayout(self, spacing=0)

        # Initialize header:
        header = self._init_header(self._title)

        widget = QtWidgets.QFrame()
        layout.addWidget(header)
        layout.addWidget(widget)

    # Header initializer:
    def _init_header(self, title: str) -> QtWidgets.QToolButton:
        header = QtWidgets.QToolButton(
            self,
            autoRaise=True,
            toolButtonStyle=QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
        )

        header.setText(title)
        header.setIcon(
            qta_icon(
                "fa5s.chevron-right",
                color="#f5f5f5",
                selected="fa5s.chevron-down",
                scale_factor=0.75,
            )
        )
        return header
