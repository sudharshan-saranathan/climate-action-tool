from __future__ import annotations

import dataclasses
import logging
import platform

from PySide6 import QtCore, QtGui, QtWidgets
from qtawesome import icon as qta_icon

# Initialize logger
logger = logging.getLogger(__name__)


@dataclasses.dataclass
class TabViewOpts:
    max_tabs: int = 8


# A QTabWidget subclass with
class TabView(QtWidgets.QTabWidget):
    """
    A tab-switching widget based on QtWidgets.QTabWidget.

    Feature(s):
        - Create/close/rename tabs.
        - Configurable max-tabs.
    """

    # Initializer
    def __init__(self, parent: QtWidgets.QWidget | None = None, **kwargs):
        super().__init__(parent, **kwargs)

        # Connect the tab widget's signals to appropriate slots:
        self.setIconSize(QtCore.QSize(16, 16))
        self.tabCloseRequested.connect(self._on_tab_close)

        # Set font from application settings to ensure cross-platform consistency
        app = QtWidgets.QApplication.instance()
        if app and hasattr(app, "options"):
            fonts = app.options.fonts
            envir = platform.system().lower()
            if envir in fonts:
                font_spec = fonts[envir]
                self.setFont(QtGui.QFont(font_spec.family, font_spec.pointSize))

        # Shortcuts (using QKeySequence for cross-platform compatibility):
        QtGui.QShortcut(QtGui.QKeySequence.StandardKey.AddTab, self, self.create_tab)
        QtGui.QShortcut(QtGui.QKeySequence.StandardKey.Close, self, self.remove_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, self.rename_tab)

        # Create the initial map tab:
        self.create_tab(
            widget=TabView._create_map_view(),
            label="Map",
            icon=qta_icon("mdi.map", color="lightgreen"),
        )

    @staticmethod
    def _create_map_view() -> QtWidgets.QWidget:
        """
        Instantiates `Viewer` and sets a map-scene.
        """

        from gui.maps import Scene
        from gui.widgets.viewer import Viewer

        return Viewer(Scene())

    # Create a new tab:
    def create_tab(
        self,
        widget: QtWidgets.QWidget | None = None,
        label: str = "",
        icon: QtGui.QIcon | None = None,
    ) -> None:
        """
        Create a new tab.
        :param widget: The widget to display in the tab.
        :param label: The name of the new tab.
        :param icon: The icon for the new tab.
        :return: None
        """

        # Check if maximum tabs reached:
        if self.count() >= TabViewOpts().max_tabs:
            QtWidgets.QApplication.beep()
            return

        count = self.count()
        label = label or f"Tab {count + 1}"
        widget = widget or QtWidgets.QFrame()

        self.addTab(widget, label)
        self.setTabIcon(count, icon or qta_icon("mdi.tab", color="gray"))
        self.setCurrentIndex(count)

    def remove_tab(self) -> None:
        """
        Remove the current tab.
        :return:
        """
        self._on_tab_close(self.currentIndex())

    # Rename an existing tab:
    def rename_tab(self, index: int = -1, name: str = "") -> None:
        """
        Rename an existing tab.
        :param index: The index of the tab to rename.
        :param name: The new name for the tab.
        :return: None
        """

        # If no index provided, use the current tab:
        if index == -1:
            index = self.currentIndex()

        # If no name is provided, get name from user:
        name = (
            name
            or QtWidgets.QInputDialog.getText(self, "Tab Rename", "Enter new label:")[0]
        )

        # Rename the tab:
        if 0 <= index < self.count() and name:
            self.setTabText(index, name)

    # Remove the tab at the specified index:
    def _on_tab_close(self, index: int) -> None:
        """
        Remove the current tab.
        :param index: The index of the tab to remove.
        :return: None
        """

        # Remove the tab:
        if self.count() > 1:
            widget = self.widget(index)
            self.removeTab(index)
            if widget:
                widget.deleteLater()
        else:
            QtWidgets.QApplication.beep()
