from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu

from kvgui.components.abstract import FormSelector
from kvgui.modules import signals as sig

Builder.load_file('kvgui/kv/ammo_card.kv')


class BCSelector(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super(BCSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        ...

    def bind_ui(self):
        ...


class DragModelSelector(FormSelector):
    def __init__(self, **kwargs):
        super(DragModelSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()
        self.value = "G7"

    def init_ui(self):
        self.menu = MDDropdownMenu(
            caller=self,
            items=[
                {"text": "G1", "on_release": lambda: self.on_menu(action="G1")},
                {"text": "G7", "on_release": lambda: self.on_menu(action="G7")},
                {"text": "CDM", "on_release": lambda: self.on_menu(action="CDM")},
            ],
        )

    def bind_ui(self):
        self.bind(on_release=self.show_menu)

    def show_menu(self, *args, **kwargs):
        self.menu.open()

    def on_menu(self, action):
        self.text = action
        self.value = action
        self.menu.dismiss()
        sig.ammo_dm_change.emit(caller=self)


class AmmoCardScreen(Screen):
    def __init__(self, **kwargs):
        super(AmmoCardScreen, self).__init__(**kwargs)
        self.name = 'ammo_card'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.powder_sens_calc: MDRectangleFlatButton = self.ids.pws_act

    def bind_ui(self):
        self.powder_sens_calc.bind(on_release=lambda x: sig.ammo_powder_sens_act.emit(caller=self))

    def on_enter(self, *args):
        ...
