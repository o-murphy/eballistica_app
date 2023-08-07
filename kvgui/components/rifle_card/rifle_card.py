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

    @property
    def value(self) -> float:
        return float(self.text)

    @value.setter
    def value(self, value: float):
        self.set_text(self, str(value))
        
    # def on_text_validate(self):
    #     super(FloatField, self).on_text_validate(self)


class ConvertableNumField(MDFloatLayout):
    pass


class ComboField(MDFloatLayout):
    pass




class RiflesCardScreen(Screen):
    pass



