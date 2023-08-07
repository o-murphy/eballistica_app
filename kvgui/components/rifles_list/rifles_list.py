from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import Screen

from signalslot import Signal


Builder.load_file('../kvgui/components/rifles_list/rifles_list.kv')


class RiflesList(MDScrollView):
    pass


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
    pass


