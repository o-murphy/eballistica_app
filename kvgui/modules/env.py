import logging

from kivy.utils import platform
import os

__all__ = ['APP_DATA', 'STORAGE', 'USER_DATA']


ANDROID_APP_DATA = '/data/data/o.murphy.eballistica'
ANDROID_STORAGE = '/storage/emulated/0'
ANDROID_USER_DATA = '/storage/emulated/0/Android/data/o.murphy.eballistica/files'

WINDOWS_APP_DATA = os.path.join(os.environ['LocalAppData'], 'eBallistica')
WINDOWS_STORAGE = os.path.expanduser("~\documents")
WINDOWS_USER_DATA = os.path.expanduser("~\documents\eBallistica")

UNIX_APP_DATA = os.path.expanduser("~\.eBallistica")
UNIX_STORAGE = os.path.expanduser("~\documents")
UNIX_USER_DATA = os.path.expanduser("~\documents\eBallistica")


if platform == 'android':
    APP_DATA = ANDROID_APP_DATA
    STORAGE = ANDROID_STORAGE
    USER_DATA = ANDROID_USER_DATA
elif platform == 'win':
    APP_DATA = WINDOWS_APP_DATA
    STORAGE = WINDOWS_STORAGE
    USER_DATA = WINDOWS_USER_DATA
else:
    APP_DATA = UNIX_APP_DATA
    STORAGE = UNIX_STORAGE
    USER_DATA = UNIX_USER_DATA


if not os.path.exists(APP_DATA):
    os.mkdir(APP_DATA)
if not os.path.exists(STORAGE):
    os.mkdir(STORAGE)
if not os.path.exists(USER_DATA):
    os.mkdir(USER_DATA)

DB_PATH = os.path.join(USER_DATA, 'local.sqlite3')
SETTINGS_PATH = os.path.join(USER_DATA, 'settings.json')

logging.info(f'APP_DATA: {APP_DATA}')
logging.info(f'STORAGE: {STORAGE}')
logging.info(f'USER_DATA: {USER_DATA}')
logging.info(f'DB_PATH: {DB_PATH}')
logging.info(f'SETTINGS_PATH: {SETTINGS_PATH}')
