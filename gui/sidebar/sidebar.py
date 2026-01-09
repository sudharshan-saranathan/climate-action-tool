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
                    ("mdi.cog", "Settings"),
                    ("mdi.sitemap", "Schematic"),
                    ("mdi.chat", "Assistant"),
                    ("mdi.database", "Database"),
                ],
            )
        )

        self.titleBarWidget().setStyleSheet("margin: 2px 0px 2px 0px;")

    #   Initialize the stacked widget:
    def _init_stack(self):

        from .setting import GlobalSettings

        settings = GlobalSettings(self)
        self._stack = QtWidgets.QStackedWidget(self)
        self._stack.addWidget(settings)
        self.setWidget(self._stack)
