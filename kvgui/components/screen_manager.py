from kivy.uix.screenmanager import ScreenManager

from kvgui.components import *


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

    def switch_screen(self, screen_name, direction='left', caller=None, **kwargs):
        self.transition.direction = direction
        self.current = screen_name
