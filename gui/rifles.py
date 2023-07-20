from PySide6 import QtWidgets, QtCore, QtGui

# from datatypes.datatypes import RifleData
from datatypes.dbworker import Worker, TwistDir, RifleData
from .app_logo import AppLogo, AppLabel
from .widgets import FormSpinBox, FormCheckBox, FormComboBox


class RifleItemWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RifleItemWidget, self).__init__(parent)
        self.setupUi(self)
        self.rifle_data = None

    def setupUi(self, rifleItemWidget):
        rifleItemWidget.setObjectName("rifleItemWidget")

        self.box = QtWidgets.QGroupBox('', self)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.box)

        self.boxLayout = QtWidgets.QGridLayout(self.box)
        self.boxLayout.setObjectName("boxLayout")

        # self.name = QtWidgets.QLabel()
        self.barrel = QtWidgets.QLabel()
        self.sight = QtWidgets.QLabel()

        # self.gridLayout.addWidget(self.name)
        self.boxLayout.addWidget(self.barrel)
        self.boxLayout.addWidget(self.sight)

    def translateUi(self, rifleItemWidget):
        ...

    def set_data(self, rifle):
        self.rifle_data = rifle
        self.box.setTitle(self.rifle_data.name)
        self.barrel.setText(f'Barrel: 1 in {rifle.barrel_twist}"')
        self.sight.setText(f'Sight Ht/Ofs: {rifle.sight_height}/{rifle.sight_offset}"')


class RiflesDelegate(QtWidgets.QStyledItemDelegate):

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        widget = index.data(QtCore.Qt.UserRole)
        if widget is not None:
            widget.setGeometry(QtCore.QRect(0, 0, size.width(), size.height()))
            size.setHeight(widget.sizeHint().height())
        return size


class RiflesLi(QtWidgets.QListWidget):
    edit_context_action = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(RiflesLi, self).__init__(parent)
        self.setupUi(self)
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
        print(self.findChildren(QtWidgets.QWidget))


    def create_item(self, rifle):
        widget = RifleItemWidget()
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

    # def store_rifle(self, uid, rifle):
    #     if uid is None:
    #         widget = RifleItemWidget()
    #         widget.display_data(rifle)
    #         item = QtWidgets.QListWidgetItem()
    #         item.setSizeHint(widget.sizeHint())
    #         item.setData(0, self.count())
    #         self.addItem(item)
    #         self.setItemWidget(item, widget)
    #     else:
    #         item = self.item(uid)
    #         widget = self.itemWidget(item)
    #         widget.display_data(rifle)


# class RiflesHeader(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(RiflesHeader, self).__init__(parent)
#         self.setupUi(self)
#
#     def setupUi(self, riflesHeader):
#         riflesHeader.setObjectName("riflesHeader")
#
#         self.hBoxLayout = QtWidgets.QHBoxLayout(self)
#         self.hBoxLayout.setObjectName("hBoxLayout")
#
#         self.logo = AppLogo()
#         self.label = AppLabel()
#         self.hBoxLayout.addWidget(self.logo)
#         self.hBoxLayout.addWidget(self.label)
#
#         riflesHeader.setObjectName("riflesHeader")
#         self.addButton = QtWidgets.QPushButton('+')
#         # self.menuButton = QtWidgets.QPushButton('...')
#
#         self.hBoxLayout.addWidget(self.addButton)
#         # self.hBoxLayout.addWidget(self.menuButton)
#
#         self.retranslateUi(riflesHeader)
#         QtCore.QMetaObject.connectSlotsByName(riflesHeader)
#
#     def retranslateUi(self, riflesHeader: 'RiflesHeader'):
#         _translate = QtCore.QCoreApplication.translate
#         riflesHeader.setWindowTitle(_translate("riflesHeader", "Form"))
#         riflesHeader.addButton.setText(_translate("riflesHeader", "+"))
#         # riflesHeader.menuButton.setText(_translate("riflesHeader", "..."))


class RiflesWidget(QtWidgets.QWidget):
    rifle_clicked_sig = QtCore.Signal(object)
    rifle_double_clicked_sig = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(RiflesWidget, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)

    def setupUi(self, riflesWidget):
        riflesWidget.setObjectName("riflesWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(riflesWidget.sizePolicy().hasHeightForWidth())
        riflesWidget.setSizePolicy(sizePolicy)
        riflesWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.vBoxLayout = QtWidgets.QVBoxLayout(riflesWidget)
        self.vBoxLayout.setObjectName("vBoxLayout")
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        # self.header = RiflesHeader(self)
        self.rifles_list = RiflesLi(self)
        # self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.rifles_list)

        self.retranslateUi(riflesWidget)
        QtCore.QMetaObject.connectSlotsByName(riflesWidget)

    def retranslateUi(self, riflesWidget: 'RiflesWidget'):
        _translate = QtCore.QCoreApplication.translate
        riflesWidget.setWindowTitle(_translate("riflesWidget", "Form"))

    def connectUi(self, riflesWidget: 'RiflesWidget'):
        self.rifles_list.itemDoubleClicked.connect(self.rifle_double_clicked)
        self.rifles_list.itemClicked.connect(self.rifle_clicked)
        self.rifles_list.edit_context_action.connect(self.rifle_double_clicked)

    def rifle_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: RifleItemWidget = self.rifles_list.itemWidget(item)
        self.rifle_clicked_sig.emit(widget.rifle_data)

    def rifle_double_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: RifleItemWidget = self.rifles_list.itemWidget(item)
        self.rifle_double_clicked_sig.emit(widget.rifle_data)


class AddRifleHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AddRifleHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, editRifleWidgetHeader):
        editRifleWidgetHeader.setObjectName("editRifleWidgetHeader")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")

        # self.logo = AppLogo()
        # self.label = AppLabel()
        # self.hBoxLayout.addWidget(self.logo)
        # self.hBoxLayout.addWidget(self.label)

        editRifleWidgetHeader.setObjectName("editRifleWidgetHeader")
        self.okButton = QtWidgets.QPushButton('Ok')
        self.okButton.setShortcut(QtGui.QKeySequence('Ctrl+S'))
        self.okButton.setProperty('class', 'success')

        self.hBoxLayout.addWidget(self.okButton)

        self.retranslateUi(editRifleWidgetHeader)
        QtCore.QMetaObject.connectSlotsByName(editRifleWidgetHeader)

    def retranslateUi(self, editRifleWidgetHeader: 'AddRifleHeader'):
        _translate = QtCore.QCoreApplication.translate
        editRifleWidgetHeader.setWindowTitle(_translate("editRifleWidgetHeader", "Form"))
        editRifleWidgetHeader.okButton.setText(_translate("editRifleWidgetHeader", "Ok"))
        # editRifleWidgetHeader.menuButton.setText(_translate("editRifleWidgetHeader", "..."))


class EditRifleWidget(QtWidgets.QWidget):
    ok_clicked = QtCore.Signal()

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

        self.header = AddRifleHeader(self)

        self.name_box = QtWidgets.QGroupBox('Rifle name', self)
        self.props_box = QtWidgets.QGroupBox('Properties', self)
        self.reticle_box = QtWidgets.QGroupBox('Reticle', self)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.vBoxLayout.setObjectName("vBoxLayout")
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        self.name_boxLayout = QtWidgets.QFormLayout(self.name_box)
        self.name_boxLayout.setObjectName("name_boxLayout")

        self.props_boxLayout = QtWidgets.QVBoxLayout(self.props_box)
        self.props_boxLayout.setObjectName("props_boxLayout")

        self.name_label = QtWidgets.QLabel('Name')
        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText('Name')

        self.barrel_twist = FormSpinBox(self, 0.01, 20, 0.5, 'in', 'Barel Twist')
        self.barrel_twist_dir = FormComboBox(self, prefix='Twist direction')
        self.barrel_twist_dir.addItem('Right', TwistDir.Right)
        self.barrel_twist_dir.addItem('Left', TwistDir.Left)

        self.sight_height = FormSpinBox(self, 1, 100, 0.5, 'mm', 'Sight height')
        self.sight_offset = FormSpinBox(self, 1, 500, 1, 'mm', 'Sight offset')

        self.name_boxLayout.addRow(self.name_label, self.name)

        self.props_boxLayout.addWidget(self.barrel_twist)
        self.props_boxLayout.addWidget(self.barrel_twist_dir)
        self.props_boxLayout.addWidget(self.sight_height)
        self.props_boxLayout.addWidget(self.sight_offset)

        self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.name_box)
        self.vBoxLayout.addWidget(self.props_box)
        self.vBoxLayout.addWidget(self.reticle_box)

        self.retranslateUi(editRifleWidget)
        QtCore.QMetaObject.connectSlotsByName(editRifleWidget)

    def retranslateUi(self, editRifleWidget: 'EditRifleWidget'):
        _translate = QtCore.QCoreApplication.translate
        editRifleWidget.setWindowTitle(_translate("editRifleWidget", "Form"))

    def connectUi(self, editRifleWidget):
        self.header.okButton.clicked.connect(self.save_rifle)

    def display_data(self, rifle: 'RifleData'):
        if not rifle:
            rifle = RifleData('New Rifle')
        print(rifle.barrel_twist)
        self.uid = rifle.id
        self.name.setText(rifle.name)
        self.barrel_twist.setValue(rifle.barrel_twist)
        index = self.barrel_twist_dir.findData(rifle.barrel_twist_dir)
        self.barrel_twist_dir.setCurrentIndex(index)
        self.sight_height.setValue(rifle.sight_height)
        self.sight_offset.setValue(rifle.sight_offset)

    def save_rifle(self):
        print(self.sender())
        Worker.rifle_add_or_update(
            id=self.uid,
            name=self.name.text() if self.name.text() else self.name.placeholderText(),
            barrel_twist=self.barrel_twist.value(),
            barrel_twist_dir=self.barrel_twist_dir.currentData(),
            sight_height=self.sight_height.value(),
            sight_offset=self.sight_offset.value(),
        )
        self.ok_clicked.emit()
