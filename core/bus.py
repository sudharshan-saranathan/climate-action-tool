# Filename: bus.py
# Module name: core
# Description: Event bus for application-wide component communication.

"""
Event bus for inter-component communication.

Provides a singleton EventsBus that emits signals for graph item lifecycle events
(created, clicked, deleted, updated, focused). Used to decouple graph items
from the canvas and other components.
"""

from __future__ import annotations
from PySide6 import QtCore, QtWidgets, QtGui


# Event bus class
class EventsBus(QtCore.QObject):
    """
    Application-wide event bus for inter-component communication.
    Implements the singleton pattern to ensure a single instance.
    """

    # Singleton instance
    _instance = None

    # Signals for graphics object lifecycle events
    sig_item_created = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_clicked = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_deleted = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_updated = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_focused = QtCore.Signal(QtWidgets.QGraphicsObject)

    def __init__(self):
        super().__init__()

    @classmethod
    def instance(cls) -> "EventsBus":
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Instantiate the global event bus
bus = EventsBus.instance()
