# Filename: dock.py
# Module name: lower_dock
# Description: Lower dock widget UI.

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets


# Dataclass
from dataclasses import field
from dataclasses import dataclass


class DockWidget(QtWidgets.QDockWidget):

    @dataclass(frozen=True)
    class Attrs:
        title_height: int = 24
        min_size: QtCore.QSize = field(default_factory=lambda: QtCore.QSize(360, 360))
        floating: bool = False
        features: QtWidgets.QDockWidget.DockWidgetFeature = (
            QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )

    def __init__(self, title: str, widget: QtWidgets.QWidget, parent=None, **kwargs):

        # Define attribute(s)
        self._attrs = DockWidget.Attrs()

        # Initialize parent class
        super().__init__(
            parent,
            floating=self._attrs.floating,
            features=self._attrs.features,
        )

        # UI components
        self.setWidget(widget)
        self._init_title_bar(title)

        # Customize appearance and behaviour
        self.setMinimumSize(self._attrs.min_size)
        self.titleBarWidget().setFixedHeight(self._attrs.title_height)

    def _init_title_bar(self, title: str) -> None:

        self.setTitleBarWidget(
            QtWidgets.QLabel(
                title,
                alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            )
            if title
            else QtWidgets.QFrame()
        )
