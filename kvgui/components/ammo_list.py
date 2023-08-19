from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView

from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/ammo_list_item.kv')


class AmmoListItem(ThreeLineListItem, TouchBehavior):

    def __init__(self, *args, **kwargs):
        super(AmmoListItem, self).__init__(*args, **kwargs)

        self.is_long_touch = False

        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.text = tr('New ammo', "AmmoItem")

    def bind_ui(self):
        ...

    def on_long_touch(self, touch, *args):
        self.is_long_touch = True
        self.show_menu()

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if not self.is_long_touch:
                sig.ammo_item_touch.emit(caller=self)
            else:
                sig.ammo_item_long_touch.emit(caller=self)
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
            sig.ammo_edit_act.emit(caller=self)
        elif action == 'Delete':
            sig.ammo_del_act.emit(caller=self)
        self.menu.dismiss()


class AmmosScreen(Screen):

    def __init__(self, **kwargs):
        super(AmmosScreen, self).__init__(**kwargs)
        self.name = 'ammos_screen'
        self.init_ui()

    def on_pre_enter(self, *args):  # Note: Definition that may translate ui automatically
        # self.translate_ui()
        ...

    def translate_ui(self):
        ...

    def init_ui(self):
        self.scroll = MDScrollView()
        self.list = MDList()

        # TODO: temporary
        item = AmmoListItem()
        item.text = 'Hornady'
        item.secondary_text = item.secondary_text.format('9', 'inch')
        item.tertiary_text = item.tertiary_text.format('9', 'cm')

        item2 = AmmoListItem()
        item2.text = 'RWS'
        item2.secondary_text = item2.secondary_text.format('9', 'inch')
        item2.tertiary_text = item2.tertiary_text.format('9', 'cm')

        self.list.add_widget(item)
        self.list.add_widget(item2)

        self.scroll.add_widget(self.list)
        self.add_widget(self.scroll)
