# Builder.load_string("""
# <CardTitle>
#     font_style: 'Subtitle1'
#     size_hint_y: None
#     height: self.texture_size[1]
#
# <FloatField>
#     text: '0.0'
#     input_filter: 'float'
#
# <MD3Card>
#     orientation: "vertical"
#     padding: "20dp"
#     spacing: "5dp"
#     # height: self.minimum_height
#     # size_hint_y: None
#
# <UnitValueField>
#     orientation: "horizontal"
#     height: self.minimum_height
#     size_hint_y: None
#
# <TwistDirSelector>
#     orientation: "horizontal"
#     height: self.minimum_height
#     size_hint_y: None
#
# <NameField>
#     text: 'New rifle'
#     # hint_text: "Weapon name"
#     helper_text: "Required field"
#     helper_text_mode: "on_error"
#     max_text_length: 40
#     required: True
# """)
#
#
# class UnitValueField(BoxLayout):
#     def __init__(self, **kwargs):
#         super(UnitValueField, self).__init__(**kwargs)
#         self.init_ui()
#
#     def init_ui(self):
#         self.prefix = MDLabel(size_hint_x=.6)
#         self.field = ConverMDSpinBox(size_hint_x=.3)
#         self.suffix = MDLabel(size_hint_x=.1)
#         self.add_widget(self.prefix)
#         self.add_widget(self.field)
#         self.add_widget(self.suffix)
#
#
# class TwistDirSelector(BoxLayout):
#     def __init__(self, **kwargs):
#         super(TwistDirSelector, self).__init__(**kwargs)
#         self.init_ui()
#         self.bind_ui()
#
#     def init_ui(self):
#         self.label = Label()
#         self.dropdown = Button()
#         self.dropdown.text = "Right"
#         self.dropdown.icon = "rotate-right"
#
#         self.add_widget(self.label)
#         self.add_widget(self.dropdown)
#         # self.add_widget(MDWidget(size_hint_x=.1))
#
#     def bind_ui(self):
#         self.dropdown.bind(on_release=self.show_menu)
#
#     def show_menu(self, *args):
#         self.menu = MDDropdownMenu(
#             caller=self.dropdown,
#             items=[
#                 {"text": "Right", "leading_icon": "rotate-right",
#                  "on_release": lambda: self.on_menu(action="Right")},
#                 {"text": "Left", "leading_icon": "rotate-left",
#                  "on_release": lambda: self.on_menu(action="Left")},
#             ],
#         )
#         self.menu.open()
#
#     def on_menu(self, action):
#         if action == 'Right':
#             self.dropdown.icon = "rotate-right"
#             self.dropdown.text = 'Right'
#         elif action == 'Left':
#             self.dropdown.icon = "rotate-left"
#             self.dropdown.text = 'Left'
#         self.menu.dismiss()
#
#
# class CardTitle(MDLabel):
#     pass
#
# class MD3Card(MDCard):
#     def __init__(self, **kwargs):
#         super(MD3Card, self).__init__(**kwargs)
#         self.init_ui()
#
#     def init_ui(self):
#         self.title = CardTitle()
#         self.add_widget(self.title)
#
#
# class NameField(MDTextField):
#     pass
#
#
# class NameCard(MD3Card):
#     def init_ui(self):
#         super(NameCard, self).init_ui()
#         self.title.text = 'Name:'
#         self.name = NameField()
#         self.add_widget(self.name)
#
#
# class PropsCard(BoxLayout):
#     def init_ui(self):
#         super(PropsCard, self).init_ui()
#         self.title.text = 'Properties:'
#
#         self.height = self.minimum_height
#         self.size_hint_y = None
#
#         self.layout = MDGridLayout(cols=3)
#
#         self.sh_p = Label(text='Sight height', size_hint_x=0.6)
#         self.sh_v = TextInput(size_hint_x=0.3)
#         self.sh_s = Label(text='cm', size_hint_x=0.1)
#
#         self.td_p = Label(text='Twist direction', size_hint_x=0.6)
#         self.td_v = Button(size_hint_x=0.3)
#         self.td_s = Widget(size_hint_x=0.1)
#
#         self.tw_p = Label(text='Twist', size_hint_x=0.6)
#         self.tw_v = TextInput(size_hint_x=0.3)
#         self.tw_s = Widget(size_hint_x=0.1)
#
#         self.layout.add_widget(self.sh_p)
#         self.layout.add_widget(self.sh_v)
#         self.layout.add_widget(self.sh_s)
#
#         self.layout.add_widget(self.td_p)
#         self.layout.add_widget(self.td_v)
#         self.layout.add_widget(self.td_s)
#
#         self.layout.add_widget(self.tw_p)
#         self.layout.add_widget(self.tw_v)
#         self.layout.add_widget(self.tw_s)
#
#         self.add_widget(self.layout)
#
#
# class InScrollBox(BoxLayout):
#     pass


# class RifleCardScreen(Screen):
#     def __init__(self, **kwargs):
#         super(RifleCardScreen, self).__init__(**kwargs)
#         self.name = 'rifle_card'
#         self.init_ui()
#
#     def init_ui(self):
#         self.scroll = MDScrollView()
#         self.layout = InScrollBox()
#
#         # self.name_card = NameCard()
#         self.props_card = PropsCard()
#
#         # self.layout.add_widget(self.name_card)
#         self.layout.add_widget(self.props_card)
#
#         self.scroll.add_widget(self.layout)
#         self.add_widget(self.scroll)


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
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
    
<RifleCardScreen>
    
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: "20dp"
            spacing: "15dp"
                
            MDCard:
                _padding: dp(15)
                _spacing: dp(15)
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(60)
                padding: self._padding
                spacing: self._spacing
            
                FormLabel:
                    id: name_l
                    text: 'Name'
                    size_hint_x: 0.2
                
                FormInput:
                    id: name_v
                    text: 'Rifle'
                    size_hint_x: 0.8
            
            MDCard:
                _padding: dp(15)
                _spacing: dp(15)
                orientation: 'vertical'
                size_hint_y: None
                height: dp(220)
                padding: self._padding
                spacing: self._spacing
                
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
                        
<TwistDirSelector>
    text: 'Right'
    size_hint_x: 0.3
    size_hint_y: None
    height: dp(30)
"""

Builder.load_string(rifle_card_helper)


class FormInput(MDTextField):
    pass


class FormFloatInput(MDUnitsInput):
    pass


class FormLabel(MDLabel):
    pass


class FormSuffix(MDLabel):
    pass


class TwistDirSelector(MDRectangleFlatIconButton):
    pass


class RifleCardScreen(Screen):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()

    def init_ui(self):
        ...

    def on_enter(self, *args):
        print(self.ids)
