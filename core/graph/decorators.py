"""Decorators for graph operations."""

from __future__ import annotations

import logging
import typing
import json
import functools

_decorator_logger = logging.getLogger("core.graph.decorators")


def guid_validator(func: typing.Callable) -> typing.Callable:
    """Decorator to validate that a GUID exists in graph_db before executing."""

    @functools.wraps(func)
    async def async_wrapper(self, guid: str, *args, **kwargs):
        if guid not in self.database:
            return {
                "status": "FAILED",
                "reason": f"Graph [UID={guid}] does not exist.",
            }

        result = await func(self, guid, *args, **kwargs)
        return result

    return async_wrapper


def json_parser(func: typing.Callable) -> typing.Callable:
    """Decorator to parse JSON string and pass parsed dict to the function."""

    @functools.wraps(func)
    async def async_wrapper(self, guid: str, payload: str, *args, **kwargs):
        try:
            data = json.loads(payload) if payload else {}
        except json.JSONDecodeError as e:
            _decorator_logger.warning(f"Invalid JSON for {func.__name__}: {e}")
            return {
                "status": "FAILED",
                "reason": f"Invalid JSON: {e}",
            }

        result = await func(self, guid, data, *args, **kwargs)
        return result

    return async_wrapper
