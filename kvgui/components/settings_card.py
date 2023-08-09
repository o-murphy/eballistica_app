from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatIconButton

from kvgui.components.abstract import FormSelector

Builder.load_file('kvgui/kv/settings_card.kv')


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.name = 'settings'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.theme: FormSelector = self.ids.theme_v
        # self.theme.menu.items = [
        #     {"text": "Dark", "leading_icon": "weather-night", "on_release": lambda: self.change_theme(action='Dark')},
        #     {"text": "Light", "leading_icon": "weather-sunny", "on_release": lambda: self.change_theme(action='Light')},
        # ]

        self.lang: FormSelector = self.ids.lang_v
        self.lang.menu.items = [
            {"text": "English", "on_release": lambda: self.change_lang(action='English')},
            {"text": "Ukrainian", "on_release": lambda: self.change_lang(action='Ukrainian')},
        ]

        self.twist: FormSelector = self.ids.unit_tw_v
        self.sh: FormSelector = self.ids.unit_sh_v
        self.sh: FormSelector = self.ids.unit_sh_v

        self.twist.menu.items = [
            {"text": "inch", "on_release": lambda: self.on_menu_action(caller=self.twist, action='inch')},
            {"text": "cm", "on_release": lambda: self.on_menu_action(caller=self.twist, action='cm')},
            {"text": "mm", "on_release": lambda: self.on_menu_action(caller=self.twist, action='mm')},
            {"text": "ln", "on_release": lambda: self.on_menu_action(caller=self.twist, action='ln')}
        ]

        self.sh.menu.items = [
            {"text": "inch", "on_release": lambda: self.on_menu_action(caller=self.sh, action='inch')},
            {"text": "cm", "on_release": lambda: self.on_menu_action(caller=self.sh, action='cm')},
            {"text": "mm", "on_release": lambda: self.on_menu_action(caller=self.sh, action='mm')},
            {"text": "ln", "on_release": lambda: self.on_menu_action(caller=self.sh, action='ln')}
        ]

    def bind_ui(self):
        for uid, widget in self.ids.items():
            if isinstance(widget, FormSelector):
                widget.bind(on_release=self.show_menu)
        self.theme.bind(on_release=lambda x: self.change_theme())

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
            # self.theme.text = action
            # if action == 'Dark':
            #     self.theme.icon = "weather-night"
            # else:
            #     self.theme.icon = "weather-sunny"

    def change_lang(self, action):
        # TODO:
        self.lang.menu.dismiss()
        self.lang.text = action

    def on_menu_action(self, caller, action):
        caller.text = action
        caller.menu.dismiss()

    def show_menu(self, caller):
        if hasattr(caller, 'name') and hasattr(caller, 'menu'):
            caller.menu.open()
