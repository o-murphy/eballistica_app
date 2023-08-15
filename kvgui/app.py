from kivy import platform
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDActionBottomAppBarButton

from datatypes.defines import DragModel
from kvgui.components import *
from kvgui.components import abstract
from kvgui.components.ammo_card import AmmoCardScreen
from kvgui.components.dm_bc_editor import BCEditor
from kvgui.components.dm_cdm_editor import CDMEditor
from kvgui.components.shot_card import ShotCardScreen
from kvgui.modules import signals as sig
from kvgui.modules.settings import app_settings
# from kvgui.modules.translator import create_translation_template
from kvgui.modules.translator import translate as tr

assert app_settings
assert abstract

if platform == 'win':
    Window.size = (500, 700)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


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
        self.shot_card_screen = ShotCardScreen()

        self.bc_edit = BCEditor()
        self.cdm_editor = CDMEditor()

        self.add_widget(self.rifles_screen)
        self.add_widget(self.ammos_screen)
        self.add_widget(self.rifle_card_screen)
        self.add_widget(self.settings_screen)
        self.add_widget(self.ammo_card_screen)
        self.add_widget(self.shot_card_screen)
        self.add_widget(self.bc_edit)
        self.add_widget(self.cdm_editor)


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
        self.switch_rifles_list()

    def change_theme(self, theme='Dark', **kwargs):
        self.theme_cls.theme_style = (
            "Dark" if theme == "Dark" else "Light"
        )
        self.layout.md_bg_color = (
            self.theme_cls.bg_dark if self.theme_cls.theme_style == "Dark" else self.theme_cls.bg_light
        )

    def bind_ui(self):
        Window.bind(on_keyboard=self.droid_back_act)

        sig.set_theme.connect(self.change_theme)

        sig.top_bar_cog_act.connect(self.switch_settings)
        # sig.top_bar_apply_act.connect(self.apply_settings)

        sig.bot_bar_back_act.connect(self.back_action)
        sig.bot_bar_fab_act.connect(self.bot_fab_action)

        sig.rifle_edit_act.connect(self.edit_rifle)
        sig.rifle_del_act.connect(self.del_rifle)
        sig.rifle_item_touch.connect(self.switch_ammos_list)

        sig.ammo_edit_act.connect(self.edit_ammo)
        sig.ammo_del_act.connect(self.del_ammo)
        sig.ammo_item_touch.connect(self.switch_shot_edit)

        sig.bot_bar_back_act.connect(self.back_action)

        sig.drag_model_edit_act.connect(self.switch_drag_model_edit)

        self.app_screen_manager.rifles_screen.on_enter = self.app_top_bar.show_cog
        self.app_screen_manager.rifles_screen.on_leave = self.app_top_bar.hide_all

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.2
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.primary_hue = "700"
        # self.theme_cls.accent_palette = 'Orange'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "800"

        self.init_ui()
        self.bind_ui()

        app_settings.bind_on_load()
        app_settings.bind_on_set()
        return self.screen

    def on_start(self):
        ...

    def droid_back_act(self, window, key, *args):
        if key == 27:
            sig.bot_bar_back_act.emit()

    def on_bottom_action_buttons(self, action: MDActionBottomAppBarButton):
        if action.icon == "arrow-left":
            self.back_action()

    def back_action(self, **kwargs):
        current = self.app_screen_manager.current
        if current == 'ammos_screen':
            self.switch_rifles_list('right')
        elif current == 'rifle_card':
            self.switch_rifles_list('right')
        elif current == 'settings':
            self.switch_rifles_list('right')
        elif current == 'ammo_card':
            self.switch_ammos_list('right')
        elif current == 'shot_card':
            self.switch_ammos_list('right')
        elif current in ['bc_editor_screen', 'cdm_editor_screen']:
            self.switch_ammo_card('right')
        elif current == 'rifles_screen':
            # self.stop()
            self.show_exit_confirmation(self)

    def show_exit_confirmation(self, instance):
        # Todo: refactor
        self.dialog = MDDialog(
            text=tr('Are you sure you want to exit?', 'root'),
            buttons=[
                MDRaisedButton(
                    text=tr("No", 'root'),
                    theme_text_color="Custom",
                    # text_color=self.theme_cls.se,
                    on_release=lambda x: self.close_exit_dialog(False)
                ),
                MDRectangleFlatButton(
                    text=tr("Yes", 'root'),
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.close_exit_dialog(True)
                ),
            ],
        )
        self.dialog.open()

    def close_exit_dialog(self, action):
        if action:
            self.stop()
        else:
            self.dialog.dismiss()

    def bot_fab_action(self, caller=None, **kwargs):
        current = self.app_screen_manager.current
        if current == 'rifles_screen':
            self.switch_rifle_card('left')
        elif current == 'ammos_screen':
            self.switch_shot_edit('left')
        elif current == 'rifle_card':
            self.save_rifle_card()
        elif current == 'ammo_card':
            self.save_ammo_card()
        elif current == 'shot_card':
            self.save_shot_card()

    def save_rifle_card(self):
        # Todo:
        self.switch_rifles_list('right')
        self.toast(tr("Rifle data saved"), duration=1)

    def save_ammo_card(self):
        # Todo:
        self.switch_ammos_list('right')
        self.toast(tr("Ammo data saved"), duration=1)

    def save_shot_card(self):
        # Todo:
        self.switch_ammos_list('right')
        self.toast(tr("Shot data saved"), duration=1)

    def edit_rifle(self, caller=None, **kwargs):
        # TODO
        self.switch_rifle_card('left')

    def del_rifle(self, caller, **kwargs):
        # TODO
        ...

    def edit_ammo(self, caller=None, **kwargs):
        # TODO
        self.switch_ammo_card('left')

    def del_ammo(self, caller, **kwargs):
        # TODO
        ...

    def switch_shot_edit(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'shot_card'
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.breadcrumb = [
            'Rifles', '{rifle name}', 'Ammos', '{ammo name}', 'Shot data'
        ]

    def switch_rifles_list(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'rifles_screen'
        self.app_bottom_bar.fab_add_new()
        self.app_top_bar.breadcrumb = ['Rifles']

    def switch_ammo_card(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'ammo_card'
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.breadcrumb = [
            'Rifles', '{rifle name}', 'Ammos', '{ammo name}', 'Properties'
        ]

    def switch_rifle_card(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'rifle_card'
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.breadcrumb = ['Rifles', '<rifle name>']

    def switch_ammos_list(self, direction='left', caller=None, **kwargs):
        # Todo:
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'ammos_screen'
        self.app_bottom_bar.fab_add_new()
        self.app_top_bar.breadcrumb = ['Rifles', '<rifle name>', 'Ammos']

    def switch_settings(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'settings'
        self.app_bottom_bar.fab_hide()
        self.app_top_bar.breadcrumb = ['Settings']

    def switch_drag_model_edit(self, drag_model: DragModel, **kwargs):
        self.app_screen_manager.transition.direction = 'left'
        self.app_bottom_bar.fab_hide()
        if drag_model in [DragModel.G7, DragModel.G1]:
            self.app_screen_manager.current = 'bc_editor_screen'
        elif drag_model == DragModel.CDM:
            self.app_screen_manager.current = 'cdm_editor_screen'

    def toast(self, text='', duration=2.5):
        try:
            if platform == 'android':
                toast(text=text, gravity=80, length_long=duration)
            else:
                toast(text=text, duration=duration)
        except Exception:
            toast(text=text)

    def on_stop(self):
        # # TODO: temporary
        # print('creating translation template')
        # create_translation_template()
        pass


if __name__ == '__main__':
    pass
