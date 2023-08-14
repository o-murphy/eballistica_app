from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField

from kvgui.components.abstract import FormSelector
from kvgui.components.measure_widgets import *
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr
from units import *

Builder.load_file('kvgui/kv/ammo_card.kv')


class BCSelector(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super(BCSelector, self).__init__(**kwargs)
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
        self.value = "G7"

    def init_ui(self):
        self.menu = MDDropdownMenu(
            caller=self,
            items=[
                {"text": "G1", "on_release": lambda: self.on_menu(action="G1")},
                {"text": "G7", "on_release": lambda: self.on_menu(action="G7")},
                {"text": "CDM", "on_release": lambda: self.on_menu(action="CDM")},
            ],
        )

    def bind_ui(self):
        self.bind(on_release=self.showeight_menu)

    def showeight_menu(self, *args, **kwargs):
        self.menu.open()

    def on_menu(self, action):
        self.text = action
        self.value = action
        self.menu.dismiss()


class AmmoCardScreen(Screen):
    def __init__(self, **kwargs):
        super(AmmoCardScreen, self).__init__(**kwargs)
        self.name = 'ammo_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):

        for uid in self.ids:
            child = self.ids[uid]
            if hasattr(child, 'text') and not isinstance(child, MDTextField):
                child.text = tr(child.text, ctx='AmmoCard')

        # convertable values
        self.diameter: DiameterValue = self.ids.diameter
        self.diameter_suffix = self.ids.diameter_suffix
        self.weight: WeightValue = self.ids.weight
        self.weight_suffix = self.ids.weight_suffix
        self.length: LengthValue = self.ids.length
        self.length_suffix = self.ids.length_suffix
        self.muzzle_velocity: MuzzleValue = self.ids.muzzle_velocity
        self.muzzle_velocity_suffix = self.ids.muzzle_velocity_suffix

        # convertable values
        self.powder_temp: PowderTempValue = self.ids.powder_temp
        self.powder_temp_suffix = self.ids.powder_temp_suffix
        self.zero_dist: ZeroDistValue = self.ids.zero_dist
        self.zero_dist_suffix = self.ids.zero_dist_suffix
        self.altitude: AltitudeValue = self.ids.altitude
        self.altitude_suffix = self.ids.altitude_suffix
        self.pressure: PressureValue = self.ids.pressure
        self.pressure_suffix = self.ids.pressure_suffix
        self.temperature: TemperatureValue = self.ids.temperature
        self.temperature_suffix = self.ids.temperature_suffix

        # not need conversion values
        self.powder_sens = self.ids.powder_sens
        self.humidity = self.ids.humidity

        # special actions
        self.dm_select = self.ids.dm_select
        self.bc_select = self.ids.bc_select
        self.powder_sens_act: MDRectangleFlatButton = self.ids.powder_sens_act

    def bind_ui(self):
        self.powder_sens_act.bind(on_release=lambda x: sig.ammo_powder_sens_act.emit(caller=self))

        sig.set_settings.connect(self.on_set_settings)

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

    def on_enter(self, *args):
        ...
