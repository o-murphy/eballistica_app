from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField


class MD3CardAbs(MDCard):
    pass


class FormInput(MDTextField):
    pass


class FormLabel(MDLabel):
    pass


class FormSuffix(MDLabel):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    ...


class FormSelector(MDRectangleFlatIconButton):
    def __init__(self, *args, **kwargs):
        super(FormSelector, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.menu = MDDropdownMenu(caller=self)


class UnitSelector(FormSelector):
    def __init__(self, *args, **kwargs):
        super(UnitSelector, self).__init__(*args, **kwargs)
        self.init_ui()
        self.unit_class = None
        self.units_specified: list = []

    def init_ui(self):
        self.menu = MDDropdownMenu(caller=self)
