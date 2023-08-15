import logging
import sys

from kivy.clock import Clock
from kivy.properties import partial
from kivymd.uix.textfield import MDTextField


class MDNumericField(MDTextField):
    def __init__(self, *args, **kwargs):
        super(MDNumericField, self).__init__(*args, **kwargs)
        self._value: float = 0
        self._min_value: [float, callable] = sys.float_info.min
        self._max_value: [float, callable] = sys.float_info.max
        self._decimals: int = 2
        self._step: [float, callable] = 0.1
        self.input_filter = 'float'
        self.input_type = 'number'
        # self.helper_text = 'error'
        # self.helper_text_mode = 'on_error'
        self.value = 0

    @property
    def max_value(self):
        if callable(self._max_value):
            return self._max_value()
        return self._max_value

    @max_value.setter
    def max_value(self, value: [float, callable]):
        invalid = self.min_value > value() if callable(value) else self.min_value > value
        if invalid:
            raise ValueError("max_value can't be < min_value")
        self._max_value = value

    @property
    def min_value(self):
        if callable(self._min_value):
            return self._min_value()
        return self._min_value

    @min_value.setter
    def min_value(self, value: [float, callable]):
        invalid = self.max_value < value() if callable(value) else self.max_value < value
        if invalid:
            raise ValueError("min_value can't be > max_value")
        self._min_value = value

    @property
    def step(self):
        if callable(self._step):
            return self._step()
        return self._step

    @step.setter
    def step(self, value: [float, callable]):
        self._step = value

    @property
    def decimals(self):
        if callable(self._decimals):
            return self._decimals()
        return self._decimals

    @decimals.setter
    def decimals(self, value: [float, callable]):
        self._decimals = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        self.text = self._formatted(value)

    def _formatted(self, value):
        return '{:.{}f}'.format(value, self.decimals)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # self._set_cursor_right(self)
        if keycode == (273, 'up'):
            self._increment()
        elif keycode == (274, 'down'):
            self._decrement()
        super(MDNumericField, self).keyboard_on_key_down(window, keycode, text, modifiers)

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
        # self._set_cursor_right(instance)
        super(MDNumericField, self).on_focus(instance, isFocused)

    def on_double_tap(self):
        Clock.schedule_once(lambda dt: self.select_all())

    def set_text(self, instance, text: str) -> None:
        if text == "":
            self._value = 0
        else:
            try:
                text = text.replace('.', '')
                new_value = int(text) / 10**self.decimals

                # if self.min_value > new_value:
                #     self.error = True
                #     self.hint_text = f"> {self.min_value}"
                # elif new_value > self.max_value:
                #     self.error = True
                #     self.hint_text = f"< {self.max_value}"
                # else:
                #     self.error = False
                #     self.hint_text = ''
                self._value = new_value

                # if self.min_value > new_value:
                #     self._value = self.min_value
                # elif new_value > self.max_value:
                #     self._value = self.max_value
                # else:
                #     self._value = new_value

            except ValueError as err:
                logging.warning(err)

        super(MDNumericField, self).set_text(instance, self._formatted(self._value))
        # self._set_cursor_right(instance)

    def insert_text(self, substring, from_undo=False):

        # self._set_cursor_right(self)
        return super().insert_text(substring, from_undo=from_undo)


if __name__ == '__main__':
    ...
