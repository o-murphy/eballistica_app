from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField

from kvgui.components.abstract import FormSelector
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
        self.diameter = self.ids.diameter
        self.diameter_s = self.ids.diameter_s
        self.weight = self.ids.weight
        self.weight_s = self.ids.weight_s
        self.length = self.ids.length
        self.length_s = self.ids.length_s
        self.muzzleelocity = self.ids.muzzleelocity
        self.muzzleelocity_s = self.ids.muzzleelocity_s

        # convertable values
        self.powder_temp = self.ids.powder_temp
        self.powder_temp_s = self.ids.powder_temp_s
        self.zero_dist = self.ids.zero_dist
        self.zero_dist_s = self.ids.zero_dist_s
        self.altitude = self.ids.altitude
        self.altitude_s = self.ids.altitude_s
        self.pressure = self.ids.pressure
        self.pressure_s = self.ids.pressure_s
        self.temperature = self.ids.temperature
        self.temperature_s = self.ids.temperature_s

        # not need conversion values
        self.powder_sens = self.ids.powder_sens
        self.humidity = self.ids.humidity

        # special actions
        self.diameter_select = self.ids.diameter_select
        self.bc_select = self.ids.bc_select
        self.powder_sens_act: MDRectangleFlatButton = self.ids.powder_sens_act

    def bind_ui(self):
        self.powder_sens_act.bind(on_release=lambda x: sig.ammo_powder_sens_act.emit(caller=self))

    def on_enter(self, *args):
        ...
