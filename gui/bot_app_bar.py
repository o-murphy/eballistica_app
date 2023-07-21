from PySide6 import QtGui, QtWidgets, QtCore


class BotAppBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BotAppBar, self).__init__(parent)
        self.init_ui(self)

    def init_ui(self, botAppBar):
        self.rowLayout = QtWidgets.QHBoxLayout(self)

        self.backAct = QtWidgets.QToolButton()
        self.backAct.setIcon(QtGui.QIcon('rsrc/arrow_back.svg'))
        self.homeAct = QtWidgets.QToolButton()
        self.homeAct.setIcon(QtGui.QIcon('rsrc/home.svg'))
        self.addAct = QtWidgets.QToolButton()
        self.addAct.setIcon(QtGui.QIcon('rsrc/add.svg'))
        self.setAct = QtWidgets.QToolButton()
        self.setAct.setIcon(QtGui.QIcon('rsrc/settings.svg'))
        self.rowLayout.addWidget(self.setAct)
        self.rowLayout.addWidget(self.homeAct)
        self.rowLayout.addWidget(self.backAct)
        self.rowLayout.addWidget(self.addAct)

        buttons = self.findChildren(QtWidgets.QToolButton)
        for btn in buttons:
            btn.setIconSize(QtCore.QSize(64, 64))
