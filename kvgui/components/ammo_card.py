from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu

from datatypes.dbworker import AmmoData
from datatypes.defines import DragModel
from kvgui.components.abstract import FormSelector
from kvgui.components.measure_widgets import *
from kvgui.components.mixines import MapIdsMixine
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/ammo_card.kv')


class DragEdit(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super(DragEdit, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        ...

    def bind_ui(self):
        ...


class DragModelSelector(FormSelector):
    def __init__(self, **kwargs):
        super(DragModelSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()
        self.value = DragModel.G7

    def init_ui(self):
        self.menu = MDDropdownMenu(
            caller=self,
            items=[
                {"text": "G1", "on_release": lambda: self.on_menu(action=DragModel.G1)},
                {"text": "G7", "on_release": lambda: self.on_menu(action=DragModel.G7)},
                {"text": "CDM", "on_release": lambda: self.on_menu(action=DragModel.CDM)},
            ],
        )

    def bind_ui(self):
        self.bind(on_release=self.showeight_menu)

    def showeight_menu(self, *args, **kwargs):
        self.menu.open()

    def on_menu(self, action):
        self.value = action
        self.menu.dismiss()

    @property
    def value(self) -> DragModel:
        return self._value

    @value.setter
    def value(self, value: DragModel):
        self._value = value
        self.text = value.name
        sig.drag_model_changed.emit(drag_model=self._value)


class AmmoCardScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(AmmoCardScreen, self).__init__(**kwargs)
        self.name = 'ammo_card'
        self.init_ui()
        self.bind_ui()

        self.bc = []
        self.bc7 = []
        self.cdm = []

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        # self.translate_ui()
        ...

    def init_ui(self):
        super(AmmoCardScreen, self).init_ui()
        self.translate_ui()

    def translate_ui(self, **kwargs):
        self.name_label.text = tr('Name', 'AmmoCard')
        self.prop_title.text = tr('Properties', 'AmmoCard')
        self.diameter_label.text = tr('Diameter', 'AmmoCard')
        self.weight_label.text = tr('Weight', 'AmmoCard')
        self.length_label.text = tr('Length', 'AmmoCard')
        self.muzzle_velocity_label.text = tr('Muzzle velocity', 'AmmoCard')
        self.dm_label.text = tr('Drag model', 'AmmoCard')
        self.powder_sens_label.text = tr('Powder sensitivity', 'AmmoCard')
        self.powder_temp_label.text = tr('Powder temperature', 'AmmoCard')
        self.zero_dist_label.text = tr('Zero distance', 'AmmoCard')
        self.altitude_label.text = tr('Altitude', 'AmmoCard')
        self.pressure_label.text = tr('Pressure', 'AmmoCard')
        self.temperature_label.text = tr('Temperature', 'AmmoCard')
        self.humidity_label.text = tr('Humidity', 'AmmoCard')

        self.powder_sens_act.text = tr('Calculate powder sensitivity', 'AmmoCard')

    def bind_ui(self):
        self.powder_sens_act.bind(on_release=lambda x: sig.ammo_powder_sens_act.emit(caller=self))
        self.drag_edit.bind(on_release=lambda x: sig.drag_model_edit_act.emit(
            drag_model=self.drag_model.value, drag_data=self.get_current_drag_data()
        ))

        sig.set_settings.connect(self.on_set_settings)
        sig.translator_update.connect(self.translate_ui)
        sig.bc_data_edited.connect(self.update_drag_data)
        sig.cdm_data_edited.connect(self.update_drag_data)

    def update_drag_data(self, drag_data, **kwargs):
        if self.drag_model.value == DragModel.G1:
            self.bc = drag_data
        elif self.drag_model.value == DragModel.G7:
            self.bc7 = drag_data
        elif self.drag_model.value == DragModel.CDM:
            self.cmd = drag_data

    def on_set_settings(self, **kwargs):

        def set_unit_for_target(target, target_suffix, key):
            if kwargs.get(key):
                unit = kwargs.get(key)
                if unit:
                    target.unit = unit
                    target_suffix.text = tr(target.measure.name(target.unit), 'Unit')

        set_unit_for_target(self.diameter, self.diameter_suffix, 'unit_diameter')
        set_unit_for_target(self.weight, self.weight_suffix, 'unit_weight')
        set_unit_for_target(self.length, self.length_suffix, 'unit_length')
        set_unit_for_target(self.muzzle_velocity, self.muzzle_velocity_suffix, 'unit_velocity')

    def display(self, data: AmmoData):
        self.name_input.text = data.name if data.name else tr('New ammo', 'AmmoCard')
        self.diameter.raw_value = data.diameter
        self.weight.raw_value = data.weight
        self.length.raw_value = data.length
        self.muzzle_velocity.raw_value = data.muzzle_velocity
        self.powder_sens.raw_value = data.temp_sens
        self.powder_temp.raw_value = data.powder_temp

        self.zero_dist.raw_value = data.zerodata.zero_range
        self.altitude.raw_value = data.zerodata.altitude
        self.pressure.raw_value = data.zerodata.pressure
        self.temperature.raw_value = data.zerodata.temperature
        self.humidity.raw_value = data.zerodata.humidity

        self.drag_model.value = data.drag_model

        self.bc = data.bc_list
        self.bc7 = data.bc7_list
        self.cdm = data.cdm_list

    def get_current_drag_data(self):
        if self.drag_model.value == DragModel.G1:
            return self.bc
        elif self.drag_model.value == DragModel.G7:
            return self.bc7
        elif self.drag_model.value == DragModel.CDM:
            return self.cdm

    def validate(self):
        print(sum([i[0] for i in self.bc]))
        if sum([i[0] for i in self.bc]) != 0 and self.drag_model.value == DragModel.G1:
            return True
        elif sum([i[0] for i in self.bc7]) != 0 and self.drag_model.value == DragModel.G7:
            return True
        elif sum([i[0] for i in self.cdm]) != 0 and self.drag_model.value == DragModel.CDM:
            return True
        else:
            return False

    def get_ammo(self):
        return dict(
            name=self.name_input.text,
            diameter=self.diameter.raw_value,
            weight=self.weight.raw_value,
            length=self.length.raw_value,
            muzzle_velocity=self.muzzle_velocity.raw_value,
            temp_sens=self.powder_sens.raw_value,
            powder_temp=self.powder_temp.raw_value,
            drag_model=self.drag_model.value,
            bc_list=self.bc,
            bc7_list=self.bc7,
            cdm_list=self.cdm
        )
        # TODO:
        # drag_model, drag_data

    def get_zero(self):
        return dict(
            zero_range=self.zero_dist.raw_value,
            altitude=self.altitude.raw_value,
            pressure=self.pressure.raw_value,
            temperature=self.temperature.raw_value,
            humidity=self.humidity.raw_value,
        )
