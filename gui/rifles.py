from getqt import *

from datatypes.dbworker import Worker, TwistDir, RifleData
from gui.settings import SettingsWidget
from units import Distance, Convertor
from .widgets import FormRow3, ComboBox, ConverSpinBox, GesturedListView


_translate = QtCore.QCoreApplication.translate


class RifleItemWidget(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(RifleItemWidget, self).__init__(parent)
        self.setup_ui(self)
        self.translateUi(self)
        self.rifle_data = None

    def setup_ui(self, rifleItemWidget):
        rifleItemWidget.setObjectName("RifleItemWidget")
        self.gridLayout = QtWidgets.QFormLayout(self)
        self.barre_label = QtWidgets.QLabel()
        self.barrel = QtWidgets.QLabel()
        self.sight_label = QtWidgets.QLabel()
        self.sight = QtWidgets.QLabel()
        self.gridLayout.addRow(self.barre_label, self.barrel)
        self.gridLayout.addRow(self.sight_label, self.sight)

    def translateUi(self, rifleItemWidget):
        # _translate = QtCore.QCoreApplication.translate
        rifleItemWidget.barre_label.setText(_translate("rifleItemWidget", 'Barrel: 1 in'))
        rifleItemWidget.sight_label.setText(_translate("rifleItemWidget", 'Sight Ht:'))

    def set_data(self, rifle):
        settings = self.get_settings()

        twist = Distance(rifle.barrel_twist, Distance.Inch).convert(settings.twistUnits.currentData())
        sh = Distance(rifle.sight_height, Distance.Centimeter).convert(settings.shUnits.currentData())

        self.rifle_data = rifle
        self.setTitle(self.rifle_data.name)
        self.barrel.setText(str(twist))
        self.sight.setText(str(sh))

        self.translateUi(self)

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings


class RiflesLi(GesturedListView):
    edit_context_action = Signal(object)

    rifle_clicked_sig = Signal(object)
    rifle_edit_sig = Signal(object)

    def __init__(self, parent=None):
        super(RiflesLi, self).__init__(parent)
        self.connectUi(self)
        self.refresh()

    def showContextMenu(self, pos=None):
        if pos is None:
            pos = self.mapFromGlobal(self.cursor().pos())

        item = self.itemAt(pos)
        if item:
            context_menu = QtWidgets.QMenu(self)

            context_menu.addAction(_translate("riflesLi", "Edit"), lambda: self.onContextMenuAction(item, "Edit"))
            context_menu.addAction(_translate("riflesLi", "Delete"), lambda: self.onContextMenuAction(item, "Delete"))
            context_menu.exec_(self.mapToGlobal(pos))

    def onContextMenuAction(self, item, action):
        # Implement the code to handle context menu actions
        if action == "Edit":
            self.edit_context_action.emit(item)
        elif action == 'Delete':
            uid = self.itemWidget(item).rifle_data.id
            Worker.delete_rifle(uid)
            self.refresh()

    def setupUi(self, riflesLi):
        super(RiflesLi, self).setupUi(self)
        self.setObjectName('riflesLi')

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
    errorSig = Signal(str)

    def __init__(self, parent=None, uid: int = None, rifle: 'RifleData' = None):
        super(EditRifleWidget, self).__init__(parent)
        self.setupUi(self)
        self.translate_ui()
        self.connectUi(self)
        self.uid = uid

        if rifle is not None:
            self.display_data(rifle)

    def translate_ui(self):
        self.name_box.setTitle(_translate("editRifleWidget", 'Rifle name'))
        self.props_box.setTitle(_translate("editRifleWidget", 'Properties'))
        self.reticle_box.setTitle(_translate("editRifleWidget", 'Reticle'))
        self.name_label.setText(_translate("editRifleWidget", 'Name'))
        self.name.setPlaceholderText(_translate("editRifleWidget", 'Name'))
        self.twist_dir.setItemText(0, _translate("editRifleWidget", 'Right'))
        self.twist_dir.setItemText(1, _translate("editRifleWidget", 'Left'))
        self.barrel_twist.prefix.setText(_translate("editRifleWidget", 'Barel Twist'))
        self.twist_dir.prefix.setText(_translate("editRifleWidget", 'Twist direction'))
        self.sight_height.prefix.setText(_translate("editRifleWidget", 'Sight height'))


    def setupUi(self, editRifleWidget):
        editRifleWidget.setObjectName("editRifleWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(editRifleWidget.sizePolicy().hasHeightForWidth())
        editRifleWidget.setSizePolicy(sizePolicy)
        editRifleWidget.setMinimumSize(QtCore.QSize(0, 0))

        self.name_box = QtWidgets.QGroupBox(self)
        self.props_box = QtWidgets.QGroupBox(self)
        self.reticle_box = QtWidgets.QGroupBox(self)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.vBoxLayout.setObjectName("vBoxLayout")
        self.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        self.name_boxLayout = QtWidgets.QFormLayout(self.name_box)
        self.name_boxLayout.setObjectName("name_boxLayout")

        self.props_boxLayout = QtWidgets.QVBoxLayout(self.props_box)
        self.props_boxLayout.setObjectName("props_boxLayout")

        self.name_label = QtWidgets.QLabel()
        self.name = QtWidgets.QLineEdit()

        barrel_twist = ConverSpinBox(self, 0.5)
        twist_dir = ComboBox(self, (
            ('Right', TwistDir.Right),
            ('Left', TwistDir.Left)
        ))
        sight_height = ConverSpinBox(self, 0.5)

        self.barrel_twist = FormRow3(barrel_twist)
        self.twist_dir = FormRow3(twist_dir)
        self.sight_height = FormRow3(sight_height)

        self.name_boxLayout.addRow(self.name_label, self.name)

        self.props_boxLayout.addWidget(self.barrel_twist)
        self.props_boxLayout.addWidget(self.twist_dir)
        self.props_boxLayout.addWidget(self.sight_height)

        self.vBoxLayout.addWidget(self.name_box)
        self.vBoxLayout.addWidget(self.props_box)
        self.vBoxLayout.addWidget(self.reticle_box)

        QtCore.QMetaObject.connectSlotsByName(editRifleWidget)

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
            rifle = RifleData(_translate('editRifleWidget', 'New Rifle'))
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
            self.errorSig.emit(_translate('editRifleWidget', 'Sight height must be > 0'))
        elif not self.barrel_twist.rawValue() > 0:
            self.barrel_twist.value_field.setFocus()
            self.errorSig.emit(_translate('editRifleWidget', 'Twist must be > 0'))
        else:
            return

        raise ValueError('Validation error')
