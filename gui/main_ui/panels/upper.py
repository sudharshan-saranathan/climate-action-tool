# Filename: upper.py
# Module name: panels
# Description: Upper panel to be shown within a dock

# Pyside6 (Python/Qt)
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Dataclass
from dataclasses import field
from dataclasses import dataclass


class UpperPanel(QtWidgets.QFrame):

    @dataclass
    class Style:
        border: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x40474D),
                "width": 1.0,
            }
        )

        background: dict = field(
            default_factory=lambda: {
                "color": QtGui.QColor(0x40474D),
                "brush": QtCore.Qt.BrushStyle.SolidPattern,
            }
        )

    def __init__(self, parent=None):
        super().__init__(parent)

        # Instantiate dataclasses
        self._style = UpperPanel.Style()

        # Customize appearance and behaviour:
        self.setContentsMargins(8, 8, 8, 8)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # UI components
        self._init_form()

    def _init_form(self):

        # Set up form fields
        name_edit = QtWidgets.QLineEdit("Example-Industry.hdf5")
        name_edit.setEnabled(False)

        text_edit = QtWidgets.QTextEdit()
        combo_box = QtWidgets.QComboBox()
        spin_start = QtWidgets.QSpinBox()
        spin_final = QtWidgets.QSpinBox()

        # Define field growth policy
        growth_policy = QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow

        # Configure form layout
        self._form = QtWidgets.QFormLayout(self)
        self._form.setFieldGrowthPolicy(growth_policy)
        self._form.setContentsMargins(0, 0, 0, 0)
        self._form.setSpacing(4)

        # Add form rows
        self._form.addRow("Project:", name_edit)
        self._form.addRow("Scenario:", combo_box)
        self._form.addRow("Start Epoch:", spin_start)
        self._form.addRow("Final Epoch:", spin_final)
        self._form.addRow("", QtWidgets.QFrame())

        # Configure widget values
        text_edit.setMaximumHeight(160)
        spin_start.setRange(-100, 100)
        spin_final.setRange(-100, 100)
        spin_final.setValue(50)

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pen = QtGui.QPen(self._style.border["color"], self._style.border["width"])
        brs = QtGui.QBrush(self._style.background["color"])

        painter.setPen(pen)
        painter.setBrush(brs)
        painter.drawRoundedRect(self.rect(), 4, 4)
