from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


Builder.load_file('kvgui/kv/ammo_card.kv')


class AmmoCardScreen(Screen):
    def __init__(self, **kwargs):
        super(AmmoCardScreen, self).__init__(**kwargs)
        self.name = 'ammo_card'
        self.init_ui()

    def init_ui(self):
        ...

    def on_enter(self, *args):
        print(self.ids)
