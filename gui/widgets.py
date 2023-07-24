from enum import IntFlag

from PySide6.QtCore import Qt
from PySide6.QtWidgets import *


class SpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, vmin=0, vmax=100, step=1, suffix=None, prefix=None, decimals=2, *args, **kwargs):
        super(SpinBox, self).__init__(parent, *args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setMinimum(vmin)
        self.setMaximum(vmax)
        self.setSingleStep(step)
        self.setSuffix(suffix)
        self.setPrefix(prefix)
        self.setDecimals(decimals)

    def validate(self, text: str, pos: int) -> object:
        text = text.replace(".", ",")
        return QDoubleSpinBox.validate(self, text, pos)

    def valueFromText(self, text: str) -> float:
        text = text.replace(",", ".")
        return float(text)


class Button(QPushButton):
    class Type(IntFlag):
        Elevated = 1
        Filled = 2
        Tonal = 4
        Outlined = 8
        Text = 16

    Elevated = '''
        QPushButton {
            background-color: #3498db;
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        }

        QPushButton:hover {
            background-color: #2980b9;
        }

        QPushButton:pressed {
            background-color: #1f618d;
        }
    '''

    def __init__(self, *args, flags: Type = Type.Elevated, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.compileStyle(flags)

    def compileStyle(self, flags: Type):
        if flags:
            style = self.styleSheet()
            if flags & Button.Type.Elevated:
                style += Button.Elevated
            print(style)
            self.setStyleSheet(style)


class Spacer(QWidget):
    Vertical = 0
    Horizontal = 1

    def __init__(self, parent=None, width: int = 1, direction=Vertical):
        super(Spacer, self).__init__(parent)
        if direction is Spacer.Vertical:
            self.setFixedWidth(width)
        elif direction is Spacer.Horizontal:
            self.setFixedHeight(width)
        else:
            raise ValueError(direction)


class ComboBoxHCenter(QComboBox):
    class Delegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            option.displayAlignment = Qt.AlignmentFlag.AlignCenter  # Set the alignment as needed

    def __init__(self, *args, **kwargs):
        super(ComboBoxHCenter, self).__init__(*args, **kwargs)
        self.setItemDelegate(self.Delegate())


class FormSpinBox(QWidget):
    def __init__(self, parent=None, vmin=0, vmax=100, step=1, suffix=None, prefix=None, decimals=2, *args, **kwargs):
        super(FormSpinBox, self).__init__(parent, *args, **kwargs)
        self.init_ui(self)
        self.value_field.setMinimum(vmin)
        self.value_field.setMaximum(vmax)
        self.value_field.setSingleStep(step)
        self.suffix.setText(suffix)
        self.prefix.setText(prefix)
        self.value_field.setDecimals(decimals)

    def init_ui(self, form):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rowLayout = QHBoxLayout(self)
        self.rowLayout.setContentsMargins(0, 0, 0, 0)

        self.prefix = QLabel()
        self.value_field = SpinBox()
        self.suffix = QLabel()
        self.suffix.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.rowLayout.addWidget(self.prefix)
        self.rowLayout.addWidget(self.value_field)
        self.rowLayout.addWidget(self.suffix)

        self.rowLayout.setStretchFactor(self.prefix, 6)
        self.rowLayout.setStretchFactor(self.value_field, 3)
        self.rowLayout.setStretchFactor(self.suffix, 1)

    def setValue(self, *args, **kwargs):
        self.value_field.setValue(*args, **kwargs)

    def value(self):
        return self.value_field.value()


class FormComboBox(QWidget):
    def __init__(self, parent=None, suffix=None, prefix=None, *args, **kwargs):
        super(FormComboBox, self).__init__(parent, *args, **kwargs)
        self.init_ui(self)
        self.suffix.setText(suffix)
        self.prefix.setText(prefix)

    def init_ui(self, measure_widget):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rowLayout = QHBoxLayout(self)
        self.rowLayout.setContentsMargins(0, 0, 0, 0)
        self.prefix = QLabel()
        self.value_field = QComboBox()
        self.suffix = QLabel()
        self.rowLayout.addWidget(self.prefix)
        self.rowLayout.addWidget(self.value_field)
        self.rowLayout.addWidget(self.suffix)

        self.suffix.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.rowLayout.setStretchFactor(self.prefix, 6)
        self.rowLayout.setStretchFactor(self.value_field, 3)
        self.rowLayout.setStretchFactor(self.suffix, 1)

    def addItem(self, *args, **kwargs):
        self.value_field.addItem(*args, **kwargs)

    def addItems(self, data):
        self.value_field.addItems(data)

    def findData(self, *args, **kwargs):
        return self.value_field.findData(*args, **kwargs)

    def setCurrentIndex(self, *args, **kwargs):
        self.value_field.setCurrentIndex(*args, **kwargs)

    def currentData(self, *args, **kwargs):
        return self.value_field.currentData(*args, **kwargs)

    @property
    def currentIndex(self):
        return self.value_field.currentIndex

    @property
    def currentIndexChanged(self):
        return self.value_field.currentIndexChanged


class FormCheckBox(QWidget):
    def __init__(self, parent=None, suffix=None, prefix=None, *args, **kwargs):
        super(FormCheckBox, self).__init__(parent, *args, **kwargs)
        self.init_ui(self)
        self.suffix.setText(suffix)
        self.prefix.setText(prefix)

    def init_ui(self, measure_widget):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rowLayout = QHBoxLayout(self)
        self.rowLayout.setContentsMargins(0, 0, 0, 0)
        self.prefix = QLabel()
        self.value_field = QCheckBox()
        self.suffix = QLabel()
        self.rowLayout.addWidget(self.prefix)
        self.rowLayout.addWidget(self.value_field)
        self.rowLayout.addWidget(self.suffix)

        self.suffix.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.rowLayout.setStretchFactor(self.prefix, 6)
        self.rowLayout.setStretchFactor(self.value_field, 3)
        self.rowLayout.setStretchFactor(self.suffix, 1)

    def isChecked(self):
        return self.value_field.isChecked()

    def setChecked(self, value: bool):
        self.value_field.setChecked(value)


class FormButton(QWidget):
    def __init__(self, parent=None, text='', suffix=None, prefix=None, *args, **kwargs):
        super(FormButton, self).__init__(parent, *args, **kwargs)
        self.init_ui(self)
        self.value_field.setText(text)
        self.suffix.setText(suffix)
        self.prefix.setText(prefix)

    @property
    def clicked(self):
        return self.value_field.clicked

    def text(self):
        return self.value_field.text()

    def setText(self, text):
        self.value_field.setText(text)

    def init_ui(self, form):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rowLayout = QHBoxLayout(self)
        self.rowLayout.setContentsMargins(0, 0, 0, 0)

        self.prefix = QLabel()
        self.value_field = QPushButton()
        self.suffix = QLabel()
        self.suffix.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.rowLayout.addWidget(self.prefix)
        self.rowLayout.addWidget(self.value_field)
        self.rowLayout.addWidget(self.suffix)

        self.rowLayout.setStretchFactor(self.prefix, 6)
        self.rowLayout.setStretchFactor(self.value_field, 3)
        self.rowLayout.setStretchFactor(self.suffix, 1)
