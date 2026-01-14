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

    # Signals:
    sig_open_project = QtCore.Signal(str)
    sig_clone_project = QtCore.Signal(str)
    sig_delete_project = QtCore.Signal(str)

    # Default constructor:
    def __init__(self, name: str, path: str = "", **kwargs):

        # Super-class initialization:
        super().__init__(None)
        super().setMouseTracking(True)
        super().setProperty("project", name)

        self._project_name = name
        self._project_path = path

        # Layout:
        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)

        self._project_label = QtWidgets.QLabel(name)
        self._project_acts = self._project_actions()
        self._buttons = kwargs.get("buttons", [])

        layout.addWidget(self._project_label, 0, 0)
        layout.addWidget(self._project_acts, 0, 1)

    # Project actions:
    def _project_actions(self):

        toolbar = ToolBar(
            iconSize=QtCore.QSize(18, 18),
            actions=[
                (
                    qta_icon("ph.upload-simple", color="gray", color_active="white"),
                    "Open Project",
                    lambda path=self._project_path: self.sig_open_project.emit(path),
                ),
                (
                    qta_icon(
                        "ph.shield-check-fill", color="gray", color_active="white"
                    ),
                    "Open Project (Safe Mode)",
                    lambda path=self._project_path: self.sig_open_project.emit(path),
                ),
                (
                    qta_icon(
                        "mdi.plus-circle-multiple-outline",
                        color="gray",
                        color_active="white",
                    ),
                    "Clone Project",
                    lambda path=self._project_path: self.sig_clone_project.emit(path),
                ),
                (
                    qta_icon("mdi.delete", color="gray", color_active="red"),
                    "Delete Project",
                    lambda path=self._project_path: self.sig_delete_project.emit(path),
                ),
            ],
        )

        toolbar.hide()  # Hide the actions by default.
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
        columns: list[str] = dataclasses.field(
            default_factory=lambda: ["Projects", "Last Modified"]
        )

    def __init__(self, parent=None):

        # Initialize options:
        self._opts = StartupFileTable.Options()

        # Initialize parent class:
        super().__init__(parent, columnCount=len(self._opts.columns))

        # Set attribute(s):
        self.setShowGrid(False)
        self.setIconSize(self._opts.icon_size)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        self.setColumnWidth(1, 120)
        self.setHorizontalHeaderLabels(self._opts.columns)
        self.verticalHeader().setVisible(False)

        # Adjust column resizing policy:
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def paintEvent(self, event):
        super().paintEvent(event)  # Call base-class implementation

        # Paint an empty indicator if the table is empty:
        if self.rowCount() == 0:

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
        file_item = FileTableItem(path.stem, path=str(path))
        self.setCellWidget(row, 0, file_item)
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

        self.setHorizontalHeaderLabels([stem, self._opts.columns[1]])
        for item in Path(directory).glob(pattern):
            stat = item.stat().st_mtime  # Last modified time
            date = datetime.fromtimestamp(stat)  # Convert to datetime
            time = date.strftime("%Y-%m-%d")  # Format as string

            self.add_item(item, time)
