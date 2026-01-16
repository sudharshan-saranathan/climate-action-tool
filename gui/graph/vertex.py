# Filename: vertex.py
# Module name: graph
# Description: Graph vertex nodes.

"""
Vertex items representing nodes in the graph.

Provides interactive vertex nodes (VertexItem) that can be connected via edges.
Each vertex has input/output anchors and can contain handles for connections.
Includes a resizable frame and visual styling with selection feedback.
"""

from __future__ import annotations
import logging
import copy
import types

from qtawesome import icon as qta_icon
from PySide6 import QtGui, QtCore, QtWidgets

from gui.graph.enums import ItemState, ItemRole
from core.bus import EventsBus
from gui.custom import Image, Label
from gui.graph.anchor import AnchorItem
from gui.graph.handle import HandleItem


# Default vertex options
VertexOpts = {
    "corner-radius": 4,
    "frame": QtCore.QRectF(-36, -40, 72, 68),
    "board": {
        "corner-radius": 4,
        "frame": QtCore.QRectF(-36, -28, 72, 56),
        "brush": QtGui.QBrush(QtGui.QColor(0xFFFFFF)),
    },
    "style": {
        "pen": {
            "normal": QtGui.QPen(QtGui.QColor(0x232A2E), 2.0),
            "select": QtGui.QPen(QtGui.QColor(0xFFCB00), 2.0),
        },
        "brush": {
            "normal": QtGui.QBrush(QtGui.QColor(0x232A2E)),
            "select": QtGui.QBrush(QtGui.QColor(0xFFCB00)),
        },
    },
}


# Class ResizeHandle:
class ResizeHandle(QtWidgets.QGraphicsObject):
    """A resizable handle at the bottom of a vertex."""

    sig_resize_handle_moved = QtCore.Signal()

    def __init__(self, **kwargs):
        super().__init__(kwargs.get("parent", None))
        self.setProperty("frame", kwargs.get("frame", QtCore.QRectF(-32, -2, 64, 4)))
        self.sig_resize_handle_moved.connect(kwargs.get("callback", None))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemSendsScenePositionChanges)

    def boundingRect(self) -> QtCore.QRectF:
        return self.property("frame").adjusted(-2, -2, 2, 2)

    def paint(self, painter, option, /, widget=...):
        painter.setPen(QtGui.QPen(QtCore.Qt.PenStyle.NoPen))
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.boundingRect(), 2, 2)

    def itemChange(self, change, value, /):
        if change == QtWidgets.QGraphicsObject.GraphicsItemChange.ItemPositionHasChanged:
            if self.scene():
                self.scene().clearSelection()
            self.sig_resize_handle_moved.emit()
        return value


# Class VertexItem
class VertexItem(QtWidgets.QGraphicsObject):
    """A vertex node in the graph."""

    sig_item_created = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_clicked = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_updated = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_focused = QtCore.Signal(QtWidgets.QGraphicsObject)
    sig_item_deleted = QtCore.Signal(QtWidgets.QGraphicsObject)

    def __init__(
        self,
        cpos: QtCore.QPointF,
        parent: QtWidgets.QGraphicsObject | None = None,
        **kwargs,
    ):
        super().__init__(parent)

        self.setPos(cpos)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsObject.GraphicsItemFlag.ItemIsSelectable)

        self.setProperty("style", VertexOpts["style"])

        self.database = types.SimpleNamespace(inp=dict(), out=dict(), par=dict(), eqn=list())

        self.attr = {
            "id": id(self),
            "name": kwargs.get("name", "Process"),
            "icon": kwargs.get("icon", None),
            "limit": VertexOpts["frame"].bottom(),
            "frame": QtCore.QRectF(kwargs.get("frame", VertexOpts["frame"])),
        }

        self._inp_anchor = AnchorItem(
            ItemRole.INP.value,
            parent=self,
            cpos=QtCore.QPointF(self.attr["frame"].left(), 0),
            callback=self._on_anchor_clicked,
        )
        self._out_anchor = AnchorItem(
            ItemRole.OUT.value,
            parent=self,
            cpos=QtCore.QPointF(self.attr["frame"].right(), 0),
            callback=self._on_anchor_clicked,
        )

        self._resize_handle = ResizeHandle(parent=self, callback=self._on_resize_handle_moved)
        self._resize_handle.moveBy(0, self.attr["frame"].bottom())

        self._image = Image(
            parent=self,
            buffer=":/svg/component.svg",
            size=QtCore.QSize(32, 32),
        )
        self._image.setOpacity(0.20)

        self._label = Label(
            parent=self,
            label=self.attr["name"],
            width=self.attr["frame"].width() - 4,
            color=QtCore.Qt.GlobalColor.white,
        )
        self._label.setX(self.attr["frame"].left() + 2)
        self._label.setY(self.attr["frame"].top() - 2)
        self._label.sig_text_changed.connect(self._on_text_changed)

        self._menu = self._init_menu()
        self._register_with_bus()

    def _init_menu(self):
        menu = QtWidgets.QMenu()
        edit = menu.addAction(qta_icon("mdi.pencil"), "Configure", self.open_configuration_widget)
        lock = menu.addAction(qta_icon("mdi.lock"), "Lock")
        delete = menu.addAction(
            qta_icon("mdi.delete"), "Delete", lambda: self.sig_item_deleted.emit(self)
        )

        edit.setIconVisibleInMenu(True)
        lock.setIconVisibleInMenu(True)
        delete.setIconVisibleInMenu(True)

        lock.setCheckable(True)
        lock.setChecked(False)

        return menu

    def _register_with_bus(self):
        bus = EventsBus.instance()
        self.sig_item_created.connect(bus.sig_item_created)
        self.sig_item_clicked.connect(bus.sig_item_clicked)
        self.sig_item_updated.connect(bus.sig_item_updated)
        self.sig_item_focused.connect(bus.sig_item_focused)
        self.sig_item_deleted.connect(bus.sig_item_deleted)

    def _set_limit(self, handle: HandleItem):
        ymin = self.mapRectFromItem(self._inp_anchor, self._inp_anchor.boundingRect()).top()
        ymax = self.attr["frame"].bottom() - 6
        handle.setProperty("ymin", ymin)
        handle.setProperty("ymax", ymax)

    def _add_to_database(self, handle: HandleItem):
        if handle.attr["role"] == ItemRole.INP:
            self.database.inp[handle] = handle
        else:
            self.database.out[handle] = handle

    def boundingRect(self) -> QtCore.QRectF:
        return self.attr["frame"].adjusted(-4, -4, 4, 4)

    def paint(self, painter, option, /, widget=...):
        pen = self.property("style")["pen"]["select" if self.isSelected() else "normal"]
        brush = self.property("style")["brush"]["select" if self.isSelected() else "normal"]

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRoundedRect(
            self.attr["frame"],
            VertexOpts["corner-radius"],
            VertexOpts["corner-radius"],
        )

        painter.setBrush(VertexOpts["board"]["brush"])
        painter.drawRoundedRect(
            self.attr["frame"].adjusted(0, 16, -0, -0),
            VertexOpts["board"]["corner-radius"],
            VertexOpts["board"]["corner-radius"],
        )

    def contextMenuEvent(self, event) -> None:
        super().contextMenuEvent(event)
        if event.isAccepted():
            return

        if self.scene():
            self.scene().clearSelection()
            self.setSelected(True)

        if hasattr(self, "_menu"):
            self._menu.exec(event.screenPos())
            event.accept()

    def hoverEnterEvent(self, event) -> None:
        super().setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event, /):
        super().unsetCursor()
        super().hoverLeaveEvent(event)

    def mouseDoubleClickEvent(self, event, /):
        self.open_configuration_widget()
        super().mouseDoubleClickEvent(event)

    @QtCore.Slot()
    def _on_resize_handle_moved(self):
        limit = self.attr["limit"]
        frame = self.attr["frame"]
        floor = max(
            [
                handle.y()
                for handle in list(self.database.inp.keys()) + list(self.database.out.keys())
            ]
            or [limit]
        )

        frame.setBottom(max(self._resize_handle.y(), max(floor, limit) + 6))
        self.attr["frame"] = frame

        self._resize_handle.setX(0)
        self._resize_handle.setY(frame.bottom())
        self._inp_anchor.resize(frame.bottom() - 6)
        self._out_anchor.resize(frame.bottom() - 6)

        for handle in list(self.database.inp.keys()) + list(self.database.out.keys()):
            self._set_limit(handle)

        self.update(self.boundingRect().adjusted(-2, -48, 2, 48))

    @QtCore.Slot(QtCore.QPointF)
    def _on_anchor_clicked(self, cpos: QtCore.QPointF):
        anchor = self.sender()
        if not isinstance(anchor, AnchorItem):
            return

        coords = self.mapFromItem(anchor, cpos)
        handle = self.create_handle(
            (
                ItemRole.INP
                if anchor is self._inp_anchor
                else ItemRole.OUT
            ),
            coords,
        )

        self.sig_item_clicked.emit(handle)
        self.sig_item_created.emit(handle)

    @QtCore.Slot(str)
    def _on_text_changed(self, text: str):
        self.attr["name"] = text
        self.sig_item_updated.emit(self)

    def serialize_to_dict(self) -> dict:
        inp = [
            handle.serialize_to_dict()
            for handle in self.database.inp.keys()
            if hasattr(handle, "serialize_to_dict")
        ]
        out = [
            handle.serialize_to_dict()
            for handle in self.database.out.keys()
            if hasattr(handle, "serialize_to_dict")
        ]
        par = copy.deepcopy(self.database.par)

        data = {
            "attr": copy.deepcopy(self.attr),
            "database": {"inp": inp, "out": out, "par": par},
            "cpos": {"x": self.scenePos().x(), "y": self.scenePos().y()},
        }

        return data

    def create_handle(self, role: ItemRole | str, cpos: QtCore.QPointF) -> HandleItem:
        """Create a new handle at the specified position."""
        if isinstance(role, str):
            role = (
                ItemRole.INP if role.upper() == "INP" else ItemRole.OUT
            )

        handle = HandleItem(
            role,
            cpos,
            self,
        )

        self._set_limit(handle)
        self._add_to_database(handle)

        return handle

    def create_parameter(self, name: str = "Parameter", /):
        """Create a new parameter."""
        self.database.par[name] = True
        self.sig_item_updated.emit(self)

    def clone(self) -> "VertexItem":
        """Clone this vertex at an offset position."""
        vertex = VertexItem(
            cpos=self.scenePos() + QtCore.QPointF(25, 25),
            name=self.attr["name"],
            icon=self.attr["icon"],
            limit=self.attr["limit"],
            frame=self.attr["frame"],
        )

        inp = list(self.fetch_items(ItemRole.INP, ItemState.ACTIVE))
        out = list(self.fetch_items(ItemRole.OUT, ItemState.ACTIVE))

        for handle in inp + out:
            new_handle = vertex.create_handle(handle.attr["role"], handle.pos())
            new_handle.attr = copy.deepcopy(handle.attr)
            new_handle.set_stream(handle.attr["flow"].LABEL)

        return vertex

    def fetch_items(self, role: ItemRole, state: ItemState) -> list:
        """Fetch items of a specific role and state."""
        if role == ItemRole.INP:
            return [
                handle
                for handle in self.database.inp
                if handle.isVisible() == bool(state)
            ]

        elif role == ItemRole.OUT:
            return [
                handle
                for handle in self.database.out
                if handle.isVisible() == bool(state)
            ]

        elif role == ItemRole.PAR:
            return self.database.par

        elif role == ItemRole.EQN:
            return self.database.eqn

        return list()

    def open_configuration_widget(self):
        """Open the configuration widget for this vertex."""
        self.sig_item_focused.emit(self)

    def icon(self):
        """Get the vertex's icon."""
        return self._image.to_icon()

    def deregister(self, handle: HandleItem):
        """Deregister a handle from the database."""
        if not handle.isVisible():
            self.database.inp.pop(handle, None)
            self.database.out.pop(handle, None)
