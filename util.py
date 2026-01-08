# Encoding: utf-8
# Filename: util.py
# Description: Utility functions for the application.

# Import (standard)
import os

# Imports (third party)
import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets


# Returns a right justified toolbar:
def right_justified_toolbar(**kwargs) -> QtWidgets.QToolBar:
    """
    Returns a right justified toolbar.
    :param kwargs: Additional keyword arguments for the QToolBar.
    :return: QtWidgets.QToolBar
    """

    spacer = QtWidgets.QWidget()
    spacer.setStyleSheet("background: transparent;")
    spacer.setSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding
    )

    toolbar = QtWidgets.QToolBar(None, **kwargs)
    toolbar.addWidget(spacer)
    return toolbar


# Method to show available QtAwesome icons:
def qt_awesome_icon_browser() -> None:
    """
    Displays the QtAwesome icon browser in a new non-modal window.

    :return: None
    """

    # Qt-awesome package for the icon browser:
    from qtawesome import icon_browser as ib  # type: ignore[import-untyped]

    browser = ib.IconBrowser()
    browser.setStyleSheet(
        "border-radius: 4px;background: #4a344d;"
    )  # Required because the background could be transparent

    browser.show()  # type: ignore[attr-defined]


# Returns all signals associated with a QObject instance using Qt's metaobject system:
def signals(instance: QtCore.QObject) -> dict[str, QtCore.QMetaMethod]:
    """
    Returns a dictionary of signal names and their corresponding metamethods for the specified QObject instance.
    An exception is raised if the object contains duplicate signal names.

    :param instance: The QObject instance to inspect.
    :return dict[str, QtCore.QMetaMethod]: A dictionary mapping signal-names to their metamethods.
    """

    signal_dict: dict[str, QtCore.QMetaMethod] = {}

    meta_object = instance.metaObject()  # Metaobject of the instance
    fnum_method = meta_object.methodCount()  # Total number of methods

    for index in range(fnum_method):  # Iterate through all methods
        method = meta_object.method(index)

        # Filter only signals and append them to the dictionary:
        if method.methodType() == QtCore.QMetaMethod.MethodType.Signal:
            signal_name = method.name().data().decode()
            if signal_name in signal_dict:
                raise KeyError(f"Duplicate signal name found: {signal_name}")

            signal_dict[signal_name] = method

    return signal_dict
