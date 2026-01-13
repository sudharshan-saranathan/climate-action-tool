# Filename: ftable.py
# Module name: startup
# Description: A QTableWidget subclass that displays projects.

from __future__ import annotations
from pathlib import Path

import dataclasses
from qtawesome import icon as qta_icon
from PySide6 import QtGui, QtCore, QtWidgets

from gui.widgets import ToolBar


# Widget representing a single file/project, added to the FileTable:
class FileTableItem(QtWidgets.QWidget):

    # Default constructor:
    def __init__(self, name: str, **kwargs):

        # Super-class initialization:
        super().__init__(None)
        super().setMouseTracking(True)
        super().setProperty("project", name)

        # Layout:
        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        self._project_name = QtWidgets.QLabel(name)
        self._project_acts = self._project_actions()
        self._buttons = kwargs.get("buttons", [])

        layout.addWidget(self._project_name, 0, 0)
        layout.addWidget(self._project_acts, 0, 1)

    # Project actions:
    @staticmethod
    def _project_actions():

        toolbar = ToolBar(
            iconSize=QtCore.QSize(20, 20),
            actions=[
                (qta_icon("mdi.share", color="#efefef"), "Share Project", None),
                (qta_icon("mdi.pencil", color="#efefef"), "Edit Project", None),
                (
                    qta_icon("mdi.dots-horizontal", color="#efefef"),
                    "More Options",
                    None,
                ),
            ],
        )

        toolbar.hide()  # Hide these icons by default
        return toolbar

    # Reimplementation of QWidget.enterEvent():
    def enterEvent(self, event, /):
        self._project_acts.show()

    # Reimplementation of QWidget.leaveEvent():
    def leaveEvent(self, event, /):
        self._project_acts.hide()


# Table of models:
class StartupFileTable(QtWidgets.QTableWidget):

    @dataclasses.dataclass
    class Options:
        row_height: int = 36
        icon_size: QtCore.QSize = dataclasses.field(
            default_factory=lambda: QtCore.QSize(16, 16)
        )
        empty_icon_opacity: float = 0.2
        header_labels: list[str] = dataclasses.field(
            default_factory=lambda: ["Projects", "Last Modified"]
        )

    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent, columnCount=2)

        # Initialize options:
        self._opts = StartupFileTable.Options()

        # Set attribute(s):
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setIconSize(self._opts.icon_size)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        self.setColumnWidth(1, 120)
        self.setHorizontalHeaderLabels(self._opts.header_labels)
        self.verticalHeader().setVisible(False)

        # Adjust column resizing policy:
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

    #   Reimplementation of QTableWidget.paintEvent():
    def paintEvent(self, event):

        super().paintEvent(event)  # Call base-class implementation

        if self.rowCount() == 0:  # If the table is empty:

            painter = QtGui.QPainter(self.viewport())
            painter.setOpacity(self._opts.empty_icon_opacity)
            icon = QtGui.QIcon(":/png/empty.png")
            icon.paint(painter, self.viewport().rect())

            painter.drawText(
                self.viewport().rect(),
                QtCore.Qt.AlignmentFlag.AlignCenter,
                "No items found",
            )
            painter.end()

    #   Reimplementation of QTableWidget.mousePressEvent():
    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            item = self.itemAt(event.pos())
            if item is None:
                self.clearSelection()  # This will also emit the `selectionChanged()` signal to re-disable the "Open" button

        super().mousePressEvent(event)  # Call base-class implementation

    # Method to add a new row:
    def add_item(self, path: Path, time: str):

        row = self.rowCount()  # Get the current row count
        self.insertRow(self.rowCount())  # Insert a new row at the end

        # The second column displays the last modified time:
        item_second_column = QtWidgets.QTableWidgetItem(time)
        item_second_column.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item_second_column.setFlags(
            item_second_column.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable
        )

        # Change the icon based on whether the item is a directory or not:
        item_first_column = QtWidgets.QTableWidgetItem(
            QtGui.QIcon(":/logo/logo.png"), str()
        )

        self.setRowHeight(row, self._opts.row_height)
        self.setCellWidget(row, 0, FileTableItem(path.stem))
        self.setItem(row, 1, item_second_column)
        self.setItem(row, 0, item_first_column)

    # Show all models in the specified directory:
    def populate(self, directory: str, pattern: str):

        # Import pathlib:
        from pathlib import Path
        from datetime import datetime

        # Check validity of directory:
        base = Path(directory)
        if not base.is_dir():
            return

        self.clearContents()
        self.setRowCount(0)

        stem = Path(directory).stem  # Get the stem of the directory name
        stem = stem.capitalize()  # Capitalize the first letter

        self.setHorizontalHeaderLabels([stem, self._opts.header_labels[1]])
        for item in Path(directory).glob(pattern):
            stat = item.stat().st_mtime  # Last modified time
            date = datetime.fromtimestamp(stat)  # Convert to datetime
            time = date.strftime("%Y-%m-%d")  # Format as string

            self.add_item(item, time)
