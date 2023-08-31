import logging

from kivy.utils import platform
import os

__all__ = ['APP_DATA', 'STORAGE', 'USER_DATA', 'DB_PATH', 'SETTINGS_PATH']

if platform == 'android':
    import logging
    import android
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path, secondary_external_storage_path

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    primary_ext_storage = primary_external_storage_path()
    secondary_ext_storage = secondary_external_storage_path()
    logging.info(f'{type(primary_ext_storage)}')
    logging.info(f"Primary Storage: {primary_ext_storage}")
    logging.info(f"Secondary Storage: {secondary_ext_storage}")

    APP_DATA = '/data/data/o.murphy.eballistica'
    STORAGE = '/storage/emulated/0'
    # USER_DATA = '/storage/emulated/0/Android/data/o.murphy.eballistica/files'
    USER_DATA = '/storage/emulated/0/eballistica'
elif platform == 'win':
    APP_DATA = os.path.join(os.environ['LocalAppData'], 'eBallistica')
    STORAGE = os.path.expanduser(r"~\documents")
    USER_DATA = os.path.expanduser(r"~\documents\eBallistica")
else:
    APP_DATA = os.path.expanduser(r"~/.eBallistica")
    STORAGE = os.path.expanduser(r"~/documents")
    USER_DATA = os.path.expanduser(r"~/documents\eBallistica")

try:
    if not os.path.exists(APP_DATA):
        os.makedirs(APP_DATA, exist_ok=True)
    if not os.path.exists(STORAGE):
        os.makedirs(STORAGE, exist_ok=True)
    if not os.path.exists(USER_DATA):
        os.makedirs(USER_DATA, exist_ok=True)
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
