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
        self.bind(on_release=self.show_menu)

    def show_menu(self, *args, **kwargs):
        self.menu.open()

    def on_menu(self, action):
        self.text = action
        self.value = action
        self.menu.dismiss()
        sig.ammo_dm_change.emit(caller=self)


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
        self.dm_v = self.ids.dm_v
        self.dm_s = self.ids.dm_s
        self.w_v = self.ids.w_v
        self.w_s = self.ids.w_s
        self.ln_v = self.ids.ln_v
        self.ln_s = self.ids.ln_s
        self.mv_v = self.ids.mv_v
        self.mv_s = self.ids.mv_s

        # convertable values
        self.pwt_v = self.ids.pwt_v
        self.pwt_s = self.ids.pwt_s
        self.zd_v = self.ids.zd_v
        self.zd_s = self.ids.zd_s
        self.alt_v = self.ids.alt_v
        self.alt_s = self.ids.alt_s
        self.ps_v = self.ids.ps_v
        self.ps_s = self.ids.ps_s
        self.t_v = self.ids.t_v
        self.t_s = self.ids.t_s

        # not need conversion values
        self.pws_v = self.ids.pws_v
        self.h_v = self.ids.h_v

        # special actions
        self.dm_select = self.ids.dm_select
        self.bc_select = self.ids.bc_select
        self.pws_act: MDRectangleFlatButton = self.ids.pws_act

    def bind_ui(self):
        self.pws_act.bind(on_release=lambda x: sig.ammo_powder_sens_act.emit(caller=self))

        # sig.set_unit_diameter.connect(self.dm_unit_change)
        # sig.set_unit_weight.connect(self.w_unit_change)
        # sig.set_unit_velocity.connect(self.mv_unit_change)
        # sig.set_unit_velocity.connect(self.mv_unit_change)
        # sig.set_unit_temperature.connect(self.t_unit_change)
        # sig.set_unit_distance.connect(self.dt_unit_change)
        # sig.set_unit_pressure.connect(self.ps_unit_change)

    def on_enter(self, *args):
        ...

    def dm_unit_change(self, unit, **kwargs):
        self.dm_v.convertor = Convertor(Distance, Distance.Centimeter, unit)
        self.dm_s.text = tr(Distance.name(unit), 'Unit')

    def w_unit_change(self, unit, **kwargs):
        self.w_v.convertor = Convertor(Weight, Weight.Grain, unit)
        self.w_s.text = tr(Weight.name(unit), 'Unit')

    def ln_unit_change(self, unit, **kwargs):
        self.ln_v.convertor = Convertor(Distance, Distance.Inch, unit)
        self.ln_s.text = tr(Distance.name(unit), 'Unit')

    def mv_unit_change(self, unit, **kwargs):
        self.mv_v.convertor = Convertor(Velocity, Velocity.MPS, unit)
        self.mv_s.text = tr(Velocity.name(unit), 'Unit')

    def t_unit_change(self, unit, **kwargs):
        self.pwt_v.convertor = Convertor(Temperature, Temperature.Celsius, unit)
        self.pwt_s.text = tr(Temperature.name(unit), 'Unit')
        self.t_v.convertor = Convertor(Temperature, Temperature.Celsius, unit)
        self.t_s.text = tr(Temperature.name(unit), 'Unit')

    def dt_unit_change(self, unit, **kwargs):
        self.zd_v.convertor = Convertor(Distance, Distance.Meter, unit)
        self.zd_s.text = tr(Distance.name(unit), 'Unit')
        self.alt_v.convertor = Convertor(Distance, Distance.Meter, unit)
        self.alt_s.text = tr(Distance.name(unit), 'Unit')

    def ps_unit_change(self, unit, **kwargs):
        self.ps_v.convertor = Convertor(Pressure, Pressure.MmHg, unit)
        self.ps_s.text = tr(Pressure.name(unit), 'Unit')
