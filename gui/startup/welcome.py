from __future__ import annotations

from PySide6 import QtCore, QtWidgets
from qtawesome import icon as qta_icon

from gui.startup.widget import FileTable
from gui.widgets import VLayout, HLayout


# Class StartupWelcome:
class StartupWelcome(QtWidgets.QWidget):
    """Integrated startup welcome screen with project browser."""

    # Signals:
    new_project = QtCore.Signal()
    open_project = QtCore.Signal(str)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        main_layout = HLayout(self, spacing=0, margins=(0, 0, 0, 0))

        # Left panel: Features and quick actions
        left_panel = self._create_left_panel()
        main_layout.addLayout(left_panel, 1)

        # Right panel: Project browser
        right_panel = self._create_right_panel()
        main_layout.addLayout(right_panel, 1)

    def _create_left_panel(self) -> QtWidgets.QVBoxLayout:
        """
        Creates the left panel with a project browser.
        """

        layout = VLayout(spacing=20, margins=(40, 40, 40, 40))

        # Header:
        header_layout = QtWidgets.QHBoxLayout()
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(qta_icon("mdi.leaf", color="#2ecc71").pixmap(64, 64))

        title = QtWidgets.QLabel("Climate Action Tool")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Subtitle:
        subtitle = QtWidgets.QLabel("Build, analyze, and optimize climate models")
        subtitle.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Features:
        features_title = QtWidgets.QLabel("Key Features")
        features_title.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(features_title)

        features = [
            ("mdi.map", "Interactive Map", "Visualize and query geo-spatial data."),
            (
                "mdi.sitemap",
                "Schematic Editor",
                "Build energy/material flow diagrams.",
            ),
            ("mdi.database", "Data Management", "Import and manage datasets"),
            ("mdi.chart-box", "Analytics", "Optimize models and analyze results."),
        ]

        for icon_name, title, desc in features:
            item = self._create_feature_item(icon_name, title, desc)
            layout.addLayout(item)

        layout.addStretch()

        # Action buttons:
        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.setSpacing(8)

        new_btn = QtWidgets.QPushButton("New Project")
        new_btn.setMinimumHeight(36)
        new_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            """
        )
        new_btn.clicked.connect(self.new_project)

        buttons_layout.addWidget(new_btn)
        layout.addLayout(buttons_layout)

        # Footer:
        footer = QtWidgets.QLabel("Version 0.1 • © 2024 Climate Action")
        footer.setStyleSheet("font-size: 10px; color: #95a5a6;")
        layout.addWidget(footer)

        return layout

    def _create_right_panel(self) -> QtWidgets.QVBoxLayout:
        """Create the right panel with project browser."""
        layout = VLayout(spacing=8, margins=(20, 20, 20, 20))

        # Header:
        header = QtWidgets.QLabel("Recent Projects")
        header.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(header)

        # File table:
        self._table = FileTable(self)
        self._table.populate("models", "*.clim")
        self._table.itemDoubleClicked.connect(self._on_table_item_double_clicked)
        self._table.itemSelectionChanged.connect(self._on_table_item_changed)
        layout.addWidget(self._table)

        # Buttons:
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.addStretch()

        quit_btn = QtWidgets.QPushButton("Quit")
        quit_btn.setFixedWidth(80)
        quit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            """
        )

        open_btn = QtWidgets.QPushButton("Open")
        open_btn.setFixedWidth(100)
        open_btn.setEnabled(False)
        open_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover:enabled {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
            """
        )
        open_btn.clicked.connect(self._on_open_clicked)

        self._open_btn = open_btn
        self._quit_btn = quit_btn

        button_layout.addWidget(quit_btn)
        button_layout.addWidget(open_btn)
        layout.addLayout(button_layout)

        return layout

    def _create_feature_item(
        self, icon_name: str, title: str, desc: str
    ) -> QtWidgets.QHBoxLayout:
        """Create a feature item."""
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(12)

        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(qta_icon(icon_name, color="#3498db").pixmap(28, 28))
        icon_label.setFixedSize(28, 28)

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 11px; color: #2c3e50;")

        desc_label = QtWidgets.QLabel(desc)
        desc_label.setStyleSheet("font-size: 10px; color: #7f8c8d;")
        desc_label.setWordWrap(True)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)

        layout.addWidget(icon_label)
        layout.addLayout(text_layout)

        return layout

    def _on_table_item_changed(self):
        """
        Enable/disable Open button based on selection.
        """
        self._open_btn.setEnabled(len(self._table.selectedItems()) > 0)

    def _on_table_item_double_clicked(self, item):
        """
        Handle double-click on a table item.
        """

        self._on_open_clicked()

    def _on_open_clicked(self):
        """Emit open_project signal with the selected file."""
        selected = self._table.selectedItems()
        if selected:
            widget = self._table.cellWidget(selected[0].row(), 0)
            if widget:
                project_name = widget.property("project")
                self.open_project.emit(project_name)

    def quit_button(self) -> QtWidgets.QPushButton:
        """Get the quit button for connection in the dialog."""
        return self._quit_btn
