from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

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
        self.theme: FormSelector = self.ids.theme

        self.lang: FormSelector = self.ids.lang
        self.lang.menu.items = [
            {"text": "English", "on_release": lambda: self.change_lang(lang='English')},
            {"text": "Ukrainian", "on_release": lambda: self.change_lang(lang='Ukrainian')},
        ]

        # for uid in self.ids:
        #     child = self.ids[uid]
        #     if hasattr(child, 'text') and not isinstance(child, MDTextField):
        #         # child.text = tr(child.text, ctx='SettingsScreen')
        #         print(uid, child, child.text)

        self.unit_twist: FormSelector = self.ids.unit_twist
        self.unit_sight_height: FormSelector = self.ids.unit_sight_height
        self.unit_velocity: FormSelector = self.ids.unit_velocity
        self.unit_distance: FormSelector = self.ids.unit_distance
        self.unit_temperature: FormSelector = self.ids.unit_temperature
        self.unit_weight: FormSelector = self.ids.unit_weight
        self.unit_length: FormSelector = self.ids.unit_length
        self.unit_diameter: FormSelector = self.ids.unit_diameter
        self.unit_pressure: FormSelector = self.ids.unit_pressure
        self.unit_drop: FormSelector = self.ids.unit_drop
        self.unit_angular: FormSelector = self.ids.unit_angular
        self.unit_adjustment: FormSelector = self.ids.unit_adjustment
        self.unit_energy: FormSelector = self.ids.unit_energy

        def create_unit_menu(selector: FormSelector):
            if selector.unit_class and selector.units_specified:
                selector.menu.items = [
                    {
                        "text": tr(selector.unit_class.name(unit), ctx='Unit'),
                        "on_release": lambda selector=selector, unit=unit:
                        self.set_unit(selector=selector, unit=unit)
                    } for unit in selector.units_specified
                ]

        self.unit_twist.id = 'unit_twist'
        self.unit_twist.unit_class = Distance
        self.unit_twist.units_specified = (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)

        self.unit_sight_height.id = 'unit_sight_height'
        self.unit_sight_height.unit_class = Distance
        self.unit_sight_height.units_specified = (
            Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)

        self.unit_velocity.id = 'unit_velocity'
        self.unit_velocity.unit_class = Velocity
        self.unit_velocity.units_specified = (Velocity.MPS, Velocity.FPS, Velocity.KMH, Velocity.MPS, Velocity.KT)

        self.unit_distance.unit_class = 'unit_distance'
        self.unit_distance.unit_class = Distance
        self.unit_distance.units_specified = (Distance.Meter, Distance.Kilometer, Distance.Foot,
                                              Distance.Yard, Distance.Mile, Distance.NauticalMile)

        self.unit_temperature.unit_class = 'unit_temperature'
        self.unit_temperature.unit_class = Temperature
        self.unit_temperature.units_specified = (Temperature.Celsius, Temperature.Fahrenheit,
                                                 Temperature.Kelvin, Temperature.Rankin)

        self.unit_weight.unit_class = 'unit_weight'
        self.unit_weight.unit_class = Weight
        self.unit_weight.units_specified = (Weight.Grain, Weight.Gram, Weight.Kilogram,
                                            Weight.Pound, Weight.Newton, Weight.Ounce)

        self.unit_length.unit_class = 'unit_length'
        self.unit_length.unit_class = Distance
        self.unit_length.units_specified = (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)

        self.unit_diameter.unit_class = 'unit_diameter'
        self.unit_diameter.unit_class = Distance
        self.unit_diameter.units_specified = (Distance.Inch, Distance.Centimeter, Distance.Millimeter, Distance.Line)

        self.unit_pressure.unit_class = 'unit_pressure'
        self.unit_pressure.unit_class = Pressure
        self.unit_pressure.units_specified = (Pressure.MmHg, Pressure.HP, Pressure.InHg, Pressure.Bar, Pressure.PSI)

        self.unit_drop.unit_class = 'unit_drop'
        self.unit_drop.unit_class = Distance
        self.unit_drop.units_specified = (Distance.Centimeter, Distance.Inch, Distance.Millimeter, Distance.Line,
                                          Distance.Meter, Distance.Kilometer, Distance.Foot, Distance.Yard,
                                          Distance.Mile, Distance.NauticalMile)

        self.unit_angular.unit_class = 'unit_angular'
        self.unit_angular.unit_class = Angular
        self.unit_angular.units_specified = (Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                                             Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand, Angular.Degree)

        self.unit_adjustment.unit_class = 'unit_adjustment'
        self.unit_adjustment.unit_class = Angular
        self.unit_adjustment.units_specified = (Angular.CmPer100M, Angular.Mil, Angular.MOA, Angular.MRad,
                                                Angular.Radian, Angular.InchesPer100Yd, Angular.Thousand,
                                                Angular.Degree)

        self.unit_energy.unit_class = 'unit_energy'
        self.unit_energy.unit_class = Energy
        self.unit_energy.units_specified = (Energy.Joule, Energy.FootPound)

        create_unit_menu(self.unit_twist)
        create_unit_menu(self.unit_sight_height)
        create_unit_menu(self.unit_velocity)
        create_unit_menu(self.unit_distance)
        create_unit_menu(self.unit_temperature)
        create_unit_menu(self.unit_weight)
        create_unit_menu(self.unit_length)
        create_unit_menu(self.unit_diameter)
        create_unit_menu(self.unit_pressure)
        create_unit_menu(self.unit_drop)
        create_unit_menu(self.unit_angular)
        create_unit_menu(self.unit_adjustment)

        self.translate_ui()

    def translate_ui(self):
        self.ids.view_title.text = tr('View', ctx='SettingsScreen')
        self.ids.theme_label.text = tr('Theme', ctx='SettingsScreen')
        self.ids.theme.text = tr('Dark', ctx='SettingsScreen')
        self.ids.lang_label.text = tr('Language', ctx='SettingsScreen')
        self.ids.lang.text = tr('English', ctx='SettingsScreen')
        self.ids.unit_twist_label.text = tr('Twist', ctx='SettingsScreen')
        self.ids.unit_sight_height_label.text = tr('Sight height', ctx='SettingsScreen')
        self.ids.unit_velocity_label.text = tr('Velocity', ctx='SettingsScreen')
        self.ids.unit_distance_label.text = tr('Distance', ctx='SettingsScreen')
        self.ids.unit_temperature_label.text = tr('Temperature', ctx='SettingsScreen')
        self.ids.unit_weight_label.text = tr('Weight', ctx='SettingsScreen')
        self.ids.unit_length_label.text = tr('Length', ctx='SettingsScreen')
        self.ids.unit_diameter_label.text = tr('Diameter', ctx='SettingsScreen')
        self.ids.unit_pressure_label.text = tr('Pressure', ctx='SettingsScreen')
        self.ids.unit_drop_label.text = tr('Drop / Windage', ctx='SettingsScreen')
        self.ids.unit_angular_label.text = tr('Angular', ctx='SettingsScreen')
        self.ids.unit_adjustment_label.text = tr('Adjustment', ctx='SettingsScreen')
        self.ids.unit_energy_label.text = tr('Energy', ctx='SettingsScreen')

    def bind_ui(self):
        for uid, widget in self.ids.items():
            if isinstance(widget, FormSelector):
                widget.bind(on_release=self.show_menu)
        self.theme.bind(on_release=lambda action: self.change_theme())

        sig.load_set_theme.connect(self.update_theme_selector)
        sig.load_set_lang.connect(self.change_lang)

        sig.load_unit_sight_height.connect(lambda unit, **kw: self.set_unit(self.unit_sight_height, unit))
        sig.load_unit_twist.connect(lambda unit, **kw: self.set_unit(self.unit_twist, unit))
        sig.load_unit_velocity.connect(lambda unit, **kw: self.set_unit(self.unit_velocity, unit))
        sig.load_unit_distance.connect(lambda unit, **kw: self.set_unit(self.unit_distance, unit))
        sig.load_unit_temperature.connect(lambda unit, **kw: self.set_unit(self.unit_temperature, unit))
        sig.load_unit_weight.connect(lambda unit, **kw: self.set_unit(self.unit_weight, unit))

        sig.load_unit_length.connect(lambda unit, **kw: self.set_unit(self.unit_length, unit))
        sig.load_unit_diameter.connect(lambda unit, **kw: self.set_unit(self.unit_diameter, unit))
        sig.load_unit_pressure.connect(lambda unit, **kw: self.set_unit(self.unit_pressure, unit))
        sig.load_unit_drop.connect(lambda unit, **kw: self.set_unit(self.unit_drop, unit))
        sig.load_unit_angular.connect(lambda unit, **kw: self.set_unit(self.unit_angular, unit))
        sig.load_unit_adjustment.connect(lambda unit, **kw: self.set_unit(self.unit_adjustment, unit))
        sig.load_unit_energy.connect(lambda unit, **kw: self.set_unit(self.unit_energy, unit))

        # def load_setting(target, value, **kwargs):
        #     print(target, value)
        #     print()
        #     widget = self.ids.get(target)
        #     if isinstance(widget, FormSelector):
        #         widget.
        #
        #
        # sig.load_setting.connect(load_setting)

    def set_unit(self, selector, unit, **kwargs):
        text = tr(selector.unit_class.name(unit), ctx='Unit')
        self.on_menu_action(selector, text)
        sig.set_setting.emit(**{selector.id: unit})

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
        sig.set_theme.emit(theme=self.theme.text)

    def change_theme(self, **kwargs):
        if self.theme.icon == "weather-night":
            self.update_theme_selector('Light')
        elif self.theme.icon == "weather-sunny":
            self.update_theme_selector('Dark')

    def change_lang(self, lang, **kwargs):
        # TODO:
        self.lang.menu.dismiss()
        self.lang.text = lang
        sig.set_lang.emit(lang=lang)


