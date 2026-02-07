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

    def __init__(
        self,
        title: QtWidgets.QWidget = None,
        widget: QtWidgets.QWidget = None,
        parent=None,
    ):
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
        self.setTitleBarWidget(title)
        self.setWidget(widget)
