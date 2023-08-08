from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.toolbar import MDActionBottomAppBarButton


from kivymd.app import MDApp
from kivy.lang import Builder

from kvgui.components import *
assert RiflesScreen  # temp


Window.size = (400, 700)


class AppScreenManager(ScreenManager):
    pass


class EBallisticaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'BlueGray'

        screen = Builder.load_file('app.kv')
        return screen

    def on_start(self):
        print(self.root.ids.screen_manager.__dir__())
        print(self.root.ids.screen_manager.children)
        print(self.root.ids.screen_manager.screens)
        # self.root.ids.screen_manager.current_screen = self.root.ids.screen_manager.ids.ammos_list

    def get_current_screen(self):
        return self.root.ids.screen_manager.current_screen

    def add_act(self):
        print('add on', self.get_current_screen())

    def on_bottom_action_buttons(self, action: MDActionBottomAppBarButton):
        if action.icon == "arrow-left":
            self.back_action()

    def back_action(self):
        current = self.root.ids.screen_manager.current
        if current == 'ammos_screen':
            self.switch_rifles_list()
        elif current == 'rifle_card':
            self.switch_rifles_list()
        elif current == 'settings':
            self.switch_rifles_list()

    def top_act_click(self, action):
        if action.icon == 'cog-outline':
            self.switch_settings()

    def switch_settings(self):
        self.root.ids.screen_manager.transition.direction = 'right'
        self.root.ids.screen_manager.current = 'settings'

    def switch_rifles_list(self):
        self.root.ids.screen_manager.transition.direction = 'right'
        self.root.ids.screen_manager.current = 'rifles_screen'

    def switch_rifle_card(self):
        self.root.ids.screen_manager.transition.direction = 'left'
        self.root.ids.screen_manager.current = 'rifle_card'

    def switch_ammos_list(self):
        self.root.ids.screen_manager.transition.direction = 'left'
        self.root.ids.screen_manager.current = 'ammos_screen'


EBallisticaApp().run()
