from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from datatypes.dbworker import RifleData
from kvgui.components.abstract import FormSelector
from kvgui.components.mixines import MapIdsMixine
from datatypes.defines import TwistDir
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/rifle_card.kv')


class TwistDirSelector(FormSelector, MapIdsMixine):
    def __init__(self, **kwargs):
        super(TwistDirSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()
        self.value = TwistDir.Right

    def init_ui(self):
        # self.text = tr('Right', ctx='RifleCard')
        self.translate_ui()

    def translate_ui(self, **kwargs):
        ...

    def bind_ui(self):
        self.bind(on_release=self.change_twist)
        sig.translator_update.connect(self.translate_ui)

    def change_twist(self, *args, **kwargs):
        if self.value == TwistDir.Right:
            self.value = TwistDir.Left

        elif self.value == TwistDir.Left:
            self.value = TwistDir.Right

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: TwistDir):
        self._value = value
        if self._value == TwistDir.Right:
            self.icon = "rotate-right"
            self.text = tr('Right', ctx='RifleCard')
        elif self._value == TwistDir.Left:
            self.icon = "rotate-left"
            self.text = tr('Left', ctx='RifleCard')


class RifleCardScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(RifleCardScreen, self).init_ui()
        # self.translate_ui()

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        # self.translate_ui()
        ...

    def translate_ui(self, **kwargs):
        self.name_label.text = tr('Name', 'RifleCard')
        self.prop_title_label.text = tr('Properties', 'RifleCard')
        self.sight_height_label.text = tr('Sight height', 'RifleCard')
        self.twist_label.text = tr('Twist', 'RifleCard')
        self.twist_dir_label.text = tr('Twist direction', 'RifleCard')

    def bind_ui(self):
        sig.set_settings.connect(self.on_set_settings)
        sig.translator_update.connect(self.translate_ui)

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

    def display(self, data: RifleData):
        self.name_input.text = data.name if data.name else tr('New weapon', 'RifleItem')
        self.twist.raw_value = data.barrel_twist
        self.twist_dir.value = data.barrel_twist_dir
        self.sight_height.raw_value = data.sight_height

    def get(self):
        return dict(
            name=self.name_input.text,
            barrel_twist=self.twist.raw_value,
            barrel_twist_dir=self.twist_dir.value,
            sight_height=self.sight_height.raw_value
        )

