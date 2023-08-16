from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('kvgui/kv/one_shot_screen.kv')


class OneShotScreen(Screen):
    def __init__(self, **kwargs):
        super(OneShotScreen, self).__init__(**kwargs)
        self.name = 'one_shot'
