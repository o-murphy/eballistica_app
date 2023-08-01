from enum import Enum

class QtBackend(Enum):
    PySide6 = 0
    PyQt6 = 1
    PyQt5 = 2

QT_BACKEND = None



try:
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtCore import Signal, QObject, Slot
    QT_BACKEND = QtBackend.PySide6
except ImportError:
    pass
#     try:
#         from PyQt5 import QtCore, QtWidgets, QtGui
#         from PyQt5.QtCore import pyqtSignal as Signal
#         from PyQt5.QtCore import pyqtSlot as Slot
#         QT_BACKEND = QtBackend.PyQt5
#     except ImportError:
#         from PyQt6 import QtCore, QtWidgets, QtGui
#         from PyQt6.QtCore import pyqtSignal as Signal
#         from PyQt6.QtCore import pyqtSlot as Slot
#         QT_BACKEND = QtBackend.PyQt6
#
# print(QT_BACKEND)

