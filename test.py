from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty


class RoundedSpinBox(BoxLayout):
    min_value = NumericProperty(0)
    max_value = NumericProperty(100)

    def __init__(self, **kwargs):
        super(RoundedSpinBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10

        self._value = self.min_value

        self.decrement_button = Button(text="-", on_release=self.decrement)
        self.text_input = TextInput(multiline=False)
        self.increment_button = Button(text="+", on_release=self.increment)

        self.add_widget(self.decrement_button)
        self.add_widget(self.text_input)
        self.add_widget(self.increment_button)

        self.update_value()

    def increment(self, instance):
        self.value = min(self.value + 1, self.max_value)

    def decrement(self, instance):
        self.value = max(self.value - 1, self.min_value)

    def on_value(self, instance, value):
        self.update_value()

    def update_value(self):
        rounded_value = round(self._value, 2)  # Round to two decimal places
        self._value = rounded_value
        self.text_input.text = str(rounded_value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self.update_value()


class SpinBoxApp(App):
    def build(self):
        return RoundedSpinBox(min_value=0, max_value=100)


if __name__ == '__main__':
    SpinBoxApp().run()
