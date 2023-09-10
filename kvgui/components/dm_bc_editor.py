from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from datatypes.defines import DragModel
from kvgui.components.mixines import MapIdsMixine
from modules import signals as sig
from modules.translator import translate as tr


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
        # self.translate_ui()
        ...

    def init_ui(self):
        super(BCEditor, self).init_ui()
        self.translate_ui()

    def bind_ui(self):
        sig.set_settings.connect(self.on_set_settings)
        sig.translator_update.connect(self.translate_ui)
        sig.drag_model_edit_act.connect(self.display)

    def translate_ui(self, **kwargs):
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

    def display(self, drag_model: DragModel, drag_data, **kwargs):
        vmeasure = self.ids['vbc0'].ids.velocity.measure
        vunit = vmeasure.name(self.ids['vbc0'].ids.velocity.unit)
        vunit = tr(vunit, 'Unit')
        self.velocity_label.text = tr('Velocity, ', 'BCEditor') + vunit
        self.bc_label.text = tr('BC, ', 'BCEditor') + f'{drag_model.name}'

        for i in range(5):
            vbc = self.ids[f'vbc{i}']
            vbc.ids.velocity.raw_value = 0
            vbc.ids.bc.value = 0

        if drag_data:
            for i, item in enumerate(drag_data):
                vbc = self.ids[f'vbc{i}']
                vbc.ids.velocity.raw_value = item[0]
                vbc.ids.bc.value = item[1]

    def get(self):
        mbc = []
        for i in range(5):
            vbc = self.ids[f'vbc{i}']
            mbc.append([vbc.ids.velocity.raw_value, vbc.ids.bc.value])
        mbc.sort(reverse=True)
        return mbc
