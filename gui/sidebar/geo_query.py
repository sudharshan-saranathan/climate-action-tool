# Encoding: utf-8
# Filename: mapdata.py
# Description: A widget with controls to filter or view geotagged items.

# Imports (standard)
from __future__ import annotations

# Imports (third party)
from PySide6 import QtCore, QtWidgets

# Imports (local)
from gui.widgets import HLayout, VLayout


# Class GeoView:
class GeoQuery(QtWidgets.QTreeWidget):
    """
    A widget with controls to filter or view geotagged items.
    """

    # Initializer:
    def __init__(self, parent=None):
        super().__init__(parent)

        # Define top-level items:
        self.addTopLevelItem(QtWidgets.QTreeWidgetItem(["Sectors"]))
        self.addTopLevelItem(QtWidgets.QTreeWidgetItem(["Filters"]))
