# Encoding: utf-8
# Module name: custom
# Module description: Custom QtAwesome icon integration for the Climact application


# Imports (standard)
from __future__ import annotations


# Imports (third party)
import qtawesome as qta
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


class QtaItem(QtWidgets.QGraphicsSimpleTextItem):
    """
    Custom QGraphicsSimpleTextItem that shows QtAwesome icons. The icon is rendered as a font glyph for use in a
    QGraphicsScene.
    """

    def __init__(
        self,
        label: str,  # This label is a qt-awesome icon name, e.g., 'mdi.home'
        width: int = 16,  # Size of the icon
        parent: QtWidgets.QGraphicsObject | None = None,
        **kwargs,  # Additional keyword arguments for the QtAwesome icon function (e.g., color).
    ) -> None:

        super().__init__(parent)

        self._width = width
        self._color = kwargs.get("color", "#efefef")

        self.render_icon(label)
        self.setTransformOriginPoint(self.boundingRect().center())

    # Method to render the icon
    def render_icon(self, label: str, color: str | None = None) -> None:

        if "." not in label:
            raise ValueError(
                f"Icon name '{label}' must have a prefix (e.g., 'mdi.icon-name'). "
                f"See the docstring for supported prefixes."
            )

        prefix = label.split(".")[0].lower()
        if prefix not in ("mdi", "ph", "fa5", "fa6", "fa5s", "fa6s", "ri"):
            raise ValueError(f"Unsupported icon prefix: '{prefix}'")

        # Get character from name and create a text item:
        char = qta.charmap(label)
        self.setText(char)

        # Set font and color:
        self.setFont(qta.font(prefix, self._width))
        self.setBrush(QtGui.QBrush(color or self._color))

    # Reimplement boundingRect to ensure proper sizing:
    def boundingRect(self) -> QtCore.QRectF:
        return super().boundingRect().adjusted(0, 0, 0, -1)
