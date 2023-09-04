from kivy.utils import platform
import os
import logging
from __version__ import __version__

__all__ = ['APP_DATA', 'STORAGE', 'USER_DATA', 'DB_PATH', 'SETTINGS_PATH']

logging.info(f"App version:  {__version__}")

if platform == 'android':
    from android import api_version
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage, ShareSheet

    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()

    try:
        with open(os.path.join(primary_ext_storage, 'test_direct_file.txt'), 'w') as fp:
            fp.write("0")
    except Exception as exc:
        logging.warning('test_direct_file write error')

    if api_version < 29:
        # Android < 10
        # Permission to write to Shared Storage
        ANDROID_PERMISSIONS = [Permission.WRITE_EXTERNAL_STORAGE]
    else:
        # Android >= 10
        # Permission required to see Shared files created by other apps
        ANDROID_PERMISSIONS = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]

    request_permissions(ANDROID_PERMISSIONS)


    def use_test_ss():
        with open(f'version-{__version__}.txt', 'w') as txt:
            txt.write(__version__)
            SharedStorage().copy_to_shared(f'version-{__version__}.txt', filepath=f'version-{__version__}.txt')


    def create_test_uri():
        # create a file in Private storage
        cash_dir = SharedStorage().get_cache_dir()
        logging.info(f"SharedStorage Cache Dir: {cash_dir}")
        filename = os.path.join(cash_dir, 'test.html')
        with open(filename, "w") as f:
            f.write("<html>\n")
            f.write(" <head>\n")
            f.write(" </head>\n")
            f.write(" <body>\n")
            f.write("  <h1>All we are saying, is<h1>\n")
            f.write("  <h1>give bees a chance<h1>\n")
            f.write(" </body>\n")
            f.write("</html>\n")

        return SharedStorage().copy_to_shared(filename)


    def share_test_file():
        test_uri = create_test_uri()
        ShareSheet().share_file(test_uri)

    try:
        logging.info("trying get access to cache dir")
        cash_dir = SharedStorage().get_cache_dir()
        os.makedirs(os.path.join(cash_dir, 'test_dir'), exist_ok=True)
        logging.info("cache dir ok")
    except Exception as exc:
        logging.exception(exc)

    ANDROID_APP_DATA = '/data/data/o.murphy.eballistica'
    APP_DATA = '/data/data/o.murphy.eballistica/files'

    STORAGE = '/storage/emulated/0/Documents/eBallistica'
    USER_DATA = APP_DATA
    # STORAGE = '/storage/emulated/0'
    # USER_DATA = '/storage/emulated/0/Documents/eBallistica'
    # USER_DATA = '/storage/emulated/0/Android/data/o.murphy.eballistica/files'

elif platform == 'win':
    APP_DATA = os.path.join(os.environ['LocalAppData'], 'eBallistica')
    STORAGE = os.path.expanduser(r"~\documents")
    USER_DATA = os.path.expanduser(r"~\documents\eBallistica")
else:
    APP_DATA = os.path.expanduser(r"~/.eBallistica")
    STORAGE = os.path.expanduser(r"~/documents")
    USER_DATA = os.path.expanduser(r"~/documents\eBallistica")

for path in [APP_DATA, USER_DATA, STORAGE]:
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except PermissionError as err:
            logging.warning(err)

DB_PATH = os.path.join(APP_DATA, 'local.sqlite3')
SETTINGS_PATH = os.path.join(APP_DATA, 'settings.json')

logging.info(f'APP_DATA: {APP_DATA}')
logging.info(f'STORAGE: {STORAGE}')
logging.info(f'USER_DATA: {USER_DATA}')
logging.info(f'DB_PATH: {DB_PATH}')
logging.info(f'SETTINGS_PATH: {SETTINGS_PATH}')
