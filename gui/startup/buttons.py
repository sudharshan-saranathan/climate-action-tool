# Filename: buttons.py
# Module name: startup
# Description: A button-group with various buttons shown during the application's startup.

import dataclasses
from PySide6 import QtGui
from PySide6 import QtWidgets

from gui.widgets import VLayout


class StartupButtons(QtWidgets.QWidget):

    @dataclasses.dataclass
    class Options:
        actions: list[str] = dataclasses.field(
            default_factory=lambda: list(
                [
                    "New Project",  # Button to create a new project.
                    "Templates",  # Opens project templates.
                    "Models",  # Opens user-chosen models.
                    "Quit",  # Abort startup and quit the application.
                ]
            )
        )
        style: str = (
            "QPushButton {"
            "   width: 200px;"
            "   font-size: 12px;"
            "   color: #efefef;"
            "   text-align: right;"
            "   border-left: 2px solid transparent;"
            "   border-radius: 0px;"
            "   background-color: transparent;"
            "}"
            "QPushButton:hover {"
            "   border-left: 2px solid #ffcb00;"
            "}"
            "QPushButton:checked {"
            "   font-weight: bold;"
            "}"
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        self._opts = StartupButtons.Options()
        self._group = QtWidgets.QButtonGroup(self, exclusive=True)

        # Set up UI:
        self._setup_ui()

    def _setup_ui(self):

        # Required:
        from qtawesome import icon as qtaicon

        # Custom style for QPushButton widgets:
        self.setStyleSheet(self._opts.style)

        # Buttons:
        button_new = QtWidgets.QPushButton(self._opts.actions[0])
        button_tmp = QtWidgets.QPushButton(self._opts.actions[1])
        button_mod = QtWidgets.QPushButton(self._opts.actions[2])
        button_quit = QtWidgets.QPushButton(self._opts.actions[3])

        button_new.setIcon(qtaicon("mdi.folder-plus", color="#ffcb00"))
        button_tmp.setIcon(qtaicon("mdi.folder-star", color="lightblue"))
        button_mod.setIcon(qtaicon("mdi.database", color="#c73434"))
        button_quit.setIcon(qtaicon("mdi.exit-run", color="#efefef"))

        button_tmp.setCheckable(True)
        button_mod.setCheckable(True)
        self._group.addButton(button_tmp)
        self._group.addButton(button_mod)

        layout = VLayout(
            self,
            spacing=4,
            margins=(4, 4, 4, 4),
        )

        layout.addStretch(5)
        layout.addWidget(button_new)
        layout.addWidget(button_tmp)
        layout.addWidget(button_mod)
        layout.addWidget(button_quit)
        layout.addStretch(5)
