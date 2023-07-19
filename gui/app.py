from PySide6 import QtWidgets, QtCore, QtGui

from .ammos import AmmosWidget, EditAmmoWidget
from .rifles import RiflesWidget, EditRifleWidget


# class AppState(QtCore.QObject):
#     def __init__(self, parent=None):
#         super(AppState, self).__init__(parent)
#         self.rifle_id = None
#         self.ammo_id = None


class App(QtWidgets.QMainWindow):

    def __init__(self, app=None):
        super(App, self).__init__(app)
        self.setupUi(self)

        # self.app_state = AppState()

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

        self.ammos = AmmosWidget(self)
        self.edit_ammo = EditAmmoWidget(self)

        self.stacked.addWidget(self.rifles)
        self.stacked.addWidget(self.edit_rifle)
        self.stacked.addWidget(self.ammos)
        self.stacked.addWidget(self.edit_ammo)

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

    def switch_to_ammos(self, rifle):
        self.ammos.ammos_list.set_filter(rifle=rifle)
        self.ammos.ammos_list.refresh()
        self.stacked.setCurrentWidget(self.ammos)

    def switch_edit_ammo_screen(self, ammo=None):
        rifle = self.ammos.ammos_list.filter.get('rifle')
        self.edit_ammo.display_data(rifle, ammo)
        self.stacked.setCurrentWidget(self.edit_ammo)

    def connectUi(self, MainWindow):
        self.rifles.header.addButton.clicked.connect(self.switch_edit_rifle_screen)
        self.edit_rifle.ok_clicked.connect(self.switch_to_rifles)
        self.rifles.rifle_double_clicked_sig.connect(self.switch_edit_rifle_screen)
        self.rifles.rifle_clicked_sig.connect(self.switch_to_ammos)

        self.ammos.header.addButton.clicked.connect(self.switch_edit_ammo_screen)
        self.edit_ammo.ok_clicked.connect(self.switch_to_ammos)
        self.ammos.ammo_double_clicked_sig.connect(self.switch_edit_ammo_screen)


