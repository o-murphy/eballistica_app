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
        self.menu = MDDropdownMenu(
            caller=self,
            items=[
                {"text": "Right", "leading_icon": "rotate-right",
                 "on_release": lambda: self.on_menu(action="Right")},
                {"text": "Left", "leading_icon": "rotate-left",
                 "on_release": lambda: self.on_menu(action="Left")},
            ],
        )

    def bind_ui(self):
        self.bind(on_release=self.show_menu)

    def show_menu(self, *args, **kwargs):
        self.menu.open()

    def on_menu(self, action):
        if action == 'Right':
            self.icon = "rotate-right"
            self.text = 'Right'
            self.value = action
        elif action == 'Left':
            self.icon = "rotate-left"
            self.text = 'Left'
            self.value = action
        self.menu.dismiss()


class RifleCardScreen(Screen):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()

    def init_ui(self):
        ...

    def on_enter(self, *args):
        print(self.ids)
