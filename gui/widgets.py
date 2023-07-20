from PySide6.QtGui import QPainter
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


class DSpinBoxHCenter(QDoubleSpinBox):

    def __init__(self, vmin=0, vmax=100, step=1, suffix=None, prefix=None, *args, **kwargs):
        super(DSpinBoxHCenter, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setMinimum(vmin)
        self.setMaximum(vmax)
        self.setSingleStep(step)
        self.setSuffix(suffix)
        self.setPrefix(prefix)


class ComboBoxHCenter(QComboBox):

    class Delegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            option.displayAlignment = Qt.AlignmentFlag.AlignCenter  # Set the alignment as needed

    def __init__(self, *args, **kwargs):
        super(ComboBoxHCenter, self).__init__(*args, **kwargs)
        self.setItemDelegate(self.Delegate())


class FormSpinBox(QWidget):
    def __init__(self, parent=None, vmin=0, vmax=100, step=1, suffix=None, prefix=None, *args, **kwargs):
        super(FormSpinBox, self).__init__(parent, *args, **kwargs)
        self.init_ui(self)
        self.value_field.setMinimum(vmin)
        self.value_field.setMaximum(vmax)
        self.value_field.setSingleStep(step)
        self.suffix.setText(suffix)
        self.prefix.setText(prefix)

    def init_ui(self, form):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rowLayout = QHBoxLayout(self)
        self.rowLayout.setContentsMargins(0, 0, 0, 0)

        self.prefix = QLabel()
        self.value_field = DSpinBoxHCenter()
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

    def findData(self, *args, **kwargs):
        return self.value_field.findData(*args, **kwargs)

    def setCurrentIndex(self, *args, **kwargs):
        self.value_field.setCurrentIndex(*args, **kwargs)

    def currentData(self, *args, **kwargs):
        return self.value_field.currentData(*args, **kwargs)


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

