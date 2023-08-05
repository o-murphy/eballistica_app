from kivy.lang import Builder
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import Screen


Builder.load_file('../kvgui/components/ammo_list/ammo_list.kv')


class AmmosList(MDScrollView):
    pass


class AmmoListItem(ThreeLineListItem):
    pass


class AmmosScreen(Screen):
    pass