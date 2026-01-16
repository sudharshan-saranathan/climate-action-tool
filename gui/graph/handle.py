# Filename: handle.py
# Module name: graph
# Description: Connection handles for graph vertices.

"""
Handle items for input/output connections on graph vertices.

Provides interactive connection points (HandleItem) that can be connected to other handles
via edges. Supports different stream types and visual feedback for connections.
"""

from __future__ import annotations
from typing import Any
import logging
import enum

from qtawesome import icon as qta_icon
from PySide6 import QtCore, QtGui, QtWidgets

from gui.graph.enums import ItemRole
from core.bus import EventsBus
from core.stream import Stream, BasicFlows, ComboFlows
from gui.graph.vector import VectorItem
from gui.custom import QtaItem


# Default options for HandleItem
HandleOpts = {
    "frame": QtCore.QRectF(-1.5, -1.5, 3, 3),
    "color": 0xB4F7D2,
}

logger = logging.getLogger(__name__)


# Enum HandleConnectivity
class HandleConnectivity(enum.Enum):
    ONE_TO_ONE = enum.auto()
    MANY_TO_MANY = enum.auto()


# Class HandleItem
class HandleItem(QtWidgets.QGraphicsObject):
    """Handles represent input/output connection points on vertices."""

    # Signals
    sig_stream_changed = QtCore.Signal(type(Stream))
    sig_item_created = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_clicked = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_deleted = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_moved = QtCore.Signal(QtWidgets.QGraphicsObject)

    # Clone registry for copy/paste
    clone_registry: dict["HandleItem", "HandleItem"] = {}

    def __init__(
        self,
        role: ItemRole,
        position: QtCore.QPointF,
        parent: QtWidgets.QGraphicsObject | QtWidgets.QGraphicsItem | None = None,
        **kwargs,
    ):
        super().__init__(parent)
        super().visibleChanged.connect(self._on_visibility_changed)

        self._connectivity = kwargs.get("connectivity", HandleConnectivity.ONE_TO_ONE)
        self._snap = kwargs.get("snap", True)

        self.attr = {
            "id": id(self),
            "role": role,
            "xpos": position.x(),
            "name": kwargs.get("name", "Resource"),
            "flow": kwargs.get("flow", BasicFlows["ItemFlow"]),
            "frame": QtCore.QRectF(kwargs.get("frame", HandleOpts["frame"])),
            "color": QtGui.QColor(kwargs.get("color", HandleOpts["color"])),
            "icon-size": kwargs.get("icon-size", 12),
        }

        self.setProperty("ymin", kwargs.get("ymin", -float("inf")))
        self.setProperty("ymax", kwargs.get("ymax", float("inf")))

        self._icon = self._set_icon(self.attr["flow"])
        self._anim = self._init_anim()
        self._menu = self._init_menu()

        self.connected = False
        self.conjugate = None
        self.connector = None

        self.setPos(position)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemSendsScenePositionChanges)

        self._bus = EventsBus.instance()
        self.sig_item_created.connect(self._bus.sig_item_created.emit)
        self.sig_item_clicked.connect(self._bus.sig_item_clicked.emit)
        self.sig_item_deleted.connect(self._bus.sig_item_deleted.emit)

    def __getitem__(self, key: str):
        if key in self.dynamicPropertyNames():
            return self.property(key)
        return None

    def __setitem__(self, key: str, value: Any) -> None:
        self.setProperty(key, value)

    def _init_menu(self) -> QtWidgets.QMenu:
        self._menu = QtWidgets.QMenu()
        self._flow_submenu = self._menu.addMenu("Stream")
        pencil = self._menu.addAction(qta_icon("mdi.pencil"), "Configure")
        unpair = self._menu.addAction(
            qta_icon("mdi.link-off", color="#ffcb00"), "Unpair", self._on_unpaired
        )
        self._menu.addSeparator()
        delete = self._menu.addAction(
            qta_icon("mdi.delete", color="red"),
            "Delete",
            lambda: self.sig_item_deleted.emit(self),
        )
        pencil.setIconVisibleInMenu(True)
        unpair.setIconVisibleInMenu(True)
        delete.setIconVisibleInMenu(True)
        return self._menu

    def _init_anim(self) -> QtCore.QPropertyAnimation:
        animation = QtCore.QPropertyAnimation(self, b"radius")
        animation.setEasingCurve(QtCore.QEasingCurve.Type.OutQuad)
        animation.setDuration(240)
        return animation

    def _set_icon(self, cls: type[Stream]) -> QtaItem:
        width = self.attr["icon-size"]
        icon = QtaItem(cls.ICON, color=cls.COLOR, width=width, parent=self)
        icon.setParentItem(self)
        icon.setPos(
            QtCore.QPointF(-4 - width if self.attr["role"] == ItemRole.OUT else 4, -width / 2 - 1)
        )
        return icon

    def _animate(
        self,
        start: float,
        final: float,
        duration: int = 240,
    ) -> None:
        self._anim.setDuration(duration)
        self._anim.setStartValue(start)
        self._anim.setEndValue(final)
        self._anim.start()

    def boundingRect(self, /):
        frame = self.attr["frame"]
        frame = (
            frame.adjusted(-20, -4, 4, 4)
            if self.attr["role"] == ItemRole.OUT
            else frame.adjusted(-4, -4, 20, 4)
        )
        return frame

    def paint(self, painter, option, widget=...):
        color = QtGui.QColor(self.attr["color"])
        brush = QtGui.QBrush(color)
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 0.50)

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(self.attr["frame"])

        if self.isUnderMouse():
            frame = self.attr["frame"].adjusted(0.75, 0.75, -0.75, -0.75)
            painter.setBrush(QtCore.Qt.GlobalColor.black)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawEllipse(frame)

    def itemChange(self, change, value, /):
        sc_changed = QtWidgets.QGraphicsObject.GraphicsItemChange.ItemSceneHasChanged
        sp_changed = QtWidgets.QGraphicsObject.GraphicsItemChange.ItemScenePositionHasChanged

        if change == sc_changed and value:
            self.sig_item_created.emit(self)

        if change == sp_changed:
            self.sig_item_moved.emit(self)

        return super().itemChange(change, value)

    def contextMenuEvent(self, event, /):
        self._flow_submenu.clear()
        self.setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemIsMovable, False)

        for key, stream in (BasicFlows | ComboFlows).items():
            icon = qta_icon(stream.ICON, color=stream.COLOR)
            text = stream.LABEL

            action = self._flow_submenu.addAction(icon, text, lambda t=text: self.set_stream(t))
            action.setIconVisibleInMenu(True)
            action.setCheckable(True)

            if self.attr["flow"].LABEL == action.text():
                action.setChecked(True)
                action.setIcon(qta_icon("mdi.check-bold", color="#efefef"))

        event.accept()
        self._menu.exec(event.screenPos())

    def hoverEnterEvent(self, event, /):
        super().hoverEnterEvent(event)
        super().setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        radius = HandleOpts["frame"].width() / 2
        self._animate(radius, radius + 0.5)

    def hoverLeaveEvent(self, event, /):
        super().hoverLeaveEvent(event)
        super().unsetCursor()
        radius = HandleOpts["frame"].width() / 2
        self._animate(radius + 0.5, radius)

    def mousePressEvent(self, event, /):
        if self.scene():
            self.scene().clearSelection()

        if not self.connected and event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.sig_item_clicked.emit(self)
        else:
            super().setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemIsMovable, True)
            super().mousePressEvent(event)
            event.accept()

    def mouseReleaseEvent(self, event, /):
        if self.connected:
            xpos = self.attr["xpos"] if self._snap else self.pos().x()
            ymax = self.property("ymax")
            ymin = self.property("ymin")
            ypos = max(min(self.pos().y(), ymax), ymin)
            self.setPos(QtCore.QPointF(xpos, ypos))

        super().setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemIsMovable, False)
        super().mouseReleaseEvent(event)

    def pair(self, connector: QtWidgets.QGraphicsObject, conjugate: "HandleItem") -> None:
        """Connect this handle to another via a connector."""
        self.connected = True
        self.connector = connector
        self.conjugate = conjugate

    def free(self, mirror: bool = True) -> None:
        """Disconnect this handle from its partner."""
        if mirror and self.connector and self.conjugate:
            self.connector.hide()
            self.conjugate.free(mirror=False)

        self.connected = False
        self.connector = None
        self.conjugate = None

    def hide(self):
        if self.connected:
            self.conjugate.free(mirror=False)
            self.setEnabled(False)
            self.blockSignals(True)
        super().hide()

    def show(self):
        if self.connected:
            self.conjugate.pair(self.connector, self)
            self.blockSignals(True)
            self.setEnabled(True)
        super().show()

    def set_stream(
        self,
        stream: str,
        mirror: bool = True,
    ) -> None:
        """Set the stream type for this handle."""
        cls: type[Stream] | None = next(
            (flow for flow in (BasicFlows | ComboFlows).values() if flow.LABEL == stream),
            None,
        )

        if cls is not None:
            self.attr["flow"] = cls
            self._icon.render_icon(cls.ICON, cls.COLOR)

            if mirror and self.connector and self.conjugate:
                self.connector.color = cls.COLOR
                self.conjugate.set_stream(stream, mirror=False)

        self.sig_stream_changed.emit(self.attr["flow"])

    @QtCore.Slot()
    def _on_visibility_changed(self) -> None:
        if not self.connected:
            return

        visible = self.isVisible()
        if visible:
            self.conjugate.pair(self.connector, self)
            self.connector.show()
        else:
            self.conjugate.free(mirror=False)
            self.connector.hide()

    @QtCore.Slot()
    def _on_unpaired(self) -> None:
        self.free()

    @QtCore.Property(float)
    def radius(self) -> float:
        return float(self.attr["frame"].width() / 2.0)

    @radius.setter
    def radius(self, value: float) -> None:
        self.attr["frame"] = QtCore.QRectF(-value, -value, value * 2, value * 2)
        self.update()
