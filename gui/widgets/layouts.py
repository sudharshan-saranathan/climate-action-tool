# Filename: layouts.py
# Module name: widgets
# Description: Layout utilities for the Climate Action Tool application.

# Import(s):
import dataclasses
from PySide6 import QtWidgets


# Class GLayout:
class GLayout(QtWidgets.QGridLayout):

    @dataclasses.dataclass
    class Options:
        spacing: int = 0
        margins: tuple[int, int, int, int] = (0, 0, 0, 0)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        # Initialize options:
        self._opts = GLayout.Options(
            spacing=kwargs.get("spacing", 0),
            margins=kwargs.get("margins", (0, 0, 0, 0)),
        )

        # Set attribute(s):
        self.setSpacing(self._opts.spacing)
        ml, mt, mr, md = self._opts.margins
        self.setContentsMargins(ml, mt, mr, md)


# Class HLayout:
class HLayout(QtWidgets.QHBoxLayout):

    @dataclasses.dataclass
    class Options:
        spacing: int = 0
        margins: tuple[int, int, int, int] = (0, 0, 0, 0)
        widgets: list[QtWidgets.QWidget] = dataclasses.field(default_factory=list)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        # Initialize options:
        self._opts = HLayout.Options(
            spacing=kwargs.get("spacing", 0),
            margins=kwargs.get("margins", (0, 0, 0, 0)),
            widgets=kwargs.get("widgets", []),
        )

        # Set attribute(s):
        self.setSpacing(self._opts.spacing)
        ml, mt, mr, md = self._opts.margins
        self.setContentsMargins(ml, mt, mr, md)

        # If widgets are available, add them:
        for widget in self._opts.widgets:
            self.addWidget(widget)


# Class VLayout:
class VLayout(QtWidgets.QVBoxLayout):

    @dataclasses.dataclass
    class Options:
        spacing: int = 0
        margins: tuple[int, int, int, int] = (0, 0, 0, 0)
        widgets: list[QtWidgets.QWidget] = dataclasses.field(default_factory=list)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        # Initialize options:
        self._opts = VLayout.Options(
            spacing=kwargs.get("spacing", 0),
            margins=kwargs.get("margins", (0, 0, 0, 0)),
            widgets=kwargs.get("widgets", []),
        )

        # Set attribute(s):
        self.setSpacing(self._opts.spacing)
        ml, mt, mr, md = self._opts.margins
        self.setContentsMargins(ml, mt, mr, md)

        # If widgets are available, add them:
        for widget in self._opts.widgets:
            self.addWidget(widget)
