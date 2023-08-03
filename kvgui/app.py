from kivymd.app import MDApp
# from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
# from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder


username_helper = """
MDTextField:
    hint_text: "Enter username"
    helper_text: "or click on forgot username"
    helper_text_mode: "on_focus"
    icon_right: "account"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    size_hint_x: None
    width: 300
"""


class KvColor:

    @staticmethod
    def rgb(r: int, g: int, b: int):
        print(tuple(v / 255.0 for v in (r, g, b)))
        return tuple(v / 255.0 for v in (r, g, b))

    @staticmethod
    def rgba(r: int, g: int, b: int, alpha: int = 255):
        return *KvColor.rgb(r, g, b), alpha / 255.0

    @staticmethod
    def hexa(hex_color: str, alpha: float = 1):
        if not hex_color.startswith("#"):
            raise ValueError('Color must start with #')
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        return *KvColor.rgb(*rgb), alpha


class App(MDApp):
    def build(self):
        # # Labels
        # label = MDLabel(text='Hello!', halign='center', theme_text_color="Custom",
        #                 text_color=KvColor.rgba(236, 98, 81, 255),
        #                 font_style='H2')
        # icon_label = MDIcon(icon='airplane', pos_hint={"center_x": 0.5, "center_y": 0.5})

        # # Screen and buttons
        # screen = Screen()
        # btn_flat = MDRectangleFlatButton(text='Show', pos_hint={"center_x": 0.5, "center_y": 0.4})
        # icon_btn = MDFloatingActionButton(icon='airplane', pos_hint={"center_x": 0.5, "center_y": 0.8})
        # screen.add_widget(btn_flat)
        # screen.add_widget(icon_btn)

        # # theme palette
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = "Dark"
        # screen = Screen()
        # btn_flat = MDRectangleFlatButton(text='Hello', pos_hint={"center_x": 0.5, "center_y": 0.5})
        # screen.add_widget(btn_flat)



        # Text Input
        screen = Screen()
        # username = MDTextField(
        #     text="Enter username",
        #     pos_hint={"center_x": 0.5, "center_y": 0.5},
        #     size_hint_x=None, width=300
        # )
        self.username = Builder.load_string(
            username_helper
        )
        btn_flat = MDRectangleFlatButton(
            text='Show', pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.show_data
        )
        screen.add_widget(self.username)
        screen.add_widget(btn_flat)

        return screen

    def show_data(self, obj):
        print(self.username.text)

App().run()
