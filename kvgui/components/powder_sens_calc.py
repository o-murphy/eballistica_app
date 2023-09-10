from kivy.uix.screenmanager import Screen


class PowderSensScreen(Screen):
    def __init__(self, **kwargs):
        super(PowderSensScreen, self).__init__(**kwargs)
        self.name = 'powder_screen'
