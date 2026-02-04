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

# Local imports
from gui.widgets import FlowHub


class LowerPanel(QtWidgets.QFrame):
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

        # Set up layout with FlowHub
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the panel UI with FlowHub."""
        self.setContentsMargins(8, 8, 8, 8)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._flowhub = FlowHub(self)
        layout.addWidget(self._flowhub)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pen = QtGui.QPen(self._style.border["color"], self._style.border["width"])
        brs = QtGui.QBrush(self._style.background["color"])

        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(self.rect(), 4, 4)
