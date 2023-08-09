from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from kvgui.components.abstract import FormSelector

Builder.load_string("""
<SettingsScreen>
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: "20dp"
            spacing: "15dp"
            
            MD3CardAbs:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                
                FormLabel:
                    id: view_title
                    text: 'View'
                    font_style: 'H6'
                    size_hint: 1, None
                    height: self.texture_size[1]
                    
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"
                    
                    FormLabel:
                        id: theme_l
                        text: 'Theme'
                        size_hint_x: 0.6
                    
                    FormSelector:
                        id: theme_v
                        name: 'theme'
                        text: 'Dark'
                        size_hint_x: 0.4
                        size_hint_y: None
                        height: dp(30)
                        
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"
                    
                    FormLabel:
                        id: lang_l
                        text: 'Language'
                        size_hint_x: 0.6
                    
                    FormSelector:
                        id: lang_v
                        name: 'lang'
                        text: 'English'
                        size_hint_x: 0.4
                        size_hint_y: None
                        height: dp(30)
                        
            MD3CardAbs:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                
                FormLabel:
                    id: units_title
                    text: 'Units'
                    font_style: 'H6'
                    size_hint: 1, None
                    height: self.texture_size[1]
                    
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_tw_l
                        text: 'Twist'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_tw_v
                        name: 'twist'
                        text: 'inch'
                        size_hint_x: 0.4
                        size_hint_y: None
                        height: dp(30)
                        
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_sh_l
                        text: 'Sight height'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_sh_v
                        name: 'sh'
                        text: 'cm'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)
                        
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_v_l
                        text: 'Velocity'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_v_v
                        name: 'v'
                        text: 'm/s'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)
                        
                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_dt_l
                        text: 'Distance'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_dt_v
                        name: 'dist'
                        text: 'm'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_t_l
                        text: 'Temperature'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_t_v
                        name: 'temp'
                        text: '°C'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_w_l
                        text: 'Weight'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_w_v
                        name: 'w'
                        text: 'gr'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_ln_l
                        text: 'Length'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_ln_v
                        name: 'ln'
                        text: 'inch'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_dm_l
                        text: 'Diameter'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_dm_v
                        name: 'diam'
                        text: 'inch'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_ps_l
                        text: 'Pressure'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_ps_v
                        name: 'press'
                        text: 'mmhg'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_dp_l
                        text: 'Drop / Windage'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_dp_v
                        name: 'drop'
                        text: 'cm'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_an_l
                        text: 'Angular'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_an_v
                        name: 'angle'
                        text: 'mmhg'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_ad_l
                        text: 'Adjustment'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_ad_v
                        name: 'path'
                        text: 'cm/100m'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)
                    spacing: "15dp"

                    FormLabel:
                        id: unit_e_l
                        text: 'Energy'
                        size_hint_x: 0.6
                        height: self.texture_size[1]
                    
                    FormSelector:
                        id: unit_e_v
                        name: 'en'
                        text: 'ft*lb'
                        size_hint_x: 0.4
                        # size_hint_y: None
                        # height: dp(30)     

""")


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.name = 'settings'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.theme: FormSelector = self.ids.theme_v
        self.theme.menu.items = [
            {"text": "Dark", "on_release": lambda: self.change_theme(action='Dark')},
            {"text": "Light", "on_release": lambda: self.change_theme(action='Light')},
        ]

        self.twist: FormSelector = self.ids.unit_tw_v
        self.sh: FormSelector = self.ids.unit_sh_v

        self.twist.menu.items = [
            {"text": "inch", "on_release": lambda: self.on_menu_action(caller=self.twist, action='inch')},
            {"text": "cm", "on_release": lambda: self.on_menu_action(caller=self.twist, action='cm')},
            {"text": "mm", "on_release": lambda: self.on_menu_action(caller=self.twist, action='mm')},
            {"text": "ln", "on_release": lambda: self.on_menu_action(caller=self.twist, action='ln')}
        ]

        self.sh.menu.items = [
            {"text": "inch", "on_release": lambda: self.on_menu_action(caller=self.sh, action='inch')},
            {"text": "cm", "on_release": lambda: self.on_menu_action(caller=self.sh, action='cm')},
            {"text": "mm", "on_release": lambda: self.on_menu_action(caller=self.sh, action='mm')},
            {"text": "ln", "on_release": lambda: self.on_menu_action(caller=self.sh, action='ln')}
        ]

    def change_theme(self, action):
        app: MDApp = MDApp.get_running_app()
        if app:
            app.theme_cls.theme_style = action
            self.theme.menu.dismiss()

    def on_menu_action(self, caller, action):
        caller.text = action
        caller.menu.dismiss()

    def bind_ui(self):
        for uid, widget in self.ids.items():
            if isinstance(widget, FormSelector):
                widget.bind(on_release=self.show_menu)

    def show_menu(self, caller):
        if hasattr(caller, 'name') and hasattr(caller, 'menu'):
            caller.menu.open()
