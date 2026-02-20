"""Signal class for event-driven architecture."""

from __future__ import annotations

import logging
import uuid
from dataclasses import field


class Signal:
    """A pure Python implementation of a Signal."""

    _logger = logging.getLogger("Signal")

    def __init__(self, *types):
        self._types = types
        self._listeners = dict()

    def connect(self, listener):

        uid = listener.uid if hasattr(listener, "uid") else uuid.uuid4().hex
        self._listeners[uid] = listener

    def emit(self, *args, **kwargs):

        for listener in self._listeners.values():

            try:
                listener(*args, **kwargs)

            except Exception as e:

                import traceback

                self._logger.error(f"Error in signal listener: {e}")
                self._logger.debug(f"Listener: {listener}")
                self._logger.debug(f"Args: {args}")
                traceback.print_exc()

    @staticmethod
    def factory(*types) -> Signal:
        return field(default_factory=lambda: Signal(*types))