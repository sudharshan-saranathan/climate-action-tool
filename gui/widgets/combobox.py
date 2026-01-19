# Filename: combobox.py
# Module name: widgets
# Description: Custom combobox widget with fixed item height and icon support.

"""
Custom combobox widget with enhanced styling and icon support.

Provides a QComboBox subclass with fixed item heights, custom styling, and support for icon-label tuples.
"""

from qtawesome import icon as qta_icon
from PySide6 import QtGui, QtCore, QtWidgets


class FixedHeightDelegate(QtWidgets.QStyledItemDelegate):
    """
    Item delegate for combobox items with fixed height.

    Overrides the size hint to enforce a consistent item height regardless of content.
    """

    def __init__(self, height: int, parent=None):
        """
        Initialize the fixed height delegate.

        Args:
            height: The fixed height for all items in pixels.
            parent: Parent widget (optional).
        """
        super().__init__(parent)
        self._height = int(height)

    def sizeHint(
        self, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex
    ) -> QtCore.QSize:
        """
        Return the fixed size hint for combo box items.

        Args:
            option: The style option containing display settings.
            index: The model index of the item.

        Returns:
            A QSize with the original width and fixed height.
        """
        base = super().sizeHint(option, index)
        return QtCore.QSize(base.width(), self._height)


class ComboBox(QtWidgets.QComboBox):
    """
    Custom combo box widget with enhanced styling and icon support.

    Provides a styled combo box with fixed item heights, custom appearance, and support for icon-label pairs.
    """

    def __init__(self, parent=None, **kwargs):
        """
        Initialize the custom combo box widget.

        Configures the combo box with fixed item height, custom styling, and support for icon-label pairs.

        Args:
            parent: Parent widget (optional).
            **kwargs: Configuration options:
                - iconSize: QSize for combo box icon size (default: 16x16)
                - editable: Whether the combo box is editable (default: False)
                - items: List of items or (icon, label) tuples to add
                - autofill: If True, populate with flow items from the core module
        """
        super().__init__(
            parent,
            iconSize=kwargs.get("iconSize", QtCore.QSize(16, 16)),
            editable=kwargs.get("editable", False),
        )

        # Configure list view with fixed item height and spacing
        view = QtWidgets.QListView(self)
        view.setItemDelegate(FixedHeightDelegate(24, view))
        view.setSpacing(2)

        # Apply custom QSS styling to the combo box and its dropdown
        self.setView(view)
        self.setObjectName("ComboBox")
        self.setStyleSheet(
            "QComboBox {"
            "margin: 0px;"
            "border: 0px solid gray; "
            "border-radius: 4px;"
            "}"
            "QComboBox QAbstractView {"
            "margin: 4px 0px 4px 0px;"
            "border: 0px solid gray; "
            "border-radius: 4px;"
            "}"
            "QComboBox QAbstractView::item {"
            "width:  80px;"
            "padding: 4px;"
            "}"
            "QComboBox QAbstractView::item:selected {"
            "background-color: #3874F2;"
            "color: white;"
            "}"
        )

        # Populate initial items from kwargs (supports both strings and (icon, label) tuples)
        for item in kwargs.get("items", []):
            if isinstance(item, tuple) and len(item) == 2:
                icon, label = item
                self.addItem(qta_icon(icon, color="lightgray"), label)
            else:
                self.addItem(item)
