from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

from kvgui.components.measure_widgets import *
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/shot_card.kv')


class ShotCardScreen(Screen):
    def __init__(self, **kwargs):
        super(ShotCardScreen, self).__init__(**kwargs)
        self.name = 'shot_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        for uid in self.ids:
            child = self.ids[uid]
            if hasattr(child, 'text') and not isinstance(child, MDTextField):
                child.text = tr(child.text, ctx='ShotCard')

        # convertable values
        self.distance: DistanceValue = self.ids.distance
        self.distance_suffix = self.ids.distance_suffix
        self.look_angle: LookAngleValue = self.ids.look_angle
        self.look_angle_suffix = self.ids.look_angle_suffix
        self.altitude: AltitudeValue = self.ids.altitude
        self.altitude_suffix = self.ids.altitude_suffix
        self.pressure: PressureValue = self.ids.pressure
        self.pressure_suffix = self.ids.pressure_suffix
        self.temperature: TemperatureValue = self.ids.temperature
        self.temperature_suffix = self.ids.temperature_suffix
        self.wind_speed: WindSpeedValue = self.ids.wind_speed
        self.wind_speed_suffix = self.ids.wind_speed_suffix
        self.wind_angle: WindAngleValue = self.ids.wind_angle
        self.wind_angle_suffix = self.ids.wind_angle_suffix

        # not need conversion values
        self.humidity = self.ids.humidity

        # special actions
        self.one_shot: MDRaisedButton = self.ids.one_shot
        self.trajectory: MDRaisedButton = self.ids.trajectory

    def bind_ui(self):
        self.one_shot.bind(on_release=lambda x: sig.one_shot_act.emit(caller=self))
        self.trajectory.bind(on_release=lambda x: sig.trajectory_act.emit(caller=self))
        sig.set_settings.connect(self.on_set_settings)

    def on_set_settings(self, **kwargs):

        def set_unit_for_target(target, target_suffix, key):
            if kwargs.get(key):
                unit = kwargs.get(key)
                if unit:
                    target.unit = unit
                    target_suffix.text = tr(target.measure.name(target.unit), 'Unit')

        set_unit_for_target(self.distance, self.distance_suffix, 'unit_distance')
        set_unit_for_target(self.look_angle, self.look_angle_suffix, 'unit_angular')
        set_unit_for_target(self.pressure, self.pressure_suffix, 'unit_pressure')
        set_unit_for_target(self.temperature, self.temperature_suffix, 'unit_temperature')
        set_unit_for_target(self.wind_speed, self.wind_speed_suffix, 'unit_velocity')
        set_unit_for_target(self.wind_angle, self.wind_angle_suffix, 'unit_angular')

    def on_enter(self, *args):
        ...
