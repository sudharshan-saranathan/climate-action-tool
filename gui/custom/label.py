# Filename: label.py
# Module name: custom
# Description: Editable text labels for graphics scenes.

"""
QGraphicsTextItem-based labels for graph items.

Provides customizable text labels (Label) that can be edited in place on a QGraphicsScene.
Supports styling, font customization, and signals for text changes.
"""

from __future__ import annotations
from PySide6.QtCore import Qt, Signal, QPointF
from PySide6.QtGui import QTextCursor, QPen, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QStyle


LabelOpts = {
    "const": False,
    "round": 4,
    "coord": QPointF(0, 0),
    "style": {
        "border": Qt.GlobalColor.transparent,
        "background": Qt.GlobalColor.transparent,
    },
    "label": {
        "font": QFont("Trebuchet MS", 7),
        "color": Qt.GlobalColor.black,
        "align": Qt.AlignmentFlag.AlignCenter,
        "width": 80,
    },
}


class Label(QGraphicsTextItem):
    """A QGraphicsTextItem with customizable styling and text editing."""

    sig_text_changed = Signal(str, name="Label.sig_text_changed")

    def __init__(self, label: str, parent: QGraphicsItem | None = None, **kwargs):
        super().__init__(label, parent)
        super().setAcceptHoverEvents(True)

        self.setProperty("const", kwargs.get("const", LabelOpts["const"]))
        self.setProperty("round", kwargs.get("round", LabelOpts["round"]))
        self.setProperty("style", kwargs.get("style", LabelOpts["style"]))

        self.setProperty("text-color", kwargs.get("color", LabelOpts["label"]["color"]))
        self.setProperty("text-width", kwargs.get("width", LabelOpts["label"]["width"]))
        self.setProperty("text-align", kwargs.get("align", LabelOpts["label"]["align"]))
        self.setProperty("text-font", kwargs.get("font", LabelOpts["label"]["font"]))

        self.setFont(self.property("text-font"))
        self.setTextWidth(self.property("text-width"))
        self.setDefaultTextColor(self.property("text-color"))
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditorInteraction
            if not self.property("const")
            else Qt.TextInteractionFlag.NoTextInteraction
        )

        option = self.document().defaultTextOption()
        option.setAlignment(self.property("text-align"))
        self.document().setDefaultTextOption(option)

    def paint(self, painter, option, widget):
        option.state = QStyle.StateFlag.State_None
        painter.setPen(QPen(self.property("style")["border"], 0.75))
        painter.setBrush(self.property("style")["background"])
        painter.drawRoundedRect(
            self.boundingRect(), self.property("round"), self.property("round")
        )
        super().paint(painter, option, widget)

    def edit(self):
        if self.property("const"):
            return
        self.setFocus(Qt.FocusReason.OtherFocusReason)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.clearFocus()
            event.accept()
            return
        super().keyPressEvent(event)

    def focusInEvent(self, event):
        if self.property("const"):
            return
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        string = self.toPlainText().strip()
        self.sig_text_changed.emit(string)
        self.textCursor().clearSelection()
        super().focusOutEvent(event)

    def hoverEnterEvent(self, event):
        if not self.property("const"):
            self.setCursor(Qt.CursorShape.IBeamCursor)
            self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if not self.property("const"):
            self.setCursor(Qt.CursorShape.IBeamCursor)
            self.update()
        super().hoverLeaveEvent(event)

    @property
    def const(self):
        return self.property("const")

    @const.setter
    def const(self, value: bool):
        self.setProperty("const", value)
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.NoTextInteraction
            if value
            else Qt.TextInteractionFlag.TextEditorInteraction
        )
        self.update()
