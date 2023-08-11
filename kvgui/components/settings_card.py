from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

from kvgui.components.abstract import FormSelector
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr
from units import *

Builder.load_file('kvgui/kv/settings_card.kv')


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.name = 'settings'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.theme: FormSelector = self.ids.theme_v

        self.lang: FormSelector = self.ids.lang_v
        self.lang.menu.items = [
            {"text": "English", "on_release": lambda: self.change_lang(action='English')},
            {"text": "Ukrainian", "on_release": lambda: self.change_lang(action='Ukrainian')},
        ]

        for uid in self.ids:
            child = self.ids[uid]
            if hasattr(child, 'text') and not isinstance(child, MDTextField):
                child.text = tr(child.text, ctx='SettingsScreen')

        self.tw: FormSelector = self.ids.unit_tw_v
        self.sh: FormSelector = self.ids.unit_sh_v
        self.v: FormSelector = self.ids.unit_v_v
        self.dt: FormSelector = self.ids.unit_dt_v
        self.t: FormSelector = self.ids.unit_t_v
        self.w: FormSelector = self.ids.unit_w_v
        self.ln: FormSelector = self.ids.unit_ln_v
        self.dm: FormSelector = self.ids.unit_dm_v
        self.ps: FormSelector = self.ids.unit_ps_v
        self.dp: FormSelector = self.ids.unit_dp_v
        self.an: FormSelector = self.ids.unit_an_v
        self.ad: FormSelector = self.ids.unit_ad_v
        self.e: FormSelector = self.ids.unit_e_v

        self.tw.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_tw_change(caller=self.tw, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.sh.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_sh_change(caller=self.sh, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.v.menu.items = [
            {
                "text": tr(Velocity.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_v_change(caller=self.v, unit=item)
            }
            for item in (Velocity.MPS, Velocity.FPS, Velocity.KMH, Velocity.MPS, Velocity.KT)
        ]

        self.dt.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_dt_change(caller=self.dt, unit=item)
            }
            for item in (Distance.Meter, Distance.Kilometer, Distance.Foot,
                         Distance.Yard, Distance.Mile, Distance.NauticalMile)
        ]

        self.t.menu.items = [
            {
                "text": tr(Temperature.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_t_change(caller=self.t, unit=item)
            }
            for item in (Temperature.Celsius, Temperature.Fahrenheit, Temperature.Kelvin, Temperature.Rankin)
        ]

        self.w.menu.items = [
            {
                "text": tr(Weight.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_w_change(caller=self.w, unit=item)
            }
            for item in (Weight.Grain, Weight.Gram, Weight.Kilogram, Weight.Pound, Weight.Newton, Weight.Ounce)
        ]

        self.ln.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_ln_change(caller=self.ln, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.dm.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_dm_change(caller=self.dm, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.ps.menu.items = [
            {
                "text": tr(Pressure.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_ps_change(caller=self.ps, unit=item)
            }
            for item in (Pressure.MmHg, Pressure.HP, Pressure.InHg, Pressure.Bar, Pressure.PSI)
        ]

        self.dp.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_dp_change(caller=self.dp, unit=item)
            }
            for item in (
                Distance.Centimeter, Distance.Inch, Distance.Millimeter, Distance.Line,
                Distance.Meter, Distance.Kilometer, Distance.Foot, Distance.Yard,
                Distance.Mile, Distance.NauticalMile
            )
        ]

        self.an.menu.items = [
            {
                "text": tr(Angular.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_an_change(caller=self.dp, unit=item)
            }
            for item in (
                Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand
            )
        ]

        self.ad.menu.items = [
            {
                "text": tr(Angular.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_ad_change(caller=self.dp, unit=item)
            }
            for item in (
                Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand
            )
        ]

        self.e.menu.items = [
            {
                "text": tr(Energy.name(item), ctx='SettingsScreen'),
                "on_release": lambda item=item: self.on_e_change(caller=self.dp, unit=item)
            }
            for item in (Energy.Joule, Energy.FootPound)
        ]

    def bind_ui(self):
        for uid, widget in self.ids.items():
            if isinstance(widget, FormSelector):
                widget.bind(on_release=self.show_menu)
        self.theme.bind(on_release=lambda x: self.change_theme())

    def on_menu_action(self, caller=None, text=None):
        caller.text = text
        caller.menu.dismiss()

    def show_menu(self, caller):
        if hasattr(caller, 'name') and hasattr(caller, 'menu'):
            caller.menu.open()

    def change_theme(self):

        if self.theme.icon == "weather-night":
            self.theme.icon = "weather-sunny"
            self.theme.text = 'Light'

        elif self.theme.icon == "weather-sunny":
            self.theme.icon = "weather-night"
            self.theme.text = 'Dark'

        app: MDApp = MDApp.get_running_app()
        if app:
            app.theme_cls.theme_style = self.theme.text
            self.theme.menu.dismiss()

    def change_lang(self, action):
        # TODO:
        self.lang.menu.dismiss()
        self.lang.text = action

    def on_sh_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_sh_unit_change.emit(unit=unit)

    def on_tw_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_tw_unit_change.emit(unit=unit)

    def on_v_change(self, caller=None, unit=None):
        text = tr(Velocity.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_v_unit_change.emit(unit=unit)

    def on_dt_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_dt_unit_change.emit(unit=unit)

    def on_t_change(self, caller=None, unit=None):
        text = tr(Temperature.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_t_unit_change.emit(unit=unit)

    def on_w_change(self, caller=None, unit=None):
        text = tr(Weight.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_w_unit_change.emit(unit=unit)

    def on_ln_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_ln_unit_change.emit(unit=unit)

    def on_dm_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_dm_unit_change.emit(unit=unit)

    def on_ps_change(self, caller=None, unit=None):
        text = tr(Pressure.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_ps_unit_change.emit(unit=unit)

    def on_dp_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_dp_unit_change.emit(unit=unit)

    def on_an_change(self, caller=None, unit=None):
        text = tr(Angular.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_an_unit_change.emit(unit=unit)

    def on_ad_change(self, caller=None, unit=None):
        text = tr(Angular.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_ad_unit_change.emit(unit=unit)

    def on_e_change(self, caller=None, unit=None):
        text = tr(Energy.name(unit), ctx='SettingsScreen')
        self.on_menu_action(caller, text)
        sig.set_e_unit_change.emit(unit=unit)
