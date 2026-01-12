from __future__ import annotations

import dataclasses
import logging

from PySide6 import QtCore, QtWidgets


class TabView(QtWidgets.QTabWidget):

    @dataclasses.dataclass
    class Options:
        max_tabs: int = 8

    def __init__(self, parent: QtWidgets.QWidget, **kwargs):
        super().__init__(
            parent,
            tabsClosable=kwargs.get("tabsClosable", True),
            tabPosition=kwargs.get("position", QtWidgets.QTabWidget.TabPosition.North),
            movable=kwargs.get("movable", True),
        )

        # Add a default tab:
        self.new_tab()

    def new_tab(self, widget: QtWidgets.QWidget | None = None):

        count = self.count()
        label = f"New Tab {count + 1}"

        widget = widget or QtWidgets.QGraphicsView(self)
        self.addTab(widget, label)
