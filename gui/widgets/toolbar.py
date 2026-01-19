# Filename: toolbar.py
# Module name: widgets
# Description: Custom toolbar widget with action management.

"""
Custom toolbar with action handling and alignment.

Provides a QToolBar subclass with configurable actions, spacing options,
and support for custom styling.
"""

import dataclasses
from PySide6 import QtCore
from PySide6 import QtWidgets


class ToolBar(QtWidgets.QToolBar):
    """
    Custom toolbar with configurable actions and layout.

    Supports icon-based actions with optional text labels, customizable spacing,
    and trailing/leading action alignment relative to a spacer.
    """

    @dataclasses.dataclass(frozen=True)
    class Options:
        """Toolbar configuration options."""
        iconSize: QtCore.QSize = QtCore.QSize(16, 16)
        floatable: bool = False
        trailing: bool = True
        movable: bool = False
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal
        toolButtonStyle: QtCore.Qt.ToolButtonStyle = (
            QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly
        )

    def __init__(self, parent=None, **kwargs):
        """
        Initialize the toolbar with actions and styling.

        Args:
            parent: Parent widget (optional).
            **kwargs: Configuration options:
                - iconSize: QSize for toolbar icons (default: 16x16)
                - floatable: Whether toolbar can float (default: False)
                - trailing: Position actions after spacer (default: True)
                - movable: Whether toolbar can be moved (default: False)
                - orientation: Toolbar orientation (default: Horizontal)
                - toolButtonStyle: Button style (default: IconOnly)
                - style: Custom stylesheet (default: "")
                - actions: List of (icon, label, callback) tuples (default: [])
        """

        self._opts = ToolBar.Options(
            iconSize=kwargs.get("iconSize", QtCore.QSize(16, 16)),
            floatable=kwargs.get("floatable", False),
            trailing=kwargs.get("trailing", True),
            movable=kwargs.get("movable", False),
            orientation=kwargs.get("orientation", QtCore.Qt.Orientation.Horizontal),
            toolButtonStyle=kwargs.get(
                "toolButtonStyle", QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly
            ),
        )

        super().__init__(
            parent,
            movable=self._opts.movable,
            floatable=self._opts.floatable,
            orientation=self._opts.orientation,
            toolButtonStyle=self._opts.toolButtonStyle,
            iconSize=self._opts.iconSize,
        )

        style = kwargs.get("style", "")
        items = kwargs.get("actions", [])
        trail = kwargs.get("trailing", True)

        # Create spacer to align actions
        spacer = QtWidgets.QFrame()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        # Add spacer and actions in appropriate order
        if trail:
            self.addWidget(spacer)
            self.add_actions(items)
        else:
            self.add_actions(items)
            self.addWidget(spacer)

        self.setStyleSheet(style)

    def add_actions(self, actions: list) -> None:
        """
        Add actions to the toolbar.

        Args:
            actions: List of (icon, label, callback) tuples to add as toolbar actions.
        """

        try:
            for icon, label, callback in actions:
                self.addAction(icon, label, callback)
        except (RuntimeError, IndexError, ValueError) as e:
            print(f"Error adding actions to toolbar: {e}")
