from kivy.lang import Builder

helper = """
<CDMEditor>

"""

Builder.load_file('kvgui/kv/dm_cdm_editor.kv')
Builder.load_string(helper)

from kivy.uix.screenmanager import Screen

from kvgui.components.mixines import MapIdsMixine


class CDMEditor(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(CDMEditor, self).__init__(**kwargs)
        self.name = 'cdm_editor_screen'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        ...

    def bind_ui(self):
        ...

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        self.translate_ui()

    def translate_ui(self):
        ...
