from PySide6 import QtWidgets, QtCore, QtGui

from dbworker import Worker, AmmoData, DragModel
from gui.app_logo import AppLogo, AppLabel


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
        self.addButton = QtWidgets.QPushButton('+')

        self.hBoxLayout.addWidget(self.addButton)

        self.retranslateUi(ammosHeader)
        QtCore.QMetaObject.connectSlotsByName(ammosHeader)

    def retranslateUi(self, ammosHeader: 'AmmosHeader'):
        _translate = QtCore.QCoreApplication.translate
        ammosHeader.setWindowTitle(_translate("ammosHeader", "Form"))
        ammosHeader.addButton.setText(_translate("ammosHeader", "+"))


class AmmosWidget(QtWidgets.QWidget):
    ammo_clicked_sig = QtCore.Signal(object)
    ammo_double_clicked_sig = QtCore.Signal(object)

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

        self.header = AmmosHeader(self)
        self.ammos_list = AmmosLi(self)
        self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.ammos_list)

        self.retranslateUi(ammosWidget)
        QtCore.QMetaObject.connectSlotsByName(ammosWidget)

    def retranslateUi(self, ammosWidget: 'AmmosWidget'):
        _translate = QtCore.QCoreApplication.translate
        ammosWidget.setWindowTitle(_translate("ammosWidget", "Form"))

    def connectUi(self, ammosWidget: 'AmmosWidget'):
        self.ammos_list.itemDoubleClicked.connect(self.ammo_double_clicked)
        self.ammos_list.itemClicked.connect(self.ammo_clicked)
        self.ammos_list.edit_context_action.connect(self.ammo_double_clicked)

    def ammo_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: AmmoItemWidget = self.ammos_list.itemWidget(item)
        self.ammo_clicked_sig.emit(widget.ammo_data)

    def ammo_double_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: AmmoItemWidget = self.ammos_list.itemWidget(item)
        self.ammo_double_clicked_sig.emit(widget.ammo_data)


class AddAmmoHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AddAmmoHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, editAmmoWidgetHeader):
        editAmmoWidgetHeader.setObjectName("editAmmoWidgetHeader")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")

        self.logo = AppLogo()
        self.label = AppLabel()
        self.hBoxLayout.addWidget(self.logo)
        self.hBoxLayout.addWidget(self.label)

        editAmmoWidgetHeader.setObjectName("editAmmoWidgetHeader")
        self.okButton = QtWidgets.QPushButton('Ok')

        self.hBoxLayout.addWidget(self.okButton)

        self.retranslateUi(editAmmoWidgetHeader)
        QtCore.QMetaObject.connectSlotsByName(editAmmoWidgetHeader)

    def retranslateUi(self, editAmmoWidgetHeader: 'AddAmmoHeader'):
        _translate = QtCore.QCoreApplication.translate
        editAmmoWidgetHeader.setWindowTitle(_translate("editAmmoWidgetHeader", "Form"))
        editAmmoWidgetHeader.okButton.setText(_translate("editAmmoWidgetHeader", "Ok"))


class EditAmmoWidget(QtWidgets.QWidget):
    ok_clicked = QtCore.Signal(object)

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
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        self.name_boxLayout = QtWidgets.QFormLayout(self.name_box)
        self.name_boxLayout.setObjectName("name_boxLayout")

        self.ammo_boxLayout = QtWidgets.QGridLayout(self.ammo_box)
        self.ammo_boxLayout.setObjectName("ammo_boxLayout")

        self.zero_boxLayout = QtWidgets.QFormLayout(self.zero_box)
        self.zero_boxLayout.setObjectName("zero_boxLayout")

        self.header = AddAmmoHeader(self)
        self.name_label = QtWidgets.QLabel('Name')
        self.name = QtWidgets.QLineEdit('Template')

        self.diameter_label = QtWidgets.QLabel('Diameter')
        self.diameter = QtWidgets.QDoubleSpinBox()
        self.weight_label = QtWidgets.QLabel('Weight')
        self.weight = QtWidgets.QDoubleSpinBox()
        self.length_label = QtWidgets.QLabel('Length')
        self.length = QtWidgets.QDoubleSpinBox()
        self.mv_label = QtWidgets.QLabel('Muzzle velocity')
        self.mv = QtWidgets.QDoubleSpinBox()
        self.powder_sens_label = QtWidgets.QLabel('Powder sensitivity')
        self.powder_sens = QtWidgets.QDoubleSpinBox()
        self.powder_temp_label = QtWidgets.QLabel('Powder temp')
        self.powder_temp = QtWidgets.QDoubleSpinBox()
        self.drag_model_label = QtWidgets.QLabel('Drag model')
        self.drag_model = QtWidgets.QComboBox()
        self.bc_label = QtWidgets.QLabel('Ballistic coefficient')
        self.bc = QtWidgets.QDoubleSpinBox()

        self.drag_model.addItem('G1', DragModel.G1)
        self.drag_model.addItem('G7', DragModel.G7)
        self.drag_model.addItem('CDM', DragModel.CDM)

        self.zero_range_label = QtWidgets.QLabel('Zero range')
        self.zero_range = QtWidgets.QDoubleSpinBox()
        self.zero_height_label = QtWidgets.QLabel('Zero range')
        self.zero_height = QtWidgets.QDoubleSpinBox()
        self.zero_offset_label = QtWidgets.QLabel('Zero range')
        self.zero_offset = QtWidgets.QDoubleSpinBox()

        self.is_zero_atmo_label = QtWidgets.QLabel('Zero atmosphere')
        self.is_zero_atmo = QtWidgets.QCheckBox()

        self.altitude_label = QtWidgets.QLabel('Altitude')
        self.altitude = QtWidgets.QDoubleSpinBox()

        self.pressure_label = QtWidgets.QLabel('Pressure')
        self.pressure = QtWidgets.QDoubleSpinBox()
        self.temperature_label = QtWidgets.QLabel('Temperature')
        self.temperature = QtWidgets.QDoubleSpinBox()
        self.humidity_label = QtWidgets.QLabel('Humidity')
        self.humidity = QtWidgets.QDoubleSpinBox()

        # for ch in self.ammo_box.findChildren(QtWidgets.QDoubleSpinBox):
        #     ch.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        # for ch in self.ammo_box.findChildren(QtWidgets.QComboBox):
        #     ch.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)

        self.name_boxLayout.addRow(self.name_label, self.name)

        self.ammo_boxLayout.addWidget(self.diameter_label)
        self.ammo_boxLayout.addWidget(self.diameter, 0, 1)
        self.ammo_boxLayout.addWidget(self.weight_label)
        self.ammo_boxLayout.addWidget(self.weight)
        self.ammo_boxLayout.addWidget(self.length_label)
        self.ammo_boxLayout.addWidget(self.length)
        self.ammo_boxLayout.addWidget(self.mv_label)
        self.ammo_boxLayout.addWidget(self.mv)
        self.ammo_boxLayout.addWidget(self.powder_sens_label)
        self.ammo_boxLayout.addWidget(self.powder_sens)
        self.ammo_boxLayout.addWidget(self.powder_temp_label)
        self.ammo_boxLayout.addWidget(self.powder_temp)
        self.ammo_boxLayout.addWidget(self.drag_model_label)
        self.ammo_boxLayout.addWidget(self.drag_model)
        self.ammo_boxLayout.addWidget(self.bc_label)
        self.ammo_boxLayout.addWidget(self.bc)

        self.zero_boxLayout.addRow(self.zero_range_label, self.zero_range)
        self.zero_boxLayout.addRow(self.zero_height_label, self.zero_height)
        self.zero_boxLayout.addRow(self.zero_offset_label, self.zero_offset)
        self.zero_boxLayout.addRow(self.is_zero_atmo_label, self.is_zero_atmo)
        self.zero_boxLayout.addRow(self.altitude_label, self.altitude)
        self.zero_boxLayout.addRow(self.pressure_label, self.pressure)
        self.zero_boxLayout.addRow(self.temperature_label, self.temperature)
        self.zero_boxLayout.addRow(self.humidity_label, self.humidity)

        self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.name_box)
        self.vBoxLayout.addWidget(self.ammo_box)
        self.vBoxLayout.addWidget(self.zero_box)

        self.retranslateUi(editAmmoWidget)
        QtCore.QMetaObject.connectSlotsByName(editAmmoWidget)

    def retranslateUi(self, editAmmoWidget: 'EditAmmoWidget'):
        _translate = QtCore.QCoreApplication.translate
        editAmmoWidget.setWindowTitle(_translate("editAmmoWidget", "Form"))

    def connectUi(self, editAmmoWidget):
        self.header.okButton.clicked.connect(self.save_ammo)

    def save_ammo(self):

        self.ammo.name = self.name.text()
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
        self.ok_clicked.emit(self.rifle)

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

        zerodata = self.ammo.zerodata
        self.zero_range.setValue(zerodata.zero_range)
        self.zero_height.setValue(zerodata.zero_height)
        self.zero_offset.setValue(zerodata.zero_offset)
        self.is_zero_atmo.setChecked(zerodata.is_zero_atmo)
        self.altitude.setValue(zerodata.altitude)
        self.pressure.setValue(zerodata.pressure)
        self.temperature.setValue(zerodata.temperature)
        self.humidity.setValue(zerodata.humidity)