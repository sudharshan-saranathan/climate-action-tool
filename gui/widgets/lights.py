# Filename: lights.py
# Module name: widgets
# Description: Traffic light window control buttons (minimize, maximize, close).

from PySide6 import QtCore
from qtawesome import icon as qta_icon
from gui.widgets.toolbar import ToolBar


class TrafficLights(ToolBar):

    # Signals emitted when traffic light buttons are clicked
    sig_minimize_clicked = QtCore.Signal()
    sig_maximize_clicked = QtCore.Signal()
    sig_close_clicked = QtCore.Signal()

    def __init__(self, parent=None, on_minimize=None, on_maximize=None, on_close=None):

        on_minimize = on_minimize or (lambda: self.sig_minimize_clicked.emit())
        on_maximize = on_maximize or (lambda: self.sig_maximize_clicked.emit())
        on_close = on_close or (lambda: self.sig_close_clicked.emit())

        super().__init__(
            parent,
            iconSize=QtCore.QSize(20, 20),
            floatable=False,
            movable=False,
            trailing=False,
            actions=[
                (
                    qta_icon(
                        "mdi.circle",
                        color="#28c840",
                        active="mdi.plus-circle",
                    ),
                    "Maximize",
                    on_maximize,
                ),
                (
                    qta_icon(
                        "mdi.circle",
                        color="#ffcb00",
                        active="mdi.minus-circle",
                    ),
                    "Minimize",
                    on_minimize,
                ),
                (
                    qta_icon(
                        "mdi.circle",
                        color="#ff5f57",
                        active="mdi.close-circle",
                    ),
                    "Close",
                    on_close,
                ),
            ],
        )

        self.setStyleSheet("QToolBar QToolButton {"
                           "    background-color:transparent;"
                           "    margin: 0px;"
                           "    padding: 0px;"
                           "}")
