import logging

from kivy.clock import Clock
from kivy.properties import partial
from kivymd.uix.textfield import MDTextField


class MDSpinBox(MDTextField):
    def __init__(self, *args, **kwargs):
        super(MDSpinBox, self).__init__(*args, **kwargs)
        self._value: float = 0
        self.max_value: float = 100
        self.min_value: float = 0
        self.decimals: int = 2
        self.step: float = 0.1
        self.input_filter = 'float'
        self.value = 0

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        self.text = self._formatted(value)

    def _formatted(self, value):
        return '{:.{}f}'.format(value, self.decimals)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        self._set_cursor_right(self)
        if keycode == (273, 'up'):
            self._increment()
        elif keycode == (274, 'down'):
            self._decrement()
        super(MDSpinBox, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def _increment(self):
        self.value += self.step

    def _decrement(self):
        self.value -= self.step

    def set_cursor(self, instance, dt):
        instance.cursor = (len(instance.text), 0)

    def _set_cursor_right(self, instance):
        if instance.focus:
            final_len = len(instance.text)
            self.cursor = (final_len, 0)
            Clock.schedule_once(partial(self.set_cursor, instance), 0)
            return

    def on_focus(self, instance, isFocused):
        self._set_cursor_right(instance)
        super(MDSpinBox, self).on_focus(instance, isFocused)

    def on_double_tap(self):
        Clock.schedule_once(lambda dt: self.select_all())

    def set_text(self, instance, text: str) -> None:

        if text == "":
            self._value = 0
        else:
            try:
                text = text.replace('.', '')
                new_value = int(text) / 10**self.decimals

                if self.min_value > new_value:
                    self._value = self.min_value
                elif new_value > self.max_value:
                    self._value = self.max_value
                else:
                    self._value = new_value

            except ValueError as err:
                logging.warning(err)

        super(MDSpinBox, self).set_text(instance, self._formatted(self._value))
        self._set_cursor_right(instance)

    def insert_text(self, substring, from_undo=False):

        self._set_cursor_right(self)
        return super().insert_text(substring, from_undo=from_undo)


class MDUnitsInput(MDSpinBox):
    def __init__(self, *args, **kwargs):
        super(MDUnitsInput, self).__init__(*args, **kwargs)

        self._convertor = None

    @property
    def convertor(self):
        return self._convertor

    @convertor.setter
    def set_convertor(self, value):
        self._convertor = value

    @property
    def raw_value(self):
        if self._convertor is not None:
            return self._convertor.toRaw(self.value)
        else:
            return self.value

    @raw_value.setter
    def raw_value(self, value):
        if self._convertor is not None:
            self.value = self._convertor.fromRaw(value)
        else:
            self.value = value




if __name__ == '__main__':
    from kivymd.app import MDApp

    class SpinBoxApp(MDApp):
        
        def build(self):
            spinbox = MDUnitsInput()
            return spinbox

    SpinBoxApp().run()
