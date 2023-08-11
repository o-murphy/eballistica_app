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

        self.sh = self.ids.sh_l
        self.sh_v: MDUnitsInput = self.ids.sh_v
        self.sh_s = self.ids.sh_s

        self.td_l = self.ids.td_l
        self.td_v = self.ids.td_v

        self.tw_l = self.ids.tw_l
        self.tw_v = self.ids.tw_v
        self.tw_s = self.ids.tw_s

    def bind_ui(self):
        # setup convertors
        sig.set_sh_unit_change.connect(self.set_sh_units)
        sig.set_tw_unit_change.connect(self.set_tw_units)

    def on_enter(self, *args):
        ...

    def set_sh_units(self, unit, **kwargs):
        self.sh_v.convertor = Convertor(Distance, Distance.Centimeter, unit)
        self.sh_s.text = tr(Distance.name(unit), 'RifleCard')

    def set_tw_units(self, unit, **kwargs):
        self.tw_v.convertor = Convertor(Distance, Distance.Inch, unit)
        self.tw_s.text = tr(Distance.name(unit), 'RifleCard')
