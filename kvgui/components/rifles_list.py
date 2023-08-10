from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import Screen

from signalslot import Signal
from kvgui.modules import signals as sig


Builder.load_string("""
<RifleListItem>
    text: "New rifle"
    md_bg_color: "#191c1a"
    font_style: "H6"
    secondary_text: "Twist: 1 in {} {}"
    secondary_font_style: "Subtitle2"
    tertiary_text: "Sight height: {} {}"
    tertiary_font_style: "Subtitle2"
""")


class RifleListItem(ThreeLineListItem, TouchBehavior):

    def __init__(self, *args, **kwargs):
        super(RifleListItem, self).__init__(*args, **kwargs)

        self.is_long_touch = False

        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        ...

    def bind_ui(self):
        ...

    def on_long_touch(self, touch, *args):
        self.is_long_touch = True
        self.show_menu()

    def on_touch_up(self, touch):
        if not self.is_long_touch:
            sig.rifle_item_touch.emit(caller=self)
        else:
            sig.rifle_item_long_touch.emit(caller=self)
        self.is_long_touch = False

    def show_menu(self):

        menu_items = [
            {
                "text": "Edit", "leading_icon": "pencil-outline",
                "on_release": lambda: self.on_menu_action(action='Edit')
            },
            {
                "text": "Delete", "leading_icon": "delete-outline",
                "on_release": lambda: self.on_menu_action(action='Delete')
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self, items=menu_items
        )
        self.menu.open()

    def on_menu_action(self, action, **kwargs):
        if action == 'Edit':
            sig.rifle_edit_act.emit(caller=self)
        elif action == 'Delete':
            sig.rifle_del_act.emit(caller=self)
        self.menu.dismiss()


class RiflesScreen(Screen):

    def __init__(self, **kwargs):
        super(RiflesScreen, self).__init__(**kwargs)
        self.name = 'rifles_screen'
        self.init_ui()

    def init_ui(self):
        self.scroll = MDScrollView()
        self.list = MDList()

        # TODO: temporary
        item = RifleListItem()
        item.secondary_text = item.secondary_text.format('9', 'inch')
        item.tertiary_text = item.tertiary_text.format('9', 'cm')

        item2 = RifleListItem()
        item2.secondary_text = item2.secondary_text.format('9', 'inch')
        item2.tertiary_text = item2.tertiary_text.format('9', 'cm')

        self.list.add_widget(item)
        self.list.add_widget(item2)

        self.scroll.add_widget(self.list)
        self.add_widget(self.scroll)

