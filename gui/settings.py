import json

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QSettings

from gui.widgets import FormComboBox, FormCheckBox
from units import Distance, Pressure, Weight, Temperature, Velocity, Angular

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

TEMPERATURE = (
    ('°C', Temperature.Celsius),
    ('°F', Temperature.Fahrenheit),
    ('°R', Temperature.Rankin),
    ('°K', Temperature.Kelvin),
)

VELOCITY = (
    ("m/s", Velocity.MPS),
    ("km/h", Velocity.KMH),
    ("ft/s", Velocity.FPS),
    ("mph", Velocity.MPH),
    ("kt", Velocity.KT)
)

ANGULAR = (
    ('°', Angular.Degree),
    ('rad', Angular.Radian),
    ('mrad', Angular.MRad),
    ('ths', Angular.Thousand),
)

PATH = (
    ('mil', Angular.Mil),
    ('moa', Angular.MOA),
    ('mrad', Angular.MRad),
    ('ths', Angular.Thousand),
    ('cm/100m', Angular.CmPer100M),
    ('in/100yd', Angular.InchesPer100Yd)
)


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
        self.vUnits.setObjectName('vUnits')
        self.distUnits = FormComboBox(self, prefix='Distance')
        self.distUnits.setObjectName('distUnits')
        self.tempUnits = FormComboBox(self, prefix='Temperature')
        self.tempUnits.setObjectName('tempUnits')
        self.wUnits = FormComboBox(self, prefix='Weight')
        self.wUnits.setObjectName('wUnits')
        self.lnUnits = FormComboBox(self, prefix='Length')
        self.lnUnits.setObjectName('lnUnits')
        self.dUnits = FormComboBox(self, prefix='Diameter')
        self.dUnits.setObjectName('dUnits')
        self.pUnits = FormComboBox(self, prefix='Pressure')
        self.pUnits.setObjectName('pUnits')
        self.dropUnits = FormComboBox(self, prefix='Drop')
        self.dropUnits.setObjectName('dropUnits')
        self.angleUnits = FormComboBox(self, prefix='Angular')
        self.angleUnits.setObjectName('angleUnits')
        self.pathUnits = FormComboBox(self, prefix='Path')
        self.pathUnits.setObjectName('pathUnits')
        # self.eUnits = FormComboBox(self, prefix='Energy')

        [self.shUnits.addItem(k, v) for k, v in SIGHT_HEIGHT]
        [self.twistUnits.addItem(k, v) for k, v in TWIST]
        [self.distUnits.addItem(k, v) for k, v in DISTANCE]
        [self.dUnits.addItem(k, v) for k, v in DIAMETER]
        [self.dropUnits.addItem(k, v) for k, v in DROP]
        [self.pUnits.addItem(k, v) for k, v in PRESSURE]
        [self.wUnits.addItem(k, v) for k, v in WEIGHT]
        [self.lnUnits.addItem(k, v) for k, v in LENGTH]
        [self.tempUnits.addItem(k, v) for k, v in TEMPERATURE]
        [self.vUnits.addItem(k, v) for k, v in VELOCITY]
        [self.pathUnits.addItem(k, v) for k, v in PATH]
        [self.angleUnits.addItem(k, v) for k, v in ANGULAR]

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
        settings = {}

        for obj in self.findChildren(FormComboBox) + self.findChildren(QtWidgets.QComboBox):
            settings[obj.objectName()] = obj.currentData()
        for obj in self.findChildren(FormCheckBox) + self.findChildren(QtWidgets.QCheckBox):
            settings[obj.objectName()] = obj.isChecked()

        try:
            with open('settings.json', 'w') as fp:
                json.dump(settings, fp)
        except Exception as err:
            print(err)

        # main = self.window()
        # if main:
        #     self.apply_theme()

    def get_settings(self):

        try:
            with open('settings.json', 'r') as fp:
                settings = json.load(fp)
                for k, v in settings.items():
                    ch = self.findChild(QtWidgets.QWidget, k)
                    if isinstance(ch, (FormComboBox, QtWidgets.QComboBox)):
                        ch.setCurrentIndex(ch.findData(v))
                    elif isinstance(ch, (FormCheckBox, QtWidgets.QCheckBox)):
                        ch.setChecked(v)

        except Exception as exc:
            print(exc)

    def connectUi(self):
        # self.scale.valueChanged.connect(self.apply_theme)
        ...
