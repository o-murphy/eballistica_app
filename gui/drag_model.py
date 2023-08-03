from functools import reduce

from getqt import *

from datatypes.dbworker import DragModel, AmmoData
from gui.settings import SettingsWidget
from gui.widgets import SpinBox, ConverSpinBox, LabelCenter
from units import Convertor, Velocity


_translate = QtCore.QCoreApplication.translate


class MultiBCWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MultiBCWidget, self).__init__(parent)
        self.init_ui(self)
        self.connect_ui()

    def translateUi(self, mbcWidget):
        ...

    def init_ui(self, dragModelWidget):
        self.setObjectName('dragModelWidget')

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)

        self.title = LabelCenter()
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.velocity_label = LabelCenter('Velocity, mps')
        self.bc_label = LabelCenter('BC')
        self.velocity_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.bc_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.gridLayout.addWidget(self.title, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.velocity_label)
        self.gridLayout.addWidget(self.bc_label)

        for i in range(5):
            velocity = ConverSpinBox(self, 1)
            velocity.setObjectName(f'v{i}')
            bc = SpinBox(self, 0, 2, 0.001, decimals=3)
            bc.setObjectName(f'bc{i}')
            self.gridLayout.addWidget(velocity)
            self.gridLayout.addWidget(bc)
        self.translateUi(self)

    def display_data(self, dm: DragModel, ammo):
        if dm == DragModel.G1:
            multi_bc: list[list[float, float]] = ammo.bc_list
        elif dm == DragModel.G7:
            multi_bc: list[list[float, float]] = ammo.bc7_list
        else:
            multi_bc = [[0, 0]] * 5
        self.title.setText(_translate('mbcWidget', 'Edit BC: ') + dm.name)
        self.bc_label.setText(_translate('mbcWidget', 'BC: ') + dm.name)
        if multi_bc:
            for i, (v, bc) in enumerate(multi_bc):
                velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
                bc_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'bc{i}')
                if velocity_sb and bc_sb:
                    velocity_sb.setRawValue(v)
                    bc_sb.setValue(bc)

    def get_data(self):
        ret_list = []
        for i in range(5):
            velocity_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
            bc_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'bc{i}')
            if velocity_sb and bc_sb:
                ret_list.append([velocity_sb.rawValue(), bc_sb.value()])
        return ret_list

    def on_settings_update(self, settings: SettingsWidget):

        v_units = settings.vUnits.currentData()
        self.velocity_label.setText(_translate("mbcWidget", "Velocity, ") + Velocity.name(v_units))

        for i in range(5):
            velocity_sb: ConverSpinBox = self.findChild(QtWidgets.QDoubleSpinBox, f'v{i}')
            velocity_sb.setConvertor(Convertor(Velocity, v_units, Velocity.MPS))
            velocity_sb.setDecimals(velocity_sb.convertor().accuracy)

    def connect_ui(self):
        window = self.window()
        if window:
            if hasattr(window, 'settings'):
                settings: SettingsWidget = window.settings
                settings.settingsUpdated.connect(self.on_settings_update)



class CDMWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CDMWidget, self).__init__(parent)
        self.init_ui(self)
        self.connectUi(self)
        self.unlock(False)

    def translateUi(self, cdmWidget):
        self.agree.setText(_translate("cdmWidget", 'Unlock this settings'))
        self.warning.setText(_translate("cdmWidget", 'Changing this settings can corrupt the calculation'))
        self.mach_label.setText(_translate("cdmWidget", 'Mach'))
        self.cd_label.setText(_translate("cdmWidget", 'Cd'))

    def init_ui(self, cdmWidget):
        self.setObjectName('cdmWidget')

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)

        self.title = LabelCenter()
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.agree = QtWidgets.QCheckBox()
        self.warning = LabelCenter()
        self.warning.setProperty('class', 'danger')
        self.warning.setAlignment(QtCore.Qt.AlignCenter)

        self.mach_label = LabelCenter('Mach')
        self.cd_label = LabelCenter('Cd')
        self.mach_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.cd_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.gridLayout.addWidget(self.title, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.warning, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.agree, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.mach_label)
        self.gridLayout.addWidget(self.cd_label)

        for i in range(100):
            mach = SpinBox(self, 0, 5, 0.01, decimals=2)
            mach.setObjectName(f'mach{i}')
            cd = SpinBox(self, 0, 2, 0.0001, decimals=4)
            cd.setObjectName(f'cd{i}')
            self.gridLayout.addWidget(mach)
            self.gridLayout.addWidget(cd)
            # mach.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            # mach.wheelEvent = None
            # cd.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            # cd.wheelEvent = None
        self.translateUi(self)

    def display_data(self, dm: DragModel, ammo):
        if dm == DragModel.G1:
            multi_bc: list[list[float, float]] = ammo.bc_list
        elif dm == DragModel.G7:
            multi_bc: list[list[float, float]] = ammo.bc7_list
        else:
            multi_bc = [[0, 0]] * 100
        self.title.setText(dm.name)
        for i, (v, bc) in enumerate(multi_bc):
            mach_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'mach{i}')
            cd_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'cd{i}')
            if mach_sb and cd_sb:
                mach_sb.setValue(v)
                cd_sb.setValue(bc)
        self.agree.setChecked(False)

    def connectUi(self, cdmWidget):
        self.agree.stateChanged.connect(self.unlock)

    def unlock(self, checked):
        for i in range(100):
            mach_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'mach{i}')
            cd_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'cd{i}')
            # mach_sb.lineEdit().setEnabled(checked)
            # cd_sb.lineEdit().setEnabled(checked)
            mach_sb.setEnabled(checked)
            cd_sb.setEnabled(checked)

    def get_data(self):
        ret_list = []
        for i in range(100):
            mach_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'mach{i}')
            cd_sb = self.findChild(QtWidgets.QDoubleSpinBox, f'cd{i}')
            if mach_sb and cd_sb:
                ret_list.append([mach_sb.value(), cd_sb.value()])
        return ret_list


class EditDragDataButton(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super(EditDragDataButton, self).__init__(*args, **kwargs)

    @staticmethod
    def count_nonzero_pairs(pair_list):
        if pair_list is None:
            return 0
        def count_valid_pairs(acc, pair):
            if pair[0] != 0 and pair[1] != 0:
                return acc + 1
            return acc

        return reduce(count_valid_pairs, pair_list, 0)

    def update_df(self, drag_model: DragModel, ammo: AmmoData):
        if drag_model == DragModel.G1:
            count = self.count_nonzero_pairs(ammo.bc_list)
            first = ammo.bc_list[0][1] if count else None
        elif drag_model == DragModel.G7:
            count = self.count_nonzero_pairs(ammo.bc7_list)
            first = ammo.bc7_list[0][1] if count else None
        elif drag_model == DragModel.CDM:
            count = self.count_nonzero_pairs(ammo.cdm_list)
            first = None
        else:
            return
        if count == 0:
            self.setText(f'{drag_model.name} (' + _translate("cdmWidget", "None") + ')')
        elif count > 1:
            self.setText(f'{drag_model.name} ({count})')
        else:
            self.setText(f'{drag_model.name} (' + _translate("cdmWidget", "BC") + f': {first})')


if __name__ == '__main__':
    import sys
    from qt_material import apply_stylesheet

    extra = {
        'primaryTextColor': '#FFFFFF'
    }
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, extra=extra, theme='dark_blue.xml')

    window = MultiBCWidget()
    window.display_data([[900, 0.358], [800, 0.360]])

    window.show()
    app.exit(app.exec())