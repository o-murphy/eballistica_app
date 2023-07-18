from PySide6 import QtWidgets, QtCore, QtGui

from gui.app_logo import AppLogo, AppLabel


class BulletsDelegate(QtWidgets.QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        widget = index.data(QtCore.Qt.UserRole)
        if widget is not None:
            widget.setGeometry(QtCore.QRect(0, 0, size.width(), size.height()))
            size.setHeight(widget.sizeHint().height())
        return size


class BulletsLi(QtWidgets.QListWidget):
    edit_context_action = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(BulletsLi, self).__init__(parent)

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
                self.takeItem(uid)

    def setupUi(self, BulletsLi):
        self.menu = QtWidgets.QMenu()
        self.menu.addAction(self.edit_item)

    def store_bullet(self, uid, bullet):
        if uid is None:
            widget = BulletItemWidget()
            widget.set_data(bullet)
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            item.setData(0, self.count())
            self.addItem(item)
            self.setItemWidget(item, widget)
        else:
            item = self.item(uid)
            widget = self.itemWidget(item)
            widget.set_data(bullet)
            

class BulletsHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BulletsHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, bulletsHeader):
        bulletsHeader.setObjectName("bulletsHeader")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")

        self.logo = AppLogo()
        self.label = AppLabel()
        self.hBoxLayout.addWidget(self.logo)
        self.hBoxLayout.addWidget(self.label)

        bulletsHeader.setObjectName("bulletsHeader")
        self.addButton = QtWidgets.QPushButton('+')

        self.hBoxLayout.addWidget(self.addButton)

        self.retranslateUi(bulletsHeader)
        QtCore.QMetaObject.connectSlotsByName(bulletsHeader)

    def retranslateUi(self, bulletsHeader: 'BulletsHeader'):
        _translate = QtCore.QCoreApplication.translate
        bulletsHeader.setWindowTitle(_translate("bulletsHeader", "Form"))
        bulletsHeader.addButton.setText(_translate("bulletsHeader", "+"))


class BulletsWidget(QtWidgets.QWidget):
    bullet_clicked_sig = QtCore.Signal(object, object)
    bullet_double_clicked_sig = QtCore.Signal(object, object)

    def __init__(self, parent=None):
        super(BulletsWidget, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)

    def setupUi(self, bulletsWidget):
        bulletsWidget.setObjectName("bulletsWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(bulletsWidget.sizePolicy().hasHeightForWidth())
        bulletsWidget.setSizePolicy(sizePolicy)
        bulletsWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.vBoxLayout = QtWidgets.QVBoxLayout(bulletsWidget)
        self.vBoxLayout.setObjectName("vBoxLayout")
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.header = BulletsHeader(self)
        self.bullets_list = BulletsLi(self)
        self.vBoxLayout.addWidget(self.header)
        self.vBoxLayout.addWidget(self.bullets_list)
        self.vBoxLayout.addWidget(BulletItemWidget())

        self.retranslateUi(bulletsWidget)
        QtCore.QMetaObject.connectSlotsByName(bulletsWidget)

    def retranslateUi(self, bulletsWidget: 'BulletsWidget'):
        _translate = QtCore.QCoreApplication.translate
        bulletsWidget.setWindowTitle(_translate("bulletsWidget", "Form"))

    def connectUi(self, bulletsWidget: 'BulletsWidget'):
        self.bullets_list.itemDoubleClicked.connect(self.bullet_double_clicked)
        self.bullets_list.itemClicked.connect(self.bullet_clicked)
        self.bullets_list.edit_context_action.connect(self.bullet_double_clicked)

    def bullet_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: BulletItemWidget = self.bullets_list.itemWidget(item)
        self.bullet_clicked_sig.emit(self.bullets_list.indexFromItem(item).row(), widget.bullet_data)

    def bullet_double_clicked(self, item: QtWidgets.QListWidgetItem):
        widget: BulletItemWidget = self.bullets_list.itemWidget(item)
        self.bullet_double_clicked_sig.emit(self.bullets_list.indexFromItem(item).row(), widget.bullet_data)
        

class AddBulletHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AddBulletHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, editBulletWidgetHeader):
        editBulletWidgetHeader.setObjectName("editBulletWidgetHeader")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")

        self.logo = AppLogo()
        self.label = AppLabel()
        self.hBoxLayout.addWidget(self.logo)
        self.hBoxLayout.addWidget(self.label)

        editBulletWidgetHeader.setObjectName("editBulletWidgetHeader")
        self.okButton = QtWidgets.QPushButton('Ok')

        self.hBoxLayout.addWidget(self.okButton)

        self.retranslateUi(editBulletWidgetHeader)
        QtCore.QMetaObject.connectSlotsByName(editBulletWidgetHeader)

    def retranslateUi(self, editBulletWidgetHeader: 'AddBulletHeader'):
        _translate = QtCore.QCoreApplication.translate
        editBulletWidgetHeader.setWindowTitle(_translate("editBulletWidgetHeader", "Form"))
        editBulletWidgetHeader.okButton.setText(_translate("editBulletWidgetHeader", "Ok"))
        # editBulletWidgetHeader.menuButton.setText(_translate("editBulletWidgetHeader", "..."))
        
        
class EditBulletWidget(QtWidgets.QWidget):
    ok_clicked = QtCore.Signal(object, object)

    def __init__(self, parent=None, uid: int = None, data: BulletData = None):
        super(EditBulletWidget, self).__init__(parent)
        self.setupUi(self)
        self.connectUi(self)
        self.uid = uid

        if data is not None:
            self.set_data(data)

    def setupUi(self, editBulletWidget):
        editBulletWidget.setObjectName("editBulletWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(editBulletWidget.sizePolicy().hasHeightForWidth())
        editBulletWidget.setSizePolicy(sizePolicy)
        editBulletWidget.setMinimumSize(QtCore.QSize(0, 0))

        self.header = AddBulletHeader(self)




        self.retranslateUi(editBulletWidget)
        QtCore.QMetaObject.connectSlotsByName(editBulletWidget)
        
    def retranslateUi(self, editBulletWidget: 'EditBulletWidget'):
        _translate = QtCore.QCoreApplication.translate
        editBulletWidget.setWindowTitle(_translate("editBulletWidget", "Form"))

    def connectUi(self, editBulletWidget):
        self.header.okButton.clicked.connect(self.save_bullet)

    def set_data(self, bullet: BulletData, uid=None):
        self.uid = uid
        if bullet:
            self.name.setText(bullet.name)

    def save_bullet(self):
        bullet_data = BulletData(
            self.name.text(),
        )
        self.ok_clicked.emit(self.uid, bullet_data)
