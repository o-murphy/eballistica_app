from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField


Builder.load_file('kvgui/kv/abstract.kv')


from kvgui.components.numeric_field import MDUnitsInput


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


class FormSelector(MDRectangleFlatIconButton):
    def __init__(self, *args, **kwargs):
        super(FormSelector, self).__init__(*args, **kwargs)
        self.init_ui()
        self.unit_class = None
        self.units_specified: list = []

    def init_ui(self):
        self.menu = MDDropdownMenu(caller=self)
