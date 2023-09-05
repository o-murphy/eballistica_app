from kivy.lang import Builder
import os


def _load_kv():
    for root, dirs, files in os.walk('kvgui/kv'):
        for file_name in files:
            if file_name.endswith('.kv'):
                Builder.load_file(os.path.join(root, file_name))


_load_kv()
