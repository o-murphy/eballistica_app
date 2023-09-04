import logging
import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView

from datatypes.dbworker import AmmoData
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr
from kvgui.modules.env import STORAGE, StorageWorker

# from a7p import A7PFile, profedit_pb2

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
            {
                "text": tr("Export", "AmmoItem"), "leading_icon": "export-variant",
                "on_release": lambda: self.on_menu_action(action='Export')
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
        elif action == 'Export':
            self.share_ammo()
        self.menu.dismiss()

    # TODO: realise sharing profile to a7p file

    def share_ammo(self):

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
            select_path=self.select_path,  # function called when selecting a file/directory
            search='dirs',
            # ext=['.a7p']
        )
        self.file_manager.show(STORAGE)

    def exit_manager(self, obj):
        logging.info(obj)
        self.file_manager.close()

    def select_path(self, path):
        logging.info(f"from file mngr {path}")
        # profile = profedit_pb2.Payload()
        # print(profile)
        # # with A7PFile() as fp:
        # #     profedit_pb2
        StorageWorker.share_file(path)


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

        self.scroll.add_widget(self.list)
        self.add_widget(self.scroll)

    def display(self, data):
        self.list.clear_widgets()

        if data:
            for ammo in data:
                ammo: AmmoData
                item = AmmoListItem()
                item.dbid = ammo.id
                item.text = ammo.name
                item.secondary_text = f"{tr('Caliber', 'AmmoItem')}: {ammo.diameter} {tr('inch', 'Unit')}, " \
                                      f"{tr('Bullet', 'AmmoItem')}: {ammo.weight} {tr('gr', 'Unit')} / " \
                                      f"{ammo.drag_model.name}"
                item.tertiary_text = f"{tr('MV', 'AmmoList')}: {ammo.muzzle_velocity} {tr('m/s', 'Unit')}"
                self.list.add_widget(item)
