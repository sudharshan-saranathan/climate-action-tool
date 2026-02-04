# Filename: dock.py
# Module name: widgets
# Description: A QDockWidget subclass.


# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass


class Dock(QtWidgets.QDockWidget):

    @dataclass
    class Attrs:
        floating: bool = False
        features: QtWidgets.QDockWidget.DockWidgetFeature = (
            QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )
        minimumSize: QtCore.QSize = field(
            default_factory=lambda: QtCore.QSize(360, 360)
        )

    def __init__(self, title: str, widget: QtWidgets.QWidget, parent=None):
        """
        Initialize the sidebar dock widget.
        """

        # Define attribute(s)
        self._attrs = Dock.Attrs()

        # Initialize super class
        super().__init__(
            parent,
            floating=self._attrs.floating,
            features=self._attrs.features,
        )

        # Customize appearance and behaviour
        self.setMinimumSize(self._attrs.minimumSize)

        # UI components
        self._init_titlebar(title)
        self._init_main_panel(widget)

    def _init_titlebar(self, title: str) -> None:

        self.setTitleBarWidget(
            QtWidgets.QLabel(title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            if title
            else QtWidgets.QFrame()
        )

    def _init_main_panel(self, widget: QtWidgets.QWidget) -> None:
        self.setWidget(widget)
