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

    # def on_enter(self, *args):
    #     ...
    #
    # def on_leave(self, *args):
    #     ...

    def init_ui(self):
        self.theme: FormSelector = self.ids.theme_v

        self.lang: FormSelector = self.ids.lang_v
        self.lang.menu.items = [
            {"text": "English", "on_release": lambda: self.change_lang(lang='English')},
            {"text": "Ukrainian", "on_release": lambda: self.change_lang(lang='Ukrainian')},
        ]

        # for uid in self.ids:
        #     child = self.ids[uid]
        #     if hasattr(child, 'text') and not isinstance(child, MDTextField):
        #         # child.text = tr(child.text, ctx='SettingsScreen')
        #         print(uid, child, child.text)



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
                "text": tr(Distance.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_tw_change(caller=self.tw, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.sh.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_sh_change(caller=self.sh, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.v.menu.items = [
            {
                "text": tr(Velocity.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_v_change(caller=self.v, unit=item)
            }
            for item in (Velocity.MPS, Velocity.FPS, Velocity.KMH, Velocity.MPS, Velocity.KT)
        ]

        self.dt.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_dt_change(caller=self.dt, unit=item)
            }
            for item in (Distance.Meter, Distance.Kilometer, Distance.Foot,
                         Distance.Yard, Distance.Mile, Distance.NauticalMile)
        ]

        self.t.menu.items = [
            {
                "text": tr(Temperature.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_t_change(caller=self.t, unit=item)
            }
            for item in (Temperature.Celsius, Temperature.Fahrenheit, Temperature.Kelvin, Temperature.Rankin)
        ]

        self.w.menu.items = [
            {
                "text": tr(Weight.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_w_change(caller=self.w, unit=item)
            }
            for item in (Weight.Grain, Weight.Gram, Weight.Kilogram, Weight.Pound, Weight.Newton, Weight.Ounce)
        ]

        self.ln.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_ln_change(caller=self.ln, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.dm.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_dm_change(caller=self.dm, unit=item)
            }
            for item in (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)
        ]

        self.ps.menu.items = [
            {
                "text": tr(Pressure.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_ps_change(caller=self.ps, unit=item)
            }
            for item in (Pressure.MmHg, Pressure.HP, Pressure.InHg, Pressure.Bar, Pressure.PSI)
        ]

        self.dp.menu.items = [
            {
                "text": tr(Distance.name(item), ctx='Unit'),
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
                "text": tr(Angular.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_an_change(caller=self.an, unit=item)
            }
            for item in (
                Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand, Angular.Degree
            )
        ]

        self.ad.menu.items = [
            {
                "text": tr(Angular.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_ad_change(caller=self.ad, unit=item)
            }
            for item in (
                Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand, Angular.Degree
            )
        ]

        self.e.menu.items = [
            {
                "text": tr(Energy.name(item), ctx='Unit'),
                "on_release": lambda item=item: self.on_e_change(caller=self.e, unit=item)
            }
            for item in (Energy.Joule, Energy.FootPound)
        ]

        self.translate_ui()

    def translate_ui(self):
        self.ids.view_title.text = tr('View', ctx='SettingsScreen')
        self.ids.theme_l.text = tr('Theme', ctx='SettingsScreen')
        self.ids.theme_v.text = tr('Dark', ctx='SettingsScreen')
        self.ids.lang_l.text = tr('Language', ctx='SettingsScreen')
        self.ids.lang_v.text = tr('English', ctx='SettingsScreen')
        self.ids.unit_tw_l.text = tr('Twist', ctx='SettingsScreen')
        self.ids.unit_sh_l.text = tr('Sight height', ctx='SettingsScreen')
        self.ids.unit_v_l.text = tr('Velocity', ctx='SettingsScreen')
        self.ids.unit_dt_l.text = tr('Distance', ctx='SettingsScreen')
        self.ids.unit_t_l.text = tr('Temperature', ctx='SettingsScreen')
        self.ids.unit_w_l.text = tr('Weight', ctx='SettingsScreen')
        self.ids.unit_ln_l.text = tr('Length', ctx='SettingsScreen')
        self.ids.unit_dm_l.text = tr('Diameter', ctx='SettingsScreen')
        self.ids.unit_ps_l.text = tr('Pressure', ctx='SettingsScreen')
        self.ids.unit_dp_l.text = tr('Drop / Windage', ctx='SettingsScreen')
        self.ids.unit_an_l.text = tr('Angular', ctx='SettingsScreen')
        self.ids.unit_ad_l.text = tr('Adjustment', ctx='SettingsScreen')
        self.ids.unit_e_l.text = tr('Energy', ctx='SettingsScreen')

    def bind_ui(self):
        for uid, widget in self.ids.items():
            if isinstance(widget, FormSelector):
                widget.bind(on_release=self.show_menu)
        self.theme.bind(on_release=lambda action: self.change_theme())

        sig.load_set_theme.connect(self.update_theme_selector)
        sig.load_set_lang.connect(self.change_lang)

        sig.load_set_sh_unit_change.connect(lambda unit, **kw: self.on_sh_change(self.sh, unit))
        sig.load_set_tw_unit_change.connect(lambda unit, **kw: self.on_tw_change(self.tw, unit))
        sig.load_set_v_unit_change.connect(lambda unit, **kw: self.on_v_change(self.v, unit))
        sig.load_set_dt_unit_change.connect(lambda unit, **kw: self.on_dt_change(self.dt, unit))
        sig.load_set_t_unit_change.connect(lambda unit, **kw: self.on_t_change(self.t, unit))
        sig.load_set_w_unit_change.connect(lambda unit, **kw: self.on_w_change(self.w, unit))

        sig.load_set_ln_unit_change.connect(lambda unit, **kw: self.on_sh_change(self.ln, unit))
        sig.load_set_dm_unit_change.connect(lambda unit, **kw: self.on_dm_change(self.dm, unit))
        sig.load_set_ps_unit_change.connect(lambda unit, **kw: self.on_ps_change(self.ps, unit))
        sig.load_set_dp_unit_change.connect(lambda unit, **kw: self.on_dp_change(self.dp, unit))
        sig.load_set_an_unit_change.connect(lambda unit, **kw: self.on_an_change(self.an, unit))
        sig.load_set_ad_unit_change.connect(lambda unit, **kw: self.on_ad_change(self.ad, unit))
        sig.load_set_e_unit_change.connect(lambda unit, **kw: self.on_e_change(self.e, unit))


    def on_menu_action(self, caller=None, text=None):
        caller.text = text
        caller.menu.dismiss()

    def show_menu(self, caller):
        if hasattr(caller, 'name') and hasattr(caller, 'menu'):
            caller.menu.open()

    def update_theme_selector(self, theme, **kwargs):
        if theme == "Light":
            self.theme.icon = "weather-sunny"
            self.theme.text = 'Light'

        elif theme == 'Dark':
            self.theme.icon = "weather-night"
            self.theme.text = 'Dark'
        sig.set_theme_changed.emit(theme=self.theme.text)

    def change_theme(self, **kwargs):
        if self.theme.icon == "weather-night":
            self.update_theme_selector('Light')
        elif self.theme.icon == "weather-sunny":
            self.update_theme_selector('Dark')

    def change_lang(self, lang, **kwargs):
        # TODO:
        self.lang.menu.dismiss()
        self.lang.text = lang
        sig.set_lang_changed.emit(lang=lang)

    def on_sh_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_sh_unit_change.emit(unit=unit)

    def on_tw_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_tw_unit_change.emit(unit=unit)

    def on_v_change(self, caller=None, unit=None):
        text = tr(Velocity.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_v_unit_change.emit(unit=unit)

    def on_dt_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_dt_unit_change.emit(unit=unit)

    def on_t_change(self, caller=None, unit=None):
        text = tr(Temperature.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_t_unit_change.emit(unit=unit)

    def on_w_change(self, caller=None, unit=None):
        text = tr(Weight.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_w_unit_change.emit(unit=unit)

    def on_ln_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_ln_unit_change.emit(unit=unit)

    def on_dm_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_dm_unit_change.emit(unit=unit)

    def on_ps_change(self, caller=None, unit=None):
        text = tr(Pressure.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_ps_unit_change.emit(unit=unit)

    def on_dp_change(self, caller=None, unit=None):
        text = tr(Distance.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_dp_unit_change.emit(unit=unit)

    def on_an_change(self, caller=None, unit=None):
        text = tr(Angular.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_an_unit_change.emit(unit=unit)

    def on_ad_change(self, caller=None, unit=None):
        text = tr(Angular.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_ad_unit_change.emit(unit=unit)

    def on_e_change(self, caller=None, unit=None):
        text = tr(Energy.name(unit), ctx='Unit')
        self.on_menu_action(caller, text)
        sig.set_e_unit_change.emit(unit=unit)
