from kivy.lang import Builder
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import Screen


Builder.load_file('../kvgui/components/rifles_list/rifles_list.kv')


class RiflesList(MDScrollView):
    pass


class RifleListItem(ThreeLineListItem):
    pass


class RiflesScreen(Screen):
    pass
    # def on_touch_move(self, touch):
    #     print(touch)
    #     return super(RiflesScreen, self).on_touch_move(touch)

