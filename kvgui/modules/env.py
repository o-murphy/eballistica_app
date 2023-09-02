import logging

from kivy.utils import platform
import os

__all__ = ['APP_DATA', 'STORAGE', 'USER_DATA', 'DB_PATH', 'SETTINGS_PATH', 'SS']


SS = None
ANDROID_PERMISSIONS = []


if platform == 'android':
    import logging
    from android import api_version
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path  #, secondary_external_storage_path
    from androidstorage4kivy import SharedStorage
    from kvgui.modules import signals as sig

    if api_version < 29:
        # Android < 10
        # Permission to write to Shared Storage
        ANDROID_PERMISSIONS = [Permission.WRITE_EXTERNAL_STORAGE]
    else:
        # Android >= 10
        # Permission required to see Shared files created by other apps
        ANDROID_PERMISSIONS = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]

    request_permissions(ANDROID_PERMISSIONS)

    primary_ext_storage = primary_external_storage_path()
    # secondary_ext_storage = secondary_external_storage_path()
    logging.info(f"Primary Storage: {primary_ext_storage}")
    # logging.info(f"Secondary Storage: {secondary_ext_storage}")

    SS = SharedStorage()
    logging.info(f'SharedStorage: {SS}')

    if SS:
        SS.copy_to_shared('test_shared.txt', filepath='test_shared.txt')

    try:
        sig.toast.emit(text=f'SharedStorage: {SS}')
    except Exception as exc:
        logging.exception(exc)
        logging.warning('SharedStorage toast exception')

    APP_DATA = '/data/data/o.murphy.eballistica'
    STORAGE = '/storage/emulated/0'
    #USER_DATA = '/storage/emulated/0/Android/data/o.murphy.eballistica/files'
    USER_DATA = '/storage/emulated/0/eballistica'
    #STORAGE = ''
elif platform == 'win':
    APP_DATA = os.path.join(os.environ['LocalAppData'], 'eBallistica')
    STORAGE = os.path.expanduser(r"~\documents")
    USER_DATA = os.path.expanduser(r"~\documents\eBallistica")
else:
    APP_DATA = os.path.expanduser(r"~/.eBallistica")
    STORAGE = os.path.expanduser(r"~/documents")
    USER_DATA = os.path.expanduser(r"~/documents\eBallistica")

#for dir in (APP_DATA, USER_DATA, STORAGE):
#    if not os.path.exists(dir):
#        try:
#            os.makedirs(dir, exist_ok=True)
#        except PermissionError as err:
#            logging.warning(err)
#            dir = APP_DATA

try:
    if not os.path.exists(APP_DATA):
        os.makedirs(dir, exist_ok=True)
    if not os.path.exists(USER_DATA):
        os.makedirs(dir, exist_ok=True)
    if not os.path.exists(STORAGE):
        os.makedirs(dir, exist_ok=True)
except PermissionError as err:
    logging.warning(err)
    USER_DATA = APP_DATA
    STORAGE = APP_DATA

DB_PATH = os.path.join(USER_DATA, 'local.sqlite3')
SETTINGS_PATH = os.path.join(USER_DATA, 'settings.json')

logging.info(f'APP_DATA: {APP_DATA}')
logging.info(f'STORAGE: {STORAGE}')
logging.info(f'USER_DATA: {USER_DATA}')
logging.info(f'DB_PATH: {DB_PATH}')
logging.info(f'SETTINGS_PATH: {SETTINGS_PATH}')
