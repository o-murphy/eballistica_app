from getqt import *

from gui.app import App
import res_rc
assert res_rc
from qt_material import apply_stylesheet


extra_dark = {
    'primaryTextColor': '#FFFFFF'
}


def main(argv):
    app = QtWidgets.QApplication(argv)

    app.setWindowIcon(QtGui.QIcon('Icon.ico'))
    apply_stylesheet(app, extra={'primaryTextColor': '#FFFFFF'}, theme='dark_blue.xml')

    window = App()
    desktop = QtGui.QGuiApplication.screenAt(window.geometry().center())
    width, height = desktop.size().toTuple()

    if width > height:
        window.show()
    else:
        window.showFullScreen()

    app.exit(app.exec())


if __name__ == '__main__':
    import sys
    main(sys.argv)
