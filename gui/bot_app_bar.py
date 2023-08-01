from getqt import *


class BarButton(QtWidgets.QToolButton):

    def __init__(self, parent=None):
        super(BarButton, self).__init__(parent)


class BotAppBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BotAppBar, self).__init__(parent)
        self.init_ui(self)

    def init_ui(self, botAppBar):
        self.rowLayout = QtWidgets.QHBoxLayout(self)

        self.backAct = BarButton()
        self.backAct.setIcon(QtGui.QIcon('rsrc/arrow_back.svg'))
        # self.backAct.setIcon(QtGui.QIcon('rsrc/arrow_back_disabled.svg'))

        self.homeAct = BarButton()
        self.homeAct.setIcon(QtGui.QIcon('rsrc/home.svg'))
        # self.homeAct.disabled_icon = QtGui.QIcon('rsrc/home_disabled.svg')

        self.addAct = BarButton()
        self.addAct.setIcon(QtGui.QIcon('rsrc/add.svg'))
        # self.addAct.disabled_icon = QtGui.QIcon('rsrc/add_disabled.svg')

        self.setAct = BarButton()
        self.setAct.setIcon(QtGui.QIcon('rsrc/settings.svg'))
        # self.setAct.disabled_icon = QtGui.QIcon('rsrc/settings_disabled.svg')

        self.okAct = BarButton()
        self.okAct.setIcon(QtGui.QIcon('rsrc/done.svg'))

        self.shareAct = BarButton()
        self.shareAct.setIcon(QtGui.QIcon('rsrc/share.svg'))

        self.rowLayout.addWidget(self.setAct)
        self.rowLayout.addWidget(self.homeAct)
        self.rowLayout.addWidget(self.backAct)
        self.rowLayout.addWidget(self.addAct)
        self.rowLayout.addWidget(self.okAct)
        self.rowLayout.addWidget(self.shareAct)

        for btn in self.findChildren(QtWidgets.QToolButton):
            btn.setIconSize(QtCore.QSize(64, 64))
