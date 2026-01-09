# Encoding: utf-8
# Module name: toolbar
# Description: A custom toolbar for the Climact application with action handling and alignment.


# Imports (standard)
from __future__ import annotations
import logging

# Imports (third party)
from PySide6 import QtCore
from PySide6 import QtWidgets


# Class Toolbar
class ToolBar(QtWidgets.QToolBar):

    # Signals
    sig_action_triggered = QtCore.Signal(str)

    # Initializer
    def __init__(self, parent=None, **kwargs):
        super().__init__(
            parent,
            movable=False,
            floatable=False,
            orientation=kwargs.get('orientation', QtCore.Qt.Orientation.Horizontal),
            iconSize=kwargs.get("iconSize", QtCore.QSize(16, 16)),
        )

        items = kwargs.get("actions", []) # List of actions
        trail = kwargs.get("trailing", True) # Flag determines where the spacer is added
        style = kwargs.get('style', None)

        spacer = QtWidgets.QFrame()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        # Add spacer based on the provided (or default) alignment:
        if trail:
            self.addWidget(spacer)
            self.add_actions(items)

        else:
            self.add_actions(items)
            self.addWidget(spacer)


        # Apply style if provided:
        if style:
            self.setStyleSheet(style)

    # Add actions to the toolbar, if provided
    def add_actions(self, actions: list) -> None:

        # Add actions to the toolbar, encapsulated in a try-except block:
        try:
            for icon, label, callback in actions:
                self.addAction(icon, label, callback)

        except (RuntimeError, IndexError, ValueError) as e:
            logging.error(f"Error adding actions to toolbar: {e}")
            return
