# Filename: viewer.py
# Module name: widgets
# Description: QGraphicsView-based graph viewer widget.

"""
Graph viewer for displaying graphics scenes with zooming and panning.

Provides a QGraphicsView subclass with smooth zoom and pan animations, OpenGL viewport
for hardware acceleration, and keyboard/mouse event handling for navigation and selection.
"""

from __future__ import annotations

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtOpenGLWidgets

from gui.graph import Canvas


# Collections

# Climact modules: gui.graph


class Viewer(QtWidgets.QGraphicsView):
    """
    A QGraphicsView-based viewer for displaying graphics scenes.

    Features:
    - Smooth zooming and panning animations
    - OpenGL viewport for hardware acceleration
    - Keyboard and mouse event handling for intuitive navigation
    - Standard shortcuts (Undo, Redo, Copy, Paste) passed to the scene
    """

    # Initializer
    def __init__(self, **kwargs):

        # Initialize zoom-related attributes
        self._zooming_attrs = {
            "val": 1.0,
            "max": 2.0,
            "min": 0.2,
            "exp": 1.4,
        }

        # Invoke super class initializer
        super().__init__(**kwargs)

        # Zoom animation with exponential easing
        self._zoom_anim = QtCore.QPropertyAnimation(self, b"zoom")
        self._zoom_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        self._zoom_anim.setDuration(360)

        # Pan animation with cubic easing
        self._focus_anim = QtCore.QPropertyAnimation(self, b"center")
        self._focus_anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        self._focus_anim.setDuration(720)

        # OpenGL viewport with 4x MSAA for hardware-accelerated rendering
        if kwargs.get("opengl", True):
            self._setup_opengl_viewport()

        # Set scene
        self.setScene(Canvas())

        # Register keyboard shortcuts for zoom, undo/redo, and copy/paste:
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
        QtGui.QShortcut(
            QtGui.QKeySequence.StandardKey.Delete, self, self._shortcut_handler
        )

        # Connect to the application's viewer instructions signal group
        app = QtWidgets.QApplication.instance()
        if hasattr(app, "view_ctrl"):
            app.view_ctrl.focus_item.connect(self._on_item_focused)

    @QtCore.Slot()
    def _setup_opengl_viewport(self) -> None:

        self._format = QtGui.QSurfaceFormat()
        self._format.setSamples(4)

        self._openGL_viewport = QtOpenGLWidgets.QOpenGLWidget(self)
        self._openGL_viewport.setFormat(self._format)
        self._openGL_viewport.setMouseTracking(True)
        self.setViewport(self._openGL_viewport)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard press events for view manipulation.
        """

        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)
            self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

        if event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard release events.
        """

        self.unsetCursor()
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        super().keyReleaseEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """
        Handle mouse wheel events for zooming.
        """
        delta = event.angleDelta().y()
        delta = self._zooming_attrs["exp"] ** (delta / 100.0)

        self.execute_zoom(
            delta, event.deviceType() == QtGui.QInputDevice.DeviceType.Mouse
        )

    @QtCore.Slot()
    def _shortcut_handler(self) -> None:
        """
        Route standard shortcuts to the scene.
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

        if key_seq == QtGui.QKeySequence(
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

        elif key_seq == QtGui.QKeySequence(
            QtGui.QKeySequence.StandardKey.Delete
        ).toString() and hasattr(scene, "delete_items"):
            scene.delete_items()

    @QtCore.Property(float)
    def zoom(self) -> float:
        """Get the current zoom level (read-only property)."""
        return self._zooming_attrs["val"]

    @zoom.setter
    def zoom(self, value: float) -> None:
        """
        Set the zoom level and apply scale transformation.

        Args:
            value: Target zoom level to apply.
        """
        factor = value / self._zooming_attrs["val"]
        self.scale(factor, factor)
        self._zooming_attrs["val"] = value

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
        target = self._zooming_attrs["val"] * factor
        target = max(
            self._zooming_attrs["min"], min(self._zooming_attrs["max"], target)
        )

        if animate:
            self._zoom_anim.setStartValue(self._zooming_attrs["val"])
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
        """

        self.centerOn(value)

    def _on_item_focused(self, item: QtWidgets.QGraphicsObject) -> None:
        """
        Handle item focus signal by animating the view to center on the item.
        """

        item_pos = item.mapToScene(item.boundingRect().center())
        view_pos = self.mapToScene(self.viewport().rect().center())

        self._focus_anim.stop()
        self._focus_anim.setStartValue(view_pos)
        self._focus_anim.setEndValue(item_pos)
        self._focus_anim.start()
