# Filename: buttons.py
# Module name: startup
# Description: A button-group with various buttons shown during the application's startup.

import dataclasses
from qtawesome import icon as qta_icon
from PySide6 import QtWidgets, QtCore
from gui.widgets import VLayout


class StartupChoice(QtWidgets.QWidget):

    # Signal:
    sig_button_new_clicked = QtCore.Signal()
    sig_button_tmp_clicked = QtCore.Signal()
    sig_button_mod_clicked = QtCore.Signal()
    sig_button_quit_clicked = QtCore.Signal()

    @dataclasses.dataclass
    class Options:
        style: str = (
            "QPushButton {"
            "   padding: 4px 0px 4px 0px;"
            "   color: #aaaaaa;"
            "   width: 200px;"
            "   text-align: right;"
            "   border-radius: 0px;"
            "   background-color: transparent;"
            "}"
            "QPushButton:hover {"
            "   color: #efefef;"
            "}"
            "QPushButton:checked {"
            "   color: white;"
            "   font-weight: bold;"
            "}"
        )

        actions: list[str] = dataclasses.field(
            default_factory=lambda: list(
                [
                    "New Project",  # Button to create a new project.
                    "Library",  # Displays the project library to the user.
                    "Recent",  # Displays the most recently opened projects.
                    "Quit",  # Abort startup and quit the application.
                ]
            )
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        self._opts = StartupChoice.Options()
        self._group = QtWidgets.QButtonGroup(self, exclusive=True)

        # Set up UI:
        self._setup_ui()

    def _setup_ui(self):

        # Buttons:
        button_new = self._create_button(
            self._opts.actions[0],
            attr={"label": "mdi.folder-plus", "color": "#ffcb00"},
            style=self._opts.style,
        )

        button_tmp = self._create_button(
            self._opts.actions[1],
            attr={"label": "mdi.database", "color": "#e56b70"},
            checkable=True,
            style=self._opts.style,
        )

        button_mod = self._create_button(
            self._opts.actions[2],
            attr={"label": "mdi.folder-star", "color": "lightblue"},
            checkable=True,
            style=self._opts.style,
        )

        button_quit = self._create_button(
            self._opts.actions[3],
            attr={"label": "mdi.exit-run", "color": "#efefef"},
            style=self._opts.style,
        )

        # Re-emit buttons' signals:
        button_new.clicked.connect(self.sig_button_new_clicked)
        button_tmp.clicked.connect(self.sig_button_tmp_clicked)
        button_mod.clicked.connect(self.sig_button_mod_clicked)
        button_quit.clicked.connect(self.sig_button_quit_clicked)

        # Add all buttons to the button group:
        self._group.addButton(button_new)
        self._group.addButton(button_tmp)
        self._group.addButton(button_mod)
        self._group.addButton(button_quit)

        layout = VLayout(self)
        layout.addStretch(5)
        layout.addWidget(button_new)
        layout.addWidget(button_tmp)
        layout.addWidget(button_mod)
        layout.addWidget(button_quit)
        layout.addStretch(5)

    @staticmethod
    def _create_button(
        text: str, attr: dict[str, str], checkable=False, style: str = str()
    ) -> QtWidgets.QPushButton:
        """
        Creates a QPushButton with the given label and QtAwesome icon.
        """

        label = attr.get("label")
        color = attr.get("color")

        button = QtWidgets.QPushButton(text)
        button.setIcon(qta_icon(label, color=color))
        button.setCheckable(checkable)
        button.setStyleSheet(style)

        return button
