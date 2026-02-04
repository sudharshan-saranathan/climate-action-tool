# Filename: lower.py
# Module name: panels
# Description: Lower panel to be shown within a dock

"""
Lower panel widget containing the FlowHub.

Displays available stream/flow types for use in the graph editor.
"""

# Pyside6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass


class LowerPanel(QtWidgets.QListWidget):
    """Lower panel containing the FlowHub widget."""

    @dataclass
    class Style:
        border: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x40474D),
                "width": 1.0,
            }
        )

        background: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x40474D),
                "brush": QtCore.Qt.BrushStyle.SolidPattern,
            }
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        # Instantiate dataclasses
        self._style = LowerPanel.Style()
