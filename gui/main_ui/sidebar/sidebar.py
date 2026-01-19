# Filename: sidebar.py
# Module name: sidebar
# Description: Sidebar dock widget for the main window.

"""
Sidebar panel for the main application window.

Provides a dock widget containing a tabbed interface with various panels including
map query, schematics, settings, assistant, and database management.
"""

from PySide6 import QtWidgets


class SideBar(QtWidgets.QDockWidget):
    """
    Sidebar dock widget with tabbed panel interface.

    Manages multiple panels accessible via a dropdown menu in the title bar,
    including map query, schematic, settings, assistant, and database panels.
    """

    def __init__(self, parent=None):
        """
        Initialize the sidebar dock widget.

        Args:
            parent: Parent widget (optional).
        """

        super().__init__(parent)
        self.setMinimumWidth(360)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        self._init_titlebar()
        self._init_stack()

    def _init_titlebar(self) -> None:
        """Initialize the title bar with a combobox for panel selection."""

        from gui.widgets.combobox import ComboBox

        self.setTitleBarWidget(
            combo := ComboBox(
                self,
                items=[
                    ("mdi.map", "Map Query"),
                    ("mdi.sitemap", "Schematic"),
                    ("mdi.cog", "Settings"),
                    ("mdi.chat", "Assistant"),
                    ("mdi.database", "Database"),
                ],
            )
        )

        combo.setStyleSheet("margin: 2px 0px 1px 0px;")
        combo.currentIndexChanged.connect(self._on_page_changed)

    def _init_stack(self) -> None:
        """Initialize the stacked widget containing all sidebar panels."""

        from .geo_query import GeoQuery
        from .setting import Preferences

        self._stack = QtWidgets.QStackedWidget(self)

        # Add pages in order matching ComboBox indices
        self._stack.addWidget(QtWidgets.QFrame(self))  # 0: Map Control (placeholder)
        self._stack.addWidget(QtWidgets.QWidget(self))  # 1: Schematic (placeholder)
        self._stack.addWidget(Preferences(self))  # 2: Settings
        self._stack.addWidget(QtWidgets.QWidget(self))  # 3: Assistant (placeholder)
        self._stack.addWidget(QtWidgets.QWidget(self))  # 4: Database (placeholder)

        self.setWidget(self._stack)

    def _on_page_changed(self, index: int) -> None:
        """
        Handle page change when combobox selection changes.

        Args:
            index: Index of the selected page.
        """

        self._stack.setCurrentIndex(index)

    @property
    def map_data(self):
        """Get the map data widget (first stacked page)."""
        return self._stack.widget(0)
