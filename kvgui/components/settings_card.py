from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from kvgui.components.abstract import FormSelector
from kvgui.components.mixines import MapIdsMixine
from kvgui.components.unit_widgets import *
from modules import signals as sig
from modules.translator import translate as tr, app_translator
from modules.settings import app_settings


class LanguageSelector(FormSelector, MapIdsMixine):
    pass


class SettingsScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.name = 'settings'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(SettingsScreen, self).init_ui()
        self.translate_ui()

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        # self.translate_ui()
        ...

    def translate_ui(self, **kwargs):
        self.ids.view_title.text = tr('View', ctx='SettingsScreen')
        self.ids.theme_label.text = tr('Theme', ctx='SettingsScreen')
        self.ids.theme.text = tr('Dark', ctx='SettingsScreen')
        self.ids.lang_label.text = tr('Language', ctx='SettingsScreen')
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

        self.theme.bind(on_release=lambda action: self.change_theme())
        self.lang.bind(on_release=self.on_lang_dropdown)

        sig.load_set_theme.connect(self.update_theme_selector)
        sig.load_set_lang.connect(self.change_lang)

        sig.load_setting.connect(self.on_load_settings)
        # sig.on_set_settings.connect(self.on_load_settings)

        sig.translator_update.connect(self.translate_ui)

        for k, uid in self.ids.items():
            if isinstance(uid, UnitSelector):
                uid.bind(on_release=self.on_unit_dropdown)

        self.on_load_settings(**app_settings.current_settings)

    def on_load_settings(self, **kwargs):
        for k, v in kwargs.items():
            found_child = self.ids.get(k)
            if isinstance(found_child, UnitSelector):
                self.set_unit(found_child, v)

    def set_unit(self, selector, unit, **kwargs):
        text = tr(selector.unit_class.name(unit), 'Unit')
        self.on_menu_action(selector, text)
        sig.set_settings.emit(**{selector.id: unit})

    def on_menu_action(self, caller=None, text=None):
        caller.text = text
        caller.menu.dismiss()

    def on_lang_dropdown(self, caller: LanguageSelector = None):
        # self.lang.menu.items = [
        #     {"text": "English", "on_release": lambda: self.change_lang(lang='English')},
        #     {"text": "Ukrainian", "on_release": lambda: self.change_lang(lang='Ukrainian')},
        # ]
        self.lang.menu.items = [
            {"text": lang, "on_release": lambda lang=lang: self.change_lang(lang=lang)}
            for lang in app_translator.translations
        ]
        self.lang.menu.open()

    def on_unit_dropdown(self, caller: UnitSelector):

        def create_unit_menu(selector: UnitSelector):
            if selector.unit_class and selector.units_specified:
                selector.menu.items = [
                    {
                        "text": tr(selector.unit_class.name(unit), ctx='Unit'),
                        "on_release": lambda selector=selector, unit=unit:
                        self.set_unit(selector=selector, unit=unit)
                    } for unit in selector.units_specified
                ]

        if hasattr(caller, 'menu'):
            create_unit_menu(caller)
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
        self.lang.menu.dismiss()
        self.lang.text = lang
        sig.set_lang.emit(lang=lang)
        self.on_load_settings(**app_settings.current_settings)
