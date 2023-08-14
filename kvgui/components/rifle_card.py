from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField

from kvgui.components.abstract import FormSelector
from kvgui.components.measure_widgets import SightHeightValue, TwistValue
from datatypes.defines import TwistDir
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/rifle_card.kv')


class TwistDirSelector(FormSelector):
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


class RifleCardScreen(Screen):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):

        for uid in self.ids:
            child = self.ids[uid]
            if hasattr(child, 'text') and not isinstance(child, MDTextField):
                child.text = tr(child.text, ctx='RifleCard')

        self.sight_height: SightHeightValue = self.ids.sight_height
        self.sight_height_suffix = self.ids.sight_height_suffix

        self.twist_dir = self.ids.td_v

        self.twist: TwistValue = self.ids.twist
        self.twist_suffix = self.ids.twist_suffix

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

        set_unit_for_target(self.twist, self.twist_suffix, 'unit_distance')
        set_unit_for_target(self.sight_height, self.sight_height_suffix, 'unit_distance')
