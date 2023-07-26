import sys
from enum import IntFlag
from typing import Iterable, Optional, Union, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6 import QtGui

from units import Angular, Distance


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


class MeasureSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, vmin=0, vmax=100, step=1, decimals=2,
                 measure=None, units: int = 0, default_units: int = 0,
                 *args, **kwargs):
        super(MeasureSpinBox, self).__init__(parent, *args, **kwargs)

        self._measure = measure
        self._units = units
        self._default_units = default_units

        self._value = self._measure(0, self._units)

        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setMinimum(vmin)
        self.setMaximum(vmax)
        self.setSingleStep(step)
        self.setDecimals(decimals)

        self.valueChanged.connect(self.on_change)

    def validate(self, text: str, pos: int) -> object:
        text = text.replace(".", ",")
        return QDoubleSpinBox.validate(self, text, pos)

    def valueFromText(self, text: str):
        text = text.replace(",", ".")
        value = float(text)
        self.setValue(value)
        return value

    def setValue(self, val):
        self._value = self._measure(val, self._units)
        print('set', self._value)

    def value(self):
        value = self._value.get_in(self._units)
        return value
    
    def textFromValue(self, val: float) -> str:
        return str(self.value())

    def on_change(self, value):
        print(locals())
        self.setValue(value)


class ComboBox(QComboBox):
    def __init__(self,
                 parent=None,
                 items: Iterable[Union[
                    Tuple[Optional[QtGui.QIcon], Optional[str], Optional[object]],
                    Tuple[Optional[QtGui.QIcon], Optional[str]],
                    Tuple[Optional[str], Optional[object]],
                    Tuple[Optional[QtGui.QIcon]],
                    Tuple[Optional[str]],
                    Tuple[()]
                 ]] = None,
                 *args, **kwargs):
        super(ComboBox, self).__init__(parent, *args, **kwargs)
        if items is not None:
            for item in items:
                self.addItem(*item)


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


class FormRow2(QWidget):
    def __init__(self, label: QLabel, value_field: QWidget, parent=None, *args, **kwargs):
        super(FormRow2, self).__init__(parent, *args, **kwargs)
        self.value_field = value_field
        self.value_field.setParent(self)
        self.label = label
        self.label.setParent(self)
        self.init_ui(self)

    def __getattr__(self, item):
        return self.value_field.__getattribute__(item)

    def set_label_text(self, text: str):
        self.label.setText(text)

    def init_ui(self, formRow3):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rowLayout = QHBoxLayout(self)
        self.rowLayout.setContentsMargins(0, 0, 0, 0)

        self.rowLayout.addWidget(self.label)
        self.rowLayout.addWidget(self.value_field)

        self.rowLayout.setStretchFactor(self.label, 6)
        self.rowLayout.setStretchFactor(self.value_field, 4)


class FormRow3(QWidget):
    def __init__(self, value_field: QWidget, prefix=None, suffix=None, parent=None, *args, **kwargs):
        super(FormRow3, self).__init__(parent, *args, **kwargs)
        self.value_field = value_field
        self.value_field.setParent(self)
        self.init_ui(self)
        self.suffix.setText(suffix)
        self.prefix.setText(prefix)

    def __getattr__(self, item):
        return self.value_field.__getattribute__(item)

    def init_ui(self, formRow3):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rowLayout = QHBoxLayout(self)
        self.rowLayout.setContentsMargins(0, 0, 0, 0)

        self.suffix = QLabel(self)
        self.prefix = QLabel(self)

        self.suffix.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.rowLayout.addWidget(self.prefix)
        self.rowLayout.addWidget(self.value_field)
        self.rowLayout.addWidget(self.suffix)

        self.rowLayout.setStretchFactor(self.prefix, 5)
        self.rowLayout.setStretchFactor(self.value_field, 3)
        self.rowLayout.setStretchFactor(self.suffix, 2)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = MeasureSpinBox(measure=Distance, units=Distance.Inch, default_units=Distance.Millimeter)
    w.setValue(13)
    print(w.value())
    w.show()
    app.exit(app.exec())