from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField

from kvgui.components.abstract import FormSelector
from kvgui.components.numeric_field import MDUnitsInput
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr
from units import Convertor, Distance
from datatypes.dbworker import TwistDir

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

        self.sight_height: MDUnitsInput = self.ids.sh_v
        self.sight_height_suffix = self.ids.sh_s

        self.twist_dir = self.ids.td_v

        self.twist = self.ids.tw_v
        self.twist_suffix = self.ids.tw_s

    def bind_ui(self):
        # setup convertors
        # sig.set_unit_sight_height.connect(self.set_sh_units)
        # sig.set_unit_twist.connect(self.set_tw_units)
        sig.set_setting.connect(self.set_setting)

    def on_enter(self, *args):
        ...

    def set_setting(self, **kwargs):
        if 'unit_twist' in kwargs:
            unit = kwargs['unit_twist']
            self.twist.convertor = Convertor(Distance, Distance.Inch, unit)
            self.twist_suffix.text = tr(Distance.name(unit), 'Unit')
        elif 'unit_sight_height' in kwargs:
            unit = kwargs['unit_sight_height']
            self.sight_height.convertor = Convertor(Distance, Distance.Centimeter, unit)
            self.sight_height_suffix.text = tr(Distance.name(unit), 'Unit')

