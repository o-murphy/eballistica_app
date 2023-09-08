import logging

from kivy import platform
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDActionBottomAppBarButton

from calculate.calculate import calculate_traj
from datatypes.dbworker import Worker, RifleData, AmmoData
from datatypes.defines import DragModel
from kvgui.components import *
from modules import signals as sig
from modules.env import IS_ANDROID
from modules.settings import app_settings
from modules.translator import translate as tr

assert app_settings

if platform == 'win' or platform == 'linux':
    Window.size = (600, 700)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class AppState:
    rifle: None
    ammo: None


class EBallisticaApp(MDApp):

    def init_ui(self):
        # self.screen = Screen()
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

        sig.bot_bar_back_act.connect(self.back_action)
        sig.bot_bar_fab_act.connect(self.bot_fab_action)

        sig.rifle_edit_act.connect(self.edit_rifle)
        sig.rifle_del_act.connect(self.del_rifle)
        sig.rifle_item_touch.connect(self.switch_ammos_list)

        sig.ammo_edit_act.connect(self.edit_ammo)
        sig.ammo_del_act.connect(self.del_ammo)
        sig.ammo_item_touch.connect(self.edit_shot)

        sig.bot_bar_back_act.connect(self.back_action)

        sig.drag_model_edit_act.connect(self.switch_drag_model_edit)

        sig.one_shot_act.connect(self.switch_one_shot)
        sig.trajectory_act.connect(self.switch_trajectory)

        self.app_screen_manager.rifles_screen.on_enter = self.app_top_bar.show_cog
        self.app_screen_manager.rifles_screen.on_leave = self.app_top_bar.hide_all

        sig.wait_me.connect(self.wait_me)
        sig.unwait_me.connect(self.unwait_me)

    def build(self):
        # NOTE: freezes on low-end devices
        # self.theme_cls.theme_style_switch_animation = True  # uncomment if animation needed
        # self.theme_cls.theme_style_switch_animation_duration = 0.2  # uncomment if animation needed

        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "800"

        self.app_state = AppState()
        self.screen = Screen()
        # self.init_ui()
        # self.bind_ui()
        #
        # app_settings.bind_on_load()
        # app_settings.bind_on_set()
        # self.switch_rifles_list()

        return self.screen

    def on_start(self):
        if IS_ANDROID:
            self.first_run_dialog()

        self.init_ui()
        self.bind_ui()

        app_settings.bind_on_load()
        app_settings.bind_on_set()
        self.switch_rifles_list()

    def first_run_dialog(self):
        if app_settings.first_run:
            self.dialog = MDDialog(
                title=f"[color=FFA726]{tr('WARNING', 'root')}[/color]",
                text=tr("Before deleting the app, make a backup of your local data in settings"),
                buttons=[
                    MDFlatButton(
                        text=tr("Don't show again", 'root'),
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: (self.dialog.dismiss(),
                                              app_settings.update(first_run=False))
                    ),
                    MDRectangleFlatButton(
                        text=tr("Ok", 'root'),
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )

            self.dialog.open()

    def droid_back_act(self, window, key, *args):
        if key == 27:
            sig.bot_bar_back_act.emit()

    def on_bottom_action_buttons(self, action: MDActionBottomAppBarButton):
        if action.icon == "arrow-left":
            self.back_action()

    def back_action(self, **kwargs):
        current = self.app_screen_manager.current
        Worker.rollback()
        if current == 'ammos_screen':
            self.switch_rifles_list('right')
        elif current == 'rifle_card_screen':
            self.switch_rifles_list('right')
        elif current == 'settings_screen':
            self.switch_rifles_list('right')
        elif current == 'ammo_card_screen':
            self.switch_ammos_list('right')
        elif current == 'shot_card_screen':
            self.switch_ammos_list('right')
        elif current in ['bc_editor_screen', 'cdm_editor_screen']:
            self.switch_ammo_card('right')
        elif current == 'rifles_screen':
            self.show_exit_confirmation()
        elif current in ['one_shot_screen', 'trajectory_screen']:
            self.switch_shot_edit('right')

    def show_exit_confirmation(self):
        self.dialog = MDDialog(
            title="Exit",
            text=tr('Are you sure you want to exit?', 'root'),
            buttons=[
                MDRaisedButton(
                    text=tr("No", 'root'),
                    theme_text_color="Custom",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRectangleFlatButton(
                    text=tr("Yes", 'root'),
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.stop()
                ),
            ],
        )
        self.dialog.open()

    def bot_fab_action(self, caller=None, **kwargs):
        current = self.app_screen_manager.current

        if current == 'rifles_screen':
            self.edit_rifle(caller=caller, **kwargs)
        elif current == 'ammos_screen':
            self.edit_ammo(caller=caller, **kwargs)
        elif current == 'rifle_card_screen':
            self.save_rifle_card()
        elif current == 'ammo_card_screen':
            self.save_ammo_card()
        elif current == 'shot_card_screen':
            self.save_shot_card()
        elif current == 'bc_editor_screen':
            self.update_card_bc()
        elif current == 'cdm_editor_screen':
            self.update_card_cdm()

    def update_card_bc(self):
        drag_data = self.app_screen_manager.bc_editor_screen.get()
        sig.bc_data_edited.emit(drag_data=drag_data)
        self.switch_ammo_card('right')
        sig.toast.emit(text=tr('BC changed', 'root'))

    def update_card_cdm(self):
        # drag_data = self.app_screen_manager.cdm_editor.get()
        # sig.cdm_data_edited.emit(drag_data=drag_data)
        # TODO:
        self.switch_ammo_card('right')
        sig.toast.emit(text=tr('CDM changed', 'root'))

    def save_rifle_card(self):
        rifle = self.app_state.rifle
        new_data = self.app_screen_manager.rifle_card_screen.get()
        if rifle:
            Worker.rifle_add_or_update(id=rifle.id, **new_data)
        else:
            Worker.rifle_add_or_update(**new_data)
        self.app_state.rifle = None
        self.switch_rifles_list('right')
        sig.toast.emit(text=tr("Rifle data saved"), duration=1)

    def save_ammo_card(self):

        if not self.app_screen_manager.ammo_card_screen.validate():
            sig.toast.emit(text=tr('Wrong drag model data', 'root'), duration=1)
            return

        ammo = self.app_screen_manager.ammo_card_screen.get_ammo()
        zero = self.app_screen_manager.ammo_card_screen.get_zero()
        for k, v in ammo.items():
            self.app_state.ammo.__setattr__(k, v)
        for k, v in zero.items():
            self.app_state.ammo.zerodata.__setattr__(k, v)

        if self.app_state.ammo.id:
            Worker.commit()
            sig.toast.emit(text=tr("Ammo data saved"), duration=1)
        elif self.app_state.ammo:
            Worker.ammo_add(self.app_state.ammo)
            sig.toast.emit(text=tr("Ammo data saved"), duration=1)
        else:
            self.undefined_error()

        self.app_state.ammo = None
        self.switch_ammos_list('right')

    def save_shot_card(self):
        target = self.app_screen_manager.shot_card_screen.get_target()
        atmo = self.app_screen_manager.shot_card_screen.get_atmo()

        for k, v in target.items():
            self.app_state.ammo.target.__setattr__(k, v)

        for k, v in atmo.items():
            self.app_state.ammo.atmo.__setattr__(k, v)

        if self.app_state.ammo:
            Worker.commit()
            sig.toast.emit(text=tr("Shot data saved"), duration=1)
        else:
            self.undefined_error()

        self.app_state.ammo = None
        self.switch_ammos_list('right')

    def edit_rifle(self, caller=None, **kwargs):

        if caller == self.app_bottom_bar.bottom_bar_fab:
            self.app_state.rifle = RifleData()
        elif isinstance(caller, RifleListItem):
            self.app_state.rifle = Worker.get_rifle(caller.dbid)
        else:
            self.undefined_error()
            return

        self.app_screen_manager.rifle_card_screen.display(self.app_state.rifle)
        self.switch_rifle_card('left', caller=caller)

    def del_rifle(self, caller, **kwargs):
        if isinstance(caller, RifleListItem):
            Worker.delete_rifle(caller.dbid)
            rifles = Worker.list_rifles().all()
            self.app_screen_manager.rifles_screen.display(rifles)
        else:
            self.undefined_error()

    def edit_ammo(self, caller=None, **kwargs):
        if caller == self.app_bottom_bar.bottom_bar_fab:
            self.app_state.ammo = AmmoData(rifle=self.app_state.rifle)
        elif isinstance(caller, AmmoListItem):
            self.app_state.ammo = Worker.get_ammo(caller.dbid)
        else:
            self.undefined_error()
            return

        self.app_screen_manager.ammo_card_screen.display(self.app_state.ammo)
        self.switch_ammo_card('left')

    def edit_shot(self, caller=None, **kwargs):

        if isinstance(caller, AmmoListItem):
            self.app_state.ammo = Worker.get_ammo(caller.dbid)
            self.app_screen_manager.shot_card_screen.display(self.app_state.ammo)
            self.switch_shot_edit('left')
        else:
            self.undefined_error()

    def del_ammo(self, caller, **kwargs):
        if isinstance(caller, AmmoListItem):
            Worker.delete_ammo(caller.dbid)
            ammos = Worker.list_ammos().all()
            self.app_screen_manager.ammos_screen.display(ammos)
        else:
            self.undefined_error()

    @staticmethod
    def undefined_error():
        sig.toast.emit(text=tr('Undefined error expected', 'root'))

    def switch_one_shot(self, direction='left', caller=None, **kwargs):
        self.app_screen_manager.switch_screen('one_shot_screen', direction)

        self.app_bottom_bar.fab_hide()
        self.app_top_bar.breadcrumb = [
            self.app_state.rifle.name, self.app_state.ammo.name, 'Shot'
        ]

    def switch_trajectory(self, direction='left', **kwargs):

        try:
            state = self.app_state
            cdm, traj = calculate_traj(state.rifle, state.ammo, state.ammo.target, state.ammo.atmo, state.ammo.zerodata)
        except Exception as exc:
            sig.toast.emit(text=tr('Error occurred on calculation', 'root'), duration=1)
            logging.warning(exc)
            return

        self.app_screen_manager.trajectory_screen.display_data(traj, cdm)
        self.app_screen_manager.switch_screen('trajectory_screen', direction)

        self.app_bottom_bar.fab_hide()
        self.app_top_bar.breadcrumb = [
            self.app_state.rifle.name, self.app_state.ammo.name, 'Trajectory'
        ]

    def switch_shot_edit(self, direction='left', **kwargs):
        self.app_screen_manager.switch_screen('shot_card_screen', direction)
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.breadcrumb = [
            self.app_state.rifle.name, self.app_state.ammo.name, 'Shot data'
        ]

    def switch_rifles_list(self, direction='left', **kwargs):

        rifles = Worker.list_rifles().all()

        self.app_screen_manager.rifles_screen.display(rifles)
        self.app_screen_manager.switch_screen('rifles_screen', direction)
        self.app_bottom_bar.fab_add_new()
        self.app_top_bar.breadcrumb = ['Rifles']

    def switch_ammo_card(self, direction='left', **kwargs):
        self.app_screen_manager.switch_screen('ammo_card_screen', direction)
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.breadcrumb = [
            self.app_state.rifle.name, self.app_state.ammo.name, 'Properties'
        ]

    def switch_rifle_card(self, direction='left', **kwargs):
        self.app_screen_manager.switch_screen('rifle_card_screen', direction)
        self.app_bottom_bar.fab_applying()
        self.app_top_bar.breadcrumb = [self.app_state.rifle.name, 'Properties']

    def switch_ammos_list(self, direction='left', caller=None, **kwargs):
        if isinstance(caller, RifleListItem):
            self.app_state.rifle = Worker.get_rifle(caller.dbid)
        if self.app_state.rifle is None:
            sig.toast.emit(text=tr('Data not found', 'root'))
            return
        ammos = Worker.list_ammos(rifle=self.app_state.rifle).all()
        self.app_screen_manager.ammos_screen.display(ammos)
        self.app_screen_manager.switch_screen('ammos_screen', direction)
        self.app_bottom_bar.fab_add_new()
        self.app_top_bar.breadcrumb = [self.app_state.rifle.name]

    def switch_settings(self, direction='left', **kwargs):
        self.app_screen_manager.switch_screen('settings_screen', direction)
        self.app_bottom_bar.fab_hide()
        self.app_top_bar.breadcrumb = ['Settings']

    def switch_drag_model_edit(self, drag_model: DragModel, **kwargs):
        if drag_model in [DragModel.G7, DragModel.G1]:
            self.app_screen_manager.switch_screen('bc_editor_screen')
        elif drag_model == DragModel.CDM:
            self.app_screen_manager.switch_screen('cdm_editor_screen')
        self.app_bottom_bar.fab_show()

    def on_stop(self):
        # print('creating translation template')
        # create_translation_template()
        pass


if __name__ == '__main__':
    pass
