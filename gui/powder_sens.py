from functools import reduce
from statistics import median

from PySide6 import QtWidgets, QtCore

from gui.settings import SettingsWidget
from gui.widgets import SpinBox, ConverSpinBox
from units import Temperature, Velocity, Convertor


class PowderSensWindget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PowderSensWindget, self).__init__(parent)
        self.init_ui(self)

    def init_ui(self, powderSensWindget):
        self.setObjectName('powderSensWindget')

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)

        self.title = QtWidgets.QLabel('Powder Sensitivity Calculation')
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.temp_label = QtWidgets.QLabel('Temp, C')
        self.velocity_label = QtWidgets.QLabel('Velocity, mps')
        self.temp_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.velocity_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.gridLayout.addWidget(self.title, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.temp_label)
        self.gridLayout.addWidget(self.velocity_label)

        for i in range(5):
            temp = ConverSpinBox(self, -50, 50, 1)
            temp.setObjectName(f't{i}')
            velocity = ConverSpinBox(self, 0, 2000, 0.1, decimals=1)
            velocity.setObjectName(f'v{i}')
            self.gridLayout.addWidget(temp)
            self.gridLayout.addWidget(velocity)

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

        self.temp_label.setText(f'Temp., {temp_name}')
        self.velocity_label.setText(f'Velocity., {velocity_name}')

        for i in range(5):
            temp_sb = self.findChild(QtWidgets.QDoubleSpinBox, f't{i}')
            velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
            temp_sb.setConvertor(Convertor(Temperature, temp_units, Temperature.Celsius))
            velocity_sb.setConvertor(Convertor(Velocity, velocity_units, Velocity.MPS))

            temp_sb.setRawValue(t0 if i == 0 else 0)
            velocity_sb.setRawValue(v0 if i == 0 else 0)

    # def display_data(self):
    #     for i, (v, bc) in enumerate(sens_list):
    #         temp_sb = self.findChild(QtWidgets.QDoubleSpinBox, f't{i}')
    #         velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
    #         if temp_sb and velocity_sb:
    #             temp_sb.setValue(v)
    #             velocity_sb.setValue(bc)

    # def get_data(self):
    #     ret_list = []
    #     for i in range(5):
    #         temp_sb = self.findChild(QtWidgets.QDoubleSpinBox, f't{i}')
    #         velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
    #         if temp_sb and velocity_sb:
    #             ret_list.append([temp_sb.value(), velocity_sb.value()])
    #     return ret_list

    # @staticmethod
    # def count_nonzero_pairs(pair_list):
    #     def count_valid_pairs(acc, pair):
    #         if pair[0] != 0 and pair[1] != 0:
    #             return acc + 1
    #         return acc
    #
    #     return reduce(count_valid_pairs, pair_list, 0)

    def calculate(self):

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
        for i in range(len(ret_list)-1):
            t0, v0 = ret_list[i]
            t1, v1 = ret_list[i+1]
            if v0 != 0 and v1 != 0:
                coeffs.append(calculate_sensitivity(v0, t0, v1, t1))

        if len(coeffs) >= 1:
            return median(coeffs)
        return None


if __name__ == '__main__':
    ...
