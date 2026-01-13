# Filename: dialog.py
# Module name: startup
# Description: A modal QDialog subclass that is displayed at startup.

import dataclasses
from PySide6 import QtCore, QtWidgets, QtGui

from gui.startup.choice import StartupChoice
from gui.startup.ftable import StartupFileTable
from gui.widgets import GLayout


class StartupWindow(QtWidgets.QDialog):

    @dataclasses.dataclass(frozen=True)
    class Options:

        radius: float = 10.0  # Radius of the rounded corners.
        border: QtGui.QPen = (
            dataclasses.field(  # Window border style (default: no border).
                default_factory=lambda: QtGui.QPen(QtGui.QColor(0x393E41), 2.0)
            )
        )

        background: QtGui.QBrush = dataclasses.field(  # Background color and style.
            default_factory=lambda: QtGui.QBrush(
                QtGui.QColor(0x232A2E),
                QtCore.Qt.BrushStyle.SolidPattern,
            )
        )

        rect: QtCore.QSize = (
            dataclasses.field(  # Size of the window (default: 900x640).
                default_factory=lambda: QtCore.QSize(900, 640)
            )
        )

    def __init__(self, parent=None):
        """
        Initializes the window, configures attributes, and adds child widgets.
        """
        super().__init__(parent)
        super().setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        super().setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        # UI components:
        self._pixmap = QtGui.QPixmap(":/theme/pattern.png")
        self._header = self._init_header()
        self._h_line = self._init_h_line()
        self._footer = self._init_footer()
        self._choice = StartupChoice()
        self._ftable = StartupFileTable()

        self._opts = StartupWindow.Options()
        self._opts.background.setTexture(self._pixmap)
        self.resize(self._opts.rect)

        # Arrange UI components in a layout:
        layout = GLayout(  # Horizontal layout.
            self,
            spacing=8,
            margins=(4, 4, 4, 4),
        )

        layout.setVerticalSpacing(16)
        layout.setRowStretch(0, 5)
        layout.addWidget(self._header, 1, 0)
        layout.addWidget(self._h_line, 2, 0)
        layout.addWidget(self._choice, 3, 0)
        layout.addWidget(self._footer, 5, 0)
        layout.addWidget(self._ftable, 0, 1, 6, 1)
        layout.setRowStretch(4, 5)
        layout.setColumnStretch(1, 2)

    def _init_header(self) -> QtWidgets.QLabel:
        """
        Creates a header for the startup window with a stylized title and subtitle.
        """

        header = QtWidgets.QLabel(
            '<span style="color:white; font-family: Bilbo; font-size:30pt;">Climate Action Tool</span><br>'
            '<span style="color:gray; font-size:9pt; font-weight: bold;">Energy Systems Modeling Platform</span>',
            self,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        header.setContentsMargins(12, 0, 12, 0)
        header.setOpenExternalLinks(True)
        return header

    def _init_h_line(self) -> QtWidgets.QFrame:
        """
        Creates and returns a light gray horizontal separator.
        """

        h_line = QtWidgets.QFrame(self)
        h_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        h_line.setStyleSheet("QFrame {background:#4f4f4f;}")
        h_line.setLineWidth(2)
        return h_line

    def _init_footer(self) -> QtWidgets.QToolBar:
        """
        Creates and returns a window-footer with tool buttons and other peripheral information.
        """

        from qtawesome import icon as qta_icon
        import webbrowser

        def _init_link_button(
            icon: str, tooltip: str, url: str
        ) -> QtWidgets.QToolButton:
            """
            Helper to create a clickable link button.
            """

            link = QtWidgets.QToolButton(self)
            link.setIcon(qta_icon(icon, color="gray", color_active="white"))
            link.setToolTip(tooltip)
            link.clicked.connect(lambda: webbrowser.open(url))
            return link

        git_link = _init_link_button(
            "mdi.github",
            "GitHub Repository",
            "https://github.com/sudharshan-saranathan/climate-action-tool.git",
        )

        web_link = _init_link_button(
            "mdi.web", "Project Website", "https://example.com/climate-action"
        )

        # Add spacing between buttons and license
        spacer = QtWidgets.QWidget(self)
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        license_label = QtWidgets.QLabel(
            '<a href="https://opensource.org/licenses/MIT" style="color: #4f4f4f;">'
            "© 2025 MIT License"
            "</a>",
            self,
            openExternalLinks=True,
        )

        # Arrange footer components in a toolbar:
        footer = QtWidgets.QToolBar(self, iconSize=QtCore.QSize(18, 18))
        footer.addWidget(git_link)
        footer.addWidget(web_link)
        footer.addWidget(spacer)
        footer.addWidget(license_label)
        return footer

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:

        painter = QtGui.QPainter(self)
        painter.setPen(self._opts.border)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setBrush(self._opts.background)
        painter.drawRoundedRect(self.rect(), self._opts.radius, self._opts.radius)
