from PySide6 import QtWidgets, QtCore

from datatypes.rifle import RifleData
from .app_logo import AppLogo, AppLabel


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
    def __init__(self, parent=None):
        super(RiflesLi, self).__init__(parent)

    def store_rifle(self, rifle):
        widget = RifleItemWidget()
        widget.set_data(rifle)
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)


class RiflesHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RiflesHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, riflesHeader):
        riflesHeader.setObjectName("riflesHeader")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")

        self.logo = AppLogo()
        self.label = AppLabel()
        self.hBoxLayout.addWidget(self.logo)
        self.hBoxLayout.addWidget(self.label)

        riflesHeader.setObjectName("riflesHeader")
        self.addButton = QtWidgets.QPushButton('+')
        self.menuButton = QtWidgets.QPushButton('...')

        self.hBoxLayout.addWidget(self.addButton)
        self.hBoxLayout.addWidget(self.menuButton)

        self.retranslateUi(riflesHeader)
        QtCore.QMetaObject.connectSlotsByName(riflesHeader)

    def retranslateUi(self, riflesHeader: 'RiflesHeader'):
        _translate = QtCore.QCoreApplication.translate
        riflesHeader.setWindowTitle(_translate("riflesHeader", "Form"))
        riflesHeader.addButton.setText(_translate("riflesHeader", "+"))
        riflesHeader.menuButton.setText(_translate("riflesHeader", "..."))


class RiflesWidget(QtWidgets.QWidget):
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

        self.header = RiflesHeader(self)
        self.rifles_list = RiflesLi(self)
        self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.rifles_list)
        self.vBoxLayout.addWidget(RifleItemWidget())

        self.retranslateUi(riflesWidget)
        QtCore.QMetaObject.connectSlotsByName(riflesWidget)

    def retranslateUi(self, riflesWidget: 'RiflesWidget'):
        _translate = QtCore.QCoreApplication.translate
        riflesWidget.setWindowTitle(_translate("riflesWidget", "Form"))

    def connectUi(self, riflesWidget: 'RiflesWidget'):
        self.rifles_list.itemDoubleClicked.connect(self.rifle_double_clicked)

    def rifle_double_clicked(self, item: QtWidgets.QListWidgetItem):
        widget = self.rifles_list.itemWidget(item)
        self.rifle_double_clicked_sig.emit(widget.rifle_data)


class FirearmProps(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FirearmProps, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, firearmProps):
        firearmProps.setObjectName("firearmProps")

    def retranslateUi(self, firearmProps):
        _translate = QtCore.QCoreApplication.translate
        firearmProps.setWindowTitle(_translate("firearmProps", "Form"))


class AddRifleHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AddRifleHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, addRifleHeader):
        addRifleHeader.setObjectName("addRifleHeader")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")

        self.logo = AppLogo()
        self.label = AppLabel()
        self.hBoxLayout.addWidget(self.logo)
        self.hBoxLayout.addWidget(self.label)

        addRifleHeader.setObjectName("addRifleHeader")
        self.okButton = QtWidgets.QPushButton('Ok')

        self.hBoxLayout.addWidget(self.okButton)

        self.retranslateUi(addRifleHeader)
        QtCore.QMetaObject.connectSlotsByName(addRifleHeader)

    def retranslateUi(self, addRifleHeader: 'AddRifleHeader'):
        _translate = QtCore.QCoreApplication.translate
        addRifleHeader.setWindowTitle(_translate("addRifleHeader", "Form"))
        addRifleHeader.okButton.setText(_translate("addRifleHeader", "Ok"))
        # addRifleHeader.menuButton.setText(_translate("addRifleHeader", "..."))


class AddRifle(QtWidgets.QWidget):
    ok_clicked = QtCore.Signal(object)

    def __init__(self, parent=None):
        print(parent)
        super(AddRifle, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)

    def setupUi(self, addRifle):
        addRifle.setObjectName("addRifle")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(addRifle.sizePolicy().hasHeightForWidth())
        addRifle.setSizePolicy(sizePolicy)
        addRifle.setMinimumSize(QtCore.QSize(0, 0))

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

        self.props_boxLayout = QtWidgets.QFormLayout(self.props_box)
        self.props_boxLayout.setObjectName("props_boxLayout")

        self.name_label = QtWidgets.QLabel('Name')
        self.barrel_twist_label = QtWidgets.QLabel('Barel Twist')
        self.barrel_twist_dir_label = QtWidgets.QLabel('Twist direction')
        self.sight_height_label = QtWidgets.QLabel('Sight Height')
        self.sight_offset_label = QtWidgets.QLabel('Sight Offset')
        
        self.name = QtWidgets.QLineEdit('Template')
        self.barrel_twist = QtWidgets.QDoubleSpinBox()
        self.barrel_twist_dir = QtWidgets.QComboBox()
        self.sight_height = QtWidgets.QDoubleSpinBox()
        self.sight_offset = QtWidgets.QDoubleSpinBox()

        self.name_boxLayout.addRow(self.name_label, self.name)
        self.props_boxLayout.addRow(self.barrel_twist_label, self.barrel_twist)
        self.props_boxLayout.addRow(self.barrel_twist_dir_label, self.barrel_twist_dir)
        self.props_boxLayout.addRow(self.sight_height_label, self.sight_height)
        self.props_boxLayout.addRow(self.sight_offset_label, self.sight_offset)

        self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.name_box)
        self.vBoxLayout.addWidget(self.props_box)
        self.vBoxLayout.addWidget(self.reticle_box)

        self.retranslateUi(addRifle)
        QtCore.QMetaObject.connectSlotsByName(addRifle)

    def retranslateUi(self, addRifle: 'AddRifle'):
        _translate = QtCore.QCoreApplication.translate
        addRifle.setWindowTitle(_translate("addRifle", "Form"))

    def connectUi(self, addRifle):
        self.header.okButton.clicked.connect(self.save_rifle)

    def save_rifle(self):
        rifle_data = RifleData(
            self.name.text(),
            self.barrel_twist.value(),
            self.barrel_twist_dir.currentData(),
            self.sight_height.value(),
            self.sight_offset.value()
        )
        self.ok_clicked.emit(rifle_data)

