from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from kvgui.components.settings_card import CardTitle
from kvgui.components.spinbox import ConverMDSpinBox

Builder.load_string("""
<FloatField>
    text: '0.0'
    input_filter: 'float'

<MD3Card>
    orientation: "vertical"
    padding: "20dp"
    spacing: "15dp"
    height: self.minimum_height
    size_hint_y: None
    
<UnitValueField>
    orientation: "horizontal"
    height: self.minimum_height
    size_hint_y: None
    
<TwistDirSelector>
    orientation: "horizontal"
    height: self.minimum_height
    size_hint_y: None
    
<NameField>
    text: 'New rifle'
    # hint_text: "Weapon name"
    helper_text: "Required field"
    helper_text_mode: "on_error"
    max_text_length: 40
    required: True
""")


class UnitValueField(BoxLayout):
    def __init__(self, **kwargs):
        super(UnitValueField, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.prefix = MDLabel(size_hint_x=.5)
        self.field = ConverMDSpinBox(size_hint_x=.3)
        self.suffix = MDLabel(size_hint_x=.2)
        self.add_widget(self.prefix)
        self.add_widget(self.field)
        self.add_widget(self.suffix)


class TwistDirSelector(BoxLayout):
    def __init__(self, **kwargs):
        super(TwistDirSelector, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.label = MDLabel(size_hint_x=.5)
        self.dropdown = MDRoundFlatIconButton(size_hint_x=.5)
        self.dropdown.icon = "rotate-right"
        self.dropdown.size_hint_x = None
        self.add_widget(self.label)
        self.add_widget(self.dropdown)

    def bind_ui(self):
        self.dropdown.bind(on_release=self.show_menu)

    def show_menu(self, *args):
        self.menu = MDDropdownMenu(
            caller=self.dropdown,
            items=[
                {"text": "Right", "leading_icon": "rotate-right",
                 "on_release": lambda: self.on_menu(action="Right")},
                {"text": "Left", "leading_icon": "rotate-left",
                 "on_release": lambda: self.on_menu(action="Left")},
            ],
        )
        self.menu.open()

    def on_menu(self, action):
        if action == 'Right':
            self.dropdown.icon = "rotate-right"
            self.dropdown.text = 'Right'
        elif action == 'Left':
            self.dropdown.icon = "rotate-left"
            self.dropdown.text = 'Left'
        self.menu.dismiss()


class MD3Card(MDCard):
    def __init__(self, **kwargs):
        super(MD3Card, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.title = CardTitle()
        self.add_widget(self.title)


class NameField(MDTextField):
    pass


class NameCard(MD3Card):
    def init_ui(self):
        super(NameCard, self).init_ui()
        self.title.text = 'Name:'
        self.name = NameField()
        self.add_widget(self.name)


class PropsCard(MD3Card):
    def init_ui(self):
        super(PropsCard, self).init_ui()
        self.title.text = 'Properties:'

        self.sh_v = UnitValueField()
        self.sh_v.prefix.text = "Sight height"
        self.sh_v.suffix.text = "cm"

        self.tw_v = UnitValueField()
        self.tw_v.prefix.text = "Twist"
        self.tw_v.suffix.text = "inch"

        self.tw_d = TwistDirSelector()
        self.tw_d.label.text = "Twist direction"
        self.tw_d.dropdown.text = 'Right'

        self.add_widget(self.tw_v)
        self.add_widget(self.tw_d)
        self.add_widget(self.sh_v)


class InScrollBox(MDBoxLayout):
    pass


class RifleCardScreen(Screen):
    def __init__(self, **kwargs):
        super(RifleCardScreen, self).__init__(**kwargs)
        self.name = 'rifle_card'
        self.init_ui()

    def init_ui(self):
        self.scroll = MDScrollView()
        self.layout = InScrollBox()

        self.name_card = NameCard()
        self.props_card = PropsCard()

        self.layout.add_widget(self.name_card)
        self.layout.add_widget(self.props_card)

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)




#
# class ConvertableNumField(MDWidget):
#     pass
#
#
# class TwistDirection(MDDropDownItem):
#     def show_menu(self):
#         menu_items = [
#             {"text": "Right", "leading_icon": "rotate-right", "on_release": lambda x='Right': self.on_menu_action(x)},
#             {"text": "Left", "leading_icon": "rotate-left", "on_release": lambda x='Left': self.on_menu_action(x)},
#         ]
#         self.menu = MDDropdownMenu(
#             caller=self, items=menu_items
#         )
#         self.menu.position = 'center'
#         self.menu.open()
#
#     def on_menu_action(self, action):
#         self.text = action
#         self.menu.dismiss()
#
#
# class ComboField(MDWidget):
#     pass
#
#
# class RiflesCardScreen(Screen):
#     pass
