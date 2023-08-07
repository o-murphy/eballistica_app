from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField

Builder.load_file('../kvgui/components/rifle_card/rifle_card.kv')


class FloatField(MDTextField):
    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)
        self.max_value = 100
        self.min_value = -100
        self.decimals = 1
        self.step = 1

    def field_filter(self, value, boolean):
        super(FloatField, self).field_filter(value, boolean)

    @property
    def value(self) -> float:
        return float(self.text)

    @value.setter
    def value(self, value: float):
        self.insert_text(str(value))

    def check_value(self) -> None:
        if self.min_value <= float(self.text) <= self.max_value:
            self.error = False
        else:
            self.error = True
            self.helper_text = 'Must be between {} and {}'.format(self.min_value, self.max_value)

    def insert_text(self, substring, from_undo=False):
        super(FloatField, self).insert_text(substring, from_undo)
        self.check_value()
        

class ConvertableNumField(MDFloatLayout):
    pass


class ComboField(MDFloatLayout):
    pass




class RiflesCardScreen(Screen):
    pass

