# Encoding: utf-8
# Module name: mapdata
# Description: Map data widget for the sidebar

# Imports (standard)
from __future__ import annotations

# Imports (third party)
from PySide6 import QtCore, QtWidgets

# Imports (local)
from gui.widgets import VLayout, CollapsibleSection


# Class LegendItem:
class LegendItem(QtWidgets.QWidget):

    # Initializer:
    def __init__(
        self,
        label: str,
        color: str,
        count: int = 0,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)

        self._label = label
        self._color = color
        self._count = count

        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)

        # Color swatch:
        self._swatch = QtWidgets.QFrame(self)
        self._swatch.setFixedSize(8, 8)
        self._swatch.setStyleSheet(
            f"background-color: {self._color}; border-radius: 4px;"
        )

        # Label:
        self._label_widget = QtWidgets.QLabel(self._label, self)
        self._label_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )

        # Count:
        self._count_widget = QtWidgets.QLabel(f"({self._count})", self)
        self._count_widget.setStyleSheet("color: gray;")

        layout.addWidget(self._swatch)
        layout.addWidget(self._label_widget)
        layout.addWidget(self._count_widget)

    def set_count(self, count: int):
        self._count = count
        self._count_widget.setText(f"({count})")

    def count(self) -> int:
        return self._count

    def label(self) -> str:
        return self._label


# Class LegendSection:
class LegendSection(CollapsibleSection):

    # Initializer:
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__("Sector(s)", parent, expanded=True)

        # Attribute(s):
        self._items: dict[str, LegendItem] = {}

        # Initialize content:
        self._init_content()

    def _init_content(self):
        # Default legend items (can be updated dynamically):
        default_items = []

        for label, color in default_items:
            item = LegendItem(label, color, count=0, parent=self)
            self._items[label] = item
            self.add_widget(item)

    def set_item_count(self, label: str, count: int):
        if label in self._items:
            self._items[label].set_count(count)

    def add_legend_item(self, label: str, color: str, count: int = 0):
        if label not in self._items:
            item = LegendItem(label, color, count, parent=self)
            self._items[label] = item
            self.add_widget(item)

    def remove_legend_item(self, label: str):
        if label in self._items:
            item = self._items.pop(label)
            item.deleteLater()


# Class StatisticsSection:
class StatisticsSection(CollapsibleSection):
    """Statistics section showing aggregate metrics."""

    # Initializer:
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__("Statistics", parent, expanded=True)

        # Attribute(s):
        self._stats: dict[str, QtWidgets.QLabel] = {}

        # Initialize content:
        self._init_content()

    def _init_content(self):
        # Form layout for stats:
        form = QtWidgets.QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(4)
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        # Default statistics:
        default_stats = [
            ("Total Sites", "0"),
            ("Total Emissions", "0 Mt"),
            ("Coverage", "0%"),
        ]

        for label, value in default_stats:
            value_label = QtWidgets.QLabel(value, self)
            value_label.setStyleSheet("font-weight: bold;")
            self._stats[label] = value_label
            form.addRow(f"{label}:", value_label)

        self.set_content_layout(form)

    # Set a statistic value:
    def set_stat(self, label: str, value: str):
        if label in self._stats:
            self._stats[label].setText(value)


# Class LayersSection:
class LayersSection(CollapsibleSection):
    """Layers section with toggleable map layers."""

    # Signal emitted when layer visibility changes:
    layer_toggled = QtCore.Signal(str, bool)

    # Initializer:
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__("Layers", parent, expanded=True)

        # Attribute(s):
        self._layers: dict[str, QtWidgets.QCheckBox] = {}

        # Initialize content:
        self._init_content()

    def _init_content(self):
        # Default layers:
        default_layers = [
            ("Emission Sources", True),
            ("Grid Boundaries", True),
            ("Administrative", False),
        ]

        for label, checked in default_layers:
            checkbox = QtWidgets.QCheckBox(label, self)
            checkbox.setChecked(checked)
            checkbox.toggled.connect(
                lambda state, lbl=label: self.layer_toggled.emit(lbl, state)
            )
            self._layers[label] = checkbox
            self.add_widget(checkbox)

    # Check if a layer is visible:
    def is_layer_visible(self, label: str) -> bool:
        if label in self._layers:
            return self._layers[label].isChecked()
        return False

    # Set layer visibility:
    def set_layer_visible(self, label: str, visible: bool):
        if label in self._layers:
            self._layers[label].setChecked(visible)

    # Add a new layer:
    def add_layer(self, label: str, visible: bool = False):
        if label not in self._layers:
            checkbox = QtWidgets.QCheckBox(label, self)
            checkbox.setChecked(visible)
            checkbox.toggled.connect(
                lambda state, lbl=label: self.layer_toggled.emit(lbl, state)
            )
            self._layers[label] = checkbox
            self.add_widget(checkbox)


# Class MapData:
class MapData(QtWidgets.QWidget):
    """Map data sidebar page with legend, statistics, and layers."""

    # Signal emitted when layer visibility changes:
    layer_toggled = QtCore.Signal(str, bool)

    # Initializer:
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        # Initialize UI:
        self._init_ui()

    def _init_ui(self):
        layout = VLayout(self, spacing=8, margins=(4, 8, 4, 8))

        # Create sections:
        self._legend = LegendSection(self)
        self._statistics = StatisticsSection(self)
        self._layers = LayersSection(self)

        # Connect layer signals:
        self._layers.layer_toggled.connect(self.layer_toggled)

        # Add sections to layout:
        layout.addWidget(self._legend)
        layout.addWidget(self._statistics)
        layout.addWidget(self._layers)
        layout.addStretch()

    # Property accessors:
    @property
    def legend(self) -> LegendSection:
        return self._legend

    @property
    def statistics(self) -> StatisticsSection:
        return self._statistics

    @property
    def layers(self) -> LayersSection:
        return self._layers
