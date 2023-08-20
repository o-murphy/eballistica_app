# from kvgui.app import EBallisticaApp
__version__ = '0.0.5'


# def main(argv):
#     EBallisticaApp().run()

from datatypes.dbworker import *


def main(argv):
    Worker.list_rifles()


if __name__ == '__main__':
    import sys
    main(sys.argv)
