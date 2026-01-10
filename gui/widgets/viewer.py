# Encoding: utf-8
# Filename: viewer.py
# Description: A QGraphicsView-based graph viewer for the Climate Action Tool

# Imports (compatibility):
from __future__ import annotations

# Imports (standard):
import dataclasses
import types

# Import(s) - third party:
from PySide6 import QtCore, QtGui, QtOpenGLWidgets, QtWidgets


# Default options for the Viewer widget:
@dataclasses.dataclass
class ViewerOpts:
    zoom_max: float = 2.0
    zoom_min: float = 0.2
    zoom_exp: float = 1.4


# Class Viewer: A QGraphicsView-based graph viewer
class Viewer(QtWidgets.QGraphicsView):
    """
    A QGraphicsView-based viewer for displaying graphics scenes. The viewer supports smooth zooming, animations,
    and panning. It features an OpenGL viewport (supports hardware acceleration), handles mouse and keyboard events
    for intuitive navigation and item selection, and defines standard shortcuts that are forwarded to the scene.
    """

    def __init__(self, canvas: QtWidgets.QGraphicsScene, **kwargs):
        # These keywords (`zoom_max`, `zoom_min` and `zoom_exp`) must be popped from kwargs before calling
        # the base-class constructor. Otherwise, an exception will be raised.
        zoom_max = kwargs.pop("zoom_max", ViewerOpts.zoom_max)
        zoom_min = kwargs.pop("zoom_min", ViewerOpts.zoom_min)
        zoom_exp = kwargs.pop("exp", ViewerOpts.zoom_exp)

        # Base-class initialization:
        super().__init__(**kwargs)
        super().setScene(canvas)
        super().setMouseTracking(True)
        super().setCornerWidget(QtWidgets.QFrame())

        # Initialize zoom and zoom-animation attribute(s):
        self._zoom = types.SimpleNamespace(
            scale=1.0, min=zoom_min, max=zoom_max, exp=zoom_exp
        )

        # Zoom animation:
        self._zoom_anim = QtCore.QPropertyAnimation(self, b"zoom")
        self._zoom_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        self._zoom_anim.setDuration(360)

        # Focus animation:
        self._focus_anim = QtCore.QPropertyAnimation(self, b"center")
        self._focus_anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        self._focus_anim.setDuration(720)

        # Use an OpenGL viewport for hardware acceleration:
        self._format = QtGui.QSurfaceFormat()
        self._format.setSamples(4)
        self._openGL_viewport = QtOpenGLWidgets.QOpenGLWidget(self)
        self._openGL_viewport.setFormat(self._format)
        self._openGL_viewport.setMouseTracking(True)
        self.setViewport(self._openGL_viewport)

        # Set update mode for OpenGL (prevents zoom artifacts):
        self.setViewportUpdateMode(
            QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.setCacheMode(QtWidgets.QGraphicsView.CacheModeFlag.CacheNone)

        # Define shortcuts
        # Zoom in/out shortcuts:
        QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+="), self, lambda: self.execute_zoom(1.2, True)
        )
        QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+-"), self, lambda: self.execute_zoom(0.8, True)
        )

        # Scene-actions:
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

        # Handle item focus signals (optional - EventsBus may not exist yet):
        try:
            from core.bus import EventsBus

            bus = EventsBus.instance()
            bus.sig_item_focused.connect(self._on_item_focused)
        except ImportError:
            pass

    # Filter the shift key to activate panning mode
    def keyPressEvent(self, event, /):
        """
        Reimplements the keyPressEvent method to capture Shift and Control presses.

        Args:
            event (QtGui.QKeyEvent): Event object instantiated and internally managed by Qt.
        """

        # When the Ctrl key is pressed, switch to selection mode:
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)

        # When the Shift key is pressed, switch to drag-mode:
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        super().keyPressEvent(event)

    # When the Shift key is released, switch back to hand-drag mode
    def keyReleaseEvent(self, event, /):
        """
        Reimplements the keyReleaseEvent method to reset the drag mode and cursor.

        Args:
            event (QtGui.QKeyEvent): Event object instantiated and internally managed by Qt.
        """

        # Reset to no-drag mode and unset cursor:
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)
        self.unsetCursor()

        super().keyReleaseEvent(event)

    # When the mouse or trackpad is scrolled:
    def wheelEvent(self, event, /):
        """
        Reimplements the wheelEvent method to zoom in/out based on the scroll direction.

        Args:
            event (QtGui.QWheelEvent): Event object instantiated and internally managed by Qt.
        """

        delta = event.angleDelta().y()
        delta = self._zoom.exp ** (delta / 100.0)

        self.execute_zoom(
            delta, event.deviceType() == QtGui.QInputDevice.DeviceType.Mouse
        )

    # Shortcut handler
    @QtCore.Slot()
    def _shortcut_handler(self):
        sender = self.sender()
        if not isinstance(sender, QtGui.QShortcut):
            return

        key_seq = sender.key().toString()
        scene = self.scene()
        if scene is None:
            return

        # Use QtGui.QKeySequence(...) to retrieve the string representation of the standard key sequences. This is
        # necessary to ensure compatibility across different platforms (e.g., Windows, macOS, Linux). Then, check
        # if the key sequence matches any of the standard actions (Copy, Paste, Undo, Redo) and call the corresponding
        # method on the scene if it exists.

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

    # Animation property
    @QtCore.Property(float)
    def zoom(self):
        return self._zoom.scale

    # Set the zoom level
    @zoom.setter
    def zoom(self, value: float):
        factor = value / self._zoom.scale
        self.scale(factor, factor)
        self._zoom.scale = value

    # Zoom execution:
    def execute_zoom(self, factor, animate=True, /):
        # Stop any ongoing animation:
        if self._zoom_anim.state() == QtCore.QPropertyAnimation.State.Running:
            self._zoom_anim.stop()

        # Calculate the target zoom level:
        target = self._zoom.scale * factor
        target = max(self._zoom.min, min(self._zoom.max, target))

        # Set up and start the animation:
        if animate:
            self._zoom_anim.setStartValue(self._zoom.scale)
            self._zoom_anim.setEndValue(target)
            self._zoom_anim.start()

        else:
            self.zoom = target

    # Focus property:
    @QtCore.Property(QtCore.QPointF)
    def center(self):
        return self.mapToScene(self.viewport().rect().center())

    @center.setter
    def center(self, value: QtCore.QPointF):
        self.centerOn(value)

    # This method implements the centering animation for graphics items:
    def _on_item_focused(self, item: QtWidgets.QGraphicsObject):
        item_pos = item.mapToScene(item.boundingRect().center())
        view_pos = self.mapToScene(self.viewport().rect().center())

        self._focus_anim.stop()
        self._focus_anim.setStartValue(view_pos)
        self._focus_anim.setEndValue(item_pos)
        self._focus_anim.start()
