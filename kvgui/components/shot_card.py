from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr
from units import *

Builder.load_file('kvgui/kv/shot_card.kv')


class ShotCardScreen(Screen):
    def __init__(self, **kwargs):
        super(ShotCardScreen, self).__init__(**kwargs)
        self.name = 'shot_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        for uid in self.ids:
            child = self.ids[uid]
            if hasattr(child, 'text') and not isinstance(child, MDTextField):
                child.text = tr(child.text, ctx='ShotCard')

        # convertable values
        self.dt_v = self.ids.dt_v
        self.dt_s = self.ids.dt_s
        self.la_v = self.ids.la_v
        self.la_s = self.ids.la_s
        self.alt_v = self.ids.alt_v
        self.alt_s = self.ids.alt_s
        self.ps_v = self.ids.ps_v
        self.ps_s = self.ids.ps_s
        self.t_v = self.ids.t_v
        self.t_s = self.ids.t_s
        self.ws_v = self.ids.ws_v
        self.ws_s = self.ids.ws_s
        self.wa_v = self.ids.wa_v
        self.wa_s = self.ids.wa_s

        # not need conversion values
        self.h_v = self.ids.h_v

        # special actions
        self.one_shot: MDRaisedButton = self.ids.one_shot
        self.trajectory: MDRaisedButton = self.ids.trajectory

    def bind_ui(self):
        self.one_shot.bind(on_release=lambda x: sig.one_shot_act.emit(caller=self))
        self.trajectory.bind(on_release=lambda x: sig.trajectory_act.emit(caller=self))

        sig.set_unit_distance.connect(self.dt_unit_change)
        sig.set_unit_velocity.connect(self.v_unit_change)
        sig.set_unit_temperature.connect(self.t_unit_change)
        sig.set_unit_pressure.connect(self.ps_unit_change)
        sig.set_unit_angular.connect(self.an_unit_change)

    def on_enter(self, *args):
        ...

    def an_unit_change(self, unit, **kwargs):
        self.wa_v.convertor = Convertor(Angular, Angular.Degree, unit)
        self.wa_s.text = tr(Velocity.name(unit), 'Unit')
        self.la_v.convertor = Convertor(Angular, Angular.Degree, unit)
        self.la_s.text = tr(Velocity.name(unit), 'Unit')

    def v_unit_change(self, unit, **kwargs):
        self.ws_v.convertor = Convertor(Velocity, Velocity.MPS, unit)
        self.ws_s.text = tr(Velocity.name(unit), 'Unit')

    def t_unit_change(self, unit, **kwargs):
        self.t_v.convertor = Convertor(Temperature, Temperature.Celsius, unit)
        self.t_s.text = tr(Temperature.name(unit), 'Unit')

    def dt_unit_change(self, unit, **kwargs):
        self.dt_v.convertor = Convertor(Distance, Distance.Meter, unit)
        self.dt_s.text = tr(Distance.name(unit), 'Unit')
        self.alt_v.convertor = Convertor(Distance, Distance.Meter, unit)
        self.alt_s.text = tr(Distance.name(unit), 'Unit')

    def ps_unit_change(self, unit, **kwargs):
        self.ps_v.convertor = Convertor(Pressure, Pressure.MmHg, unit)
        self.ps_s.text = tr(Pressure.name(unit), 'Unit')
