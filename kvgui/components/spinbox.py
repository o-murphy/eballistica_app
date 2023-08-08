import logging

from kivymd.uix.textfield import MDTextField


class MDSpinBox(MDTextField):
    def __init__(self, *args, **kwargs):
        super(MDSpinBox, self).__init__(*args, **kwargs)
        self._value: float = 0
        self.max_value: float = 0
        self.min_value: float = 100
        self.decimals: int = 2
        self.step: float = 1
        self.input_filter = 'float'
        self.value = 0

        self.prefix = ''
        self.suffix = ''

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        self.set_text(self, str(value))

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode == (273, 'up'):
            self.increment()
        elif keycode == (274, 'down'):
            self.decrement()
        # elif keycode == (127, 'delete') and len(self) and self.text[self.cursor_index()] == '.':
        elif keycode == (127, 'delete'):
            # self.value /= 10
            # self._move_cursor_word_left()
            return
        super(MDSpinBox, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def increment(self):
        self.value += self.step

    def decrement(self):
        self.value -= self.step

    def set_text(self, instance_text_field, text: str) -> None:
        if text == '':
            text = '0'
        try:
            new_decimals = int(float(text) * 10**self.decimals)
            cur_decimals = int(self.value * 10**self.decimals)
            if cur_decimals != new_decimals:
                self._value = float(text)
        except ValueError as err:
            logging.warning(err)
        formatted_text = '{:.{}f}'.format(self.value, self.decimals)
        super(MDSpinBox, self).set_text(instance_text_field, formatted_text)

    def insert_text(self, substring, from_undo=False):
        print(substring)
        substring = substring.replace(',', '')
        if substring == '.':
            self.text = self.text[:self.cursor_index()] + substring
        else:
            super(MDSpinBox, self).insert_text(substring, from_undo)


class ConverMDSpinBox(MDSpinBox):
    def __init__(self, *args, **kwargs):
        super(ConverMDSpinBox, self).__init__(*args, **kwargs)

        self._convertor = None

    def convertor(self):
        return self._convertor

    def set_convertor(self, value):
        self._convertor = value

    def set_raw_value(self, value):
        if self._convertor is not None:
            self.value = self._convertor.fromRaw(value)
        else:
            self.value = value

    def raw_value(self):
        if self._convertor is not None:
            return self._convertor.toRaw(self.value)
        else:
            return self.value


if __name__ == '__main__':
    from kivymd.app import MDApp

    class SpinBoxApp(MDApp):
        
        def build(self):
            spinbox = MDSpinBox()
            return spinbox

    SpinBoxApp().run()
