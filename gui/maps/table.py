# Encoding: utf-8
# Module name: table
# Description: A QTableWidget wrapper for displaying tabular data

# Imports (standard)
from __future__ import annotations

# Imports (third party)
import pandas
from PySide6 import QtCore, QtWidgets


# Class Table:
class Table(QtWidgets.QTableWidget):
    """A QTableWidget for displaying pandas DataFrame data."""

    # Initializer:
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)

        # Configure table settings:
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)

    # Load data from a pandas DataFrame:
    def load_data(self, data: pandas.DataFrame):
        """Load data from a pandas DataFrame into the table."""
        self.clear()
        self.setRowCount(data.shape[0])
        self.setColumnCount(data.shape[1])
        self.setHorizontalHeaderLabels(data.columns.tolist())

        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                item = QtWidgets.QTableWidgetItem(str(data.iat[row, col]))
                self.setItem(row, col, item)
