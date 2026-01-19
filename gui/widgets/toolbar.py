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
        """
        Toolbar configuration options.

        Attributes:
            iconSize: QSize for toolbar icons (default: 16x16).
            floatable: Whether toolbar can float as a separate window (default: False).
            trailing: Position actions after spacer (True) or before (False) (default: True).
            movable: Whether toolbar can be repositioned (default: False).
            orientation: Toolbar orientation - Horizontal or Vertical (default: Horizontal).
            toolButtonStyle: Button display style - IconOnly, TextOnly, or TextBesideIcon (default: IconOnly).
        """
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
        actions = kwargs.get("actions", [])

        # Create expanding spacer widget for alignment
        spacer = QtWidgets.QFrame()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        # Add spacer and actions in order based on trailing flag
        if self._opts.trailing:
            self.addWidget(spacer)
            self.add_actions(actions)
        else:
            self.add_actions(actions)
            self.addWidget(spacer)

        self.setStyleSheet(style)

    def add_actions(self, actions: list) -> None:
        """
        Add actions to the toolbar.

        Each action is created from a tuple of (icon, label, callback).
        Any malformed tuples are silently skipped with an error message.

        Args:
            actions: List of (icon, label, callback) tuples where:
                - icon: QIcon object for the action
                - label: Text label for the action
                - callback: Callable invoked when action is triggered
        """
        try:
            for icon, label, callback in actions:
                self.addAction(icon, label, callback)
        except (RuntimeError, IndexError, ValueError) as e:
            print(f"Error adding actions to toolbar: {e}")
