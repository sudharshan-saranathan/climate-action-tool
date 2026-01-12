import enum

from PySide6 import QtCore, QtWidgets
from qtawesome import icon as qta_icon

from gui.startup import widget, welcome
from gui.widgets import HLayout, VLayout
from util import right_justified_toolbar


class StartupCode(enum.Enum):
    """Result codes representing user selections during startup."""

    Closed = -1
    Quit = 0
    New = 1
    Import = 2
    Templates = 3


class StartupDialog(QtWidgets.QDialog):
    """
    A startup widget with actions/buttons to start a new project, import from templates, or open existing models.
    """

    def __init__(self):
        super().__init__(None)
        super().setObjectName("startup-dialog")  # Used in the QSS stylesheet.

        self._startup_choice = QtWidgets.QButtonGroup(exclusive=True)
        self._setup_ui()

        # Frameless window with a translucent background:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

    def _setup_ui(self):
        """
        Adds the following UI components to this dialog:
        1. `container`: A container widget with integrated welcome screen
        """

        # QDialog is transparent, so we need a non-transparent container for the background.
        # This also enforces rounded corners independent of the platform.
        container = QtWidgets.QFrame(self)
        container.setFixedSize(1000, 600)
        container.setObjectName(
            "startup-dialog-container"
        )  # DO NOT MODIFY: Used in QSS file.

        # Use the integrated StartupWelcome widget:
        welcome_widget = welcome.StartupWelcome(self)
        welcome_widget.new_project.connect(self.accept)
        welcome_widget.open_project.connect(self._on_open_project)

        VLayout(self, widgets=[container])
        VLayout(container, widgets=[welcome_widget])

    def _on_open_project(self, project_name: str):
        """Handle opening a selected project."""
        self.setProperty("action", StartupCode.Import.name)
        self.setProperty("object", project_name)
        self.done(StartupCode.Import.value)

    def _init_buttons(self) -> QtWidgets.QGroupBox:
        """
        Creates and returns a QGroupBox with three buttons: `New Project`, `Templates`, and `Models`.
        """

        button_style = (
            "QPushButton {"
            "text-align: right;"
            "background: transparent;"
            "}"
            "QPushButton:hover, QPushButton:pressed, QPushButton:checked {"
            "border-left: 2px solid #ffcb00;"
            "border-top-left-radius: 0px;"
            "border-bottom-left-radius: 0px;"
            "}"
        )

        buttons = QtWidgets.QGroupBox(
            flat=True, alignment=QtCore.Qt.AlignmentFlag.AlignRight
        )
        buttons.setFixedWidth(280)

        vlayout = VLayout(buttons, spacing=12, margins=(4, 4, 4, 4))

        vlayout.addStretch(4)
        vlayout.addWidget(new := QtWidgets.QPushButton("New Project"))
        vlayout.addWidget(hdd := QtWidgets.QPushButton("Templates"))
        vlayout.addWidget(mod := QtWidgets.QPushButton("Models"))
        vlayout.addStretch(4)

        self._startup_choice.addButton(mod)
        self._startup_choice.addButton(hdd)

        new.setIcon(qta_icon("mdi.file-plus", color="#ffcb00"))
        hdd.setIcon(qta_icon("mdi.harddisk", color="#966b9d"))
        mod.setIcon(qta_icon("mdi.folder", color="#05b2dc"))
        new.setStyleSheet(button_style)
        hdd.setStyleSheet(button_style)
        mod.setStyleSheet(button_style)

        hdd.setCheckable(True)
        mod.setCheckable(True)
        hdd.setChecked(False)
        mod.setChecked(True)  # Default selection

        new.pressed.connect(self.accept)
        hdd.pressed.connect(self._on_select_template)
        mod.pressed.connect(self._on_select_models)

        return buttons

    def _init_library(self) -> QtWidgets.QFrame:
        """
        Creates the right-side library panel with search bar, file table, and action buttons.
        """

        container = QtWidgets.QFrame(self)
        toolbar_bot = right_justified_toolbar()
        toolbar_top = QtWidgets.QToolBar(self)
        toolbar_top.setObjectName("traffic-lights")
        toolbar_top.setIconSize(QtCore.QSize(20, 20))

        spacer = QtWidgets.QFrame()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        search = QtWidgets.QLineEdit(
            frame=False, clearButtonEnabled=True, placeholderText="Search Projects"
        )
        search.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        search.textChanged.connect(self._on_search)

        toolbar_top.addWidget(search)
        toolbar_top.addWidget(spacer)
        toolbar_top.addAction(
            qta_icon(
                "ph.circle-fill",
                color="#ffcb00",
                active="ph.minus-circle-fill",
                selected="ph.minus-circle-fill",
            ),
            "Minimize",
            self.showMinimized,
        )
        toolbar_top.addAction(
            qta_icon(
                "ph.circle-fill",
                color="#ff5f57",
                active="ph.x-circle-fill",
                selected="ph.x-circle-fill",
            ),
            "Close",
            self.reject,
        )

        quit_btn = QtWidgets.QPushButton("Quit")
        quit_btn.setObjectName("Quit")
        open_btn = QtWidgets.QPushButton("Open")
        open_btn.setObjectName("Open")

        open_btn.setDisabled(True)
        open_btn.setStyleSheet("margin: 4px 4px 4px 4px;")
        open_btn.setFixedWidth(100)
        open_btn.clicked.connect(self.accept)
        quit_btn.setFixedWidth(80)
        quit_btn.clicked.connect(self.reject)

        toolbar_bot.addWidget(quit_btn)
        toolbar_bot.addWidget(open_btn)

        table = widget.FileTable(self)
        table.populate("models", "*.h5")
        table.itemSelectionChanged.connect(self._on_table_item_changed)
        table.itemDoubleClicked.connect(self._on_table_item_double_clicked)

        VLayout(
            container,
            margins=(4, 4, 4, 4),
            spacing=4,
            widgets=[toolbar_top, table, toolbar_bot],
        )

        return container

    def _on_select_template(self):
        """
        Populates the table with template files when the user clicks the "Templates" button.
        """

        if isinstance(
            table := self.findChild(QtWidgets.QTableWidget), widget.FileTable
        ):
            table.populate("templates", "*.sys")
            self.findChild(QtWidgets.QPushButton, "Open").setDisabled(True)

    def _on_select_models(self):
        """
        Populate the table with model files when the user clicks the "Models" button.
        """

        if isinstance(
            table := self.findChild(QtWidgets.QTableWidget), widget.FileTable
        ):
            table.populate("models", "*.clim")
            self.findChild(QtWidgets.QPushButton, "Open").setDisabled(True)

    def _on_search(self, text: str):
        """Filter table by search text."""
        if isinstance(
            table := self.findChild(QtWidgets.QTableWidget), widget.FileTable
        ):
            table.populate("models", f"*{text}*.clim")

    def _on_table_item_changed(self):
        """Enable/disable Open button based on table selection."""
        table = self.findChild(widget.FileTable)
        button = self.findChild(QtWidgets.QPushButton, "Open")

        if table.selectedItems():
            button.setEnabled(True)
        else:
            button.setEnabled(False)

    def _on_table_item_double_clicked(self, item: QtWidgets.QTableWidgetItem):
        """Handle double-click on table item."""
        table = self.findChild(widget.FileTable)
        label = table.cellWidget(item.row(), item.column())

        self.setProperty("action", StartupCode.Import.name)
        self.setProperty("object", label.property("project"))
        self.done(StartupCode.Import.value)
