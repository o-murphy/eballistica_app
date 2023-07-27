from PySide6 import QtWidgets, QtCore, QtGui
from gui.settings import Convertor, SettingsWidget

# from datatypes.datatypes import RifleData
from datatypes.dbworker import Worker, TwistDir, RifleData
from units import Distance
from .app_logo import AppLogo, AppLabel
from .widgets import FormRow3, SpinBox, ComboBox, ConverSpinBox


# class RifleItemWidget(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(RifleItemWidget, self).__init__(parent)
#         self.setupUi(self)
#         self.rifle_data = None
#
#     def setupUi(self, rifleItemWidget):
#         rifleItemWidget.setObjectName("rifleItemWidget")
#
#         self.box = QtWidgets.QGroupBox('', self)
#
#         self.gridLayout = QtWidgets.QGridLayout(self)
#         self.gridLayout.setObjectName("gridLayout")
#         self.gridLayout.setContentsMargins(0, 0, 0, 0)
#
#         self.gridLayout.addWidget(self.box)
#
#         self.boxLayout = QtWidgets.QGridLayout(self.box)
#
#         self.boxLayout.setObjectName("boxLayout")
#
#         # self.name = QtWidgets.QLabel()
#         self.barrel = QtWidgets.QLabel()
#         self.sight = QtWidgets.QLabel()
#
#         # self.gridLayout.addWidget(self.name)
#         self.boxLayout.addWidget(self.barrel)
#         self.boxLayout.addWidget(self.sight)

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
        ofs = Distance(rifle.sight_offset, Distance.Centimeter).convert(settings.shUnits.currentData())

        self.rifle_data = rifle
        # self.box.setTitle(self.rifle_data.name)
        self.setTitle(self.rifle_data.name)
        self.barrel.setText(f'Barrel: 1 in {twist}')
        self.sight.setText(f'Sight Ht/Ofs: {sh}/{ofs}')

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        print(window.objectName())
        if window:
            settings: SettingsWidget = window.settings
            return settings



# class RiflesDelegate(QtWidgets.QStyledItemDelegate):
#
#     def sizeHint(self, option, index):
#         size = super().sizeHint(option, index)
#         widget = index.data(QtCore.Qt.UserRole)
#         if widget is not None:
#             widget.setGeometry(QtCore.QRect(0, 0, size.width(), size.height()))
#             size.setHeight(widget.sizeHint().height())
#         return size


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
#
#
# class RiflesWidget(QtWidgets.QWidget):
#     rifle_clicked_sig = QtCore.Signal(object)
#     rifle_edit_sig = QtCore.Signal(object)
#
#     def __init__(self, parent=None):
#         super(RiflesWidget, self).__init__(parent)
#         self.setupUi(self)
#         self.connectUi(self)
#
#     def setupUi(self, riflesWidget):
#         riflesWidget.setObjectName("riflesWidget")
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(riflesWidget.sizePolicy().hasHeightForWidth())
#         riflesWidget.setSizePolicy(sizePolicy)
#         riflesWidget.setMinimumSize(QtCore.QSize(0, 0))
#         self.vBoxLayout = QtWidgets.QVBoxLayout(riflesWidget)
#         self.vBoxLayout.setObjectName("vBoxLayout")
#         self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
#
#         # self.header = RiflesHeader(self)
#         self.rifles_list = RiflesLi(self)
#         # self.vBoxLayout.addWidget(self.header)
#         self.vBoxLayout.addWidget(self.rifles_list)
#
#         self.retranslateUi(riflesWidget)
#         QtCore.QMetaObject.connectSlotsByName(riflesWidget)

    def retranslateUi(self, riflesWidget: 'RiflesWidget'):
        _translate = QtCore.QCoreApplication.translate
        riflesWidget.setWindowTitle(_translate("riflesWidget", "Form"))

    def connectUi(self, riflesWidget: 'RiflesWidget'):
        # self.rifles_list.itemDoubleClicked.connect(self.rifle_edit_clicked)
        # self.rifles_list.itemClicked.connect(self.rifle_clicked)
        self.itemClicked.connect(self.rifle_clicked)
        # self.rifles_list.edit_context_action.connect(self.rifle_edit_clicked)
        self.edit_context_action.connect(self.rifle_edit_clicked)

    def rifle_clicked(self, item: QtWidgets.QListWidgetItem):
        # widget: RifleItemWidget = self.rifles_list.itemWidget(item)
        print('clicked')
        widget: RifleItemWidget = self.itemWidget(item)
        self.rifle_clicked_sig.emit(widget.rifle_data)

    def rifle_edit_clicked(self, item: QtWidgets.QListWidgetItem):
        # widget: RifleItemWidget = self.rifles_list.itemWidget(item)
        widget: RifleItemWidget = self.itemWidget(item)
        print(widget)
        self.rifle_edit_sig.emit(widget.rifle_data)


class EditRifleWidget(QtWidgets.QWidget):
    # ok_clicked = QtCore.Signal()

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

        # self.barrel_twist = FormSpinBox(self, 0.01, 20, 0.5, 'in', 'Barel Twist')

        barrel_twist = ConverSpinBox(self, 0.01, 1000, 0.5, 2)
        twist_dir = ComboBox(self, (('Right', TwistDir.Right), ('Left', TwistDir.Left)))
        sight_height = ConverSpinBox(self, 0.01, 1000, 0.5)
        sight_offset = ConverSpinBox(self, 0.01, 1000, 1)

        self.barrel_twist = FormRow3(barrel_twist, 'Barel Twist', 'in')
        self.barrel_twist.setObjectName('barrel_twist')
        self.twist_dir = FormRow3(twist_dir, 'Twist direction')
        self.sight_height = FormRow3(sight_height, 'Sight height', 'mm')
        self.sight_height.setObjectName('sight_height')
        self.sight_offset = FormRow3(sight_offset, 'Sight offset', 'mm')
        self.sight_offset.setObjectName('sight_offset')

        # self.sight_height = FormSpinBox(self, 1, 100, 0.5, 'mm', 'Sight height')
        # self.sight_offset = FormSpinBox(self, 1, 500, 1, 'mm', 'Sight offset')

        self.name_boxLayout.addRow(self.name_label, self.name)

        self.props_boxLayout.addWidget(self.barrel_twist)
        self.props_boxLayout.addWidget(self.twist_dir)
        self.props_boxLayout.addWidget(self.sight_height)
        self.props_boxLayout.addWidget(self.sight_offset)

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
        self.barrel_twist.suffix.setText(Distance.name(settings.twistUnits.currentData()))
        self.barrel_twist.setDecimals(Distance.accuracy(settings.twistUnits.currentData()))

        self.sight_height.setConvertor(Convertor(Distance, settings.shUnits.currentData(), Distance.Centimeter))
        self.sight_height.suffix.setText(Distance.name(settings.shUnits.currentData()))
        self.sight_height.setDecimals(Distance.accuracy(settings.shUnits.currentData()))

        self.sight_offset.setConvertor(Convertor(Distance, settings.shUnits.currentData(), Distance.Centimeter))
        self.sight_offset.suffix.setText(Distance.name(settings.shUnits.currentData()))
        self.sight_offset.setDecimals(Distance.accuracy(settings.shUnits.currentData()))

    def display_data(self, rifle: 'RifleData'):
        if not rifle:
            rifle = RifleData('New Rifle')
        self.uid = rifle.id
        self.name.setText(rifle.name)
        self.barrel_twist.setRawValue(rifle.barrel_twist)
        index = self.twist_dir.findData(rifle.barrel_twist_dir)
        self.twist_dir.setCurrentIndex(index)
        self.sight_height.setRawValue(rifle.sight_height)
        self.sight_offset.setRawValue(rifle.sight_offset)

    def save_rifle(self):
        Worker.rifle_add_or_update(
            id=self.uid,
            name=self.name.text() if self.name.text() else self.name.placeholderText(),
            barrel_twist=self.barrel_twist.rawValue(),
            barrel_twist_dir=self.twist_dir.currentData(),
            sight_height=self.sight_height.rawValue(),
            sight_offset=self.sight_offset.rawValue(),
        )
        # self.ok_clicked.emit()
