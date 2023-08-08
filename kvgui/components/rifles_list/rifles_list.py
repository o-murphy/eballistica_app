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

    def on_long_touch(self, touch, *args):
        self.show_menu()

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            if "event" not in touch.ud:
                print('skipping as long touch')

        else:
            MDApp.get_running_app().switch_ammos_list()

    def show_menu(self):

        menu_items = [
            {"text": "Edit", "leading_icon": "pencil-outline", "on_release": lambda x='Edit': self.on_menu_action(x)},
            {"text": "Delete", "leading_icon": "delete-outline", "on_release": lambda x='Delete': self.on_menu_action(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self, items=menu_items
        )
        self.menu.open()

    def on_menu_action(self, obj):
        print(obj)
        if obj == 'Edit':
            MDApp.get_running_app().switch_rifle_card()
        self.menu.dismiss()


class RiflesScreen(Screen):
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

