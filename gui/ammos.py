from PySide6 import QtWidgets, QtCore, QtGui

from datatypes.dbworker import Worker, AmmoData, DragModel
from gui.app_logo import AppLogo, AppLabel
from gui.drag_model import EditDragDataButton
from gui.settings import SettingsWidget
from gui.widgets import FormRow3, SpinBox, ComboBox, ConverSpinBox
from units import Distance, Angular, Pressure, Temperature, Velocity, Weight, Convertor


class AmmoItemWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AmmoItemWidget, self).__init__(parent)
        self.setupUi(self)
        self.ammo_data = None

    def setupUi(self, ammoItemWidget):
        ammoItemWidget.setObjectName("ammoItemWidget")

        self.box = QtWidgets.QGroupBox('', self)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.box)

        self.boxLayout = QtWidgets.QFormLayout(self.box)
        self.boxLayout.setObjectName("boxLayout")

        self.caliber = QtWidgets.QLabel()
        self.caliber_label = QtWidgets.QLabel()
        self.ammo = QtWidgets.QLabel()
        self.ammo_label = QtWidgets.QLabel()
        self.mv = QtWidgets.QLabel()
        self.mv_label = QtWidgets.QLabel()
        self.zero = QtWidgets.QLabel()
        self.zero_label = QtWidgets.QLabel()

        self.boxLayout.addRow(self.caliber_label, self.caliber)
        self.boxLayout.addRow(self.ammo_label, self.ammo)
        self.boxLayout.addRow(self.mv_label, self.mv)
        self.boxLayout.addRow(self.zero_label, self.zero)
        self.translateUi(self)

    def translateUi(self, ammoItemWidget):
        _translate = QtCore.QCoreApplication.translate
        ammoItemWidget.setWindowTitle(_translate("ammoItemWidget", "Form"))
        ammoItemWidget.caliber_label.setText(_translate("ammoItemWidget", 'Caliber:'))
        ammoItemWidget.ammo_label.setText(_translate("ammoItemWidget", 'Ammo Wt/Drag:'))
        ammoItemWidget.mv_label.setText(_translate("ammoItemWidget", 'MV:'))
        ammoItemWidget.zero_label.setText(_translate("ammoItemWidget", 'Zero Rng/Ht:'))

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings

    def set_data(self, ammo: AmmoData):
        settings = self.get_settings()

        diameter = Distance(ammo.diameter, Distance.Inch).convert(settings.dUnits.currentData())
        weight = Weight(ammo.weight, Weight.Grain).convert(settings.wUnits.currentData())
        mv = Velocity(ammo.muzzle_velocity, Velocity.MPS).convert(settings.vUnits.currentData())
        zero_range = Distance(ammo.zerodata.zero_range, Distance.Meter).convert(settings.distUnits.currentData())
        sh = Distance(ammo.zerodata.zero_height, Distance.Centimeter).convert(settings.shUnits.currentData())

        self.ammo_data = ammo
        self.box.setTitle(self.ammo_data.name)
        self.caliber.setText(f'{diameter}')
        self.ammo.setText(f'{weight}/{ammo.drag_model.name}')
        self.mv.setText(f'{mv}')
        self.zero.setText(f'{zero_range}/{sh}')


class AmmosHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AmmosHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, ammosHeader):
        ammosHeader.setObjectName("ammosHeader")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")

        self.logo = AppLogo()
        self.label = AppLabel()
        self.hBoxLayout.addWidget(self.logo)
        self.hBoxLayout.addWidget(self.label)

        ammosHeader.setObjectName("ammosHeader")
        # self.addButton = QtWidgets.QPushButton('+')

        # self.hBoxLayout.addWidget(self.addButton)

        self.retranslateUi(ammosHeader)
        QtCore.QMetaObject.connectSlotsByName(ammosHeader)

    def retranslateUi(self, ammosHeader: 'AmmosHeader'):
        _translate = QtCore.QCoreApplication.translate
        ammosHeader.setWindowTitle(_translate("ammosHeader", "Form"))
        # ammosHeader.addButton.setText(_translate("ammosHeader", "+"))


class AmmosLi(QtWidgets.QListWidget):
    edit_context_action = QtCore.Signal(object)
    ammo_clicked_sig = QtCore.Signal(object)
    ammo_edit_sig = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(AmmosLi, self).__init__(parent)
        self.filter = {}

        self.connectUi(self)

    def contextMenuEvent(self, event):
        # self.itemAt(event.pos())
        context_menu = QtWidgets.QMenu(self)

        edit_item = QtGui.QAction('Edit', self)
        remove_item = QtGui.QAction('Delete', self)

        context_menu.addAction(edit_item)
        context_menu.addAction(remove_item)

        selected_item = self.itemAt(event.pos())

        if selected_item:
            # Perform custom actions based on the selected item
            uid = self.indexFromItem(selected_item).row()

            action = context_menu.exec_(event.globalPos())

            event.accept()
            if action == edit_item:
                self.edit_context_action.emit(selected_item)
            elif action == remove_item:
                uid = self.itemWidget(selected_item).ammo_data.id
                Worker.delete_ammo(uid)
                self.refresh()

    # def setupUi(self, AmmosLi):
    #     self.menu = QtWidgets.QMenu()
    #     self.menu.addAction(self.edit_item)

    def set_filter(self, **kwargs):
        self.filter = kwargs

    def create_item(self, rifle):
        widget = AmmoItemWidget(self)
        widget.set_data(rifle)
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        item.setData(0, rifle.id)
        self.addItem(item)
        self.setItemWidget(item, widget)

    def refresh(self):
        ammos = Worker.list_ammos(**self.filter)
        self.clear()
        if ammos:
            for ammo in ammos:
                self.create_item(ammo)

    def retranslateUi(self, ammosWidget: 'AmmosWidget'):
        _translate = QtCore.QCoreApplication.translate
        ammosWidget.setWindowTitle(_translate("ammosWidget", "Form"))

    def connectUi(self, ammosWidget: 'AmmosWidget'):
        # self.ammos_list.itemDoubleClicked.connect(self.ammo_edit_clicked)
        self.itemClicked.connect(self.ammo_clicked)
        self.edit_context_action.connect(self.ammo_edit_clicked)

    def ammo_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: AmmoItemWidget = self.itemWidget(item)
        self.ammo_clicked_sig.emit(widget.ammo_data)

    def ammo_edit_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: AmmoItemWidget = self.itemWidget(item)
        self.ammo_edit_sig.emit(widget.ammo_data)


class EditAmmoWidget(QtWidgets.QWidget):
    # ok_clicked = QtCore.Signal(object)
    editDrag = QtCore.Signal(object, object)
    errorSig = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(EditAmmoWidget, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)
        self.ammo = None
        self.rifle = None

    def setupUi(self, editAmmoWidget):
        editAmmoWidget.setObjectName("editAmmoWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(editAmmoWidget.sizePolicy().hasHeightForWidth())
        editAmmoWidget.setSizePolicy(sizePolicy)
        editAmmoWidget.setMinimumSize(QtCore.QSize(0, 0))

        self.name_box = QtWidgets.QGroupBox('Ammo name', self)
        self.ammo_box = QtWidgets.QGroupBox('Properties', self)
        self.zero_box = QtWidgets.QGroupBox('Zeroing', self)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.vBoxLayout.setObjectName("vBoxLayout")
        # self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        self.name_boxLayout = QtWidgets.QFormLayout(self.name_box)
        self.name_boxLayout.setObjectName("name_boxLayout")

        self.ammo_boxLayout = QtWidgets.QVBoxLayout(self.ammo_box)
        self.ammo_boxLayout.setObjectName("ammo_boxLayout")

        self.zero_boxLayout = QtWidgets.QVBoxLayout(self.zero_box)
        self.zero_boxLayout.setObjectName("zero_boxLayout")

        self.name_label = QtWidgets.QLabel('Name')
        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText('Name')

        diameter = ConverSpinBox(self, 0.01)
        weight = ConverSpinBox(self, 0.5)
        length = ConverSpinBox(self, 0.01)
        mv = ConverSpinBox(self, 1)
        powder_sens = ConverSpinBox(self, 0.1)
        powder_temp = ConverSpinBox(self, 1)

        zero_range = ConverSpinBox(self, 1)
        zero_height = ConverSpinBox(self, 0.5)
        # zero_offset = ConverSpinBox(self, 1)
        is_zero_atmo = QtWidgets.QCheckBox(self)
        altitude = ConverSpinBox(self, 10)
        pressure = ConverSpinBox(self, 1)
        temperature = ConverSpinBox(self, 1)
        humidity = ConverSpinBox(self, 1)

        drag_data = EditDragDataButton(self, 'Edit')

        drag_model = ComboBox(self, items=(
            ('G1', DragModel.G1),
            ('G7', DragModel.G7),
            ('CDM', DragModel.CDM)
        ))

        self.diameter = FormRow3(diameter, 'Diameter', 'in')
        self.weight = FormRow3(weight, 'Weight', 'grn')
        self.length = FormRow3(length, 'Length', 'in')
        self.mv = FormRow3(mv, 'Muzzle velocity', 'mps')
        self.powder_sens = FormRow3(powder_sens, 'Powder sensitivity', '%')
        self.powder_temp = FormRow3(powder_temp, 'Powder temp', 'C')

        self.calc_powder_sens = QtWidgets.QPushButton('Calculate powder sensitivity')

        self.drag_model = FormRow3(drag_model, 'Drag model', parent=self)

        self.drag_data = FormRow3(drag_data, 'Drag data', parent=self)

        self.zero_range = FormRow3(zero_range, 'Zero range', 'mm')
        self.zero_height = FormRow3(zero_height, 'Zero height', 'mm')
        self.is_zero_atmo = FormRow3(is_zero_atmo, 'Zero atmosphere')
        self.altitude = FormRow3(altitude, 'Altitude', 'degree')
        self.pressure = FormRow3(pressure, 'Pressure', 'kpa')
        self.temperature = FormRow3(temperature, 'Temperature', 'C')
        self.humidity = FormRow3(humidity, 'Humidity', '%')

        self.name_boxLayout.addRow(self.name_label, self.name)

        self.ammo_boxLayout.addWidget(self.diameter)
        self.ammo_boxLayout.addWidget(self.weight)
        self.ammo_boxLayout.addWidget(self.length)
        self.ammo_boxLayout.addWidget(self.mv)

        self.ammo_boxLayout.addWidget(self.drag_model)
        self.ammo_boxLayout.addWidget(self.drag_data)

        self.ammo_boxLayout.addWidget(self.powder_sens)
        self.ammo_boxLayout.addWidget(self.powder_temp)

        self.ammo_boxLayout.addWidget(self.calc_powder_sens)

        self.zero_boxLayout.addWidget(self.zero_range)
        self.zero_boxLayout.addWidget(self.zero_height)
        self.zero_boxLayout.addWidget(self.is_zero_atmo)
        self.zero_boxLayout.addWidget(self.altitude)
        self.zero_boxLayout.addWidget(self.pressure)
        self.zero_boxLayout.addWidget(self.temperature)
        self.zero_boxLayout.addWidget(self.humidity)

        self.vBoxLayout.addWidget(self.name_box)
        self.vBoxLayout.addWidget(self.ammo_box)
        self.vBoxLayout.addWidget(self.zero_box)

        self.retranslateUi(editAmmoWidget)
        QtCore.QMetaObject.connectSlotsByName(editAmmoWidget)

    def retranslateUi(self, editAmmoWidget: 'EditAmmoWidget'):
        _translate = QtCore.QCoreApplication.translate
        editAmmoWidget.setWindowTitle(_translate("editAmmoWidget", "Form"))

    def connectUi(self, editAmmoWidget):
        self.drag_model.currentIndexChanged.connect(self.update_drag_data_btn)
        self.drag_data.clicked.connect(self.edit_drag_data)

        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            if settings:
                settings.settingsUpdated.connect(self.on_settings_update)

    def on_settings_update(self, settings: SettingsWidget):
        self.powder_temp.setConvertor(Convertor(Temperature, settings.tempUnits.currentData(), Temperature.Celsius))
        self.powder_temp.suffix.setText(self.powder_temp.convertor().unit_name)
        self.mv.setConvertor(Convertor(Velocity, settings.vUnits.currentData(), Velocity.MPS))
        self.mv.suffix.setText(self.mv.convertor().unit_name)
        self.diameter.setConvertor(Convertor(Distance, settings.dUnits.currentData(), Distance.Inch))
        self.diameter.suffix.setText(self.diameter.convertor().unit_name)
        self.length.setConvertor(Convertor(Distance, settings.lnUnits.currentData(), Distance.Inch))
        self.length.suffix.setText(self.length.convertor().unit_name)
        self.weight.setConvertor(Convertor(Weight, settings.wUnits.currentData(), Weight.Grain))
        self.weight.suffix.setText(self.weight.convertor().unit_name)

        self.zero_range.setConvertor(Convertor(Distance, settings.distUnits.currentData(), Distance.Meter))
        self.zero_range.suffix.setText(self.zero_range.convertor().unit_name)
        self.zero_height.setConvertor(Convertor(Distance, settings.shUnits.currentData(), Distance.Centimeter))
        self.zero_height.suffix.setText(self.zero_height.convertor().unit_name)
        self.altitude.setConvertor(Convertor(Distance, settings.distUnits.currentData(), Distance.Meter))
        self.altitude.suffix.setText(self.altitude.convertor().unit_name)
        self.pressure.setConvertor(Convertor(Pressure, settings.pUnits.currentData(), Pressure.MmHg))
        self.pressure.suffix.setText(self.pressure.convertor().unit_name)
        self.temperature.setConvertor(Convertor(Temperature, settings.tempUnits.currentData(), Temperature.Celsius))
        self.temperature.suffix.setText(self.temperature.convertor().unit_name)

    def edit_drag_data(self):
        dm = self.drag_model.currentData()
        self.editDrag.emit(dm, self.ammo)

    def update_drag_data_btn(self, index):
        data = self.drag_model.currentData()
        self.drag_data.update_df(data, self.ammo)

    def update_drag_data(self, drag_data):
        dm = self.drag_model.currentData()
        if dm == DragModel.G1:
            self.ammo.bc_list = drag_data
        elif dm == DragModel.G7:
            self.ammo.bc7_list = drag_data
        else:
            self.ammo.cdm_list = drag_data
        self.drag_data.update_df(dm, self.ammo)

    def validate(self):
        if not 0.01 <= self.diameter.rawValue() <= 70:
            self.diameter.value_field.setFocus()
            msg = "Diameter must be between 0.001 and 70 inch"
        elif not 0.001 <= self.weight.rawValue() <= 5000:
            self.weight.value_field.setFocus()
            msg = "Weight must be between 0.001 and 5000 inch"
        elif not 0.01 <= self.length.rawValue() <= 70:
            self.length.value_field.setFocus()
            msg = "Length must be between 0.01 and 70 inch"
        elif not 10 <= self.mv.rawValue() <= 2000:
            self.mv.value_field.setFocus()
            msg = "Muzzle velocity must be between 10 and 2000 mps"
        elif not 0 <= self.powder_sens.rawValue() <= 10:
            self.powder_sens.value_field.setFocus()
            msg = "Powder sensitivity must be between 0 and 10 %"
        elif not -50 <= self.powder_temp.rawValue() <= 50:
            self.powder_temp.value_field.setFocus()
            msg = "Powder temperature must be between -50 and 50 °C"
        elif not 10 <= self.zero_range.rawValue() <= 1000:
            self.zero_range.value_field.setFocus()
            msg = "Zero range must be between 10 and 1000 m"
        elif not 0 < self.zero_height.rawValue() <= 1000:
            self.zero_height.value_field.setFocus()
            msg = 'Sight height must be > 0'
        elif not 9000 >= self.altitude.rawValue() >= 0:
            self.altitude.value_field.setFocus()
            msg = "Altitude must be between 0 and 9000 m"
        elif not 381 < self.pressure.rawValue() <= 1015:
            self.pressure.value_field.setFocus()
            msg = "Pressure must be between 381 and 1015 mmHg"
        elif not -50 <= self.temperature.rawValue() <= 50:
            self.temperature.value_field.setFocus()
            msg = "Temperature must be between -50 and 50 °C"
        elif not 0 <= self.humidity.value() <= 100:
            self.humidity.value_field.setFocus()
            msg = "Humidity must be between 0 and 100 %"
        else:
            return
        self.errorSig.emit(msg)
        raise ValueError('Validation error')

    def validate_drag_model(self):
        drag_model = self.drag_model.currentData()
        if drag_model == DragModel.G1:
            bclist = [p for p in self.ammo.bc_list if p[0] > 0 and p[1] > 0]
        elif drag_model == DragModel.G7:
            bclist = [p for p in self.ammo.bc7_list if p[0] > 0 and p[1] > 0]
        else:
            bclist = [p for p in self.ammo.cdm_list if p[0] >= 0 and  p[1] > 0]
        if len(bclist) <= 0:
            self.errorSig.emit('Wrong Drag data')
            raise ValueError('Wrong BC data')
        return

    def save_ammo(self):
        self.validate()
        self.validate_drag_model()

        self.ammo.name = self.name.text() if self.name.text() else self.name.placeholderText()
        self.ammo.diameter = self.diameter.rawValue()
        self.ammo.weight = self.weight.rawValue()
        self.ammo.length = self.length.rawValue()
        self.ammo.muzzle_velocity = self.mv.rawValue()
        self.ammo.powder_temp = self.powder_temp.rawValue()

        self.ammo.drag_model = self.drag_model.currentData()
        self.ammo.temp_sens = self.powder_sens.value()

        self.ammo.zerodata.zero_range = self.zero_range.rawValue()
        self.ammo.zerodata.zero_height = self.zero_height.rawValue()
        self.ammo.zerodata.altitude = self.altitude.rawValue()
        self.ammo.zerodata.pressure = self.pressure.rawValue()
        self.ammo.zerodata.temperature = self.temperature.rawValue()

        self.ammo.zerodata.is_zero_atmo = self.is_zero_atmo.isChecked()
        self.ammo.zerodata.humidity = self.humidity.value()

        Worker.ammo_add_or_update(self.ammo)

    def display_data(self, rifle, ammo):

        self.ammo = AmmoData('New Ammo', rifle=rifle) if not isinstance(ammo, AmmoData) else ammo
        self.rifle = self.ammo.rifle
        self.name.setText(self.ammo.name)
        self.diameter.setRawValue(self.ammo.diameter)
        self.weight.setRawValue(self.ammo.weight)
        self.length.setRawValue(self.ammo.length)
        self.mv.setRawValue(self.ammo.muzzle_velocity)
        self.powder_temp.setRawValue(self.ammo.powder_temp)

        self.drag_model.setCurrentIndex(self.drag_model.findData(self.ammo.drag_model))
        self.powder_sens.setValue(self.ammo.temp_sens)

        dm = self.drag_model.currentData()
        self.drag_data.update_df(dm, self.ammo)

        zerodata = self.ammo.zerodata
        self.zero_range.setRawValue(zerodata.zero_range)
        self.zero_height.setRawValue(zerodata.zero_height)
        self.altitude.setRawValue(zerodata.altitude)
        self.pressure.setRawValue(zerodata.pressure)
        self.temperature.setRawValue(zerodata.temperature)

        self.is_zero_atmo.setChecked(zerodata.is_zero_atmo)
        self.humidity.setValue(zerodata.humidity)


class EditShotWidget(QtWidgets.QWidget):
    errorSig = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(EditShotWidget, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)
        self.ammo = None
        self.rifle = None

    def setupUi(self, editShotWidget):
        editShotWidget.setObjectName("editShotWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(editShotWidget.sizePolicy().hasHeightForWidth())
        editShotWidget.setSizePolicy(sizePolicy)
        editShotWidget.setMinimumSize(QtCore.QSize(0, 0))

        self.target_box = QtWidgets.QGroupBox('Target', self)
        self.atmo_box = QtWidgets.QGroupBox('Atmosphere', self)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.vBoxLayout.setObjectName("vBoxLayout")
        self.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        self.target_boxLayout = QtWidgets.QVBoxLayout(self.target_box)
        self.target_boxLayout.setObjectName("target_boxLayout")

        self.atmo_boxLayout = QtWidgets.QVBoxLayout(self.atmo_box)
        self.atmo_boxLayout.setObjectName("atmo_boxLayout")

        distance = ConverSpinBox(self, 1)
        look_angle = ConverSpinBox(self, 1)
        altitude = ConverSpinBox(self, 1)
        pressure = ConverSpinBox(self)
        temperature = ConverSpinBox(self, 1)
        humidity = SpinBox(self, 1)
        wind_speed = ConverSpinBox(self, 1)
        wind_angle = ConverSpinBox(self, 1)

        self.distance = FormRow3(distance,  'Distance', 'm')
        self.look_angle = FormRow3(look_angle, 'Look Angle', 'degree')
        self.altitude = FormRow3(altitude, 'Altitude', 'm')
        self.pressure = FormRow3(pressure, 'Pressure', 'mmGh')
        self.temperature = FormRow3(temperature, 'Temperature', 'C')
        self.humidity = FormRow3(humidity, 'Humidity', '%')
        self.wind_speed = FormRow3(wind_speed, 'Wind speed', 'mps')
        self.wind_angle = FormRow3(wind_angle, 'Wind angle', 'degree')

        self.target_boxLayout.addWidget(self.distance)
        self.target_boxLayout.addWidget(self.look_angle)

        self.atmo_boxLayout.addWidget(self.altitude)
        self.atmo_boxLayout.addWidget(self.pressure)
        self.atmo_boxLayout.addWidget(self.temperature)
        self.atmo_boxLayout.addWidget(self.humidity)
        self.atmo_boxLayout.addWidget(self.wind_speed)
        self.atmo_boxLayout.addWidget(self.wind_angle)

        self.bottom_bar = QtWidgets.QWidget(self)
        self.bottom_bar_layout = QtWidgets.QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.one_shot_btn = QtWidgets.QPushButton('One shot')
        self.one_shot_btn.setProperty('class', 'danger')
        self.traj_btn = QtWidgets.QPushButton('Trajectory')
        self.bottom_bar_layout.addWidget(self.one_shot_btn)
        self.bottom_bar_layout.addWidget(self.traj_btn)

        self.vBoxLayout.addWidget(self.target_box)
        self.vBoxLayout.addWidget(self.atmo_box)
        self.vBoxLayout.addWidget(self.bottom_bar)

        self.retranslateUi(editShotWidget)
        QtCore.QMetaObject.connectSlotsByName(editShotWidget)

    def retranslateUi(self, editShotWidget: 'EditShotWidget'):
        _translate = QtCore.QCoreApplication.translate
        editShotWidget.setWindowTitle(_translate("editShotWidget", "Form"))

    def connectUi(self, editAmmoWidget):

        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            if settings:
                settings.settingsUpdated.connect(self.on_settings_update)

    def on_settings_update(self, settings: SettingsWidget):
        self.distance.setConvertor(Convertor(Distance, settings.distUnits.currentData(), Distance.Meter))
        self.distance.suffix.setText(self.distance.convertor().unit_name)
        self.look_angle.setConvertor(Convertor(Angular, settings.angleUnits.currentData(), Angular.Degree))
        self.look_angle.suffix.setText(self.look_angle.convertor().unit_name)
        self.altitude.setConvertor(Convertor(Distance, settings.distUnits.currentData(), Distance.Meter))
        self.altitude.suffix.setText(self.altitude.convertor().unit_name)
        self.pressure.setConvertor(Convertor(Pressure, settings.pUnits.currentData(), Pressure.MmHg))
        self.pressure.suffix.setText(self.pressure.convertor().unit_name)
        self.temperature.setConvertor(Convertor(Temperature, settings.tempUnits.currentData(), Temperature.Celsius))
        self.temperature.suffix.setText(self.temperature.convertor().unit_name)
        self.wind_angle.setConvertor(Convertor(Angular, settings.angleUnits.currentData(), Angular.Degree))
        self.wind_angle.suffix.setText(self.wind_angle.convertor().unit_name)
        self.wind_speed.setConvertor(Convertor(Velocity, settings.vUnits.currentData(), Velocity.MPS))
        self.wind_speed.suffix.setText(self.wind_speed.convertor().unit_name)

    def validate(self):
        if not 5000 >= self.distance.rawValue() >= 10:
            self.distance.value_field.setFocus()
            msg = "Target distance must be between 10 and 3000 m"
        elif not 9000 >= self.altitude.rawValue() >= 0:
            self.altitude.value_field.setFocus()
            msg = "Altitude must be between 0 and 9000 m"
        elif not 381 < self.pressure.rawValue() <= 1015:
            self.pressure.value_field.setFocus()
            msg = "Pressure must be between 381 and 1015 mmHg"
        elif not -50 <= self.temperature.rawValue() <= 50:
            self.temperature.value_field.setFocus()
            msg = "Temperature must be between -50 and 50 °C"
        elif not 0 <= self.humidity.value() <= 100:
            self.humidity.value_field.setFocus()
            msg = "Humidity must be between 0 and 100 %"
        elif not self.wind_speed.rawValue() >= 0:
            self.wind_speed.value_field.setFocus()
            msg = "Wind speed must be >= 0"
        elif not 0 <= self.wind_angle.rawValue() < 360:
            self.wind_angle.value_field.setFocus()
            msg = "Wind angle must be between 0 and 359 °"
        else:
            return
        self.errorSig.emit(msg)
        raise ValueError('Validation error')

    def save_ammo(self):
        self.validate()
        self.ammo.target.distance = self.distance.rawValue()
        self.ammo.target.look_angle = self.look_angle.rawValue()
        self.ammo.atmo.altitude = self.altitude.rawValue()
        self.ammo.atmo.pressure = self.pressure.rawValue()
        self.ammo.atmo.temperature = self.temperature.rawValue()
        self.ammo.atmo.wind_speed = self.wind_speed.value()
        self.ammo.atmo.wind_angle = self.wind_angle.value()

        self.ammo.atmo.humidity = self.humidity.value()

        Worker.ammo_add_or_update(self.ammo)

    def display_data(self, rifle, ammo):
        self.ammo = AmmoData('New Ammo', rifle=rifle) if not isinstance(ammo, AmmoData) else ammo
        self.rifle = self.ammo.rifle
        target = self.ammo.target
        atmo = self.ammo.atmo

        self.distance.setRawValue(target.distance)
        self.look_angle.setRawValue(target.look_angle)
        self.altitude.setRawValue(atmo.altitude)
        self.pressure.setRawValue(atmo.pressure)
        self.temperature.setRawValue(atmo.temperature)
        self.wind_speed.setValue(atmo.wind_speed)
        self.wind_angle.setValue(atmo.wind_angle)

        self.humidity.setValue(atmo.humidity)
