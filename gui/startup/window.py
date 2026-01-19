# Filename: window.py
# Module name: startup
# Description: A modal QDialog subclass that is displayed at startup.

"""
Startup window interface for the Climate Action Tool.

This module provides a startup dialog that allows users to create new projects,
browse existing projects in the library, and manage project files.
"""

import dataclasses
from PySide6 import QtCore, QtWidgets, QtGui

from gui.startup.choice import StartupChoice
from gui.startup.ftable import StartupFileTable, FileTableItem
from gui.widgets import GLayout


class StartupWindow(QtWidgets.QDialog):
    """
    This QDialog subclass is a startup window for the Climate Action Tool. It initializes and arranges UI
    components such as a header, separator, footer, file table, along with startup buttons for starting a
    new project or loading an existing one. It features a minimal and polished design.
    """

    @dataclasses.dataclass(frozen=True)
    class Options:
        """
        Startup window configuration options.

        Attributes:
            radius: Corner radius for rounded rectangle in pixels (default: 10.0).
            border: QPen for window border styling (default: dark gray, 2pt).
            background: QBrush for window background (default: solid dark color).
            rect: QSize for window dimensions (default: 900x640).
        """

        radius: float = 10.0
        border: QtGui.QPen = dataclasses.field(
            default_factory=lambda: QtGui.QPen(QtGui.QColor(0x393E41), 2.0)
        )

        background: QtGui.QBrush = dataclasses.field(
            default_factory=lambda: QtGui.QBrush(
                QtGui.QColor(0x232A2E),
                QtCore.Qt.BrushStyle.SolidPattern,
            )
        )

        rect: QtCore.QSize = dataclasses.field(
            default_factory=lambda: QtCore.QSize(900, 640)
        )

    def __init__(self, parent=None):
        """
        Initialize the startup window with UI components and layout.

        Sets up a frameless, translucent window with header, file table, buttons,
        and footer. Connects signals for user interactions with project management.

        Args:
            parent: Parent widget (optional).
        """
        super().__init__(parent)
        super().setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        super().setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        # Load background pattern and initialize UI components
        self._pixmap = QtGui.QPixmap(":/theme/pattern.png")
        self._header = self._init_header()
        self._h_line = self._init_h_line()
        self._footer = self._init_footer()
        self._choice = StartupChoice()
        self._ftable = StartupFileTable()
        self._ftable.populate("library", "*.h5")
        self._current_project_file = None

        # Configure window appearance and size
        self._opts = StartupWindow.Options()
        self._opts.background.setTexture(self._pixmap)
        self.resize(self._opts.rect)

        # Arrange components in grid layout: header/buttons on left, file table on right
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

        self._setup_connections()

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

    def _setup_connections(self) -> None:
        """
        Connect UI signals to their respective handler slots.

        Connects buttons and file table signals to manage project creation,
        selection, and application lifecycle.
        """
        self._choice.sig_button_new_clicked.connect(self._on_new_project)
        self._choice.sig_button_tmp_clicked.connect(self._on_library_clicked)
        self._choice.sig_button_quit_clicked.connect(self._on_quit)

        self._connect_file_table_items()

    def _connect_file_table_items(self) -> None:
        """
        Connect signals from all file table items to their handlers.

        Iterates through the file table and connects open, clone, and delete
        signals for each project item.
        """
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
        painter.setPen(self._opts.border)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setBrush(self._opts.background)
        painter.drawRoundedRect(self.rect(), self._opts.radius, self._opts.radius)
