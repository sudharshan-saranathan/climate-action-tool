# Filename: qtaitem.py
# Module name: custom
# Description: QtAwesome icon rendering for graphics scenes.

"""
QGraphicsSimpleTextItem-based QtAwesome icon rendering.

Provides icon items (QtaItem) that render QtAwesome icons on a QGraphicsScene.
Supports dynamic icon reloading and color customization.
"""

from __future__ import annotations
import qtawesome as qta
from PySide6 import QtGui, QtCore, QtWidgets


class QtaItem(QtWidgets.QGraphicsSimpleTextItem):
    """
    Custom QGraphicsSimpleTextItem that shows QtAwesome icons.
    The icon is rendered as a font glyph for use in a QGraphicsScene.
    """

    def __init__(
        self,
        label: str,
        width: int = 16,
        parent: QtWidgets.QGraphicsObject | None = None,
        **kwargs,
    ) -> None:
        super().__init__(parent)
        self._width = width
        self._color = kwargs.get("color", "#efefef")
        self.render_icon(label)
        self.setTransformOriginPoint(self.boundingRect().center())

    def render_icon(self, label: str, color: str | None = None) -> None:
        """Render the QtAwesome icon with the given label and optional color."""
        if "." not in label:
            raise ValueError(
                f"Icon name '{label}' must have a prefix (e.g., 'mdi.icon-name')"
            )

        prefix = label.split(".")[0].lower()
        if prefix not in ("mdi", "ph", "fa5", "fa6", "fa5s", "fa6s", "ri"):
            raise ValueError(f"Unsupported icon prefix: '{prefix}'")

        char = qta.charmap(label)
        self.setText(char)
        self.setFont(qta.font(prefix, self._width))
        self.setBrush(QtGui.QBrush(color or self._color))

    def boundingRect(self) -> QtCore.QRectF:
        """Reimplement boundingRect to ensure proper sizing."""
        return super().boundingRect().adjusted(0, 0, 0, -1)
