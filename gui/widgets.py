from typing import Iterable, Optional, Union, Tuple

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

from units import Distance, Convertor


class AbstractScroller:

    def __init__(self, viewport: QWidget = None):
        self._viewport = viewport

        self._sp = QScrollerProperties()
        # self._sp.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.6)
        self._sp.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.1)
        self._sp.setScrollMetric(QScrollerProperties.ScrollingCurve, QtCore.QEasingCurve(QtCore.QEasingCurve.OutExpo))
        self._sp.setScrollMetric(QScrollerProperties.MinimumVelocity, 0.0)
        self._sp.setScrollMetric(QScrollerProperties.MaximumVelocity, 0.2)
        self._sp.setScrollMetric(QScrollerProperties.AcceleratingFlickMaximumTime, 0.5)
        self._sp.setScrollMetric(QScrollerProperties.AcceleratingFlickSpeedupFactor, 1.2)
        # self._sp.setScrollMetric(QScrollerProperties.SnapPositionRatio, 0.2)
        self._sp.setScrollMetric(QScrollerProperties.SnapPositionRatio, 1)
        self._sp.setScrollMetric(QScrollerProperties.MaximumClickThroughVelocity, 1)
        self._sp.setScrollMetric(QScrollerProperties.DragStartDistance, 0.001)
        self._sp.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0.5)

        self._gesture = QScroller.scroller(self._viewport)
        self._gesture.setScrollerProperties(self._sp)

    def setScrollable(self, is_true: bool, gesture: QScroller.ScrollerGestureType):
        if is_true:
            self._gesture.grabGesture(self._viewport, QScroller.LeftMouseButtonGesture)
        else:
            self._gesture.ungrabGesture(self._viewport)


class GesturedListView(QListWidget):

        def __init__(self, parent=None):
            super(GesturedListView, self).__init__(parent)
            self.setupUi(self)
            # self.connectUi(self)
            # self.refresh()

            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.showContextMenu)
            self.setMouseTracking(True)  # Enable mouse tracking to receive mouseMoveEvent
            self.startPos = None
            self.isLongPress = False
            self.timerId = None

        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                self.isLongPress = False
                self.startPos = event.pos()
                self.timerId = self.startTimer(200)  # Start the timer for long-press detection

            super(GesturedListView, self).mousePressEvent(event)

        def mouseReleaseEvent(self, event):
            if event.button() == Qt.LeftButton:
                if self.timerId is not None:
                    self.killTimer(self.timerId)  # Stop the timer if it's still running
                    self.timerId = None

                endPos = event.pos()
                distance = (endPos - self.startPos).manhattanLength()

                if distance < QApplication.startDragDistance() and not self.isLongPress:
                    # If the distance is less than startDragDistance, it's a short click
                    self.runDefaultClickAction()

            super(GesturedListView, self).mouseReleaseEvent(event)

        def runDefaultClickAction(self):
            ...

        def timerEvent(self, event):
            if event.timerId() == self.timerId:
                self.isLongPress = True
                self.killTimer(self.timerId)  # Stop the timer

                # Open the context menu
                self.showContextMenu()

        def showContextMenu(self, pos=None):
            ...

        def onContextMenuAction(self, item, action):
            ...

        def setupUi(self, listView):
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            self.setSizePolicy(sizePolicy)

            self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            self.scroller = AbstractScroller(self.viewport())
            self.scroller.setScrollable(True, QScroller.LeftMouseButtonGesture)

            self.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                show-decoration-selected: 0;
                /*padding:0;
                margin:0;*/
                }
                
                QListWidget::item:selected {
                border-left: none;
                border-top:none;
                border-right:none;
                border-bottom:none;
                background: transparent;
                }
                
                QListWidget::item:selected:active {
                background: transparent;
                border-left: none;
                border-top:none;
                border-right:none;
                border-bottom:none;
                }
                
                QListWidget::item:selected:!active {
                background: transparent;
                border-left: none;
                border-top:none;
                border-right:none;
                border-bottom:none;
                }
                
                QListWidget::item:hover {
                    border-left: 3px solid #008080;
                    border-top:none;
                    border-right:none;
                    border-bottom:none;
                    background: transparent;
                }
                
            """)


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


class ConverSpinBox(QDoubleSpinBox):
    def __init__(self, parent, step=1, name: str = None, vmin=-10000, vmax=10000):
        super(ConverSpinBox, self).__init__(parent)

        if name:
            self.setObjectName(name)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setMinimum(vmin)
        self.setMaximum(vmax)
        self.setSingleStep(step)
        # self.setDecimals(decimals)

        self._convertor: Convertor = None

    def validate(self, text: str, pos: int) -> object:
        text = text.replace(".", ",")
        return QDoubleSpinBox.validate(self, text, pos)

    def valueFromText(self, text: str) -> float:
        text = text.replace(",", ".")
        return float(text)

    def convertor(self) -> Convertor:
        return self._convertor

    def setConvertor(self, value: Convertor):
        self._convertor = value
        self.setDecimals(self._convertor.accuracy)
        single_step = 10**(-self.decimals())
        self.setSingleStep(single_step)

    def setRawValue(self, value):
        if self._convertor is not None:
            self.setValue(self._convertor.fromRaw(value))
        else:
            self.setValue(value)

    def rawValue(self):
        if self._convertor is not None:
            return self._convertor.toRaw(self.value())
        else:
            return self.value()


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
    ...

