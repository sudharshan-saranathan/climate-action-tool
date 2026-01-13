# Filename: buttons.py
# Module name: startup
# Description: A button-group with various buttons shown during the application's startup.

import dataclasses
from qtawesome import icon as qta_icon
from PySide6 import QtWidgets, QtCore
from gui.widgets import VLayout

class StartupChoice(QtWidgets.QWidget):

    # Signal:
    sig_button_clicked = QtCore.Signal(str)

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
        button_new.pressed.connect(lambda: self.sig_button_clicked.emit("New Project"))

        button_tmp = self._create_button(
            self._opts.actions[1],
            attr={"label": "mdi.folder-star", "color": "lightblue"},
            checkable=True,
            style=self._opts.style,
        )
        button_tmp.pressed.connect(lambda: self.sig_button_clicked.emit("Templates"))

        button_mod = self._create_button(
            self._opts.actions[2],
            attr={"label": "mdi.database", "color": "#e56b70"},
            checkable=True,
            style=self._opts.style,
        )
        button_mod.pressed.connect(lambda: self.sig_button_clicked.emit("Models"))

        button_quit = self._create_button(
            self._opts.actions[3],
            attr={"label": "mdi.exit-run", "color": "#efefef"},
            style=self._opts.style,
        )
        button_quit.pressed.connect(lambda: self.sig_button_clicked.emit("Quit"))

        # Add all buttons to the button group:
        self._group.addButton(button_new)
        self._group.addButton(button_tmp)
        self._group.addButton(button_mod)
        self._group.addButton(button_quit)

        layout = VLayout(self)
        """
        links = ToolBar( # Toolbar with useful links
            self,
            orientation=QtCore.Qt.Orientation.Horizontal,
            iconSize=QtCore.QSize(24, 24),
            trailing=False,
            actions=[
                (qta_icon('mdi.github', color='gray', color_active='white'), 'GitHub', None),
                (qta_icon('mdi.web', color='gray', color_active='white'), 'YouTube', None),
            ],
        )
        """

        layout.addStretch(5)
        layout.addWidget(button_new)
        layout.addWidget(button_tmp)
        layout.addWidget(button_mod)
        layout.addWidget(button_quit)
        layout.addStretch(5)

    @staticmethod
    def _create_license_label() -> QtWidgets.QLabel:
        """
        Creates a clickable license label that opens the MIT license.
        """
        label = QtWidgets.QLabel()
        label.setText(
            '<a href="https://opensource.org/licenses/MIT" style="color: #aaaaaa; text-decoration: none;">'
            "© 2025 MIT License"
            "</a>"
        )
        label.setOpenExternalLinks(True)
        label.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        label.setStyleSheet(
            "QLabel { color: #aaaaaa; } QLabel:hover { color: #ffcb00; }"
        )
        return label

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
