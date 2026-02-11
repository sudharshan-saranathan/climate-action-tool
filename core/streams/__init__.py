#  Filename: core/streams/__init__.py
#  Module name: core.streams
#  Description: Flow data structure managing streams and parameters

from __future__ import annotations
from typing import Dict, Any
import logging
import uuid

# Dataclass
from dataclasses import field
from dataclasses import dataclass