# Encoding: utf-8
# Filename: mapdata.py
# Description: A widget with controls to filter or view geotagged items.

# Imports (standard)
from __future__ import annotations

# Imports (third party)
from PySide6 import QtCore, QtWidgets

# Imports (local)
from gui.widgets import CollapsibleSection, HLayout, VLayout


# Class GeoView:
class GeoQuery(QtWidgets.QTreeWidget):
    """
    A widget with controls to filter or view geotagged items.
    """

    # Initializer:
    def __init__(self, parent=None):
        super().__init__(parent)  # Pass parent to super-class constructor

        # Customize behaviour:
        self.setHeaderHidden(True)
        self.setUniformRowHeights(True)

        # Collapsible sections:
        self._sectors = CollapsibleSection("Sectors")
        self._filters = CollapsibleSection("Filters")

        # Add the collapsible sections to the layout:
        layout = VLayout(spacing=0)
        layout.addWidget(self._sectors)
        layout.addWidget(self._filters)
        layout.addStretch(10)
        self.setLayout(layout)
