# Encoding: utf-8
# Filename: opts.py
# Description: Default asset(s) and resource(s) for the Climate Action Tool

# Imports (standard):
from __future__ import annotations

import dataclasses
import types


@dataclasses.dataclass
class DefaultOpts:
    """
    Default asset(s) and resource(s) for the Climate Action Tool.
    """

    logo = ":/logo/logo.png"  # The application's logo
    theme = ":/theme/dark.qss"  # The qss-file to use as the default theme.
    bezel = 64  # Initial padding around the main window at application startup.
    fonts = {
        "windows": types.SimpleNamespace(family="Fira Code", pointSize=8),
        "darwin": types.SimpleNamespace(family="Menlo", pointSize=11),
        "linux": types.SimpleNamespace(family="Noto Sans", pointSize=11),
    }  # The keys should match the values returned by `platform.system()`, NOT `sys.platform()`.
