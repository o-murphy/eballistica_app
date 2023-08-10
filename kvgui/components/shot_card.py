from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton

from kvgui.modules import signals as sig

Builder.load_file('kvgui/kv/shot_card.kv')


class ShotCardScreen(Screen):
    def __init__(self, **kwargs):
        super(ShotCardScreen, self).__init__(**kwargs)
        self.name = 'shot_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.one_shot: MDRaisedButton = self.ids.one_shot
        self.trajectory: MDRaisedButton = self.ids.trajectory

    def bind_ui(self):
        self.one_shot.bind(on_release=lambda x: sig.one_shot_act.emit(caller=self))
        self.trajectory.bind(on_release=lambda x: sig.trajectory_act.emit(caller=self))

    def on_enter(self, *args):
        ...
