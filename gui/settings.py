from PySide6 import QtWidgets, QtCore
from units import Distance, Pressure, Weight
from gui.widgets import FormComboBox, FormCheckBox
from PySide6.QtCore import QSettings


SIGHT_HEIGHT = (
    ('mm', Distance.Millimeter),
    ('inch', Distance.Inch),
    ('cm', Distance.Centimeter),
    ('ln', Distance.Line),
)

DISTANCE = (
    ('m', Distance.Meter),
    ('ft', Distance.Foot),
    ('yd', Distance.Yard),
    ('km', Distance.Kilometer),
    ('mi', Distance.Mile),
    ('nm', Distance.NauticalMile),
)

DIAMETER = LENGTH = TWIST = (
    ('inch', Distance.Inch),
    ('cm', Distance.Centimeter),
    ('mm', Distance.Millimeter),
    ('ln', Distance.Line),
)

DROP = (
    ('cm', Distance.Centimeter),
    ('inch', Distance.Inch),
    ('mm', Distance.Millimeter),
    ('ln', Distance.Line),
    ('m', Distance.Meter),
    ('yd', Distance.Yard),
    ('ft', Distance.Foot),
)

PRESSURE = (
    ('mmhg', Pressure.MmHg),
    ('inhg', Pressure.InHg),
    ('bar', Pressure.Bar),
    ('hpa', Pressure.HP),
    ('psi', Pressure.PSI),
)

WEIGHT = (
    ('gr', Weight.Grain),
    ('g', Weight.Gram),
    ('kg', Weight.Kilogram),
    ('lb', Weight.Pound),
)

"""
        self.ln = (_translate('AppSettings', ' ln'), DistanceLine)
        self.yd = (_translate('AppSettings', ' yd'), DistanceYard)
        self.ft = (_translate('AppSettings', ' ft'), DistanceFoot)
        self.mm = (_translate('AppSettings', ' mm'), DistanceMillimeter)
        self.cm = (_translate('AppSettings', ' cm'), DistanceCentimeter)
        self.m = (_translate('AppSettings', ' m'), DistanceMeter)
        self.km = (_translate('AppSettings', ' km'), DistanceKilometer)
        self.mi = (_translate('AppSettings', ' mi'), DistanceMile)
        self.nm = (_translate('AppSettings', ' nm'), DistanceNauticalMile)
"""


class Settings(QtCore.QObject):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)



class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.set = QSettings(QSettings.IniFormat, QSettings.UserScope, 'settings.ini')
        self.init_ui(self)
        self.connectUi()

    def init_ui(self, settingsWidget):

        self.setObjectName('settingsWidget')
        self.boxLayout = QtWidgets.QVBoxLayout(self)

        self.viewBox = QtWidgets.QGroupBox(self)
        self.viewBox.setTitle('View')
        self.unitsBox = QtWidgets.QGroupBox(self)
        self.unitsBox.setTitle('Units of measurement')
        self.calcBox = QtWidgets.QGroupBox(self)
        self.calcBox.setTitle('Calculation')

        self.infoBox = QtWidgets.QGroupBox(self)
        self.infoBox.setTitle('Info')

        self.viewLayout = QtWidgets.QFormLayout(self.viewBox)
        self.unitLayout = QtWidgets.QGridLayout(self.unitsBox)
        self.calcLayout = QtWidgets.QVBoxLayout(self.calcBox)

        self.theme_label = QtWidgets.QLabel('Theme')
        self.theme = QtWidgets.QComboBox(self)
        # self.theme.addItem('Dark blue', 'dark_blue.xml')
        self.theme.addItem('Dark teal', 'dark_teal.xml')
        self.theme.addItem('Light', 'default.xml')

        self.scale_label = QtWidgets.QLabel('Scale')
        self.scale = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scale.setValue(0)
        self.scale.setMaximum(3)
        self.scale.setMinimum(-3)
        self.scale.setSingleStep(1)

        self.viewLayout.addRow(self.theme_label, self.theme)
        self.viewLayout.addRow(self.scale_label, self.scale)

        self.shUnits = FormComboBox(self, prefix='Sight height')
        self.shUnits.setObjectName('shUnits')
        self.twistUnits = FormComboBox(self, prefix='Twist')
        self.twistUnits.setObjectName('twistUnits')
        self.vUnits = FormComboBox(self, prefix='Velocity')
        self.vUnits.setObjectName('Velocity')
        self.distUnits = FormComboBox(self, prefix='Distance')
        self.distUnits.setObjectName('Distance')
        self.tempUnits = FormComboBox(self, prefix='Temperature')
        self.tempUnits.setObjectName('Temperature')
        self.wUnits = FormComboBox(self, prefix='Weight')
        self.wUnits.setObjectName('Weight')
        self.lnUnits = FormComboBox(self, prefix='Length')
        self.lnUnits.setObjectName('Length')
        self.dUnits = FormComboBox(self, prefix='Diameter')
        self.dUnits.setObjectName('Diameter')
        self.pUnits = FormComboBox(self, prefix='Pressure')
        self.pUnits.setObjectName('Pressure')
        self.dropUnits = FormComboBox(self, prefix='Drop')
        self.dropUnits.setObjectName('Drop')
        self.angleUnits = FormComboBox(self, prefix='Angular')
        self.angleUnits.setObjectName('Angular')
        self.pathUnits = FormComboBox(self, prefix='Path')
        self.pathUnits.setObjectName('Path')
        # self.eUnits = FormComboBox(self, prefix='Energy')

        [self.shUnits.addItem(k, v) for k, v in SIGHT_HEIGHT]
        [self.twistUnits.addItem(k, v) for k, v in TWIST]
        [self.distUnits.addItem(k, v) for k, v in DISTANCE]
        [self.dUnits.addItem(k, v) for k, v in DIAMETER]
        [self.dropUnits.addItem(k, v) for k, v in DROP]
        [self.pUnits.addItem(k, v) for k, v in PRESSURE]
        [self.wUnits.addItem(k, v) for k, v in WEIGHT]
        [self.lnUnits.addItem(k, v) for k, v in LENGTH]

        self.unitLayout.addWidget(self.shUnits)
        self.unitLayout.addWidget(self.twistUnits)
        self.unitLayout.addWidget(self.vUnits)
        self.unitLayout.addWidget(self.distUnits)
        self.unitLayout.addWidget(self.tempUnits)
        self.unitLayout.addWidget(self.wUnits)
        self.unitLayout.addWidget(self.lnUnits)
        self.unitLayout.addWidget(self.dUnits)
        self.unitLayout.addWidget(self.pUnits)
        self.unitLayout.addWidget(self.dropUnits)
        self.unitLayout.addWidget(self.angleUnits)
        self.unitLayout.addWidget(self.pathUnits)
        # self.unitLayout.addWidget(self.eUnits)

        self.is_calc_drag = FormCheckBox(self, prefix='Calculate drag')
        self.calcLayout.addWidget(self.is_calc_drag)

        self.boxLayout.addWidget(self.viewBox)
        self.boxLayout.addWidget(self.unitsBox)
        self.boxLayout.addWidget(self.calcBox)
        self.boxLayout.addWidget(self.infoBox)

    def change_theme(self, index):
        self.apply_theme()

    # def change_scale(self, value):
    #     if value % 10 == 0:
    #         self.apply_theme()

    def apply_theme(self):
        main = self.window()
        if main:
            index = self.theme.currentIndex()
            scale = self.scale.value()
            extra = dict(density_scale=scale)
            # if index == 0:
            #     extra.update(dict(primaryTextColor='#FFFFFF'))
            #     main.apply_stylesheet(main, extra=extra, theme='dark_blue.xml')
            if index == 0:
                extra.update(dict(primaryTextColor='#FFFFFF'))
                main.apply_stylesheet(main, extra=extra, theme='dark_teal.xml')
            else:
                main.apply_stylesheet(main, theme='default.xml')

    def update_settings(self):
        for obj in self.findChildren(FormComboBox):
            # print(obj.objectName())
            if hasattr(obj, 'currentIndex'):
                print(obj.objectName(), obj.currentIndex())
        # main = self.window()
        # if main:
        #     self.apply_theme()

    def get_settings(self):
        ...

    def connectUi(self):
        # self.scale.valueChanged.connect(self.apply_theme)
        ...
