from PySide6 import QtGui, QtWidgets, QtCore

from gui.widgets import Spacer


class BotAppBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BotAppBar, self).__init__(parent)
        self.init_ui(self)

    def init_ui(self, botAppBar):
        self.rowLayout = QtWidgets.QHBoxLayout(self)

        self.backAct = QtWidgets.QPushButton('<')
        self.homeAct=QtWidgets.QPushButton('Home')
        self.addAct = QtWidgets.QPushButton('+')
        self.setAct = QtWidgets.QPushButton('Set')
        self.rowLayout.addWidget(self.backAct)
        self.rowLayout.addWidget(self.homeAct)
        self.rowLayout.addWidget(self.addAct)
        self.rowLayout.addWidget(self.setAct)

