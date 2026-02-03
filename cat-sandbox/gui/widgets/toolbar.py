# Filename: toolbar.py
# Module name: widgets
# Description: Custom toolbar widget with action management.

# PySide6 (Python/Qt)
from PySide6 import QtCore
from PySide6 import QtWidgets

# Standard
import dataclasses


class ToolBar(QtWidgets.QToolBar):

    @dataclasses.dataclass(frozen=True)
    class Attrs:
        iconSize: QtCore.QSize = QtCore.QSize(16, 16)
        floatable: bool = False
        trailing: bool = True
        movable: bool = False
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal
        toolButtonStyle: QtCore.Qt.ToolButtonStyle = (
            QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly
        )

    def __init__(self, parent=None, **kwargs):

        # Initialize toolbar attributes before super().__init__()
        self._attrs = ToolBar.Attrs(
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
            movable=self._attrs.movable,
            floatable=self._attrs.floatable,
            orientation=self._attrs.orientation,
            toolButtonStyle=self._attrs.toolButtonStyle,
            iconSize=self._attrs.iconSize,
        )

        style = kwargs.get("style", "")
        actions = kwargs.get("actions", [])

        # Create an expanding spacer widget for alignment
        spacer = QtWidgets.QFrame()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        # Add spacer and actions in order based on the trailing flag
        if self._attrs.trailing:
            self.addWidget(spacer)
            self.add_actions(actions)
        else:
            self.add_actions(actions)
            self.addWidget(spacer)

        self.setStyleSheet(style)

    def add_actions(self, actions: list) -> None:

        try:
            for icon, label, callback in actions:
                action = self.addAction(icon, label)
                action.triggered.connect(callback)

        except (RuntimeError, IndexError, ValueError) as e:
            print(f"Error adding actions to toolbar: {e}")
