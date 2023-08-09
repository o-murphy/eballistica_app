from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField

from kvgui.components.spinbox import MDUnitsInput

rifle_card_helper = """

<FormInput>
    # padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
    size_hint_x: 0.3
    pos_hint: {'center_x': 0.5, 'center_y': 0.6}
    
<FormFloatInput>
    # padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
    size_hint_x: 0.3
    pos_hint: {'center_x': 0.5, 'center_y': 0.6}

    
<FormLabel>
    # halign: "left"
    size_hint_x: 0.6
    font_style: 'Subtitle2'
    
<FormSuffix>
    halign: "left"
    size_hint_x: 0.1
    
<TwistDirSelector>
    text: 'Right'
    size_hint_x: 0.3
    size_hint_y: None
    height: dp(30)
    
<MD3CardAbs>
    _padding: dp(15)
    _spacing: dp(15)
    padding: self._padding
    spacing: self._spacing

<RifleCardScreen>
    
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: "20dp"
            spacing: "15dp"
                
            MD3CardAbs:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(60)
            
                FormLabel:
                    id: name_l
                    text: 'Name'
                    size_hint_x: 0.2
                
                FormInput:
                    id: name_v
                    text: 'Rifle'
                    size_hint_x: 0.8
            
            MD3CardAbs:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(220)

                
                FormLabel:
                    id: prop_title
                    text: 'Properties:'
                    font_style: 'H6'
                    
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "15dp"
                    
                    FormLabel:
                        id: sh_l
                        text: 'Sight height'
                    
                    FormFloatInput:
                        id: sh_v
                        text: '0.0'
                        input_filter: 'float'
                        
                    FormSuffix:
                        id: sh_s
                        text: 'cm'
                        
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "15dp"
                    
                    FormLabel:
                        id: td_l
                        text: 'Twist direction'
                        size_hint_x: 0.6
                    
                    TwistDirSelector:
                        id: td_v
                        text: 'Right'
                        icon: 'rotate-right'
                        size_hint_x: 0.3
                        size_hint_y: None
                        height: dp(30)
                        
                    MDWidget:
                        size_hint_x: 0.1
                    
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "15dp"
                    
                    FormLabel:
                        id: tw_l
                        text: 'Twist'
                    
                    FormFloatInput:
                        id: tw_v
                        text: '0.0'
                        input_filter: 'float'
                        
                    FormSuffix:
                        id: tw_s
                        text: 'inch'
                        


"""

Builder.load_string(rifle_card_helper)


class MD3CardAbs(MDCard):
    pass


class FormInput(MDTextField):
    pass


class FormFloatInput(MDUnitsInput):
    pass


class FormLabel(MDLabel):
    pass


class FormSuffix(MDLabel):
    pass


class TwistDirSelector(MDRectangleFlatIconButton):
    def __init__(self, **kwargs):
        super(TwistDirSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()
        self.value = "Right"  # TODO: must be Enum

    def init_ui(self):
        self.menu = MDDropdownMenu(
            caller=self,
            items=[
                {"text": "Right", "leading_icon": "rotate-right",
                 "on_release": lambda: self.on_menu(action="Right")},
                {"text": "Left", "leading_icon": "rotate-left",
                 "on_release": lambda: self.on_menu(action="Left")},
            ],
        )

    def bind_ui(self):
        self.bind(on_release=self.show_menu)

    def show_menu(self, *args, **kwargs):
        self.menu.open()

    def on_menu(self, action):
        if action == 'Right':
            self.icon = "rotate-right"
            self.text = 'Right'
            self.value = action
        elif action == 'Left':
            self.icon = "rotate-left"
            self.text = 'Left'
            self.value = action
        self.menu.dismiss()


class RifleCardScreen(Screen):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()

    def init_ui(self):
        ...

    def on_enter(self, *args):
        print(self.ids)
