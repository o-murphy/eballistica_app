from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDActionBottomAppBarButton, MDBottomAppBar


from kivymd.app import MDApp
from kivy.lang import Builder


from kvgui.components import TopBar
from kvgui.components import AmmosList, AmmoListItem, AmmosScreen


assert TopBar
assert AmmosList
assert AmmoListItem
assert AmmosScreen


Window.size = (400, 700)


class AppScreenManager(ScreenManager):
    pass


class RiflesList(MDScrollView):
    pass


class RifleListItem(ThreeLineListItem):
    pass


class BottomBar(MDBottomAppBar):
    pass


class MainScreen(Screen):
    pass


class EBallisticaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        screen = Builder.load_file('app.kv')
        return screen

    def on_start(self):
        print(self.root.ids.screen_manager.__dir__())
        print(self.root.ids.screen_manager.children)
        print(self.root.ids.screen_manager.screens)
        # self.root.ids.screen_manager.current_screen = self.root.ids.screen_manager.ids.ammos_list

    def get_current_screen(self):
        return self.root.ids.screen_manager.current_screen

    def add_act(self):
        print('add on', self.get_current_screen())

    def on_bottom_action_buttons(self, action: MDActionBottomAppBarButton):
        print('bot action', action.icon)
        if action.icon == "arrow-left":
            self.root.ids.screen_manager.transition.direction = 'right'
            self.root.ids.screen_manager.current = 'rifles_screen'

    def switch_ammo_list(self, obj=None):
        self.root.ids.screen_manager.transition.direction = 'left'
        self.root.ids.screen_manager.current = 'ammos_screen'


EBallisticaApp().run()
