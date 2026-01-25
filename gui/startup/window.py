# Filename: window.py
# Module name: startup
# Description: A startup window based on the QDialog class (see Qt docs for more info).

from PySide6 import QtCore, QtWidgets, QtGui
from gui.startup.choice import StartupChoice
from gui.startup.ftable import StartupFileTable, FileTableItem
from gui.widgets import GLayout
import dataclasses


class StartupWindow(QtWidgets.QDialog):
    """
    A startup window based on a QDialog class.
    """

    @dataclasses.dataclass(frozen=True)
    class Style:
        """
        Configuration options for the startup window.

        Attributes:
            brush: QBrush for the window background (default: solid dark color).
            border: QPen for window border styling (default: dark gray, 2pt).
            texture: Path to the window background texture (default: ":/theme/pattern.png").
        """

        brush: QtGui.QBrush = dataclasses.field(default_factory=QtGui.QBrush)
        border: QtGui.QPen = dataclasses.field(default_factory=QtGui.QPen)
        texture: str = ":/theme/pattern.png"

    @dataclasses.dataclass(frozen=True)
    class Geometry:
        size: QtCore.QSize = dataclasses.field(default_factory=QtCore.QSize)
        radius: int = 10

    @dataclasses.dataclass(frozen=True)
    class Metadata:
        regex: str = "*.h5"

    # Class constructor
    def __init__(self, parent=None):
        """
        Initializes the startup window and sets up the UI components.

        Args:
            parent: Parent widget (optional).
        """

        super().__init__(parent)
        super().setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        super().setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        # Window styling and initialization
        self._style = StartupWindow.Style(
            brush=QtGui.QBrush(QtGui.QColor(0x232A2E)),
            border=QtGui.QPen(QtGui.QColor(0x393E41)),
        )
        self._pixmap = QtGui.QPixmap(self._style.texture)
        self._style.brush.setTexture(self._pixmap)

        self._geometry = StartupWindow.Geometry(size=QtCore.QSize(900, 640), radius=10)
        self._metadata = StartupWindow.Metadata()
        self.resize(self._geometry.size)

        # UI components
        self._header = self._init_header()
        self._h_line = self._init_h_line()
        self._footer = self._init_footer()
        self._ftable = self._init_ftable()
        self._choice = StartupChoice()
        self._current_project_file = None

        # Arrange UI components using a grid layout
        self._init_layout()

        self._init_connections()

    def _init_header(self) -> QtWidgets.QLabel:
        """
        Create and configure the window header with title and subtitle.

        Returns:
            A QLabel displaying the application title and tagline with centered alignment.
        """
        header = QtWidgets.QLabel(
            '<span style="color:white; font-family: Bilbo; font-size:30pt;">Climate Action Tool</span><br>'
            '<span style="color:gray; font-weight: bold; font-size: 8pt;">Energy Systems Modeling Platform</span>',
            self,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        header.setContentsMargins(12, 0, 12, 0)
        header.setOpenExternalLinks(True)
        return header

    def _init_h_line(self) -> QtWidgets.QFrame:
        """
        Create a horizontal separator line.

        Returns:
            A QFrame configured as a horizontal line with dark gray color.
        """
        h_line = QtWidgets.QFrame(self)
        h_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        h_line.setStyleSheet("QFrame {background:#4f4f4f;}")
        h_line.setLineWidth(2)
        return h_line

    def _init_footer(self) -> QtWidgets.QToolBar:
        """
        Create the footer toolbar with project links and license information.

        The footer contains clickable buttons for GitHub and project website, along
        with a license link. A spacer separates the links from the license text.

        Returns:
            A QToolBar configured with footer elements.
        """

        from qtawesome import icon as qta_icon
        import webbrowser

        def _init_link_button(
            icon: str, tooltip: str, url: str
        ) -> QtWidgets.QToolButton:
            """
            Create a clickable tool button that opens a URL in the default browser.

            Args:
                icon: QtAwesome icon name (e.g., "mdi.github").
                tooltip: Tooltip text shown on hover.
                url: URL to open when button is clicked.

            Returns:
                A configured QToolButton.
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

    def _init_ftable(self) -> StartupFileTable:
        """
        Initialize the file table widget displaying project files

        Returns:
            StartupFileTable: The file table widget
        """

        ftable = StartupFileTable()
        ftable.populate("library", self._metadata.regex)
        return ftable

    def _init_layout(self):

        # Arrange UI components:
        layout = GLayout(
            self,
            spacing=8,
            margins=(8, 8, 8, 8),
        )
        layout.setVerticalSpacing(8)
        layout.setRowStretch(0, 5)
        layout.addWidget(self._header, 1, 0)
        layout.addWidget(self._h_line, 2, 0)
        layout.addWidget(self._choice, 3, 0)
        layout.addWidget(self._footer, 5, 0)
        layout.addWidget(self._ftable, 0, 1, 6, 1)
        layout.setRowStretch(4, 4)
        layout.setColumnStretch(1, 2)

    def _init_connections(self) -> None:
        """
        Connect UI signals to their respective handler slots.

        Connects buttons and file table signals to manage project creation,
        selection, and application lifecycle.
        """

        self._choice.sig_button_new_clicked.connect(self._on_new_project)
        self._choice.sig_button_tmp_clicked.connect(self._on_library_clicked)
        self._choice.sig_button_quit_clicked.connect(self._on_quit)

        for row in range(self._ftable.rowCount()):
            item = self._ftable.cellWidget(row, 0)
            if isinstance(item, FileTableItem):
                item.sig_open_project.connect(self._on_open_project)
                item.sig_clone_project.connect(self._on_clone_project)
                item.sig_delete_project.connect(self._on_delete_project)

    @QtCore.Slot()
    def _on_new_project(self) -> None:
        """
        Handle new project creation button click.

        Accepts the dialog and returns to the main application.
        TODO: Implement new project creation logic.
        """
        self.accept()

    @QtCore.Slot()
    def _on_library_clicked(self) -> None:
        """
        Handle library button click.

        The file table is already visible by default, so no action is needed.
        """
        pass

    @QtCore.Slot(str)
    def _on_open_project(self, project_path: str) -> None:
        """
        Handle project selection from the file table.

        Stores the selected project file path and accepts the dialog.

        Args:
            project_path: Path to the selected project file.
        """
        self._current_project_file = project_path
        self.accept()

    @QtCore.Slot(str)
    def _on_clone_project(self, project_path: str) -> None:
        """
        Handle project cloning request.

        TODO: Implement project cloning logic.

        Args:
            project_path: Path to the project to clone.
        """
        pass

    @QtCore.Slot(str)
    def _on_delete_project(self, project_path: str) -> None:
        """
        Handle project deletion request.

        TODO: Implement project deletion logic.

        Args:
            project_path: Path to the project to delete.
        """
        pass

    @QtCore.Slot()
    def _on_quit(self) -> None:
        """Handle quit button click by rejecting the dialog."""
        self.reject()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """
        Paint the startup window with a rounded rectangle background.

        Args:
            event: The paint event.
        """

        painter = QtGui.QPainter(self)
        painter.setPen(self._style.border)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setBrush(self._style.brush)
        painter.drawRoundedRect(
            self.rect(),
            self._geometry.radius,
            self._geometry.radius,
        )
