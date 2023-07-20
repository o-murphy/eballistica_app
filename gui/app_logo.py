from PySide6 import QtWidgets, QtGui, QtCore


class AppLogo(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(AppLogo, self).__init__(parent)
        pixmap = QtGui.QPixmap("Icon.png")
        desired_size = pixmap.size().scaled(32, 32, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        scaled_pixmap = pixmap.scaled(desired_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(scaled_pixmap)


class AppLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(AppLabel, self).__init__(parent)
        self.setText("eBallistica")


class AppHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AppHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, appToolBar):
        appToolBar.setObjectName("appToolBar")

        self.hBoxLayout = QtWidgets.QHBoxLayout(self)
        self.hBoxLayout.setObjectName("hBoxLayout")
        
        self.logo = AppLogo()
        self.label = AppLabel()
        self.hBoxLayout.addWidget(self.logo)
        self.hBoxLayout.addWidget(self.label)

    def retranslateUi(self, riflesHeader: 'appHeader'):
        _translate = QtCore.QCoreApplication.translate
        riflesHeader.setWindowTitle(_translate("riflesHeader", "Form"))

