from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import Screen

from signalslot import Signal


Builder.load_string("""
<RifleListItem>
    text: "New rifle"
    md_bg_color: "#191c1a"
    secondary_text: "Twist: 1 in <num> <units>"
    secondary_font_style: "Caption"
    tertiary_text: "Sight height: <num> <units>"
    tertiary_font_style: "Caption"
""")


class RifleListItem(ThreeLineListItem, TouchBehavior):
    menu_action = Signal(args=['action'], name='menu_action')
    short_touch = Signal(args=['item'], name='short_touch')
    long_touch = Signal(args=['item'], name='long_touch')

    def __init__(self, *args, **kwargs):
        super(RifleListItem, self).__init__(*args, **kwargs)

        self.is_long_touch = False

        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        ...

    def bind_ui(self):
        self.menu_action.connect(self.on_menu_action)

    def on_long_touch(self, touch, *args):
        self.is_long_touch = True
        self.show_menu()

    def on_touch_up(self, touch):
        if not self.is_long_touch:
            self.short_touch.emit()
            MDApp.get_running_app().switch_ammos_list()
        else:
            self.long_touch.emit()
        self.is_long_touch = False

    def show_menu(self):

        menu_items = [
            {
                "text": "Edit", "leading_icon": "pencil-outline",
                "on_release": lambda: self.menu_action.emit(action='Edit')
            },
            {
                "text": "Delete", "leading_icon": "delete-outline",
                "on_release": lambda: self.menu_action.emit(action='Delete')
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self, items=menu_items
        )
        self.menu.open()

    def on_menu_action(self, action, **kwargs):
        if action == 'Edit':
            MDApp.get_running_app().switch_rifle_card()
        self.menu.dismiss()


class RiflesScreen(Screen):
    menu_action = Signal(args=['action'], name='menu_action')
    short_touch = Signal(args=['item'], name='short_touch')
    long_touch = Signal(args=['item'], name='long_touch')

    def __init__(self, *args, **kwargs):
        super(RiflesScreen, self).__init__(*args, **kwargs)
        self.name = 'rifles_screen'
        self.init_ui()

    def init_ui(self):
        self.scroll = MDScrollView()
        self.list = MDList()

        self.list.add_widget(RifleListItem())  # TODO: temporary

        self.scroll.add_widget(self.list)
        self.add_widget(self.scroll)

