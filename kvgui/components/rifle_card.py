from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField

from kvgui.components.abstract import FormSelector
from kvgui.components.mapid import MapIdsMixine
from kvgui.components.measure_widgets import SightHeightValue, TwistValue
from datatypes.defines import TwistDir
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/rifle_card.kv')


class TwistDirSelector(FormSelector, MapIdsMixine):
    def __init__(self, **kwargs):
        super(TwistDirSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()
        self.value = TwistDir.Right  # TODO: must be Enum

    def init_ui(self):
        self.text = tr(self.text, 'RifleCard')

    def bind_ui(self):
        self.bind(on_release=self.change_twist)

    def change_twist(self, *args, **kwargs):
        if self.value == TwistDir.Right:
            self.icon = "rotate-left"
            self.text = tr('Left', ctx='RifleCard')
            self.value = TwistDir.Left

        elif self.value == TwistDir.Left:
            self.icon = "rotate-right"
            self.text = tr('Right', ctx='RifleCard')
            self.value = TwistDir.Right


class RifleCardScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(RifleCardScreen, self).init_ui()
        self.translate_ui()

    def translate_ui(self):
        self.name_label.text = tr('Name', 'RifleCard')
        self.prop_title_label.text = tr('Properties', 'RifleCard')
        self.sight_height_label.text = tr('Sight height', 'RifleCard')
        self.twist_label.text = tr('Sight height', 'RifleCard')
        self.twist_dir_label.text = tr('Twist direction', 'RifleCard')

    def bind_ui(self):
        sig.set_settings.connect(self.on_set_settings)

    def on_enter(self, *args):
        ...

    def on_set_settings(self, **kwargs):

        def set_unit_for_target(target, target_suffix, key):
            if kwargs.get(key):
                unit = kwargs.get(key)
                if unit:
                    target.unit = unit
                    target_suffix.text = tr(target.measure.name(target.unit), 'Unit')

        set_unit_for_target(self.twist, self.twist_suffix, 'unit_twist')
        set_unit_for_target(self.sight_height, self.sight_height_suffix, 'unit_sight_height')
