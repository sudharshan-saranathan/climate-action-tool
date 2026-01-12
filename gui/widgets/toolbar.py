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

    def __init__(self, parent=None, **kwargs):

        # Instantiate default options:
        self._opts = ToolBar.Options(**kwargs)

        #
        super().__init__(
            parent,
            movable=self._opts.movable,
            floatable=self._opts.floatable,
            orientation=self._opts.orientation,
            iconSize=kwargs.get("iconSize", self._opts.iconSize),
        )

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
