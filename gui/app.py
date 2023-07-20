from PySide6 import QtWidgets, QtCore, QtGui

from .ammos import AmmosWidget, EditAmmoWidget, EditShotWidget
from .app_logo import AppHeader
from .bot_app_bar import BotAppBar
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

        self.main_widget = QtWidgets.QWidget(MainWindow)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        MainWindow.setCentralWidget(self.main_widget)

        self.header = AppHeader(self)
        self.stacked = QtWidgets.QStackedWidget(self)
        self.stacked.setObjectName(u"stacked")
        self.botAppBar = BotAppBar(self)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.stacked)
        self.main_layout.addWidget(self.botAppBar)

        self.rifles = RiflesWidget(self)
        self.edit_rifle = EditRifleWidget(self)

        self.ammos = AmmosWidget(self)
        self.edit_ammo = EditAmmoWidget(self)

        self.edit_shot = EditShotWidget(self)

        self.stacked.addWidget(self.rifles)
        self.stacked.addWidget(self.edit_rifle)
        self.stacked.addWidget(self.ammos)
        self.stacked.addWidget(self.edit_ammo)
        self.stacked.addWidget(self.edit_shot)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connectUi(self)

        self.switch_to_rifles()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", u"ArcherBC", None))

    def switch_to_rifles(self):
        self.rifles.rifles_list.refresh()
        self.stacked.setCurrentWidget(self.rifles)

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

    def switch_edit_shot_screen(self, ammo=None):
        rifle = self.ammos.ammos_list.filter.get('rifle')
        self.edit_shot.display_data(rifle, ammo)
        self.stacked.setCurrentWidget(self.edit_shot)

    def go_back(self):
        current_screen = self.stacked.currentWidget()
        if current_screen == self.edit_rifle:
            self.stacked.setCurrentWidget(self.rifles)
        elif current_screen == self.edit_ammo:
            self.stacked.setCurrentWidget(self.ammos)
        elif current_screen == self.ammos:
            self.stacked.setCurrentWidget(self.rifles)
        elif current_screen == self.edit_shot:
            self.stacked.setCurrentWidget(self.ammos)

    def go_add(self):
        current_screen = self.stacked.currentWidget()
        if current_screen == self.rifles:
            self.switch_edit_rifle_screen()
        elif current_screen == self.ammos:
            rifle = self.ammos.ammos_list.filter.get('rifle')
            if rifle:
                self.switch_edit_ammo_screen(rifle)

    def connectUi(self, MainWindow):
        # self.rifles.header.addButton.clicked.connect(self.switch_edit_rifle_screen)
        self.edit_rifle.ok_clicked.connect(self.switch_to_rifles)
        self.rifles.rifle_double_clicked_sig.connect(self.switch_edit_rifle_screen)
        self.rifles.rifle_clicked_sig.connect(self.switch_to_ammos)

        # self.ammos.header.addButton.clicked.connect(self.switch_edit_ammo_screen)
        self.edit_ammo.ok_clicked.connect(self.switch_to_ammos)
        self.ammos.ammo_double_clicked_sig.connect(self.switch_edit_ammo_screen)
        self.ammos.ammo_clicked_sig.connect(self.switch_edit_shot_screen)
        self.edit_shot.ok_clicked.connect(self.switch_to_ammos)

        self.botAppBar.homeAct.triggered.connect(self.switch_to_rifles)
        self.botAppBar.backAct.triggered.connect(self.go_back)
        self.botAppBar.addAct.triggered.connect(self.go_add)


