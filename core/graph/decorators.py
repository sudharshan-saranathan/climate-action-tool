"""Decorators for graph operations."""

from __future__ import annotations

import logging
import typing
import json
import functools

_decorator_logger = logging.getLogger("core.graph.decorators")


def guid_validator(func: typing.Callable) -> typing.Callable:
    """
    Decorator to validate that a GUID exists in graph_db before executing.
    """

    @functools.wraps(func)
    def wrapper(self, guid: str, *args, **kwargs):
        if guid not in self.graph_db:
            self.signal_bus.ui.notify.emit(f"ALERT: Graph [UID={guid}] does not exist.")
            return None

        result = func(self, guid, *args, **kwargs)
        return result

    return wrapper


def json_parser(func: typing.Callable) -> typing.Callable:
    """Decorator to parse JSON string and pass parsed dict to the function.

    :param func: The function to decorate.
    """

    @functools.wraps(func)
    def wrapper(self, guid: str, jstr: str, *args, **kwargs):
        try:
            data = json.loads(jstr)
        except json.JSONDecodeError as e:
            _decorator_logger.warning(f"Invalid JSON for {func.__name__}: {e}")
            return None

        # Pass both original jstr and parsed data
        return func(self, guid, jstr, data, *args, **kwargs)

    return wrapper