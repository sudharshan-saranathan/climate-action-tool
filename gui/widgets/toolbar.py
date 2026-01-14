# Filename: toolbar
# Module name: widgets
# Description: A custom toolbar with action handling and alignment.

import dataclasses
from PySide6 import QtCore
from PySide6 import QtWidgets


class ToolBar(QtWidgets.QToolBar):

    # Default options:
    @dataclasses.dataclass(frozen=True)
    class Options:
        iconSize: QtCore.QSize = QtCore.QSize(16, 16)
        floatable: bool = False
        trailing: bool = True
        movable: bool = False
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal
        toolButtonStyle: QtCore.Qt.ToolButtonStyle = (
            QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly
        )

    def __init__(self, parent=None, **kwargs):

        # Instantiate before super class:
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

        super().__init__(  # Now `self._opts` can be used.
            parent,
            movable=self._opts.movable,
            floatable=self._opts.floatable,
            orientation=self._opts.orientation,
            toolButtonStyle=self._opts.toolButtonStyle,
            iconSize=self._opts.iconSize,
        )

        style = kwargs.get("style", "")  # Custom styling.
        items = kwargs.get("actions", [])  # List of actions to add to the toolbar
        trail = kwargs.get("trailing", True)  # Position of actions w.r.t to spacer.

        spacer = QtWidgets.QFrame()  # The spacer aligns the toolbar's actions.
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        if trail:  # Actions trail the spacer.
            self.addWidget(spacer)
            self.add_actions(items)

        else:
            self.add_actions(items)
            self.addWidget(spacer)

        self.setStyleSheet(style)

    def add_actions(self, actions: list) -> None:
        """
        Adds the given actions to the toolbar sequentially.

        Args:
             actions (list): A list of tuples containing the action's icon, label, and callback method.
        """

        # Encapsulate in a try-except block:
        try:
            for icon, label, callback in actions:
                self.addAction(icon, label, callback)

        except (RuntimeError, IndexError, ValueError) as e:
            print(f"Error adding actions to toolbar: {e}")
            return
