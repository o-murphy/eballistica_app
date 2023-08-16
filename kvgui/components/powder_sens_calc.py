from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('kvgui/kv/powder_sens_calc.kv')


class PowderSensScreen(Screen):
    def __init__(self, **kwargs):
        super(PowderSensScreen, self).__init__(**kwargs)
        self.name = 'powder_screen'
