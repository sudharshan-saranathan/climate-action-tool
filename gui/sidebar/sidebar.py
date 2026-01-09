# --
# Encoding: utf-8
# Module name: sidebar
# Description: The sidebar for the Climate Action Tool application
# --

# Import(s):
from PySide6 import QtWidgets


# Class Sidebar:
class SideBar(QtWidgets.QDockWidget):
    #   Default constructor:
    def __init__(self, parent=None):
        super().__init__(parent)

        # Attribute(s):
        self.setMinimumWidth(360)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Initialize the title bar widget:
        self._init_titlebar()
        self._init_stack()

    #   Title-bar widget (a QComboBox):
    def _init_titlebar(self):
        # Import ComboBox:
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

        self.titleBarWidget().setStyleSheet("margin: 2px 0px 2px 0px;")
        self.titleBarWidget().currentIndexChanged.connect(self._on_page_changed)

    #   Initialize the stacked widget:
    def _init_stack(self):
        from .geo_query import GeoQuery
        from .setting import GlobalSettings

        self._stack = QtWidgets.QStackedWidget(self)

        # Add pages in order matching ComboBox:
        # 0: Map, 1: Schematic, 2: Settings, 3: Assistant, 4: Database
        self._stack.addWidget(GeoQuery(self))  # 0: Map
        self._stack.addWidget(QtWidgets.QWidget(self))  # 1: Schematic (placeholder)
        self._stack.addWidget(GlobalSettings(self))  # 2: Settings
        self._stack.addWidget(QtWidgets.QWidget(self))  # 3: Assistant (placeholder)
        self._stack.addWidget(QtWidgets.QWidget(self))  # 4: Database (placeholder)

        self.setWidget(self._stack)

    #   Handle page change:
    def _on_page_changed(self, index: int):
        self._stack.setCurrentIndex(index)

    #   Access to MapData:
    @property
    def map_data(self):
        return self._stack.widget(0)
