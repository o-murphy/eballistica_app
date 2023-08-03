from statistics import median

from calculate.calculate import calculate_powder_sens
from getqt import *

from gui.settings import SettingsWidget
from gui.widgets import ConverSpinBox, LabelCenter
from units import Temperature, Velocity, Convertor


_translate = QtCore.QCoreApplication.translate


class PowderSensWindget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PowderSensWindget, self).__init__(parent)
        self.init_ui(self)
        self.connect_ui()

    def translateUi(self, powderSens):
        self.title.setText(_translate("powderSens", 'Powder Sensitivity Calculation'))
        self.temp_sens_label.setText(_translate("powderSens", "Sensitivity"))
        self.temp_sens_field.setText("%")
        self.calc_btn.setText(_translate("powderSens", 'Calculate'))

    def init_ui(self, powderSens):
        self.setObjectName('powderSens')

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)

        self.title = LabelCenter()
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.temp_label = LabelCenter()
        self.velocity_label = LabelCenter()
        self.temp_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.velocity_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.temp_sens_label = LabelCenter()
        self.temp_sens_field = LabelCenter('1%')
        self.calc_btn = QtWidgets.QPushButton()

        self.gridLayout.addWidget(self.title, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.temp_label)
        self.gridLayout.addWidget(self.velocity_label)

        for i in range(5):
            temp = ConverSpinBox(self, 1)
            temp.setObjectName(f't{i}')
            velocity = ConverSpinBox(self, 0.1)
            velocity.setObjectName(f'v{i}')
            self.gridLayout.addWidget(temp)
            self.gridLayout.addWidget(velocity)

        self.gridLayout.addWidget(self.calc_btn, 9, 0, 1, 2)

        self.gridLayout.addWidget(self.temp_sens_label)
        self.gridLayout.addWidget(self.temp_sens_field)

        self.translateUi(self)

    def connect_ui(self):
        self.calc_btn.clicked.connect(self._calculate)

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings

    def display_data(self, v0, t0):
        settings = self.get_settings()
        temp_units = settings.tempUnits.currentData()
        temp_name = Temperature.name(temp_units)
        velocity_units = settings.vUnits.currentData()
        velocity_name = Velocity.name(velocity_units)

        self.temp_label.setText(_translate('powderSens', 'Temp., ') + temp_name)
        self.velocity_label.setText(_translate('powderSens', 'Velocity, ') + velocity_name)

        for i in range(5):
            temp_sb = self.findChild(QtWidgets.QDoubleSpinBox, f't{i}')
            velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
            temp_sb.setConvertor(Convertor(Temperature, temp_units, Temperature.Celsius))
            velocity_sb.setConvertor(Convertor(Velocity, velocity_units, Velocity.MPS))

            temp_sb.setRawValue(t0 if i == 0 else 0)
            velocity_sb.setRawValue(v0 if i == 0 else 0)

    def _calculate(self):

        ret_list = []
        for i in range(5):
            temp_sb = self.findChild(QtWidgets.QDoubleSpinBox, f't{i}')
            velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
            if temp_sb and velocity_sb:
                ret_list.append([temp_sb.rawValue(), velocity_sb.rawValue()])
        ret_list.sort(key=lambda item: item[1], reverse=True)

        value = calculate_powder_sens(ret_list)

        self.temp_sens_field.setText(f'{value}%' if value else _translate("powderSens", "Error"))
        return value

    def calculate(self):
        return self._calculate()


if __name__ == '__main__':
    ...
