# Filename: actions.py
# Module name: actions
# Description: Undo/redo action classes for the graph editor.

"""
Action classes for implementing undo/redo functionality.

This module provides abstract and concrete action classes that encapsulate
operations on graph items, allowing them to be undone and redone.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
import weakref
import logging

from PySide6 import QtWidgets

if TYPE_CHECKING:
    from gui.graph.canvas import Canvas


class AbstractAction(ABC):
    """Abstract base class for all undoable/redoable actions."""

    def __init__(self):
        self._is_obsolete = False

    @abstractmethod
    def execute(self) -> None:
        """Execute the action. Called when action is first performed."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Reverse the action."""
        pass

    @abstractmethod
    def redo(self) -> None:
        """Re-apply the action after it has been undone."""
        pass

    def is_obsolete(self) -> bool:
        """Check if this action is no longer relevant."""
        return self._is_obsolete

    def set_obsolete(self) -> None:
        """Mark this action as obsolete."""
        self._is_obsolete = True

    def set_relevant(self) -> None:
        """Mark this action as relevant again."""
        self._is_obsolete = False

    def cleanup(self) -> None:
        """Clean up resources when the action is pruned from history."""
        pass


class BatchActions(AbstractAction):
    """Groups multiple actions together for atomic undo/redo."""

    def __init__(self):
        super().__init__()
        self._actions: list[AbstractAction] = []

    def add_to_batch(self, action: AbstractAction) -> None:
        """Add an action to this batch."""
        if action is not None:
            self._actions.append(action)

    def add_actions(self, actions: list[AbstractAction]) -> None:
        """Add multiple actions to this batch."""
        for action in actions:
            self.add_to_batch(action)

    def cleanup(self) -> None:
        """Clean up all actions in the batch."""
        for action in self._actions:
            action.cleanup()

    def execute(self) -> None:
        """Execute all actions in order."""
        for action in self._actions:
            action.execute()

    def undo(self) -> None:
        """Undo all actions in reverse order."""
        for action in reversed(self._actions):
            action.undo()

    def redo(self) -> None:
        """Redo all actions in reverse order."""
        for action in reversed(self._actions):
            action.redo()


class CreateAction(AbstractAction):
    """Action for creating/showing an item in the scene."""

    def __init__(
        self,
        parent: Canvas | QtWidgets.QGraphicsObject,
        item: QtWidgets.QGraphicsObject,
    ):
        super().__init__()
        self._parent_ref = weakref.ref(parent)
        self._item_ref = weakref.ref(item)

        # Connect the item's destroyed signal to the set_obsolete method
        try:
            item.destroyed.connect(self.set_obsolete)
        except (AttributeError, RuntimeError, TypeError):
            logging.warning(
                f"Could not connect item's destroyed signal to {self.__class__.__name__}."
            )

    def _dereference(self) -> tuple[Any, Any]:
        """Safely dereference weak references."""
        if self._is_obsolete:
            logging.info("Reference(s) destroyed, aborting!")
            return None, None

        parent = self._parent_ref() if self._parent_ref else None
        item = self._item_ref() if self._item_ref else None
        return parent, item

    def cleanup(self) -> None:
        """Clean up: remove item from the scene and delete it."""
        parent, item = self._dereference()
        if item is None:
            return

        # No cleanup if the item is still active/visible
        if item.isVisible():
            return

        # Use parent's deregister if available (for nested QGraphicsObjects),
        # otherwise fall back to scene.removeItem()
        if hasattr(parent, "deregister") and callable(parent.deregister):
            parent.deregister(item)
        else:
            scene = item.scene()
            if scene is not None:
                scene.removeItem(item)

        # Schedule deletion
        item.deleteLater()

    def execute(self) -> None:
        """Execute - does nothing because the item is already in the scene."""
        pass

    def undo(self) -> None:
        """Undo: hide the item and block its signals."""

        parent, item = self._dereference()
        if item is None:
            return

        item.blockSignals(True)
        item.setVisible(False)
        item.setSelected(False)

    def redo(self) -> None:
        """Redo: show the item and unblock its signals."""
        parent, item = self._dereference()
        if item is None:
            return

        item.blockSignals(False)
        item.setVisible(True)


class DeleteAction(AbstractAction):
    """Action for deleting/hiding an item from the scene."""

    def __init__(
        self,
        parent: Canvas | QtWidgets.QGraphicsObject,
        item: QtWidgets.QGraphicsObject,
    ):
        super().__init__()
        self._parent_ref = weakref.ref(parent)
        self._item_ref = weakref.ref(item)

        # Connect the item's destroyed signal to the set_obsolete method
        try:
            item.destroyed.connect(self.set_obsolete)
        except (AttributeError, RuntimeError, TypeError):
            logging.warning(
                f"Could not connect item's destroyed signal to {self.__class__.__name__}."
            )

    def _dereference(self) -> tuple[Any, Any]:
        """Safely dereference weak references."""

        if self._is_obsolete:
            logging.info("Reference(s) destroyed, aborting!")
            return None, None

        parent = self._parent_ref() if self._parent_ref else None
        item = self._item_ref() if self._item_ref else None
        return parent, item

    def cleanup(self) -> None:
        """Clean up: remove the item from the scene and delete it."""
        parent, item = self._dereference()
        if item is None:
            return

        # No cleanup if the item is still active/visible
        if item.isVisible():
            return

        # Use the parent's `deregister` method, if available.
        if hasattr(parent, "deregister") and callable(parent.deregister):
            parent.deregister(item)

        scene = item.scene()
        if scene and item in scene.items():
            scene.removeItem(item)

        # Schedule deletion
        item.deleteLater()

    def execute(self) -> None:
        """Execute: hide the item and block its signals."""
        parent, item = self._dereference()
        if item is None:
            return

        item.blockSignals(True)
        item.setVisible(False)
        item.setSelected(False)

    def undo(self) -> None:
        """Undo: show the item and unblock its signals."""
        parent, item = self._dereference()
        if item is None:
            return

        item.blockSignals(False)
        item.setVisible(True)

    def redo(self) -> None:
        """Redo: hide the item and block its signals."""
        parent, item = self._dereference()
        if item is None:
            return

        item.blockSignals(True)
        item.setVisible(False)
        item.setSelected(False)
