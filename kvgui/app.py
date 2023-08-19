from kivy import platform
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_hex_from_color
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
from kvgui.components.one_shot_screen import OneShotScreen
from kvgui.components.powder_sens_calc import PowderSensScreen
from kvgui.components.shot_card import ShotCardScreen
from kvgui.components.spinner import WaitMe
from kvgui.components.trajectory_screen import TrajectoryScreen
from kvgui.modules import signals as sig
from kvgui.modules.settings import app_settings
from kvgui.modules.translator import translate as tr

from datatypes.dbworker import Worker, RifleData

assert app_settings
assert abstract

if platform == 'win':
    Window.size = (500, 700)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    # Config.set('graphics', 'multisamples', '0')  # Disable anti-aliasing (optional)
    # Config.set('graphics', 'gl_backend', 'angle_sdl2')  # Use OpenGL backend
    # Config.set('graphics', 'verify_gl_main_thread', 0)  # Use OpenGL backend


class AppState:
    rifle: None
    ammo: None
    shot: None


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
        self.powder_sens_calc = PowderSensScreen()

        self.one_shot_screen = OneShotScreen()
        self.trajectory_screen = TrajectoryScreen()

        self.add_widget(self.rifles_screen)
        self.add_widget(self.ammos_screen)
        self.add_widget(self.rifle_card_screen)
        self.add_widget(self.settings_screen)
        self.add_widget(self.ammo_card_screen)
        self.add_widget(self.shot_card_screen)
        self.add_widget(self.bc_edit)
        self.add_widget(self.cdm_editor)
        self.add_widget(self.powder_sens_calc)
        self.add_widget(self.one_shot_screen)
        self.add_widget(self.trajectory_screen)


class EBallisticaApp(MDApp):

    def init_ui(self):
        self.screen = Screen()
        self.layout = MDBoxLayout()
        self.layout.orientation = 'vertical'

        self.app_top_bar = AppTopBar()
        self.app_screen_manager = AppScreenManager()
        self.app_bottom_bar = AppBottomBar()

        self.spinner = WaitMe()

        self.layout.add_widget(self.app_top_bar)
        self.layout.add_widget(self.app_screen_manager)
        self.layout.add_widget(self.app_bottom_bar)

        self.screen.add_widget(self.layout)
        self.screen.add_widget(self.spinner)

        self.switch_rifles_list()

    def wait_me(self, **kwargs):
        self.spinner.active = True

    def unwait_me(self, **kwargs):
        self.spinner.active = False

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

        sig.one_shot_act.connect(self.switch_one_shot)
        sig.trajectory_act.connect(self.switch_trajectory)
        # sig.trajectory_preloaded.connect(self.switch_trajectory)

        self.app_screen_manager.rifles_screen.on_enter = self.app_top_bar.show_cog
        self.app_screen_manager.rifles_screen.on_leave = self.app_top_bar.hide_all

        sig.toast.connect(self.toast)

        sig.wait_me.connect(self.wait_me)
        sig.unwait_me.connect(self.unwait_me)

    def build(self):
        # self.theme_cls.theme_style_switch_animation = True  # uncomment if animation needed
        # self.theme_cls.theme_style_switch_animation_duration = 0.2  # uncomment if animation needed
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "800"

        self.app_state = AppState()

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
            self.show_exit_confirmation(self)
        elif current in ['one_shot', 'traj_screen']:
            self.switch_shot_edit('right')

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
            self.edit_rifle(caller=caller, **kwargs)
        elif current == 'ammos_screen':
            self.switch_shot_edit('left')
        elif current == 'rifle_card':
            self.save_rifle_card()
        elif current == 'ammo_card':
            self.save_ammo_card()
        elif current == 'shot_card':
            self.save_shot_card()

    def save_rifle_card(self):
        rifle = self.app_state.rifle
        new_data = self.app_screen_manager.rifle_card_screen.get()
        if rifle:
            Worker.rifle_add_or_update(id=rifle.id, **new_data)
        else:
            Worker.rifle_add_or_update(**new_data)
        self.app_state.rifle = None
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

    # def new_rifle(self, caller, **kwargs):
    #     self.switch_rifle_card('left', caller=caller)

    def edit_rifle(self, caller=None, **kwargs):

        if caller == self.app_bottom_bar.bottom_bar_fab:
            self.app_state.rifle = RifleData()
        elif isinstance(caller, RifleListItem):
            self.app_state.rifle = Worker.get_rifle(caller.dbid)

        self.app_screen_manager.rifle_card_screen.display(self.app_state.rifle)

        self.switch_rifle_card('left', caller=caller)

    def del_rifle(self, caller, **kwargs):
        if isinstance(caller, RifleListItem):
            Worker.delete_rifle(caller.dbid)
            rifles = Worker.list_rifles().all()
            self.app_screen_manager.rifles_screen.display(rifles)

    def edit_ammo(self, caller=None, **kwargs):
        # TODO
        self.switch_ammo_card('left')

    def del_ammo(self, caller, **kwargs):
        # TODO
        ...

    def switch_one_shot(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'one_shot'
        self.app_bottom_bar.fab_hide()
        self.app_top_bar.breadcrumb = [
            'Rifles', '{rifle name}', 'Ammos', '{ammo name}', 'Shot'
        ]

    # def pre_switch_trajectory(self, **kwargs):
    #     # sig.wait_me.emit()
    #     self.app_screen_manager.trajectory_screen.preload()

    def switch_trajectory(self, direction='left', caller=None, **kwargs):
        sig.unwait_me.emit()
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'traj_screen'
        self.app_bottom_bar.fab_hide()
        self.app_top_bar.breadcrumb = [
            'Rifles', '{rifle name}', 'Ammos', '{ammo name}', 'Trajectory'
        ]

    def switch_shot_edit(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.transition.direction = direction
        self.app_screen_manager.current = 'shot_card'
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.breadcrumb = [
            'Rifles', '{rifle name}', 'Ammos', '{ammo name}', 'Shot data'
        ]

    def switch_rifles_list(self, direction='left', caller=None, **kwargs):

        rifles = Worker.list_rifles().all()

        self.app_screen_manager.rifles_screen.display(rifles)

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

    def toast(self, text='', duration=2.5, **kwargs):
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
