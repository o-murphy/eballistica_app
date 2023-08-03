import pyqtgraph as pg
from getqt import *
from qt_material import QtStyleTools

from calculate.calculate import calculate_traj, calculated_drag
from datatypes.dbworker import RifleData, AmmoData, ZeroData, Target, AtmoData
from gui.settings import SettingsWidget
from gui.widgets import LabelCenter, SpinBox, Column, ConverSpinBox, Row, GesturedTableWidget
from units import Distance, Angular, Velocity, Energy

pg.setConfigOption('background', '#31363B')


_translate = QtCore.QCoreApplication.translate


class OneShotProps(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(OneShotProps, self).__init__(parent)
        self.init_ui(self)
        self.connect_ui(self)

    def display_data(self, ammo):
        self.range_spin.setValue(ammo.target.distance)
        self.wind_spin.setValue(ammo.atmo.wind_speed)
        self.dir_spin.setValue(ammo.atmo.wind_angle)

    def connect_ui(self, oneShotProps):
        self.range_up.clicked.connect(self.range_spin.stepUp)
        self.range_dwn.clicked.connect(self.range_spin.stepDown)
        self.wind_up.clicked.connect(self.wind_spin.stepUp)
        self.wind_dwn.clicked.connect(self.wind_spin.stepDown)
        self.dir_up.clicked.connect(self.dir_spin.stepUp)
        self.dir_dwn.clicked.connect(self.dir_spin.stepDown)

    def init_ui(self, oneShotProps):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.gLayout = QtWidgets.QGridLayout(self)
        self.gLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.gLayout.setContentsMargins(0, 0, 0, 0)

        self.range_label = LabelCenter()
        self.range_label.set_bold()
        self.wind_label = LabelCenter()
        self.wind_label.set_bold()
        self.wind_dir_label = LabelCenter()
        self.wind_dir_label.set_bold()

        self.range_spin = ConverSpinBox(self)
        self.range_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.range_up = QtWidgets.QPushButton('Up', self)
        self.range_dwn = QtWidgets.QPushButton('Dwn', self)

        self.wind_spin = ConverSpinBox(self)
        self.wind_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.wind_up = QtWidgets.QPushButton('Up', self)
        self.wind_dwn = QtWidgets.QPushButton('Dwn', self)

        self.dir_spin = ConverSpinBox(self)
        self.dir_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dir_up = QtWidgets.QPushButton('Up', self)
        self.dir_dwn = QtWidgets.QPushButton('Dwn', self)

        self.range_col = Column(self, [self.range_up, self.range_spin, self.range_dwn])
        self.wind_col = Column(self, [self.wind_up, self.wind_spin, self.wind_dwn])
        self.dir_col = Column(self, [self.dir_up, self.dir_spin, self.dir_dwn])
        self.range_col.vLayout.setContentsMargins(0, 0, 0, 0)
        self.wind_col.vLayout.setContentsMargins(0, 0, 0, 0)
        self.dir_col.vLayout.setContentsMargins(0, 0, 0, 0)

        self.gLayout.addWidget(self.range_label)
        self.gLayout.addWidget(self.wind_label, 0, 1)
        self.gLayout.addWidget(self.wind_dir_label, 0, 2)
        self.gLayout.addWidget(self.range_col)
        self.gLayout.addWidget(self.wind_col)
        self.gLayout.addWidget(self.dir_col)

        self.translateUi(self)

    def translateUi(self, oneShotProps):
        self.range_label.setText(_translate("oneShotProps", "Range"))
        self.wind_label.setText(_translate("oneShotProps", "Wind"))
        self.wind_dir_label.setText(_translate("oneShotProps", "Dir"))


class OneShotInfo(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(OneShotInfo, self).__init__(parent)
        self.init_ui(self)
        self.connect_ui(self)

    def display_data(self, rifle, ammo):
        self.rifle_name_label.setText(rifle.name)
        self.ammo_name_label.setText(ammo.name)

    def connect_ui(self, oneShotInfo):
        ...

    def init_ui(self, oneShotInfo):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.vLayout = QtWidgets.QVBoxLayout(self)
        self.vLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.rifle_label = LabelCenter('Rifle:')
        self.rifle_label.set_bold()
        self.ammo_label = LabelCenter('Ammo:')
        self.ammo_label.set_bold()
        self.rifle_name_label = LabelCenter('Template')
        self.ammo_name_label = LabelCenter('Template')

        # self.sight_label = LabelCenter('Sight CF:')
        # self.look_label = LabelCenter('Look Ang:')
        # self.mv_label = LabelCenter('MV:')
        #
        # self.sight_val = LabelCenter()
        # self.look_val = LabelCenter()
        # self.mv_val = LabelCenter()
        #
        self.title = Row(self, [self.rifle_label, self.rifle_name_label, self.ammo_label, self.ammo_name_label])
        # self.data = Row(self, [self.sight_label, self.sight_val,
        #                        self.look_label, self.look_val,
        #                        self.mv_label, self.mv_val])

        self.vLayout.addWidget(self.title)
        # self.vLayout.addWidget(self.data)


class OneShotValue(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OneShotValue, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.vLayout = QtWidgets.QVBoxLayout(self)
        self.vLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.value = LabelCenter('value')
        self.measure = LabelCenter('measure')
        self.vLayout.addWidget(self.value)
        self.vLayout.addWidget(self.measure)


class OneShotValues(GesturedTableWidget):
    def __init__(self, parent=None):
        super(OneShotValues, self).__init__(parent)
        self.setupUi(self)
        self.connect_ui(self)
        self.display_data()

    def display_data(self):
        headers = [
            'ELEV', 'WIND', 'LEAD'
        ]

        headers = ["\n".join(h) for h in headers]

        data = (
            (1, 2, 3, 4, 5),
            (1, 2, 3, 4, 5),
            (1, 2, 3, 4, 5),
        )

        self.setRowCount(len(headers))
        self.setColumnCount(len(data[0]) if len(data) > 0 else 0)

        for i, text in enumerate(headers):

            label = QtWidgets.QTableWidgetItem(text)
            label.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setVerticalHeaderItem(i, label)

        for row_index, row_data in enumerate(data):
            for col_index, item_data in enumerate(row_data):

                # item = QtWidgets.QTableWidgetItem(str(item_data))
                item = QtWidgets.QTableWidgetItem()
                # item.setTextAlignment(QtCore.Qt.AlignCenter)
                widget = OneShotValue()
                self.setItem(row_index, col_index, item)
                self.setCellWidget(row_index, col_index, widget)

    def setupUi(self, oneShotVal):
        super(OneShotValues, self).setupUi(self)
        hheader = self.horizontalHeader()
        hheader.setVisible(False)
        vheader = self.verticalHeader()
        vheader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setSelectionMode(GesturedTableWidget.SelectionMode.NoSelection)


    def connect_ui(self, oneShotVal):
        ...


class OneShotHUD(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OneShotHUD, self).__init__(parent)
        self.init_ui(self)

    def init_ui(self, oneShotHud):
        self.vLayout = QtWidgets.QVBoxLayout(self)
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.props_box = OneShotProps(self)
        self.info_box = OneShotInfo(self)
        self.values_box = OneShotValues(self)
        self.vLayout.addWidget(self.props_box)
        self.vLayout.addWidget(self.info_box)
        self.vLayout.addWidget(self.values_box)

    def display_data(self, rifle, ammo, trajectory):
        self.info_box.display_data(rifle, ammo)
        self.props_box.display_data(ammo)


class OneShotReticle(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OneShotReticle, self).__init__(parent)


class OneShotWidget(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(OneShotWidget, self).__init__(parent)
        self.init_ui(self)
        self.connect_ui(self)

    def init_ui(self, oneShot):
        self.vLayout = QtWidgets.QVBoxLayout(self)

        self.hud = OneShotHUD(self)
        self.reticle = OneShotReticle(self)

        self.viewCmb = QtWidgets.QComboBox(self)
        self.viewCmb.addItem('HUD', 0)
        self.viewCmb.addItem('Reticle', 1)

        self.stacked = QtWidgets.QStackedWidget(self)
        self.stacked.addWidget(self.hud)
        self.stacked.addWidget(self.reticle)

        self.stacked.setCurrentWidget(self.hud)

        self.vLayout.addWidget(self.viewCmb)
        self.vLayout.addWidget(self.stacked)

    def display_data(self, edit_shot=None):

        rifle: RifleData = edit_shot.rifle
        ammo: AmmoData = edit_shot.ammo
        zerodata: ZeroData = ammo.zerodata
        target: Target = ammo.target
        atmo: AtmoData = ammo.atmo
        trajectory = calculate_traj(rifle, ammo, target, atmo, zerodata)
        self.hud.display_data(rifle, ammo, trajectory)

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings

    def switch_view(self, index):
        if index == 0:
            self.stacked.setCurrentWidget(self.hud)
        elif index == 1:
            self.stacked.setCurrentWidget(self.reticle)

    def share_clicked(self):
        ...

    def connect_ui(self, oneShot):
        self.viewCmb.currentIndexChanged.connect(self.switch_view)
