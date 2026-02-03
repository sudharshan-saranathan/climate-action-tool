# Filename: tabber.py
# Module name: gui
# Description: A QTabWidget subclass for displaying various widgets.

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Standard
import logging


# Dataclass
from dataclasses import field
from dataclasses import dataclass


class Tabber(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super().__init__(
            parent,
            tabsClosable=True,
            tabBarAutoHide=True,
        )