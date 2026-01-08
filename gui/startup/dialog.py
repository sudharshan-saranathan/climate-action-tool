# Encoding: utf-8
# Module name: screen
# Description: The application's startup window.

# Imports (standard)
import enum

# Imports (third party)
from qtawesome import icon as qta_icon
from PySide6 import QtCore, QtWidgets

# Imports (local)
from gui.startup import widget
from gui.custom import VLayout, HLayout


# Result Codes:
class StartupCode(enum.Enum):
    Closed = -1
    Quit = 0
    New = 1
    Import = 2
    Templates = 3


# Class StartupDialog:
class StartupDialog(QtWidgets.QDialog):
    """
    A startup widget for the Climact application offering options to start a new project, import from templates, or open
    existing models.
    """

    def __init__(self):
        super().__init__(None)  # Startup dialog has no parent

        # The `_startup_choice` button group includes the "Template" and "Models" push-buttons.
        # Selecting one of these buttons updates the file table on the right-side panel to show
        # the appropriate files in the relevant subdirectory.
        self._startup_choice = QtWidgets.QButtonGroup(
            exclusive=True
        )  # Create a button group for the "Template" and "Models" buttons
        self._setup_ui()  # Set up the UI

        self.setObjectName(
            "startup-dialog"
        )  # DO NOT MODIFY: This name is referenced in the style-file for customized styling
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )  # Make the dialog background transparent
        self.setWindowFlag(
            QtCore.Qt.WindowType.FramelessWindowHint
        )  # Make it frameless to remove the title-bar

    # Set up the UI:
    def _setup_ui(self):

        # Import(s):
        from gui import custom

        # The `QDialog` is itself transparent, so we need a non-transparent container to organize the child widgets and
        # display the background. This is also one of the ways to enforce rounded corners on the dialog, independent of
        # the platform and native main_ui manager.
        container = QtWidgets.QFrame(self)  # The `QFrame` is made non-transparent via QSS styling.
        container.setObjectName(
            "startup-dialog-container"
        )  # DO NOT MODIFY: This name is used in the QSS file.
        container.setFixedSize(900, 640)  # The startup main_ui's size is fixed.

        VLayout(self, widgets=[container])  # Use a simple `VLayout` to hold the container widget.
        HLayout(container, widgets=[self._init_buttons(), self._init_library()])

    # Initialize the options panel:
    def _init_buttons(self) -> QtWidgets.QGroupBox:

        # Push-button styling only for the startup windows:
        _style = (
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

        # Button group-box (without a label) to arrange the choice-buttons:
        buttons = QtWidgets.QGroupBox(flat=True, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        buttons.setFixedWidth(280)

        vlayout = VLayout(
            buttons, spacing=12, margins=(4, 4, 4, 4)
        )  # Vertical layout to arrange the choice-buttons

        vlayout.addStretch(4)
        vlayout.addWidget(new := QtWidgets.QPushButton("New Project"))  # New Project button
        vlayout.addWidget(hdd := QtWidgets.QPushButton("Templates"))  # Templates button
        vlayout.addWidget(mod := QtWidgets.QPushButton("Models"))  # Models button
        vlayout.addStretch(4)

        self._startup_choice.addButton(mod)
        self._startup_choice.addButton(hdd)

        new.setIcon(qta_icon("mdi.file-plus", color="#ffcb00"))
        hdd.setIcon(qta_icon("mdi.harddisk", color="#966b9d"))
        mod.setIcon(qta_icon("mdi.folder", color="#05b2dc"))
        new.setStyleSheet(_style)
        hdd.setStyleSheet(_style)
        mod.setStyleSheet(_style)

        hdd.setCheckable(True)  # Make the "Templates" and "Models" buttons checkable
        mod.setCheckable(True)
        hdd.setChecked(False)
        mod.setChecked(True)  # Default selection is "Models"

        new.pressed.connect(self.accept)  # The new project button simply accepts the dialog
        hdd.pressed.connect(self._on_select_template)  # Callback for the "Templates" button
        mod.pressed.connect(self._on_select_models)  # Callback for the "Models" button

        # Initialize of all buttons is done; return the group-box:
        return buttons

    # Initialize the table:
    def _init_library(self) -> QtWidgets.QFrame:

        # Import startup widget:
        from gui.startup import widget
        from util import right_justified_toolbar

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

        # Add buttons to the top toolbar:
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

        toolbar_bot.addWidget(_quit := QtWidgets.QPushButton("Quit"))
        _quit.setObjectName("Quit")
        toolbar_bot.addWidget(_open := QtWidgets.QPushButton("Open"))
        _open.setObjectName("Open")

        _open.setDisabled(True)
        _open.setStyleSheet("margin: 12px 12px 12px 2px;")
        _open.setFixedWidth(100)
        _open.clicked.connect(self.accept)
        _quit.setFixedWidth(80)
        _quit.clicked.connect(self.reject)

        # Subdirectory:
        subdir = "models"
        pattern = "*.clim"

        # Create the table:
        table = widget.FileTable(self)
        table.populate(subdir, pattern)
        table.itemSelectionChanged.connect(self._on_table_item_changed)
        table.itemDoubleClicked.connect(self._on_table_item_double_clicked)

        # Add widgets to the layout:
        VLayout(
            container,
            margins=(4, 4, 4, 4),
            spacing=4,
            widgets=[toolbar_top, table, toolbar_bot],  # Add widgets to the layout
        )

        # Return the table:
        return container

    # Open a file dialog to import a project:
    def _on_select_template(self):

        # Find the `widget.FileTable` widget:
        if isinstance(table := self.findChild(QtWidgets.QTableWidget), widget.FileTable):
            table.populate("templates", "*.sys")

        # Disable the "Open" button:
        self.findChild(QtWidgets.QPushButton, "Open").setDisabled(True)

    # Open a file dialog to import a project:
    def _on_select_models(self):

        # Find the `widget.FileTable` widget:
        if isinstance(table := self.findChild(QtWidgets.QTableWidget), widget.FileTable):
            table.populate("models", "*.clim")

        # Disable the "Open" button:
        self.findChild(QtWidgets.QPushButton, "Open").setDisabled(True)

    # Search the project table:
    def _on_search(self, text: str):

        # Find the `widget.FileTable` widget:
        if isinstance(table := self.findChild(QtWidgets.QTableWidget), widget.FileTable):
            table.populate("models", f"*{text}*.clim")

    # Callback when the user selects a project in the table:
    def _on_table_item_changed(self):

        table = self.findChild(widget.FileTable)
        button = self.findChild(QtWidgets.QPushButton, "Open")

        if table.selectedItems():
            button.setEnabled(True)
        else:
            button.setEnabled(False)

    # Callback when the user double-clicks a project in the table:
    def _on_table_item_double_clicked(self, item: QtWidgets.QTableWidgetItem):

        table = self.findChild(widget.FileTable)
        label = table.cellWidget(item.row(), item.column())

        self.setProperty("action", StartupCode.Import.name)
        self.setProperty("object", label.property("project"))
        self.done(StartupCode.Import.value)
