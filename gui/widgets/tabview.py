# Encoding: utf-8
# Module name: tabview
# Description: A tab-switching widget for the Climate Action Tool

# Imports (standard)
from __future__ import annotations
import logging

# Imports (third party)
from qtawesome import icon as qta_icon
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Initialize logger
logger = logging.getLogger(__name__)

TAB_VIEW_OPTS = {
    "max-tabs": 8,
}


# Tab switcher class:
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

        # Shortcuts (using QKeySequence for cross-platform compatibility):
        QtGui.QShortcut(QtGui.QKeySequence.StandardKey.AddTab, self, self.create_tab)
        QtGui.QShortcut(QtGui.QKeySequence.StandardKey.Close, self, self.remove_tab)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, self.rename_tab)

        # Create an initial tab with a placeholder:
        self.create_tab(
            widget=self._create_placeholder(),
            label="Welcome",
            icon=qta_icon("mdi.home", color="lightblue"),
        )

    # Create a placeholder widget for empty tabs
    def _create_placeholder(self) -> QtWidgets.QWidget:
        placeholder = QtWidgets.QLabel("Open a project or create a new model to get started.")
        placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return placeholder

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
        if self.count() >= TAB_VIEW_OPTS["max-tabs"]:
            QtWidgets.QApplication.beep()
            return

        count = self.count()
        label = label or f"Tab {count + 1}"
        widget = widget or self._create_placeholder()

        self.addTab(widget, label)
        self.setTabIcon(count, icon or qta_icon("mdi.tab", color="gray"))
        self.setCurrentIndex(count)

    # Remove the current tab:
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
        name = name or QtWidgets.QInputDialog.getText(self, "Tab Rename", "Enter new label:")[0]

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
