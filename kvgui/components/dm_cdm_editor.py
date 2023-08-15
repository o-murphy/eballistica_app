from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from kvgui.components.abstract import FormLabel
from kvgui.components.measure_widgets import MachValue, CDValue

from kvgui.components.mixines import MapIdsMixine
from kvgui.modules.translator import translate as tr

helper = """
<CDMEditor>

"""

Builder.load_file('kvgui/kv/dm_cdm_editor.kv')


class MachCdPair(MDBoxLayout, MapIdsMixine):
    def __init__(self, **kwargs):
        super(MachCdPair, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(MachCdPair, self).init_ui()

    def bind_ui(self):
        ...


class CDMEditor(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(CDMEditor, self).__init__(**kwargs)
        self.name = 'cdm_editor_screen'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        for i in range(5):
            lab = FormLabel(id=f'lab{i}', text=f'{i+1}', size_hint_x=0.2)
            mach = MachValue(id=f'mach{i}', size_hint_x=0.4, mode='round', pos_hint={'center_y': 0})
            cd = CDValue(id=f'cl{i}', size_hint_x=0.4,  mode='round', pos_hint={'center_y': 0})
            self.ids.cdm_layout.add_widget(lab)
            self.ids.cdm_layout.add_widget(mach)
            self.ids.cdm_layout.add_widget(cd)

        super(CDMEditor, self).init_ui()

        self.translate_ui()

    def bind_ui(self):
        ...

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        self.translate_ui()

    def translate_ui(self):
        self.title.text = tr('Edit CDM: ', 'CDMEditor') + ''  # Todo: display Drag Model
        # self.mach_label.text = tr('Mach', 'CDMEditor')
        # self.cd_label.text = tr('CD', 'CDMEditor')
