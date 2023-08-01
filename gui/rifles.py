from PySide6 import QtWidgets, QtCore, QtGui

from datatypes.dbworker import Worker, TwistDir, RifleData
from gui.settings import SettingsWidget
from units import Distance, Convertor
from .widgets import FormRow3, ComboBox, ConverSpinBox


class RifleItemWidget(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(RifleItemWidget, self).__init__(parent)
        self.setup_ui(self)
        self.rifle_data = None

    def setup_ui(self, rifleItemWidget):
        rifleItemWidget.setObjectName("rifleItemWidget")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.barrel = QtWidgets.QLabel()
        self.sight = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.barrel)
        self.gridLayout.addWidget(self.sight)

    def translateUi(self, rifleItemWidget):
        ...

    def set_data(self, rifle):
        settings = self.get_settings()

        twist = Distance(rifle.barrel_twist, Distance.Inch).convert(settings.twistUnits.currentData())
        sh = Distance(rifle.sight_height, Distance.Centimeter).convert(settings.shUnits.currentData())

        self.rifle_data = rifle
        self.setTitle(self.rifle_data.name)
        self.barrel.setText(f'Barrel: 1 in {twist}')
        self.sight.setText(f'Sight Ht: {sh}')

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings


class RiflesLi(QtWidgets.QListWidget):
    edit_context_action = QtCore.Signal(object)

    rifle_clicked_sig = QtCore.Signal(object)
    rifle_edit_sig = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(RiflesLi, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)
        self.refresh()

    def contextMenuEvent(self, event):
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
                uid = self.itemWidget(selected_item).rifle_data.id
                Worker.delete_rifle(uid)
                self.refresh()

    def setupUi(self, RiflesLi):
        self.setObjectName('riflesLi')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

    def create_item(self, rifle):
        widget = RifleItemWidget(self)
        widget.set_data(rifle)
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        item.setData(0, rifle.id)
        self.addItem(item)
        self.setItemWidget(item, widget)

    def refresh(self):
        rifles = Worker.list_rifles()
        self.clear()
        if rifles:
            for rifle in rifles:
                self.create_item(rifle)

    def retranslateUi(self, riflesWidget: 'RiflesWidget'):
        _translate = QtCore.QCoreApplication.translate
        riflesWidget.setWindowTitle(_translate("riflesWidget", "Form"))

    def connectUi(self, riflesWidget: 'RiflesWidget'):
        self.itemClicked.connect(self.rifle_clicked)
        self.edit_context_action.connect(self.rifle_edit_clicked)

    def rifle_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: RifleItemWidget = self.itemWidget(item)
        self.rifle_clicked_sig.emit(widget.rifle_data)

    def rifle_edit_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: RifleItemWidget = self.itemWidget(item)
        self.rifle_edit_sig.emit(widget.rifle_data)


class EditRifleWidget(QtWidgets.QWidget):
    errorSig = QtCore.Signal(str)

    def __init__(self, parent=None, uid: int = None, rifle: 'RifleData' = None):
        super(EditRifleWidget, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)
        self.uid = uid

        if rifle is not None:
            self.display_data(rifle)

    def setupUi(self, editRifleWidget):
        editRifleWidget.setObjectName("editRifleWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(editRifleWidget.sizePolicy().hasHeightForWidth())
        editRifleWidget.setSizePolicy(sizePolicy)
        editRifleWidget.setMinimumSize(QtCore.QSize(0, 0))

        self.name_box = QtWidgets.QGroupBox('Rifle name', self)
        self.props_box = QtWidgets.QGroupBox('Properties', self)
        self.reticle_box = QtWidgets.QGroupBox('Reticle', self)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.vBoxLayout.setObjectName("vBoxLayout")
        self.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        self.name_boxLayout = QtWidgets.QFormLayout(self.name_box)
        self.name_boxLayout.setObjectName("name_boxLayout")

        self.props_boxLayout = QtWidgets.QVBoxLayout(self.props_box)
        self.props_boxLayout.setObjectName("props_boxLayout")

        self.name_label = QtWidgets.QLabel('Name')
        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText('Name')

        barrel_twist = ConverSpinBox(self, 0.5)
        twist_dir = ComboBox(self, (('Right', TwistDir.Right), ('Left', TwistDir.Left)))
        sight_height = ConverSpinBox(self, 0.5)

        self.barrel_twist = FormRow3(barrel_twist, 'Barel Twist', 'in')
        self.barrel_twist.setObjectName('barrel_twist')
        self.twist_dir = FormRow3(twist_dir, 'Twist direction')
        self.sight_height = FormRow3(sight_height, 'Sight height', 'mm')
        self.sight_height.setObjectName('sight_height')

        self.name_boxLayout.addRow(self.name_label, self.name)

        self.props_boxLayout.addWidget(self.barrel_twist)
        self.props_boxLayout.addWidget(self.twist_dir)
        self.props_boxLayout.addWidget(self.sight_height)

        self.vBoxLayout.addWidget(self.name_box)
        self.vBoxLayout.addWidget(self.props_box)
        self.vBoxLayout.addWidget(self.reticle_box)

        self.retranslateUi(editRifleWidget)
        QtCore.QMetaObject.connectSlotsByName(editRifleWidget)

    def retranslateUi(self, editRifleWidget: 'EditRifleWidget'):
        _translate = QtCore.QCoreApplication.translate
        editRifleWidget.setWindowTitle(_translate("editRifleWidget", "Form"))

    def connectUi(self, editRifleWidget):
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            if settings:
                settings.settingsUpdated.connect(self.on_settings_update)

    def on_settings_update(self, settings: SettingsWidget):
        self.barrel_twist.setConvertor(Convertor(Distance, settings.twistUnits.currentData(), Distance.Inch))
        self.barrel_twist.suffix.setText(self.barrel_twist.convertor().unit_name)

        self.sight_height.setConvertor(Convertor(Distance, settings.shUnits.currentData(), Distance.Centimeter))
        self.sight_height.suffix.setText(self.sight_height.convertor().unit_name)

    def display_data(self, rifle: 'RifleData'):
        if not rifle:
            rifle = RifleData('New Rifle')
        self.uid = rifle.id
        self.name.setText(rifle.name)
        self.barrel_twist.setRawValue(rifle.barrel_twist)
        index = self.twist_dir.findData(rifle.barrel_twist_dir)
        self.twist_dir.setCurrentIndex(index)
        self.sight_height.setRawValue(rifle.sight_height)

    def save_rifle(self):
        self.validate()
        Worker.rifle_add_or_update(
            id=self.uid,
            name=self.name.text() if self.name.text() else self.name.placeholderText(),
            barrel_twist=self.barrel_twist.rawValue(),
            barrel_twist_dir=self.twist_dir.currentData(),
            sight_height=self.sight_height.rawValue(),
        )

    def validate(self):
        if not self.sight_height.rawValue() > 0:
            self.sight_height.value_field.setFocus()
            self.errorSig.emit('Sight height must be > 0')
        elif self.barrel_twist.rawValue() > 0:
            self.barrel_twist.value_field.setFocus()
            self.errorSig.emit('Twist must be > 0')
        else:
            return

        raise ValueError('Validation error')
