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

    Displays three buttons styled as macOS-style traffic lights for minimizing, maximizing,
    and closing the window. Each button emits a corresponding signal when clicked.
    """

    # Signals emitted when traffic light buttons are clicked
    sig_minimize_clicked = QtCore.Signal()
    """Signal emitted when minimize button is clicked."""

    sig_maximize_clicked = QtCore.Signal()
    """Signal emitted when maximize button is clicked."""

    sig_close_clicked = QtCore.Signal()
    """Signal emitted when close button is clicked."""

    def __init__(self, parent=None):
        """
        Initialize the traffic lights widget.

        Args:
            parent: Parent widget (optional).
        """
        super().__init__(
            parent,
            iconSize=QtCore.QSize(18, 18),
            floatable=False,
            movable=False,
            trailing=False,
            actions=[
                (
                    qta_icon(
                        "ph.circle-fill", color="#28c840", active="ph.arrows-out-simple"
                    ),
                    "Maximize",
                    self._on_maximize,
                ),
                (
                    qta_icon(
                        "ph.circle-fill", color="#ffcb00", active="ph.minus-circle-fill"
                    ),
                    "Minimize",
                    self._on_minimize,
                ),
                (
                    qta_icon(
                        "ph.circle-fill", color="#ff5f57", active="ph.x-circle-fill"
                    ),
                    "Close",
                    self._on_close,
                ),
            ],
        )

    @QtCore.Slot()
    def _on_minimize(self) -> None:
        """Handle minimize button click by emitting sig_minimize_clicked signal."""
        self.sig_minimize_clicked.emit()

    @QtCore.Slot()
    def _on_maximize(self) -> None:
        """Handle maximize button click by emitting sig_maximize_clicked signal."""
        self.sig_maximize_clicked.emit()

    @QtCore.Slot()
    def _on_close(self) -> None:
        """Handle close button click by emitting sig_close_clicked signal."""
        self.sig_close_clicked.emit()
