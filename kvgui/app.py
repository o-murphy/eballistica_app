from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDActionBottomAppBarButton

from kvgui.components import *
from kivymd.toast import toast

from kvgui.components import abstract
from kvgui.components.ammo_card import AmmoCardScreen
from kvgui.modules import signals as sig
assert abstract


Window.size = (400, 700)


class AppScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(AppScreenManager, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.rifles_screen = RiflesScreen()
        self.ammos_screen = AmmosScreen()
        self.rifle_card_screen = RifleCardScreen()
        self.settings_screen = SettingsScreen()
        self.ammo_card_screen = AmmoCardScreen()

        self.add_widget(self.rifles_screen)
        self.add_widget(self.ammos_screen)
        self.add_widget(self.rifle_card_screen)
        self.add_widget(self.settings_screen)
        self.add_widget(self.ammo_card_screen)


class EBallisticaApp(MDApp):

    def init_ui(self):
        self.screen = Screen()
        self.layout = MDBoxLayout()
        self.layout.orientation = 'vertical'

        self.app_top_bar = AppTopBar()
        self.app_screen_manager = AppScreenManager()
        self.app_bottom_bar = AppBottomBar()

        self.layout.add_widget(self.app_top_bar)
        self.layout.add_widget(self.app_screen_manager)
        self.layout.add_widget(self.app_bottom_bar)

        self.screen.add_widget(self.layout)

    def bind_ui(self):
        sig.top_bar_cog_act.connect(self.switch_settings)
        sig.top_bar_apply_act.connect(self.apply_settings)

        sig.bot_bar_back_act.connect(self.back_action)
        sig.bot_bar_fab_act.connect(self.bot_fab_action)

        sig.rifle_edit_act.connect(self.edit_rifle)
        sig.rifle_del_act.connect(self.del_rifle)
        sig.rifle_item_touch.connect(self.switch_ammos_list)

        sig.ammo_edit_act.connect(self.edit_ammo)
        sig.ammo_del_act.connect(self.del_ammo)
        sig.ammo_item_touch.connect(self.switch_shot_edit)

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Teal'

        self.init_ui()
        self.bind_ui()
        return self.screen

    def on_start(self):
        ...

    def on_bottom_action_buttons(self, action: MDActionBottomAppBarButton):
        if action.icon == "arrow-left":
            self.back_action()

    def back_action(self, **kwargs):
        current = self.app_screen_manager.current
        if current == 'ammos_screen':
            self.switch_rifles_list()
        elif current == 'rifle_card':
            self.switch_rifles_list()
        elif current == 'settings':
            self.switch_rifles_list()

    def bot_fab_action(self, caller, **kwargs):
        current = self.app_screen_manager.current
        fab_icon = caller.icon
        if current == 'rifles_screen' and fab_icon == 'plus':
            self.switch_rifle_card()
        elif current == 'rifle_card' and fab_icon == 'check':
            self.save_rifle_card()

    def switch_shot_edit(self, caller, **kwargs):
        # TODO:
        ...

    def switch_rifles_list(self, **kwargs):
        self.app_screen_manager.transition.direction = 'right'
        self.app_screen_manager.current = 'rifles_screen'
        self.app_bottom_bar.fab_show()
        self.app_bottom_bar.fab_add_new()
        self.app_top_bar.show_cog()

    def edit_rifle(self, caller, **kwargs):
        # TODO
        self.switch_rifle_card()

    def del_rifle(self, caller, **kwargs):
        # TODO
        ...

    def edit_ammo(self, caller, **kwargs):
        # TODO
        self.switch_ammo_card()

    def del_ammo(self, caller, **kwargs):
        # TODO
        ...

    def switch_ammo_card(self, **kwargs):
        self.app_screen_manager.transition.direction = 'left'
        self.app_screen_manager.current = 'ammo_card'
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.hide_all()

    def switch_rifle_card(self, **kwargs):
        self.app_screen_manager.transition.direction = 'left'
        self.app_screen_manager.current = 'rifle_card'
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.hide_all()

    def save_rifle_card(self):
        # Todo:
        self.switch_rifles_list()
        toast("Rifle data saved", duration=1)

    def switch_ammos_list(self, caller, **kwargs):
        # Todo:
        self.app_screen_manager.transition.direction = 'left'
        self.app_screen_manager.current = 'ammos_screen'
        self.app_top_bar.hide_all()

    def switch_settings(self, **kwargs):
        self.app_screen_manager.transition.direction = 'left'
        self.app_screen_manager.current = 'settings'

        self.app_top_bar.show_check()
        self.app_bottom_bar.fab_hide()

    def apply_settings(self, **kwargs):
        # TODO:
        self.switch_rifles_list()
        self.app_top_bar.show_cog()
        toast("Settings saved", duration=1)


if __name__ == '__main__':
    pass
