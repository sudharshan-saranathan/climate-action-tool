# Filename: canvas.py
# Module name: graph
# Description: Graphics scene for displaying node graphs.

"""
Graphics scene for node-based graph editing.

Provides a QGraphicsScene subclass configured for displaying and editing
node graphs with customizable appearance and scene layout.
"""

from __future__ import annotations
import dataclasses
from PySide6 import QtGui, QtCore, QtWidgets


class Canvas(QtWidgets.QGraphicsScene):
    """
    A graphics scene for displaying and editing node graphs.

    Provides a configured QGraphicsScene with default scene bounds and background styling.
    """

    @dataclasses.dataclass
    class Options:
        """Canvas configuration options."""

        sceneRect: QtCore.QRect = dataclasses.field(
            default_factory=lambda: QtCore.QRect(0, 0, 5000, 5000)
        )
        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(QtGui.QColor(0xEFEFEF))
        )

    def __init__(self, parent=None):
        """
        Initialize the graphics scene.

        Args:
            parent: Parent object (optional).
        """

        self._opts = Canvas.Options()
        super().__init__(
            self._opts.sceneRect, parent=parent, backgroundBrush=self._opts.background
        )
