# Filename: gui/graph/vertex/config/__init__.py
# Module Name: VertexConfig
# Description: Configuration dialog for VertexItem.

# Standard Library
import weakref

# PySide6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclasses
from dataclasses import field
from dataclasses import dataclass

# Climact
from gui.widgets import GLayout, HLayout, VLayout, ToolBar
from qtawesome import icon as qta_icon


class VertexConfigDialog(QtWidgets.QDialog):
    """Configuration dialog for VertexItem."""

    @dataclass
    class Style:
        border: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x363E41),
                "width": 1,
            }
        )
        background: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x232A2E),
                "brush": QtCore.Qt.BrushStyle.SolidPattern,
                "alpha": 0.5,
                "texture": ":/theme/pattern.png",
            }
        )

    @dataclass
    class Geometric:
        size: dict = field(
            default_factory=lambda: {
                "width": 900,
                "height": 720,
            }
        )

    def __init__(
        self,
        vertex: QtWidgets.QGraphicsObject,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        super().setObjectName(vertex.objectName())

        # Resource(s)
        self._vertex = weakref.ref(vertex)
        self._style = VertexConfigDialog.Style()
        self._geoms = VertexConfigDialog.Geometric()

        # Customization
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # Set the size of the widget
        self.setFixedSize(self._geoms.size["width"], self._geoms.size["height"])

        # UI components
        self._form = self._init_form()
        self._tabs = self._init_tabs()

        # Parent Layout
        layout = HLayout(
            self, spacing=4, margins=(4, 4, 4, 4), widgets=[self._form, self._tabs]
        )
        layout.setStretch(1, 10)

    def _init_form(self) -> QtWidgets.QFrame:

        from core.flow import Time
        from gui.widgets import ComboBox

        frame = QtWidgets.QFrame(self)
        label = QtWidgets.QLineEdit("Process", self)
        combo = ComboBox(self, editable=True)
        tunit = ComboBox(self, editable=True, items=Time.Attrs.units)

        layout = QtWidgets.QFormLayout(
            frame,
            formAlignment=QtCore.Qt.AlignmentFlag.AlignCenter,
            labelAlignment=QtCore.Qt.AlignmentFlag.AlignRight,
            fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow,
        )
        layout.addRow("Entity:", label)
        layout.addRow("Type/Tech:", combo)
        layout.addRow("Time Unit:", tunit)

        # Connect signals
        label.returnPressed.connect(self._on_label_edited)
        combo.currentTextChanged.connect(self._on_combo_edited)
        tunit.currentTextChanged.connect(self._on_tunit_edited)

        return frame

    def _init_tabs(self) -> QtWidgets.QTabWidget:

        # Import StreamTree
        from gui.graph.vertex.config.tree import StreamTree
        from core.flow import ResourceDictionary, ParameterDictionary

        tabs = QtWidgets.QTabWidget(self)
        tabs.addTab(
            StreamTree(self, ResourceDictionary),
            qta_icon("ph.arrows-down-up", color="gray"),
            "Streams",
        )
        tabs.addTab(
            StreamTree(self, ParameterDictionary),
            qta_icon("mdi.alpha", color="magenta"),
            "Parameters",
        )
        tabs.addTab(
            QtWidgets.QWidget(self), qta_icon("mdi.equal", color="cyan"), "Constraints"
        )
        return tabs

    def _on_label_edited(self, text: str):

        vertex = self._vertex()
        if vertex and hasattr(vertex, "rename"):
            vertex.rename(text)

    def _on_combo_edited(self, text: str):
        pass

    def _on_tunit_edited(self, text: str):
        pass

    # Public methods
    def set_label_text(self, text: str):

        label = self.findChild(QtWidgets.QLineEdit)
        if label:
            label.setText(text)

    def paintEvent(self, event, /):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pen = QtCore.Qt.PenStyle.NoPen
        brs = QtGui.QBrush(QtGui.QColor(0x232A2E))
        brs.setTexture(QtGui.QPixmap(":/theme/pattern.png"))

        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(self.rect(), 8, 8)
