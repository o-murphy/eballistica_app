from getqt import *
from gui.widgets import Label


class AppLogo(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(AppLogo, self).__init__(parent)
        pixmap = QtGui.QPixmap("Icon.png")
        desired_size = pixmap.size().scaled(32, 32, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        scaled_pixmap = pixmap.scaled(desired_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(scaled_pixmap)


class AppLabel(Label):
    def __init__(self, parent=None):
        super(AppLabel, self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.setText("eBallistica")
        self.set_bold()


class AppHeader(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AppHeader, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, appToolBar):
        appToolBar.setObjectName("appToolBar")

        self.gLayout = QtWidgets.QGridLayout(self)
        self.gLayout.setObjectName("hBoxLayout")
        
        self.logo = AppLogo()
        self.title = AppLabel()
        self.bread = QtWidgets.QLabel()

        self.gLayout.setColumnStretch(0, 2)
        self.gLayout.setColumnStretch(1, 8)
        self.gLayout.addWidget(self.logo, 0, 0, 2, 1)
        self.gLayout.addWidget(self.title, 0, 1, 1, 1)
        self.gLayout.addWidget(self.bread, 1, 1, 1, 1)

    def retranslateUi(self, riflesHeader: 'appHeader'):
        _translate = QtCore.QCoreApplication.translate

