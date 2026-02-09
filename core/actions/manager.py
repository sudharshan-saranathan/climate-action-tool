# Filename: manager.py
# Module name: actions
# Description: Manager for undo/redo action stacks.

"""
Actions manager for handling undo/redo stacks.
"""

from __future__ import annotations
from core.actions.actions import AbstractAction


class StackManager:
    """Manages application-wide undo/redo stacks."""

    MAX_UNDO = 50  # Maximum number of undo actions to keep

    def __init__(self):
        self.undo_stack: list[AbstractAction] = []
        self.redo_stack: list[AbstractAction] = []

    def do(self, action: AbstractAction) -> None:
        """
        Execute an action and push it to the undo stack.

        Clears the redo stack since a new action invalidates redo history.
        """
        self._prune_redo()
        action.execute()
        self.undo_stack.append(action)
        self._prune_undo()

    def undo(self) -> bool:
        """
        Undo the most recent action.

        Returns:
            True if an action was undone, False if the undo stack was empty.
        """
        if not self.undo_stack:
            return False

        action = self.undo_stack.pop()
        action.undo()
        self.redo_stack.append(action)
        return True

    def redo(self) -> bool:
        """
        Redo the most recently undone action.

        Returns:
            True if an action was redone, False if the redo stack was empty.
        """
        if not self.redo_stack:
            return False

        action = self.redo_stack.pop()
        action.redo()
        self.undo_stack.append(action)
        return True

    def _prune_undo(self) -> None:
        """Remove the oldest actions if the undo stack exceeds MAX_UNDO."""

        while len(self.undo_stack) > self.MAX_UNDO:
            action = self.undo_stack.pop(0)
            action.cleanup()

    def _prune_redo(self) -> None:
        """Clear all redo actions when a new action is performed."""

        for action in self.redo_stack:
            action.cleanup()

        self.redo_stack.clear()

    def wipe_stacks(self) -> None:
        """Clear all undo and redo history."""

        for action in self.undo_stack:
            action.cleanup()

        for action in self.redo_stack:
            action.cleanup()

        self.undo_stack.clear()
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        """Check if there are actions to undo."""

        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if there are actions to redo."""

        return len(self.redo_stack) > 0
