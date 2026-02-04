# Encoding: utf-8
# Module name: viewer
# Description: A QGraphicsView-based graph viewer for the Climact application


# Import - standard
import types

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtOpenGLWidgets


# Dataclass
from dataclasses import dataclass


# Class Viewer: A QGraphicsView-based graph viewer
class Viewer(QtWidgets.QGraphicsView):

    # Dataclass
    @dataclass
    class ZoomAttrs:
        zoom_max: float = 2.0
        zoom_min: float = 0.2
        zoom_exp: float = 1.4

    def __init__(self, canvas: QtWidgets.QGraphicsScene, **kwargs):

        # Define zoom attrs before super().__init__()
        self._zoom = Viewer.ZoomAttrs(
            zoom_max=kwargs.pop("zoom_max", 2.0),
            zoom_min=kwargs.pop("zoom_min", 0.2),
            zoom_exp=kwargs.pop("zoom_exp", 1.4),
        )

        # Base-class initialization:
        super().__init__(**kwargs)
        super().setScene(canvas)
        super().setMouseTracking(True)
        super().setCornerWidget(QtWidgets.QFrame())

        # Animations
        self._init_zoom_animation()
        self._init_focus_animation()

        # Use an OpenGL viewport for hardware acceleration:
        self._format = QtGui.QSurfaceFormat()
        self._format.setSamples(4)
        self._openGL_viewport = QtOpenGLWidgets.QOpenGLWidget(self)
        self._openGL_viewport.setFormat(self._format)
        self._openGL_viewport.setMouseTracking(True)
        self.setViewport(self._openGL_viewport)

        # Define shortcuts
        self._init_shortcuts()

    # Initialize zoom animation
    def _init_zoom_animation(self):
        self._zoom_anim = QtCore.QPropertyAnimation(self, b"zoom")
        self._zoom_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutExpo)
        self._zoom_anim.setDuration(360)

    # Initialize focus animation
    def _init_focus_animation(self):
        self._focus_anim = QtCore.QPropertyAnimation(self, b"center")
        self._focus_anim.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        self._focus_anim.setDuration(720)

    def _init_shortcuts(self):

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

    # Filter the shift key to activate panning mode
    def keyPressEvent(self, event, /):

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

        # Reset to no-drag mode and unset cursor:
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)
        self.unsetCursor()

        super().keyReleaseEvent(event)

    # QWheelEvent
    def wheelEvent(self, event, /):

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

    # Animation property:
    @QtCore.Property(float)
    def zoom(self):
        return self._zoom.scale

    # Set the zoom level:
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
