import json

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QSettings

from gui.widgets import FormRow2
from units import Convertor, Distance, Pressure, Weight, Temperature, Velocity, Angular, Unit

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
    settingsUpdated = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.set = QSettings(QSettings.IniFormat, QSettings.UserScope, 'settings.ini')
        self.init_ui(self)
        self.connectUi()
        self.get_settings()

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
        self.unitLayout = QtWidgets.QVBoxLayout(self.unitsBox)
        self.calcLayout = QtWidgets.QVBoxLayout(self.calcBox)

        self.theme_label = QtWidgets.QLabel('Theme')
        self.theme = QtWidgets.QComboBox(self)
        # self.theme.addItem('Dark blue', 'dark_blue.xml')
        self.theme.addItem('Dark teal', 'dark_teal.xml')
        self.theme.addItem('Light', 'default.xml')
        self.apply_theme_btn = QtWidgets.QPushButton('Apply')
        self.apply_theme_btn.setProperty('class', 'success')
        # self.apply_theme_btn.setCheckable(True)
        # self.apply_theme_btn.setChecked(True)

        self.scale = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scale.setValue(0)
        self.scale.setMaximum(2)
        self.scale.setMinimum(-2)
        self.scale.setSingleStep(1)
        self.scale_label = QtWidgets.QLabel('Scale')

        self.viewLayout.addRow(self.theme_label, self.theme)
        self.viewLayout.addRow(self.scale_label, self.scale)
        self.scale.hide()
        self.scale_label.hide()
        self.viewLayout.addRow(self.apply_theme_btn)

        shUnits = QtWidgets.QComboBox(self)
        twistUnits = QtWidgets.QComboBox(self)
        vUnits = QtWidgets.QComboBox(self)
        distUnits = QtWidgets.QComboBox(self)
        tempUnits = QtWidgets.QComboBox(self)
        wUnits = QtWidgets.QComboBox(self)
        lnUnits = QtWidgets.QComboBox(self)
        dUnits = QtWidgets.QComboBox(self)
        pUnits = QtWidgets.QComboBox(self)
        dropUnits = QtWidgets.QComboBox(self)
        angleUnits = QtWidgets.QComboBox(self)
        pathUnits = QtWidgets.QComboBox(self)

        self.shUnits = FormRow2(QtWidgets.QLabel('Sight height / offset'), shUnits)
        self.shUnits.setObjectName('shUnits')
        self.twistUnits = FormRow2(QtWidgets.QLabel('Twist'), twistUnits)
        self.twistUnits.setObjectName('twistUnits')
        self.vUnits = FormRow2(QtWidgets.QLabel('Velocity'), vUnits)
        self.vUnits.setObjectName('vUnits')
        self.distUnits = FormRow2(QtWidgets.QLabel('Distance'), distUnits)
        self.distUnits.setObjectName('distUnits')
        self.tempUnits = FormRow2(QtWidgets.QLabel('Temperature'), tempUnits)
        self.tempUnits.setObjectName('tempUnits')
        self.wUnits = FormRow2(QtWidgets.QLabel('Weight'), wUnits)
        self.wUnits.setObjectName('wUnits')
        self.lnUnits = FormRow2(QtWidgets.QLabel('Length'), lnUnits)
        self.lnUnits.setObjectName('lnUnits')
        self.dUnits = FormRow2(QtWidgets.QLabel('Diameter'), dUnits)
        self.dUnits.setObjectName('dUnits')
        self.pUnits = FormRow2(QtWidgets.QLabel('Pressure'), pUnits)
        self.pUnits.setObjectName('pUnits')
        self.dropUnits = FormRow2(QtWidgets.QLabel('Drop'), dropUnits)
        self.dropUnits.setObjectName('dropUnits')
        self.angleUnits = FormRow2(QtWidgets.QLabel('Angular'), angleUnits)
        self.angleUnits.setObjectName('angleUnits')
        self.pathUnits = FormRow2(QtWidgets.QLabel('Path / Windage'), pathUnits)
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

        is_calc_drag = QtWidgets.QCheckBox(self)
        is_calc_drag.setChecked(True)
        self.is_calc_drag = FormRow2(QtWidgets.QLabel('Calculate drag'), is_calc_drag)
        self.is_calc_drag.setObjectName('is_drag')
        self.calcLayout.addWidget(self.is_calc_drag)

        self.boxLayout.addWidget(self.viewBox)
        self.boxLayout.addWidget(self.unitsBox)
        self.boxLayout.addWidget(self.calcBox)
        self.boxLayout.addWidget(self.infoBox)

    def apply_theme(self):
        main = self.window()
        if main:
            index = self.theme.currentIndex()
            scale = self.scale.value()
            extra = dict(density_scale=scale)

            if index == 0:
                extra.update(dict(primaryTextColor='#FFFFFF'))
                main.apply_stylesheet(main, extra=extra, theme='dark_teal.xml')
            else:
                main.apply_stylesheet(main, theme='default.xml')

    def update_settings(self):
        settings = {}

        for obj in self.findChildren(QtWidgets.QWidget):
            name = obj.objectName()
            if name:
                if hasattr(obj, 'currentData'):
                    if isinstance(obj.currentData(), Unit):
                        settings[name] = obj.currentData().value
                    else:
                        settings[name] = obj.currentData()
                elif hasattr(obj, 'value'):
                    print(obj.objectName(), obj.value())
                    settings[obj.objectName()] = obj.value()
                elif hasattr(obj, 'isChecked'):
                    print(obj.objectName(), obj.isChecked())
                    settings[obj.objectName()] = obj.isChecked()
        print(settings)
        try:
            with open('settings.json', 'w') as fp:
                json.dump(settings, fp)
        except Exception as err:
            print(err)

        self.settingsUpdated.emit(self)

    def get_settings(self):

        try:
            with open('settings.json', 'r') as fp:
                settings = json.load(fp)
                for k, v in settings.items():
                    obj = self.findChild(QtWidgets.QWidget, k)
                    if hasattr(obj, 'currentData'):
                        obj.setCurrentIndex(obj.findData(Unit(v)))
                    elif hasattr(obj, 'value'):
                        print(obj.objectName(), obj.value())
                        obj.setValue(v)
                    elif hasattr(obj, 'isChecked'):
                        obj.setCHecked(v)

        except Exception as exc:
            print(exc)

    def connectUi(self):
        self.apply_theme_btn.clicked.connect(self.apply_theme)
