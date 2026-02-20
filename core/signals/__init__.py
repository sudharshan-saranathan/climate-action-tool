#  Filename: core/signals/__init__.py
#  Module name: core.signals
#  Description: Signal management for the application.

from .signal import Signal
from .bus import SignalBus

__all__ = ["Signal", "SignalBus"]
