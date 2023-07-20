from PySide6 import QtGui, QtWidgets, QtCore

from gui.widgets import Spacer


class BotAppBar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(BotAppBar, self).__init__(parent)
        self.init_ui(self)

    def init_ui(self, botAppBar):
        self.backAct = QtGui.QAction('<', self)
        self.homeAct=QtGui.QAction('Home', self)
        self.addAct = QtGui.QAction('+', self)
        self.setAct = QtGui.QAction('Set', self)
        self.addActions((self.backAct, self.homeAct, self.addAct, self.setAct))

