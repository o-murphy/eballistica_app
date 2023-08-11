from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu

from kvgui.components.abstract import FormSelector

Builder.load_file('kvgui/kv/rifle_card.kv')


class TwistDirSelector(FormSelector):
    def __init__(self, **kwargs):
        super(TwistDirSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()
        self.value = "Right"  # TODO: must be Enum

    def init_ui(self):
        ...

    def bind_ui(self):
        self.bind(on_release=self.change_twist)

    def change_twist(self, *args, **kwargs):
        if self.value == 'Right':
            self.icon = "rotate-left"
            self.text = 'Left'
            self.value = 'Left'

        elif self.value == 'Left':
            self.icon = "rotate-right"
            self.text = 'Right'
            self.value = 'Right'


class RifleCardScreen(Screen):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()

    def init_ui(self):
        ...

    def on_enter(self, *args):
        ...
