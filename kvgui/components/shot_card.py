from kivy.uix.screenmanager import Screen

from kvgui.components.measure_widgets import *
from kvgui.components.mixines import MapIdsMixine
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/shot_card.kv')


class ShotCardScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(ShotCardScreen, self).__init__(**kwargs)
        self.name = 'shot_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(ShotCardScreen, self).init_ui()
        self.humidity_suffix.text = '%'
        self.translate_ui()

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        # self.translate_ui()
        ...

    def translate_ui(self, **kwargs):
        self.target_label.text = tr('Target', 'ShotCard')
        self.distance_label.text = tr('Distance', 'ShotCard')
        self.look_angle_label.text = tr('Look angle', 'ShotCard')
        self.atmo_label.text = tr('Atmosphere', 'ShotCard')
        self.altitude_label.text = tr('Altitude', 'ShotCard')
        self.pressure_label.text = tr('Pressure', 'ShotCard')
        self.temperature_label.text = tr('Temperature', 'ShotCard')
        self.humidity_label.text = tr('Humidity', 'ShotCard')
        self.wind_speed_label.text = tr('Wind speed', 'ShotCard')
        self.wind_dir_label.text = tr('Wind angle', 'ShotCard')
        self.one_shot.text = tr('One shot', 'ShotCard')
        self.trajectory.text = tr('Trajectory', 'ShotCard')

    def bind_ui(self):
        self.one_shot.bind(on_release=lambda x: sig.one_shot_act.emit(caller=self))
        self.trajectory.bind(on_release=lambda x: sig.trajectory_act.emit(caller=self))
        sig.set_settings.connect(self.on_set_settings)
        sig.translator_update.connect(self.translate_ui)

    def on_set_settings(self, **kwargs):

        def set_unit_for_target(target, target_suffix, key):
            if kwargs.get(key):
                unit = kwargs.get(key)
                if unit:
                    target.unit = unit
                    target_suffix.text = tr(target.measure.name(target.unit), 'Unit')

        set_unit_for_target(self.distance, self.distance_suffix, 'unit_distance')
        set_unit_for_target(self.altitude, self.altitude_suffix, 'unit_distance')
        set_unit_for_target(self.look_angle, self.look_angle_suffix, 'unit_angular')
        set_unit_for_target(self.pressure, self.pressure_suffix, 'unit_pressure')
        set_unit_for_target(self.temperature, self.temperature_suffix, 'unit_temperature')
        set_unit_for_target(self.wind_speed, self.wind_speed_suffix, 'unit_velocity')
        set_unit_for_target(self.wind_angle, self.wind_angle_suffix, 'unit_angular')

    def on_enter(self, *args):
        ...
