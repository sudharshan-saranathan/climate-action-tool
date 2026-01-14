# Filename: lights.py
# Module name: widgets
# Description: Traffic light window control buttons (minimize, maximize, close).

"""
Traffic light window control widget.

Provides a toolbar with minimize, maximize, and close buttons styled as macOS-style traffic lights.
Emits signals when buttons are clicked for window management.
"""

from qtawesome import icon as qta_icon
from PySide6 import QtCore

from gui.widgets.toolbar import ToolBar


class Lights(ToolBar):
    """
    A traffic light-style window control toolbar.

    Displays three buttons for minimizing, maximizing, and closing the window.
    Emits signals when each button is clicked.
    """

    # Signals emitted when buttons are clicked:
    sig_minimize_clicked = QtCore.Signal()
    sig_maximize_clicked = QtCore.Signal()
    sig_close_clicked = QtCore.Signal()

    def __init__(self, parent=None):
        """
        Initialize the traffic lights widget.

        Args:
            parent: Parent widget (optional).
        """
        super().__init__(
            parent,
            iconSize=QtCore.QSize(12, 12),
            floatable=False,
            movable=False,
            trailing=False,
            actions=[
                (
                    qta_icon("mdi.minus-circle", color="#ffbd2e"),
                    "Minimize",
                    self.sig_minimize_clicked.emit,
                ),
                (
                    qta_icon("mdi.plus-circle", color="#27c93f"),
                    "Maximize",
                    self.sig_maximize_clicked.emit,
                ),
                (
                    qta_icon("mdi.close-circle", color="#ff5f57"),
                    "Close",
                    self.sig_close_clicked.emit,
                ),
            ],
        )
