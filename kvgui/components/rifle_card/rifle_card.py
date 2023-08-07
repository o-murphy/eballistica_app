from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu

from kvgui.components.spinbox import MDSpinBox

Builder.load_file('../kvgui/components/rifle_card/rifle_card.kv')


class FloatField(MDSpinBox):
    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)
        self.min_value = 0.001
        self.max_value = 10
        self.step = 0.001
        self.decimals = 3


class ConvertableNumField(MDFloatLayout):
    pass


class TwistDirection(MDDropDownItem):
    def show_menu(self):
        menu_items = [
            {"text": "Right", "leading_icon": "rotate-right", "on_release": lambda x='Right': self.on_menu_action(x)},
            {"text": "Left", "leading_icon": "rotate-left", "on_release": lambda x='Left': self.on_menu_action(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self, items=menu_items
        )
        self.menu.position = 'center'
        self.menu.open()

    def on_menu_action(self, action):
        self.text = action
        self.menu.dismiss()


class ComboField(MDFloatLayout):
    pass


class RiflesCardScreen(Screen):
    pass
