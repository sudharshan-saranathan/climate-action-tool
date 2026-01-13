# Filename: toolbar
# Module name: widgets
# Description: A custom toolbar for the Climact application with action handling and alignment.

# Imports (standard):
import dataclasses


# Imports (3rd party):
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
        toolButtonStyle: QtCore.Qt.ToolButtonStyle = QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly

    def __init__(self, parent=None, **kwargs):

        # Instantiate default options:
        self._opts = ToolBar.Options(
            iconSize=kwargs.get("iconSize", QtCore.QSize(16, 16)),
            floatable=kwargs.get("floatable", False),
            trailing=kwargs.get("trailing", True),
            movable=kwargs.get("movable", False),
            orientation=kwargs.get("orientation", QtCore.Qt.Orientation.Horizontal),
            toolButtonStyle=kwargs.get("toolButtonStyle", QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly),
        )

        super().__init__(
            parent,
            movable=self._opts.movable,
            floatable=self._opts.floatable,
            orientation=self._opts.orientation,
            toolButtonStyle=self._opts.toolButtonStyle,
            iconSize=self._opts.iconSize
        )

        style = kwargs.get('style', "")
        items = kwargs.get("actions", [])
        trail = kwargs.get("trailing", True)

        spacer = QtWidgets.QFrame()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        # Add spacer based on alignment
        if trail:
            self.addWidget(spacer)
            self.add_actions(items)

        else:
            self.add_actions(items)
            self.addWidget(spacer)

    # Add actions to the toolbar, if provided
    def add_actions(self, actions: list) -> None:

        # Add actions to the toolbar, encapsulated in try-except block
        try:
            for icon, label, callback in actions:
                self.addAction(icon, label, callback)

        except (RuntimeError, IndexError, ValueError) as e:
            print(f"Error adding actions to toolbar: {e}")
            return
