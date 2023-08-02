from statistics import median

from getqt import *

from gui.settings import SettingsWidget
from gui.widgets import ConverSpinBox
from units import Temperature, Velocity, Convertor


_translate = QtCore.QCoreApplication.translate


class PowderSensWindget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PowderSensWindget, self).__init__(parent)
        self.init_ui(self)
        self.connect_ui()

    def retranslateUi(self, powderSens):
        self.title.setText(_translate("powderSens", 'Powder Sensitivity Calculation'))
        self.temp_sens_label.setText(_translate("powderSens", "Sensitivity"))
        self.temp_sens_field.setText("%")
        self.calc_btn.setText(_translate("powderSens", 'Calculate'))

    def init_ui(self, powderSens):
        self.setObjectName('powderSens')

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)

        self.title = QtWidgets.QLabel()
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.temp_label = QtWidgets.QLabel()
        self.velocity_label = QtWidgets.QLabel()
        self.temp_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.velocity_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.temp_sens_label = QtWidgets.QLabel()
        self.temp_sens_field = QtWidgets.QLabel('1%')
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

        self.gridLayout.addWidget(self.temp_sens_label)
        self.gridLayout.addWidget(self.temp_sens_field)
        self.gridLayout.addWidget(self.calc_btn)

        self.retranslateUi(self)

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

        def calculate_sensitivity(v0, t0, v1, t1):
            # Step 1: Calculate the Temperature Difference
            temp_difference = t0 - t1

            # Step 2: Calculate the Speed Difference
            speed_difference = v0 - v1

            # Step 3: Calculate the Temperature Sensitivity Factor (TempModifier)
            temp_modifier = (speed_difference / temp_difference) * (15 / v0) * 100

            return temp_modifier

        ret_list = []
        for i in range(5):
            temp_sb = self.findChild(QtWidgets.QDoubleSpinBox, f't{i}')
            velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
            if temp_sb and velocity_sb:
                ret_list.append([temp_sb.rawValue(), velocity_sb.rawValue()])
        ret_list.sort(key=lambda item: item[1], reverse=True)

        coeffs = []
        for i in range(len(ret_list) - 1):
            t0, v0 = ret_list[i]
            t1, v1 = ret_list[i + 1]
            if v0 != 0 and v1 != 0:
                coeffs.append(calculate_sensitivity(v0, t0, v1, t1))

        if len(coeffs) >= 1:
            val = round(median(coeffs), 3)
            self.temp_sens_field.setText(f'{val}%')
        else:
            val = None
            self.temp_sens_field.setText(_translate("powderSens", "Error"))
        return val

    def calculate(self):
        return self._calculate()


if __name__ == '__main__':
    ...
