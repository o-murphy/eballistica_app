from PySide6 import QtWidgets, QtCore, QtGui

from .bullets import BulletsWidget
from .rifles import RiflesWidget, EditRifleWidget


class App(QtWidgets.QMainWindow):

    def __init__(self, app=None):
        super(App, self).__init__(app)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(u"MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(480, 800))
        icon = QtGui.QIcon()
        icon.addFile(u"Icon.ico", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.stacked = QtWidgets.QStackedWidget(MainWindow)
        self.stacked.setObjectName(u"stacked")
        MainWindow.setCentralWidget(self.stacked)

        # self.toolbar = AppToolBar(self)
        # self.addToolBar(self.toolbar)

        self.rifles = RiflesWidget(self)
        self.edit_rifle = EditRifleWidget(self)

        self.bullets = BulletsWidget(self)

        self.stacked.addWidget(self.rifles)
        self.stacked.addWidget(self.edit_rifle)
        self.stacked.addWidget(self.bullets)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connectUi(self)


        self.switch_to_rifles()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", u"ArcherBC", None))

    # def switch_screen(self, widget):
    #     self.stacked.setCurrentWidget(widget)

    def switch_to_rifles(self):
        self.stacked.setCurrentWidget(self.rifles)
        self.rifles.rifles_list.refresh()

    def switch_edit_rifle_screen(self, rifle=None):
        self.edit_rifle.display_data(rifle)
        self.stacked.setCurrentWidget(self.edit_rifle)

    # def store_rifle(self, uid, rifle):
    #     self.switch_to_rifles()
    #     self.rifles.rifles_list.store_rifle(uid, rifle)

    def switch_to_bullets(self, uid, rifle):
        self.stacked.setCurrentWidget(self.bullets)

    def connectUi(self, MainWindow):
        self.rifles.header.addButton.clicked.connect(self.switch_edit_rifle_screen)
        self.edit_rifle.ok_clicked.connect(self.switch_to_rifles)
        self.rifles.rifle_double_clicked_sig.connect(self.switch_edit_rifle_screen)
        self.rifles.rifle_clicked_sig.connect(self.switch_to_bullets)

