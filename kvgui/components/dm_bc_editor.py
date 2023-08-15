from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from kvgui.components.mixines import MapIdsMixine
from kvgui.modules.translator import translate as tr
from kvgui.modules import signals as sig


Builder.load_file('kvgui/kv/dm_bc_editor.kv')


class VelocityBCPair(MDBoxLayout, MapIdsMixine):
    def __init__(self, **kwargs):
        super(VelocityBCPair, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(VelocityBCPair, self).init_ui()

    def bind_ui(self):
        ...


class BCEditor(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(BCEditor, self).__init__(**kwargs)
        self.name = 'bc_editor_screen'
        self.init_ui()
        self.bind_ui()

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        self.translate_ui()

    def init_ui(self):
        super(BCEditor, self).init_ui()


        self.translate_ui()

    def bind_ui(self):
        sig.set_settings.connect(self.on_set_settings)

    def translate_ui(self):
        self.title.text = tr('Edit BC: ', 'BCEditor') + ''  # Todo: display Drag Model
        self.velocity_label.text = tr('Velocity, ', 'BCEditor') + '{DragModel}'  # Todo: display Drag Model
        self.bc_label.text = tr('BC, ', 'BCEditor') + '{DragModel}'  # Todo: display Drag Model

    def on_set_settings(self, **kwargs):

        def set_unit_for_target(target, key):
            if kwargs.get(key):
                unit = kwargs.get(key)
                if unit:
                    target.unit = unit

        for i in range(5):
            vbc = self.ids[f'vbc{i}']
            set_unit_for_target(vbc.ids.velocity, 'unit_velocity')
