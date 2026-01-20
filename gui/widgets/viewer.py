# Filename: viewer.py
# Module name: widgets
# Description: QGraphicsView-based graph viewer widget.

"""
Graph viewer for displaying graphics scenes with zooming and panning.

Provides a QGraphicsView subclass with smooth zoom and pan animations, OpenGL viewport
for hardware acceleration, and keyboard/mouse event handling for navigation and selection.
"""

from __future__ import annotations
import dataclasses

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtOpenGLWidgets


class Viewer(QtWidgets.QGraphicsView):
    """
    A QGraphicsView-based viewer for displaying graphics scenes.

    Features:
    - Smooth zooming and panning animations
    - OpenGL viewport for hardware acceleration
    - Keyboard and mouse event handling for intuitive navigation
    - Standard shortcuts (Undo, Redo, Copy, Paste) passed to the scene
    """

    @dataclasses.dataclass
    class ViewerOpts:
        """
        Viewer animation and zoom configuration.

        Attributes:
            zoom_val: Current zoom level (default: 1.0).
            zoom_max: Maximum allowed zoom level (default: 2.0).
            zoom_min: Minimum allowed zoom level (default: 0.2).
            zoom_exp: Zoom exponential factor for mouse wheel (default: 1.4).
        """

        zoom_val: float = 1.0
        zoom_max: float = 2.0
        zoom_min: float = 0.2
        zoom_exp: float = 1.4

    def __init__(self, canvas: QtWidgets.QGraphicsScene, **kwargs):
        """
        Initialize the viewer with a graphics scene.

        Args:
            canvas: The QGraphicsScene to display.
            **kwargs: Optional configuration:
                - zoom_max: Maximum zoom level (default: 2.0)
                - zoom_min: Minimum zoom level (default: 0.2)
                - exp: Zoom exponent for mouse wheel (default: 1.4)
                - Other kwargs passed to QGraphicsView
        """

        self._opts = Viewer.ViewerOpts()

        # Extract viewer-specific kwargs before passing to the parent:
        self._opts.zoom_max = kwargs.pop("zoom_max", self._opts.zoom_max)
        self._opts.zoom_min = kwargs.pop("zoom_min", self._opts.zoom_min)
        self._opts.zoom_exp = kwargs.pop("exp", self._opts.zoom_exp)

        super().__init__(**kwargs)
        super().setScene(canvas)
        super().setCornerWidget(QtWidgets.QFrame())

        # Zoom animation with exponential easing
        self._zoom_anim = QtCore.QPropertyAnimation(self, b"zoom")
        self._zoom_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        self._zoom_anim.setDuration(360)

        # Pan animation with cubic easing
        self._focus_anim = QtCore.QPropertyAnimation(self, b"center")
        self._focus_anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        self._focus_anim.setDuration(720)

        # OpenGL viewport with 4x MSAA for hardware-accelerated rendering
        self._format = QtGui.QSurfaceFormat()
        self._format.setSamples(4)
        self._openGL_viewport = None
        QtCore.QTimer.singleShot(0, self._setup_opengl_viewport)

        # Register keyboard shortcuts for zoom, undo/redo, and copy/paste
        QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+="), self, lambda: self.execute_zoom(1.2, True)
        )
        QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+-"), self, lambda: self.execute_zoom(0.8, True)
        )
        QtGui.QShortcut(
            QtGui.QKeySequence.StandardKey.Undo, self, self._shortcut_handler
        )
        QtGui.QShortcut(
            QtGui.QKeySequence.StandardKey.Redo, self, self._shortcut_handler
        )
        QtGui.QShortcut(
            QtGui.QKeySequence.StandardKey.Copy, self, self._shortcut_handler
        )
        QtGui.QShortcut(
            QtGui.QKeySequence.StandardKey.Paste, self, self._shortcut_handler
        )

        # Listen for scene item focus signals to auto-pan
        from core.bus import EventsBus

        bus = EventsBus.instance()
        bus.sig_item_focused.connect(self._on_item_focused)

    @QtCore.Slot()
    def _setup_opengl_viewport(self) -> None:
        """Set up the OpenGL viewport after initialization."""
        if self._openGL_viewport is None:
            self._openGL_viewport = QtOpenGLWidgets.QOpenGLWidget(self)
            self._openGL_viewport.setFormat(self._format)
            self._openGL_viewport.setMouseTracking(True)
            self.setViewport(self._openGL_viewport)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard press events for view manipulation.

        - Ctrl modifier: Enable rubber band selection mode
        - Shift modifier: Enable scroll hand drag mode

        Args:
            event: The keyboard press event.
        """
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)

        if event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard release events.

        Resets drag mode to rubber band and unsets cursor.

        Args:
            event: The keyboard release event.
        """
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)
        self.unsetCursor()

        super().keyReleaseEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """
        Handle mouse wheel events for zooming.

        Scroll up zooms in, scroll down zooms out using exponential zoom factor.

        Args:
            event: The wheel event containing scroll delta.
        """
        delta = event.angleDelta().y()
        delta = self._opts.zoom_exp ** (delta / 100.0)

        self.execute_zoom(
            delta, event.deviceType() == QtGui.QInputDevice.DeviceType.Mouse
        )

    @QtCore.Slot()
    def _shortcut_handler(self) -> None:
        """
        Route standard shortcuts to the scene.

        Handles Undo, Redo, Copy, and Paste shortcuts by delegating to the scene
        if it implements the corresponding methods (undo, redo, clone_items, paste_items).
        """
        sender = self.sender()
        if not isinstance(sender, QtGui.QShortcut):
            return

        key_seq = sender.key().toString()
        scene = self.scene()
        if scene is None:
            return

        if key_seq == QtGui.QKeySequence(
            QtGui.QKeySequence.StandardKey.Copy
        ).toString() and hasattr(scene, "clone_items"):
            scene.clone_items()

        elif key_seq == QtGui.QKeySequence(
            QtGui.QKeySequence.StandardKey.Paste
        ).toString() and hasattr(scene, "paste_items"):
            scene.paste_items()

        elif key_seq == QtGui.QKeySequence(
            QtGui.QKeySequence.StandardKey.Undo
        ).toString() and hasattr(scene, "undo"):
            scene.undo()

        elif key_seq == QtGui.QKeySequence(
            QtGui.QKeySequence.StandardKey.Redo
        ).toString() and hasattr(scene, "redo"):
            scene.redo()

    @QtCore.Property(float)
    def zoom(self) -> float:
        """Get the current zoom level (read-only property)."""
        return self._opts.zoom_val

    @zoom.setter
    def zoom(self, value: float) -> None:
        """
        Set the zoom level and apply scale transformation.

        Args:
            value: Target zoom level to apply.
        """
        factor = value / self._opts.zoom_val
        self.scale(factor, factor)
        self._opts.zoom_val = value

    def execute_zoom(self, factor: float, animate: bool = True, /) -> None:
        """
        Execute a zoom operation with optional animation.

        Clamps the resulting zoom level to the configured min/max bounds before applying.

        Args:
            factor: Zoom multiplication factor to apply.
            animate: Whether to animate the zoom transition (default: True).
        """
        # Cancel any ongoing zoom animation to prevent conflicts
        if self._zoom_anim.state() == QtCore.QPropertyAnimation.State.Running:
            self._zoom_anim.stop()

        # Calculate target and clamp to allowed range
        target = self._opts.zoom_val * factor
        target = max(self._opts.zoom_min, min(self._opts.zoom_max, target))

        if animate:
            self._zoom_anim.setStartValue(self._opts.zoom_val)
            self._zoom_anim.setEndValue(target)
            self._zoom_anim.start()
        else:
            self.zoom = target

    @QtCore.Property(QtCore.QPointF)
    def center(self) -> QtCore.QPointF:
        """Get the center point of the current view (read-only property)."""
        return self.mapToScene(self.viewport().rect().center())

    @center.setter
    def center(self, value: QtCore.QPointF) -> None:
        """
        Set the center point of the view.

        Args:
            value: Target center point in scene coordinates.
        """
        self.centerOn(value)

    def _on_item_focused(self, item: QtWidgets.QGraphicsObject) -> None:
        """
        Handle item focus signal by animating the view to center on the item.

        Animates the view to pan and focus on the given graphics item.

        Args:
            item: The graphics item to focus on.
        """
        item_pos = item.mapToScene(item.boundingRect().center())
        view_pos = self.mapToScene(self.viewport().rect().center())

        self._focus_anim.stop()
        self._focus_anim.setStartValue(view_pos)
        self._focus_anim.setEndValue(item_pos)
        self._focus_anim.start()
