from kivy.uix.screenmanager import Screen


class OneShotScreen(Screen):
    def __init__(self, **kwargs):
        super(OneShotScreen, self).__init__(**kwargs)
        self.name = 'one_shot'
