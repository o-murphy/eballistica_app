import logging

from kivy.utils import platform
import os

__all__ = ['APP_DATA', 'STORAGE', 'USER_DATA']

if platform == 'android':
    APP_DATA = '/data/data/o.murphy.eballistica'
    STORAGE = '/storage/emulated/0'
    USER_DATA = '/storage/emulated/0/Android/data/o.murphy.eballistica/files'
elif platform == 'win':
    APP_DATA = os.path.join(os.environ['LocalAppData'], 'eBallistica')
    STORAGE = os.path.expanduser(r"~\documents")
    USER_DATA = os.path.expanduser(r"~\documents\eBallistica")
else:
    APP_DATA = os.path.expanduser(r"~/.eBallistica")
    STORAGE = os.path.expanduser(r"~/documents")
    USER_DATA = os.path.expanduser(r"~/documents\eBallistica")


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
