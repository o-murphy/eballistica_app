import sys

from PySide6 import QtGui, QtWidgets

from gui.app import App
from gui.stylesheet import main_app_qss
import res_rc
assert res_rc


def main(argv):
    app = QtWidgets.QApplication(argv)

    app.setWindowIcon(QtGui.QIcon('Icon.ico'))
    app.setStyleSheet(main_app_qss())

    window = App()
    desktop = QtGui.QGuiApplication.screenAt(window.geometry().center())
    width, height = desktop.size().toTuple()

    if width > height:
        window.show()
    else:
        window.showFullScreen()

    app.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv)
