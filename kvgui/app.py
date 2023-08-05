from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDActionBottomAppBarButton, MDBottomAppBar


from kivymd.app import MDApp
from kivy.lang import Builder

Window.size = (400, 700)


class AppScreenManager(ScreenManager):
    pass


class RiflesList(MDScrollView):
    pass


class RifleListItem(ThreeLineListItem):
    pass


class TopBar(MDBoxLayout):
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

    def get_current_screen(self):
        return self.root.ids.screen_manager.current_screen

    def add_act(self):
        print('add on', self.get_current_screen())

    def on_bottom_action_buttons(self, action: MDActionBottomAppBarButton):
        print('bot action', action.icon)


EBallisticaApp().run()
