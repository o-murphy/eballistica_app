from PySide6 import QtWidgets, QtCore, QtGui

from datatypes.dbworker import Worker, AmmoData, DragModel
from gui.app_logo import AppLogo, AppLabel
from gui.drag_model import EditDragDataButton
from gui.widgets import FormRow3, SpinBox, ComboBox


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

    def set_data(self, ammo: AmmoData):
        self.ammo_data = ammo
        self.box.setTitle(self.ammo_data.name)
        self.caliber.setText(f'{ammo.diameter}')
        self.ammo.setText(f'{ammo.weight}/{ammo.drag_model.name}')
        self.mv.setText(f'{ammo.muzzle_velocity}')
        self.zero.setText(f'{ammo.zerodata.zero_range}/{ammo.zerodata.zero_height}')


class AmmosDelegate(QtWidgets.QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        widget = index.data(QtCore.Qt.UserRole)
        if widget is not None:
            widget.setGeometry(QtCore.QRect(0, 0, size.width(), size.height()))
            size.setHeight(widget.sizeHint().height())
        return size


class AmmosLi(QtWidgets.QListWidget):
    edit_context_action = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(AmmosLi, self).__init__(parent)
        self.filter = {}

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

    def setupUi(self, AmmosLi):
        self.menu = QtWidgets.QMenu()
        self.menu.addAction(self.edit_item)

    def set_filter(self, **kwargs):
        self.filter = kwargs

    def create_item(self, rifle):
        widget = AmmoItemWidget()
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


class AmmosWidget(QtWidgets.QWidget):
    ammo_clicked_sig = QtCore.Signal(object)
    ammo_edit_sig = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(AmmosWidget, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)

    def setupUi(self, ammosWidget):
        ammosWidget.setObjectName("ammosWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ammosWidget.sizePolicy().hasHeightForWidth())
        ammosWidget.setSizePolicy(sizePolicy)
        ammosWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.vBoxLayout = QtWidgets.QVBoxLayout(ammosWidget)
        self.vBoxLayout.setObjectName("vBoxLayout")
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        # self.header = AmmosHeader(self)
        self.ammos_list = AmmosLi(self)
        # self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.ammos_list)

        self.retranslateUi(ammosWidget)
        QtCore.QMetaObject.connectSlotsByName(ammosWidget)

    def retranslateUi(self, ammosWidget: 'AmmosWidget'):
        _translate = QtCore.QCoreApplication.translate
        ammosWidget.setWindowTitle(_translate("ammosWidget", "Form"))

    def connectUi(self, ammosWidget: 'AmmosWidget'):
        # self.ammos_list.itemDoubleClicked.connect(self.ammo_edit_clicked)
        self.ammos_list.itemClicked.connect(self.ammo_clicked)
        self.ammos_list.edit_context_action.connect(self.ammo_edit_clicked)

    def ammo_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: AmmoItemWidget = self.ammos_list.itemWidget(item)
        self.ammo_clicked_sig.emit(widget.ammo_data)

    def ammo_edit_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: AmmoItemWidget = self.ammos_list.itemWidget(item)
        self.ammo_edit_sig.emit(widget.ammo_data)


class EditAmmoWidget(QtWidgets.QWidget):
    # ok_clicked = QtCore.Signal(object)
    editDrag = QtCore.Signal(object, object)

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

        diameter = SpinBox(self, 0.01, 155, 1)
        weight = SpinBox(self, 0.01, 1000, 1)
        length = SpinBox(self, 0.01, 10, 1)
        mv = SpinBox(self, 1, 2000, 1)
        powder_sens = SpinBox(self, 0, 100, 0.01)
        powder_temp = SpinBox(self, -50, +50, 1)

        self.diameter = FormRow3(diameter, 'Diameter', 'in')
        self.weight = FormRow3(weight, 'Weight', 'grn')
        self.length = FormRow3(length, 'Length', 'in')
        self.mv = FormRow3(mv, 'Muzzle velocity', 'mps')
        self.powder_sens = FormRow3(powder_sens, 'Powder sensitivity', '%')
        self.powder_temp = FormRow3(powder_temp, 'Powder temp', 'C')

        # self.weight = FormSpinBox(self, 0.01, 1000, 1, 'grn', 'Weight')
        # self.length = FormSpinBox(self, 0.01, 10, 1, 'in', 'Length')
        # self.mv = FormSpinBox(self, 1, 2000, 1, 'mps', 'Muzzle velocity')

        # self.powder_sens = FormSpinBox(self, 0, 100, 0.01, '%', 'Powder sensitivity')
        # self.powder_temp = FormSpinBox(self, -50, +50, 1, 'C', 'Powder temp')

        self.calc_powder_sens = QtWidgets.QPushButton('Calculate powder sensitivity')

        drag_model = ComboBox(self, items=(
            ('G1', DragModel.G1),
            ('G7', DragModel.G7),
            ('CDM', DragModel.CDM)
        ))
        self.drag_model = FormRow3(drag_model, 'Drag model', parent=self)


        # self.drag_model_label = QtWidgets.QLabel('Drag model')
        # self.drag_model = FormComboBox(prefix='Drag model')

        drag_data = EditDragDataButton(self, 'Edit')
        self.drag_data = FormRow3(drag_data, 'Drag data', parent=self)

        # self.drag_model.addItem('G1', DragModel.G1)
        # self.drag_model.addItem('G7', DragModel.G7)
        # self.drag_model.addItem('CDM', DragModel.CDM)

        zero_range = SpinBox(self, 1, 500, 1)
        zero_height = SpinBox(self, 1, 100, 0.5)
        zero_offset = SpinBox(self, 1, 500, 1)
        is_zero_atmo = QtWidgets.QCheckBox(self)
        altitude = SpinBox(self, 0, 359, 1)
        pressure = SpinBox(self, 0, 1100, 1)
        temperature = SpinBox(self, -50, 50, 1)
        humidity = SpinBox(self, 0, 100, 1)
        self.zero_range = FormRow3(zero_range, 'Zero range', 'mm')
        self.zero_height = FormRow3(zero_height, 'Zero height', 'mm')
        self.zero_offset = FormRow3(zero_offset, 'Zero offset', 'mm')
        self.is_zero_atmo = FormRow3(is_zero_atmo, 'Zero atmosphere')
        self.altitude = FormRow3(altitude, 'Altitude', 'degree')
        self.pressure = FormRow3(pressure, 'Pressure', 'kpa')
        self.temperature = FormRow3(temperature, 'Temperature', 'C')
        self.humidity = FormRow3(humidity, 'Humidity', '%')


        # self.zero_range = FormSpinBox(self, 1, 500, 1, 'mm', 'Zero range')
        # self.zero_height = FormSpinBox(self, 1, 100, 0.5, 'mm', 'Zero height')
        # self.zero_offset = FormSpinBox(self, 1, 500, 1, 'mm', 'Zero offset')

        # self.is_zero_atmo = FormCheckBox(self, prefix='Zero atmosphere')

        # self.altitude = FormSpinBox(self, 0, 359, 1, 'degree', 'Altitude')
        # self.pressure = FormSpinBox(self, 0, 1100, 1, 'kpa', 'Pressure')
        # self.temperature = FormSpinBox(self, -50, 50, 1, 'C', 'Temperature')
        # self.humidity = FormSpinBox(self, 0, 100, 1, '%', 'Humidity')

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
        self.zero_boxLayout.addWidget(self.zero_offset)
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

    def save_ammo(self):

        self.ammo.name = self.name.text() if self.name.text() else self.name.placeholderText()
        self.ammo.diameter = self.diameter.value()
        self.ammo.weight = self.weight.value()
        self.ammo.length = self.length.value()
        self.ammo.muzzle_velocity = self.mv.value()
        self.ammo.temp_sens = self.powder_sens.value()
        self.ammo.powder_temp = self.powder_temp.value()
        self.ammo.drag_model = self.drag_model.currentData()

        self.ammo.zerodata.zero_range = self.zero_range.value()
        self.ammo.zerodata.zero_height = self.zero_height.value()
        self.ammo.zerodata.zero_offset = self.zero_offset.value()
        self.ammo.zerodata.is_zero_atmo = self.is_zero_atmo.isChecked()
        self.ammo.zerodata.altitude = self.altitude.value()
        self.ammo.zerodata.pressure = self.pressure.value()
        self.ammo.zerodata.temperature = self.temperature.value()
        self.ammo.zerodata.humidity = self.humidity.value()

        Worker.ammo_add_or_update(self.ammo)
        # self.ok_clicked.emit(self.rifle)

    def display_data(self, rifle, ammo):

        self.ammo = AmmoData('New Ammo', rifle=rifle) if not isinstance(ammo, AmmoData) else ammo

        self.rifle = self.ammo.rifle
        self.name.setText(self.ammo.name)
        self.diameter.setValue(self.ammo.diameter)
        self.weight.setValue(self.ammo.weight)
        self.length.setValue(self.ammo.length)
        self.mv.setValue(self.ammo.muzzle_velocity)
        self.powder_sens.setValue(self.ammo.temp_sens)
        self.powder_temp.setValue(self.ammo.powder_temp)
        self.drag_model.setCurrentIndex(self.drag_model.findData(self.ammo.drag_model))

        dm = self.drag_model.currentData()
        self.drag_data.update_df(dm, self.ammo)

        zerodata = self.ammo.zerodata
        self.zero_range.setValue(zerodata.zero_range)
        self.zero_height.setValue(zerodata.zero_height)
        self.zero_offset.setValue(zerodata.zero_offset)
        self.is_zero_atmo.setChecked(zerodata.is_zero_atmo)
        self.altitude.setValue(zerodata.altitude)
        self.pressure.setValue(zerodata.pressure)
        self.temperature.setValue(zerodata.temperature)
        self.humidity.setValue(zerodata.humidity)


class EditShotWidget(QtWidgets.QWidget):
    # ok_clicked = QtCore.Signal(object)

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

        # self.name_box = QtWidgets.QGroupBox('Ammo name', self)
        self.target_box = QtWidgets.QGroupBox('Target', self)
        self.atmo_box = QtWidgets.QGroupBox('Atmosphere', self)
        # self.spin_box = QtWidgets.QGroupBox('Spin Drift', self)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.vBoxLayout.setObjectName("vBoxLayout")
        # self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        # self.name_boxLayout = QtWidgets.QFormLayout(self.name_box)
        # self.name_boxLayout.setObjectName("name_boxLayout")

        self.target_boxLayout = QtWidgets.QVBoxLayout(self.target_box)
        self.target_boxLayout.setObjectName("target_boxLayout")

        self.atmo_boxLayout = QtWidgets.QVBoxLayout(self.atmo_box)
        self.atmo_boxLayout.setObjectName("atmo_boxLayout")

        # self.spin_boxLayout = QtWidgets.QVBoxLayout(self.spin_box)
        # self.spin_boxLayout.setObjectName("spin_boxLayout")

        # self.header = AddAmmoHeader(self)
        # self.name_label = QtWidgets.QLabel('Name')
        # self.name = QtWidgets.QLineEdit()
        # self.name.setPlaceholderText('Name')

        distance = SpinBox(self, 1, 5000, 1)
        look_angle = SpinBox(self, 0, 359, 1)
        altitude = SpinBox(self, 0, 359, 1)
        pressure = SpinBox(self, 0, 1100, 1)
        temperature = SpinBox(self, -50, 50, 1)
        humidity = SpinBox(self, 0, 100, 1)
        wind_speed = SpinBox(self, 0, 100, 1)
        wind_angle = SpinBox(self, 0, 359, 1)

        self.distance = FormRow3(distance,  'Distance', 'm')
        self.look_angle = FormRow3(look_angle, 'Look Angle', 'degree')
        self.altitude = FormRow3(altitude, 'Look Angle', 'Altitude')
        self.pressure = FormRow3(pressure, 'Look Angle', 'Pressure')
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

        # self.spin_drift = FormCheckBox(self, prefix='Calculate spin drift')
        #
        # self.spin_boxLayout.addWidget(self.spin_drift)

        self.bottom_bar = QtWidgets.QWidget(self)
        self.bottom_bar_layout = QtWidgets.QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.one_shot_btn = QtWidgets.QPushButton('One shot')
        self.one_shot_btn.setProperty('class', 'danger')
        self.traj_btn = QtWidgets.QPushButton('Trajectory')
        self.bottom_bar_layout.addWidget(self.one_shot_btn)
        self.bottom_bar_layout.addWidget(self.traj_btn)

        # self.vBoxLayout.addWidget(self.name_box)
        self.vBoxLayout.addWidget(self.target_box)
        self.vBoxLayout.addWidget(self.atmo_box)
        # self.vBoxLayout.addWidget(self.spin_box)
        self.vBoxLayout.addWidget(self.bottom_bar)

        self.retranslateUi(editShotWidget)
        QtCore.QMetaObject.connectSlotsByName(editShotWidget)

    def retranslateUi(self, editShotWidget: 'EditShotWidget'):
        _translate = QtCore.QCoreApplication.translate
        editShotWidget.setWindowTitle(_translate("editShotWidget", "Form"))

    def connectUi(self, editShotWidget):
        ...

    def save_ammo(self):
        self.ammo.target.distance = self.distance.value()
        self.ammo.target.look_angle = self.look_angle.value()

        self.ammo.atmo.altitude = self.altitude.value()
        self.ammo.atmo.pressure = self.pressure.value()
        self.ammo.atmo.temperature = self.temperature.value()
        self.ammo.atmo.humidity = self.humidity.value()
        self.ammo.atmo.wind_speed = self.wind_speed.value()
        self.ammo.atmo.wind_angle = self.wind_angle.value()

        Worker.ammo_add_or_update(self.ammo)
        # self.ok_clicked.emit(self.rifle)

    def display_data(self, rifle, ammo):
        self.ammo = AmmoData('New Ammo', rifle=rifle) if not isinstance(ammo, AmmoData) else ammo

        self.rifle = self.ammo.rifle

        target = self.ammo.target
        atmo = self.ammo.atmo

        self.distance.setValue(target.distance)
        self.look_angle.setValue(target.look_angle)

        self.altitude.setValue(atmo.altitude)
        self.pressure.setValue(atmo.pressure)
        self.temperature.setValue(atmo.temperature)
        self.humidity.setValue(atmo.humidity)
        self.wind_speed.setValue(atmo.wind_speed)
        self.wind_angle.setValue(atmo.wind_angle)
