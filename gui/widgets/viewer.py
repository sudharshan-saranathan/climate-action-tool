# Filename: viewer.py
# Module name: widgets
# Description: A QGraphicsView-based viewer for displaying graphics scenes

"""
QGraphicsView-based viewer for displaying graphics scenes.

Provides interactive viewing with zooming, panning, and selection capabilities.
Keyboard shortcuts: Ctrl+wheel/Ctrl+=/Ctrl+- (zoom), Shift+drag (pan), Ctrl+drag (select).
"""

import dataclasses

from PySide6 import QtGui, QtCore, QtWidgets


class Viewer(QtWidgets.QGraphicsView):
    """
    A QGraphicsView-based viewer for displaying graphics scenes.

    Supports:
    - Zooming: Ctrl+wheel, Ctrl+=, Ctrl+-
    - Panning: Shift+drag (ScrollHandDrag)
    - Selection: Ctrl+drag (RubberBandDrag)
    """

    @dataclasses.dataclass(frozen=True)
    class Options:
        """Configuration options for the Viewer."""

        zoom_min: float = 0.2
        zoom_max: float = 2.0
        zoom_factor: float = 1.2

    def __init__(
        self,
        scene: QtWidgets.QGraphicsScene,
        parent = None,
        **kwargs
    ):
        """
        Initialize the viewer with a graphics scene.

        Args:
            scene: The QGraphicsScene to display.
            parent: Parent widget (optional).
            **kwargs: Additional arguments passed to QGraphicsView.
        """

        # Extract Options before passing to parent:
        self._opts = Viewer.Options()

        # Initialize super-class with keywords:
        super().__init__(scene, parent=parent, **kwargs)

        self.setMouseTracking(True)
        self._zoom_scale = 1.0

        # Keyboard shortcuts for zooming
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+="), self, lambda: self._zoom_by(self._opts.zoom_factor))
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+-"), self, lambda: self._zoom_by(1.0 / self._opts.zoom_factor))

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """
        Handle mouse wheel events for zooming.

        Args:
            event: The wheel event.
        """
        if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            factor = 1.1 if delta > 0 else 0.9
            self._zoom_by(factor)
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard events for panning and selection mode switching.

        Shift key enables panning (ScrollHandDrag), Ctrl key enables selection (RubberBandDrag).

        Args:
            event: The key event.
        """
        if event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        elif event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard release events to reset drag mode to NoDrag.

        Resets to NoDrag mode when Shift is released, clearing panning/selection.

        Args:
            event: The key event.
        """
        if not (event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier):
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self.unsetCursor()

        super().keyReleaseEvent(event)

    def _zoom_by(self, factor: float) -> None:
        """
        Zoom by the specified factor.

        Args:
            factor: The zoom factor (>1 to zoom in, <1 to zoom out).
        """
        new_scale = self._zoom_scale * factor
        new_scale = max(self._opts.zoom_min, min(self._opts.zoom_max, new_scale))

        if new_scale != self._zoom_scale:
            scale_factor = new_scale / self._zoom_scale
            self.scale(scale_factor, scale_factor)
            self._zoom_scale = new_scale