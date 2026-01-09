# Encoding: utf-8
# Filename: collapsible.py
# Description: A collapsible section widget for the Climate Action Tool

# Imports (standard)
from __future__ import annotations

# Imports (third party)
from PySide6 import QtCore, QtWidgets
from qtawesome import icon as qta_icon


# Class CollapsibleSection
class CollapsibleSection(QtWidgets.QWidget):
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
        expanded: bool = True,
    ):
        super().__init__(parent)

        # Attribute(s):
        self._expanded = expanded # The expanded state of the collapsible section
        self._title = title # The displayed title

        # Initialize UI components:
        self._init_ui()

    def _init_ui(self) -> None:
        """
        Invoked by the class's constructor.

        :return: None
        """

        # Import custom layout:
        from gui.widgets.layouts import VLayout

        # Main layout:
        layout = VLayout(self)

        # Header button:
        self._header = QtWidgets.QToolButton(self)
        self._header.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self._header.setIcon(self._get_arrow_icon(self._expanded))
        self._header.setText(self._title)
        self._header.setCheckable(True)
        self._header.setChecked(self._expanded)
        self._header.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self._header.setStyleSheet(
            """
            QToolButton {
                border: none;
                padding: 4px 8px;
                font-weight: bold;
                text-align: left;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.05);
            }
            """
        )
        self._header.clicked.connect(self._on_toggle)

        # Content container:
        self._content = QtWidgets.QWidget(self)
        self._content.setVisible(self._expanded)
        self._content_layout = QtWidgets.QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(8, 4, 8, 8)
        self._content_layout.setSpacing(4)

        layout.addWidget(self._header)
        layout.addWidget(self._content)

    @staticmethod
    def _get_arrow_icon(expanded: bool):
        icon_name = "mdi.chevron-down" if expanded else "mdi.chevron-right"
        return qta_icon(icon_name, color="gray", scale_factor=1.0)

    def _on_toggle(self, checked: bool):
        self._expanded = checked
        self._header.setIcon(self._get_arrow_icon(checked))
        self._content.setVisible(checked)
        self.toggled.emit(checked)

    def set_content_layout(self, layout: QtWidgets.QLayout):
        """
        Set a custom layout for the content area.
        """

        # Clear the existing layout:
        old_layout = self._content.layout()
        if old_layout:
            QtWidgets.QWidget().setLayout(old_layout)

        self._content.setLayout(layout)
        self._content_layout = layout

    def add_widget(self, widget: QtWidgets.QWidget):
        """Add a widget to the content area."""
        self._content_layout.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout):
        self._content_layout.addLayout(layout)

    def is_expanded(self) -> bool:
        return self._expanded

    def set_expanded(self, expanded: bool):
        if self._expanded != expanded:
            self._header.setChecked(expanded)
            self._on_toggle(expanded)

    def title(self) -> str:
        return self._title

    def set_title(self, title: str):
        self._title = title
        self._header.setText(title)