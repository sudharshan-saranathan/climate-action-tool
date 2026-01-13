# Filename: buttons.py
# Module name: startup
# Description: A button-group with various buttons shown during the application's startup.

import dataclasses
from qtawesome import icon as qta_icon
from PySide6 import QtWidgets, QtCore
from gui.widgets import VLayout, ToolBar
from .banner import StartupBanner

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
            "   border-left: 2px solid #ffcb00;"
            "}"
            "QPushButton:checked {"
            "   color: #ff5c5c;"
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
            icon_attr={"label": "mdi.folder-plus", "color": "#ffcb00"},
            style=self._opts.style,
        )
        button_new.pressed.connect(lambda: self.sig_button_clicked.emit("New Project"))

        button_tmp = self._create_button(
            self._opts.actions[1],
            icon_attr={"label": "mdi.folder-star", "color": "lightblue"},
            checkable=True,
            style=self._opts.style,
        )
        button_tmp.pressed.connect(lambda: self.sig_button_clicked.emit("Templates"))

        button_mod = self._create_button(
            self._opts.actions[2],
            icon_attr={"label": "mdi.database", "color": "#c73434"},
            checkable=True,
            style=self._opts.style,
        )
        button_mod.pressed.connect(lambda: self.sig_button_clicked.emit("Models"))

        button_quit = self._create_button(
            self._opts.actions[3],
            icon_attr={"label": "mdi.exit-run", "color": "#efefef"},
            style=self._opts.style,
        )
        button_quit.pressed.connect(lambda: self.sig_button_clicked.emit("Quit"))

        # Add all buttons to the button group:
        self._group.addButton(button_new)
        self._group.addButton(button_tmp)
        self._group.addButton(button_mod)
        self._group.addButton(button_quit)

        layout = VLayout(
            self,
            spacing=4,
            margins=(12, 12, 12, 12),
        )

        banner = StartupBanner()
        links = ToolBar( # Toolbar with useful links
            self,
            orientation=QtCore.Qt.Orientation.Horizontal,
            iconSize=QtCore.QSize(24, 24),
            trailing=True,
            actions=[
                (qta_icon('mdi.github', color='white'), 'Github', None),
                (qta_icon('ri.youtube-fill', color='red'), 'Tutorial', None),
            ],
            style="QToolButton {align: right; margin: 0px; padding: 0px;}"
        )
        h_line = QtWidgets.QFrame()
        h_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        h_line.setLineWidth(1)
        h_line.setStyleSheet("QFrame { background-color: #4f4f4f; }")

        layout.addStretch(5)
        layout.addWidget(banner)
        layout.addWidget(h_line)
        layout.addWidget(button_new)
        layout.addWidget(button_tmp)
        layout.addWidget(button_mod)
        layout.addWidget(button_quit)
        layout.addStretch(5)
        layout.addWidget(links)

    @staticmethod
    def _create_button(
        text: str, icon_attr: dict[str, str], checkable=False, style: str = str()
    ) -> QtWidgets.QPushButton:
        """
        Creates a QPushButton with the given label and QtAwesome icon.
        """

        # Required:
        from qtawesome import icon as qta_icon

        label = icon_attr.get("label")
        color = icon_attr.get("color")

        button = QtWidgets.QPushButton(text)
        button.setIcon(qta_icon(label, color=color))
        button.setCheckable(checkable)
        button.setStyleSheet(style)

        return button
