# from kivy.metrics import dp
# from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.list import MDList, ThreeLineIconListItem, IconLeftWidget, ThreeLineAvatarIconListItem
# from kivy.uix.scrollview import ScrollView
# from kivymd.uix.list import OneLineListItem
# from kivymd.uix.datatables import MDDataTable
# from kivymd.uix.label import MDLabel, MDIcon
# from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager


Window.size = (400, 600)


# screen change

screen_helper = """
ScreenManager:
    MenuScreen:
    ProfileScreen:
    UploadScreen:
    
<UploadScreen>:
    name: 'upload'
    MDLabel:
        text: 'Upload some'
        halign: 'center'
    MDRectangleFlatButton:
        text: 'back'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press: root.manager.current = 'menu'
    
<MenuScreen>:
    name: 'menu'
    MDRectangleFlatButton:
        text: 'Profile'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press: root.manager.current = 'profile'
    MDRectangleFlatButton:
        text: 'Upload'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press: root.manager.current = 'upload'

<ProfileScreen>:
    name: 'profile'
    MDLabel:
        text: 'Welcome'
        halign: 'center'
    MDRectangleFlatButton:
        text: 'back'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press: root.manager.current = 'menu'

"""

class UploadScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class MenuScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(UploadScreen(name='upload'))


class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        screen = Builder.load_string(screen_helper)
        return screen


App().run()



# # NAVBAR
# screen_helper = """
# Screen:
#     MDNavigationLayout:
#         ScreenManager:
#             Screen:
#                 BoxLayout:
#                     orientation: 'vertical'
#                     MDTopAppBar:
#                         title: 'Application'
#                         left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
#                         elevation: 2
#
#                     Widget:
#
#
#         MDNavigationDrawer:
#             id: nav_drawer
#
#
#             BoxLayout:
#                 orientation: 'vertical'
#
#                 Image:
#                     source: '../Icon.png'
#
#                 MDLabel:
#                     text: 'Props'
#                     font_style: 'Subtitle1'
#                     size_hint_y: None
#                     height: self.texture_size[1]
#                 MDLabel:
#                     text: 'Email'
#                     font_style: 'Caption'
#                     size_hint_y: None
#                     height: self.texture_size[1]
#                 ScrollView:
#                     MDList:
#                         OneLineIconListItem:
#                             text: "Settings"
#                             IconLeftWidget:
#                                 icon: 'cog-outline'
#                         OneLineIconListItem:
#                             text: "Info"
#                             IconLeftWidget:
#                                 icon: 'information-outline'
#
#
# """
#
#
# class App(MDApp):
#     def build(self):
#         self.theme_cls.primary_palette = 'Red'
#         self.theme_cls.theme_style = 'Dark'
#         screen = Builder.load_string(screen_helper)
#         return screen
#
#     def navigation_draw(self):
#         print("Navigation")
#
#
# App().run()



# # Toolbar
# screen_helper = """
# Screen:
#     BoxLayout:
#         orientation: 'vertical'
#         MDTopAppBar:
#             title: 'Application'
#             left_action_items: [["menu", lambda x: app.navigation_draw()]]
#             right_action_items: [["clock", lambda x: app.navigation_draw()]]
#             elevation: 2
#         MDLabel:
#             text: 'HelloWorld'
#             halign: 'center'
#         MDBottomAppBar:
#             MDTopAppBar:
#                 title: "Help"
#                 left_action_items: [["coffee", lambda x: app.navigation_draw()]]
#                 mode: "end"
#                 icon: "git"
#                 type: "bottom"
#                 elevation: 2
#                 on_action_button: app.navigation_draw()
#
# """
#
#
# class App(MDApp):
#     def build(self):
#         self.theme_cls.primary_palette = 'Red'
#         screen = Builder.load_string(screen_helper)
#         return screen
#
#     def navigation_draw(self):
#         print("Navigation")
#
#
# App().run()


# # MDTextField properties
# username_helper = """
# MDTextField:
#     hint_text: "Enter username"
#     helper_text: "or click on forgot username"
#     helper_text_mode: "on_focus"
#     icon_right: "account"
#     icon_right_color: app.theme_cls.primary_color
#     pos_hint: {"center_x": 0.5, "center_y": 0.5}
#     size_hint_x: None
#     width: 300
# """


# class KvColor:
#
#     @staticmethod
#     def rgb(r: int, g: int, b: int):
#         print(tuple(v / 255.0 for v in (r, g, b)))
#         return tuple(v / 255.0 for v in (r, g, b))
#
#     @staticmethod
#     def rgba(r: int, g: int, b: int, alpha: int = 255):
#         return *KvColor.rgb(r, g, b), alpha / 255.0
#
#     @staticmethod
#     def hexa(hex_color: str, alpha: float = 1):
#         if not hex_color.startswith("#"):
#             raise ValueError('Color must start with #')
#         hex_color = hex_color.lstrip("#")
#         rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
#         return *KvColor.rgb(*rgb), alpha


# class App(MDApp):
#     def build(self):
#         # # Labels
#         # label = MDLabel(text='Hello!', halign='center', theme_text_color="Custom",
#         #                 text_color=KvColor.rgba(236, 98, 81, 255),
#         #                 font_style='H2')
#         # icon_label = MDIcon(icon='airplane', pos_hint={"center_x": 0.5, "center_y": 0.5})
#
#         # # Screen and buttons
#         # screen = Screen()
#         # btn_flat = MDRectangleFlatButton(text='Show', pos_hint={"center_x": 0.5, "center_y": 0.4})
#         # icon_btn = MDFloatingActionButton(icon='airplane', pos_hint={"center_x": 0.5, "center_y": 0.8})
#         # screen.add_widget(btn_flat)
#         # screen.add_widget(icon_btn)
#
#         # # theme palette
#         self.theme_cls.primary_palette = "Green"
#         self.theme_cls.primary_hue = "A700"
#         self.theme_cls.theme_style = "Dark"
#         # screen = Screen()
#         # btn_flat = MDRectangleFlatButton(text='Hello', pos_hint={"center_x": 0.5, "center_y": 0.5})
#         # screen.add_widget(btn_flat)
#
#
#
#         # Text Input
#         screen = Screen()
#         # username = MDTextField(
#         #     text="Enter username",
#         #     pos_hint={"center_x": 0.5, "center_y": 0.5},
#         #     size_hint_x=None, width=300
#         # )
#         self.username = Builder.load_string(
#             username_helper
#         )
#         btn_flat = MDRectangleFlatButton(
#             text='Show', pos_hint={"center_x": 0.5, "center_y": 0.4},
#             on_release=self.show_data
#         )
#         screen.add_widget(self.username)
#         screen.add_widget(btn_flat)
#
#         return screen
#
#     # Dialog
#     def show_data(self, obj):
#         if self.username.text is "":
#             check_str = "Wrong username"
#         else:
#             check_str = self.username.text + " not found"
#         close_btn = MDFlatButton(text="Close", on_release=self.close_dialog)
#         more_btn = MDFlatButton(text='More')
#         self.dialog = MDDialog(
#             text=check_str,
#             title="Username Check",
#             size_hint=(0.7, 1),
#             buttons=[close_btn, more_btn]
#         )
#         self.dialog.open()
#
#     def close_dialog(self, obj):
#         self.dialog.dismiss()

# # ListView and list icons
# list_helper = """
# Screen:
#     ScrollView:
#         MDList:
#             id: container
#
# """

# class App(MDApp):
#     # def build(self):
#     #     screen = Screen()
#     #
#     #     scroll_view = ScrollView()
#     #     list_view = MDList()
#     #     scroll_view.add_widget(list_view)
#     #
#     #     for i in range(25):
#     #         image = IconLeftWidget(icon="account")
#     #         items = ThreeLineAvatarIconListItem(text=f'Item {i}', secondary_text="FooBar",
#     #                                             tertiary_text='Third line')
#     #         items.add_widget(image)
#     #         list_view.add_widget(items)
#     #
#     #     screen.add_widget(scroll_view)
#     #
#     #     screen = Builder.load_string(list_helper)
#     #
#     #     return screen
#
#     # # or use this //
#     def build(self):
#         screen = Builder.load_string(list_helper)
#         return screen
#
#     def on_start(self):
#         for i in range(20):
#             items = OneLineListItem(text=f'Item {i}')
#             self.root.ids.container.add_widget(items)


# # Table
# class App(MDApp):
#     def build(self):
#         # self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = 'Teal'
#         screen = Screen()
#         table = MDDataTable(
#             size_hint=(0.9, 0.6),
#             pos_hint=({'center_x': 0.5, 'center_y': 0.5}),
#             check=True,
#             column_data=[
#                 ("Distance", dp(30)),
#                 ("Velocity", dp(30)),
#             ],
#             rows_num=7,
#             row_data=[
#                 ('100', 800),
#                 ('200', 790),
#                 ('300', 790),
#                 ('400', 790),
#                 ('500', 790),
#                 ('600', 790),
#                 ('700', 790),
#             ]
#         )
#         table.bind(on_check_press=self.check_press)
#         table.bind(on_row_press=self.row_press)
#         screen.add_widget(table)
#         return screen
#
#     def check_press(self, instance_table, current_row):
#         print(instance_table, current_row)
#
#     def row_press(self, instance_table, current_row):
#         print(instance_table, current_row)


