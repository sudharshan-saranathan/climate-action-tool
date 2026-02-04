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
from PySide6 import QtGui
from PySide6 import QtWidgets


class ToolBar(QtWidgets.QToolBar):
    """
    Custom toolbar with configurable actions and layout.

    Supports icon-based actions with optional text labels, customizable spacing,
    and trailing/leading action alignment relative to a spacer.
    """

    sig_action_triggered = QtCore.Signal(str)

    @dataclasses.dataclass(frozen=True)
    class Options:
        """
        Toolbar configuration options.

        Attributes:
            iconSize: QSize for toolbar icons (default: 16x16).
            floatable: Whether the toolbar can float as a separate window (default: False).
            trailing: Position actions after spacer (True) or before (False) (default: True).
            movable: Whether toolbar can be repositioned (default: False).
            orientation: Toolbar orientation - Horizontal or Vertical (default: Horizontal).
            toolButtonStyle: Button display style - IconOnly, TextOnly, or TextBesideIcon (default: IconOnly).
            enable_counting: Enable counter on actions for left/right click increment/decrement (default: False).
        """
        iconSize: QtCore.QSize = QtCore.QSize(16, 16)
        floatable: bool = False
        trailing: bool = True
        movable: bool = False
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal
        toolButtonStyle: QtCore.Qt.ToolButtonStyle = (
            QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly
        )
        enable_counting: bool = False

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
                - enable_counting: Enable counter on actions (default: False)
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
            enable_counting=kwargs.get("enable_counting", False),
        )

        # If counting is enabled, force TextUnderIcon style
        tool_button_style = self._opts.toolButtonStyle
        if self._opts.enable_counting:
            tool_button_style = QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon

        super().__init__(
            parent,
            movable=self._opts.movable,
            floatable=self._opts.floatable,
            orientation=self._opts.orientation,
            toolButtonStyle=tool_button_style,
            iconSize=self._opts.iconSize,
        )

        # Initialize counter storage for actions
        self._action_counters = {}
        self._action_labels = {}

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

        # Install event filter for right-click handling if counting is enabled
        if self._opts.enable_counting:
            self.installEventFilter(self)

        self.setStyleSheet(style)

    def add_actions(self, actions: list) -> None:
        """
        Add actions to the toolbar.

        Each action is created from a tuple of (icon, label, callback).
        Emits sig_action_triggered with the action label when triggered.

        Args:
            actions: List of (icon, label, callback) tuples where:
                - icon: QIcon object for the action
                - label: Text label for the action
                - callback: Callable invoked when action is triggered (can be None)
        """
        try:
            for icon, label, callback in actions:
                action = self.addAction(icon, label)

                # Store original label and initialize counter if counting is enabled
                if self._opts.enable_counting:
                    self._action_labels[action] = label
                    self._action_counters[action] = 0
                    self._update_action_text(action)

                    # Connect to handle increment on left-click
                    action.triggered.connect(
                        lambda _, act=action: self._on_action_increment(act)
                    )
                else:
                    action.triggered.connect(lambda _, lbl=label: self.sig_action_triggered.emit(lbl))

                if callback:
                    action.triggered.connect(callback)
        except (RuntimeError, IndexError, ValueError) as e:
            print(f"Error adding actions to toolbar: {e}")

    def _on_action_increment(self, action: QtWidgets.QAction) -> None:
        """Increment counter for an action and update its text."""
        self._action_counters[action] += 1
        self._update_action_text(action)
        self.sig_action_triggered.emit(self._action_labels[action])

    def _update_action_text(self, action: QtWidgets.QAction) -> None:
        """Update action text to show counter."""
        original_label = self._action_labels[action]
        count = self._action_counters[action]
        action.setText(f"{original_label}\n(x{count})")

    def eventFilter(self, obj, event: QtCore.QEvent) -> bool:
        """Handle right-click on toolbar buttons to decrement counter."""
        if not self._opts.enable_counting:
            return super().eventFilter(obj, event)

        if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            mouse_event = event
            if mouse_event.button() == QtCore.Qt.MouseButton.RightButton:
                # Find which action was clicked
                action = self.actionAt(self.mapFromGlobal(QtGui.QCursor.pos()))
                if action and action in self._action_counters:
                    self._action_counters[action] = max(0, self._action_counters[action] - 1)
                    self._update_action_text(action)
                    return True

        return super().eventFilter(obj, event)
