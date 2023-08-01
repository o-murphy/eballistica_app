from PySide6 import QtWidgets, QtCore, QtGui
from qt_material import QtStyleTools

from datatypes.dbworker import DragModel
from .ammos import EditAmmoWidget, EditShotWidget, AmmosLi
from .app_logo import AppHeader
from .bot_app_bar import BotAppBar
from .drag_model import MultiBCWidget, CDMWidget
from .powder_sens import PowderSensWindget
from .rifles import EditRifleWidget, RiflesLi
from .settings import SettingsWidget
from .trajectory import TrajectoryWidget


class App(QtWidgets.QMainWindow, QtStyleTools):

    def __init__(self, app=None):
        super(App, self).__init__(app)
        self.setupUi(self)

        self.status_bar.showMessage('Data loaded', timeout=2000)

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

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.stacked)

        self.status_bar = QtWidgets.QStatusBar(self)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.status_bar)
        self.main_layout.addWidget(self.botAppBar)

        self.settings = SettingsWidget(self)

        self.rifles = RiflesLi(self)
        self.edit_rifle = EditRifleWidget(self)

        self.ammos = AmmosLi(self)
        self.edit_ammo = EditAmmoWidget(self)

        self.edit_shot = EditShotWidget(self)

        self.multi_bc = MultiBCWidget(self)
        self.cdm = CDMWidget(self)

        self.powder_sens = PowderSensWindget(self)

        self.trajectory = TrajectoryWidget(self)

        self.settings.update_settings()

        self.stacked.addWidget(self.rifles)
        self.stacked.addWidget(self.edit_rifle)
        self.stacked.addWidget(self.ammos)
        self.stacked.addWidget(self.edit_ammo)
        self.stacked.addWidget(self.edit_shot)
        self.stacked.addWidget(self.multi_bc)
        self.stacked.addWidget(self.cdm)
        self.stacked.addWidget(self.powder_sens)
        self.stacked.addWidget(self.settings)
        self.stacked.addWidget(self.trajectory)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connectUi(self)

        self.switch_to_rifles()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", u"ArcherBC", None))

    def switch_to_rifles(self):
        # self.rifles.rifles_list.refresh()
        self.rifles.refresh()
        self.stacked.setCurrentWidget(self.rifles)
        self.screen_changed(self.stacked.currentIndex())

    def switch_edit_rifle_screen(self, rifle=None):
        self.edit_rifle.display_data(rifle)
        self.stacked.setCurrentWidget(self.edit_rifle)

    def switch_to_ammos(self, rifle):
        self.ammos.set_filter(rifle=rifle)
        self.ammos.refresh()
        self.stacked.setCurrentWidget(self.ammos)

    def switch_edit_ammo_screen(self, ammo=None):
        rifle = self.ammos.filter.get('rifle')
        self.edit_ammo.display_data(rifle, ammo)
        self.stacked.setCurrentWidget(self.edit_ammo)

    def switch_edit_shot_screen(self, ammo=None):
        rifle = self.ammos.filter.get('rifle')
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
        elif current_screen in (self.multi_bc, self.cdm, self.powder_sens):
            self.stacked.setCurrentWidget(self.edit_ammo)
        elif current_screen == self.settings:
            self.stacked.setCurrentWidget(self.rifles)
        elif current_screen == self.trajectory:
            self.stacked.setCurrentWidget(self.edit_shot)

    def go_add(self):
        current_screen = self.stacked.currentWidget()
        if current_screen == self.rifles:
            self.switch_edit_rifle_screen()
        elif current_screen == self.ammos:
            rifle = self.ammos.filter.get('rifle')
            if rifle:
                self.switch_edit_ammo_screen(rifle)

    def screen_changed(self, index):
        current_screen = self.stacked.currentWidget()

        if current_screen == self.rifles:
            self.botAppBar.okAct.setHidden(True)
            self.botAppBar.backAct.setHidden(True)
            self.botAppBar.addAct.setVisible(True)
            self.botAppBar.setAct.setVisible(True)
            self.botAppBar.homeAct.setHidden(True)
            self.botAppBar.shareAct.setHidden(True)

            self.header.bread.setText('Rifles')

        elif current_screen == self.ammos:
            self.botAppBar.okAct.setHidden(True)
            self.botAppBar.backAct.setVisible(True)
            self.botAppBar.addAct.setVisible(True)
            self.botAppBar.setAct.setVisible(False)
            self.botAppBar.homeAct.setHidden(False)
            self.botAppBar.shareAct.setHidden(True)

            self.header.bread.setText(f"{self.ammos.filter['rifle'].name}/Ammo")

        elif current_screen == self.edit_rifle or current_screen == self.edit_ammo or current_screen == self.edit_shot:
            self.botAppBar.okAct.setVisible(True)
            self.botAppBar.backAct.setVisible(True)
            self.botAppBar.addAct.setHidden(True)
            self.botAppBar.setAct.setVisible(False)
            self.botAppBar.homeAct.setHidden(False)
            self.botAppBar.shareAct.setHidden(True)

            rifle = self.ammos.filter.get('rifle')
            rifle = rifle.name if rifle else None
            if current_screen == self.edit_rifle:
                self.header.bread.setText(f"{rifle}/edit/")
            elif current_screen == self.edit_ammo:
                self.header.bread.setText(
                    f"{rifle}/{self.edit_ammo.ammo.name}/edit/")
            elif current_screen == self.edit_shot:
                self.header.bread.setText(
                    f"{rifle}/{self.edit_shot.ammo.name}/conditions/")

        elif current_screen == self.settings:

            self.header.bread.setText('Settings')

            self.botAppBar.okAct.setVisible(True)
            self.botAppBar.backAct.setVisible(True)
            self.botAppBar.addAct.setVisible(False)
            self.botAppBar.setAct.setVisible(False)
            self.botAppBar.homeAct.setHidden(True)
            self.botAppBar.shareAct.setHidden(True)

        elif current_screen == self.trajectory:
            self.botAppBar.okAct.setHidden(True)
            self.botAppBar.addAct.setHidden(True)
            self.botAppBar.setAct.setHidden(True)
            self.botAppBar.homeAct.setVisible(True)
            self.botAppBar.backAct.setVisible(True)
            self.botAppBar.shareAct.setVisible(True)

        else:
            ...

        if 0 <= index < self.stacked.count():
            currentPage = self.stacked.widget(index)
            self.stacked.resize(currentPage.sizeHint())
            self.scroll_area.scroll(0, 0)
            current_widget = self.stacked.currentWidget()
            if current_widget:
                target_height = current_widget.sizeHint().height()
                self.stacked.setMinimumHeight(target_height)

    def go_ok(self):
        current_screen = self.stacked.currentWidget()

        if current_screen == self.edit_rifle:
            self.edit_rifle.save_rifle()
            self.switch_to_rifles()
        elif current_screen == self.edit_ammo:
            self.edit_ammo.save_ammo()
            self.switch_to_ammos(self.edit_ammo.rifle)
        elif current_screen == self.edit_shot:
            self.edit_shot.save_ammo()
            self.switch_to_ammos(self.edit_shot.rifle)
        elif current_screen == self.multi_bc:
            drag_data = self.multi_bc.get_data()
            self.edit_ammo.update_drag_data(drag_data)
            self.stacked.setCurrentWidget(self.edit_ammo)
        elif current_screen == self.cdm:
            drag_data = self.cdm.get_data()
            self.edit_ammo.update_drag_data(drag_data)
            self.stacked.setCurrentWidget(self.edit_ammo)
        elif current_screen == self.powder_sens:
            powder_sens_coeff = self.powder_sens.calculate()
            if powder_sens_coeff is not None:
                self.edit_ammo.powder_sens.setValue(powder_sens_coeff)
            self.stacked.setCurrentWidget(self.edit_ammo)
        elif current_screen == self.settings:
            self.settings.update_settings()
            self.switch_to_rifles()

    def switch_drag_edit_screen(self, dm, ammo):
        if dm != DragModel.CDM:
            self.multi_bc.display_data(dm, ammo)
            self.stacked.setCurrentWidget(self.multi_bc)
        else:
            self.cdm.display_data(dm, ammo)
            self.stacked.setCurrentWidget(self.cdm)

    def switch_calc_sens(self):
        self.powder_sens.display_data(self.edit_ammo.mv.value(), self.edit_ammo.temperature.value())
        self.stacked.setCurrentWidget(self.powder_sens)

    def switch_to_settings(self):
        # self.settings.get_settings()
        self.stacked.setCurrentWidget(self.settings)

    def switch_to_trajectory(self):
        self.edit_shot.validate()
        self.trajectory.display_data(self.edit_shot)
        self.stacked.setCurrentWidget(self.trajectory)

    def showError(self, string):
        self.status_bar.setStyleSheet("color: orange")
        self.status_bar.showMessage(string, timeout=3000)

    def showMessage(self, string):
        self.status_bar.setStyleSheet("color: white")
        self.status_bar.showMessage(string, timeout=3000)

    def connectUi(self, MainWindow):
        self.rifles.rifle_edit_sig.connect(self.switch_edit_rifle_screen)
        self.rifles.rifle_clicked_sig.connect(self.switch_to_ammos)
        self.ammos.ammo_edit_sig.connect(self.switch_edit_ammo_screen)
        self.ammos.ammo_clicked_sig.connect(self.switch_edit_shot_screen)

        self.botAppBar.homeAct.clicked.connect(self.switch_to_rifles)
        self.botAppBar.backAct.clicked.connect(self.go_back)
        self.botAppBar.addAct.clicked.connect(self.go_add)
        self.botAppBar.okAct.clicked.connect(self.go_ok)
        self.botAppBar.setAct.clicked.connect(self.switch_to_settings)

        self.stacked.currentChanged.connect(self.screen_changed)

        self.edit_ammo.editDrag.connect(self.switch_drag_edit_screen)
        self.edit_ammo.calc_powder_sens.clicked.connect(self.switch_calc_sens)

        self.edit_shot.traj_btn.clicked.connect(self.switch_to_trajectory)

        self.edit_rifle.errorSig.connect(self.showError)
        self.edit_ammo.errorSig.connect(self.showError)
        self.edit_shot.errorSig.connect(self.showError)
