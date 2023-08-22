from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView

from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/rifle_list_item.kv')


class RifleListItem(ThreeLineListItem, TouchBehavior):

    def __init__(self, *args, **kwargs):
        super(RifleListItem, self).__init__(*args, **kwargs)

        self.is_long_touch = False

        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.text = tr('New rifle', "RifleItem")
        self.secondary_text = tr('Twist:', "RifleItem")
        self.tertiary_text = tr('Sight height:', "RifleItem")

    def bind_ui(self):
        ...

    def on_long_touch(self, touch, *args):
        self.is_long_touch = True
        self.show_menu()

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if not self.is_long_touch:
                sig.rifle_item_touch.emit(caller=self)
            else:
                sig.rifle_item_long_touch.emit(caller=self)
        self.is_long_touch = False

    def show_menu(self):

        menu_items = [
            {
                "text": tr("Edit", "AmmoItem"), "leading_icon": "pencil-outline",
                "on_release": lambda: self.on_menu_action(action='Edit')
            },
            {
                "text": tr("Delete", "AmmoItem"), "leading_icon": "delete-outline",
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
        self.list.size_hint_y = None
        self.list.height = self.list.minimum_height

        self.scroll.add_widget(self.list)
        self.add_widget(self.scroll)

    def on_enter(self, *args):
        ...

    def translate_ui(self):
        ...

    def display(self, data):

        self.list.clear_widgets()

        if data:
            for rifle in data:
                item = RifleListItem()
                item.dbid = rifle.id
                item.text = rifle.name
                item.secondary_text = f"{tr('Twist', 'RiflesList')}: {rifle.barrel_twist} {tr('inch', 'Unit')}"
                item.tertiary_text = f"{tr('Sight height', 'RiflesList')}: {rifle.sight_height} {tr('cm', 'Unit')}"
                self.list.add_widget(item)
