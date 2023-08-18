from kivy.lang import Builder
from kivy.utils import get_hex_from_color
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


Builder.load_file('kvgui/kv/markup_table.kv')


class MarkupTable(MDLabel):
    def __init__(self, *args, **kwargs):
        super(MarkupTable, self).__init__(*args, **kwargs)

        self._data = []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.update()

    def append_row(self, data: list):
        self._data.append(data)
        self.update()

    def pop_row(self, index: int):
        self._data.pop(index)
        self.update()

    def insert_row(self, index, data):
        self._data.insert(index, data)
        self.update()

    def remove_row(self, data):
        self._data.remove(data)
        self.update()

    def update(self):
        text = ''
        column_widths = [max(len(item) for item in col) for col in zip(*self._data)]
        bg = get_hex_from_color(self.md_bg_color)

        row_width = sum(column_widths) + len(column_widths) * 2

        for row in self._data:
            for item, width in zip(row, column_widths):
                padding = f'[color={bg}]{"_" * (width - len(item))}[/color]'
                item = padding + item
                text += f"[b]{item}[/b][/size]  "
            text += '\n'
            text += '–' * row_width + '\n'

        print(text)
        self.text = text
        self.autosize_font()
        
    def autosize_font(self):
        original_font_size = dp(20)
        
        # Reduce the font size until the text fits within the label's width and height
        while self.texture_size[0] > self.width:
            self.font_size -= 1
            self.texture_update()
            
            if self.font_size <= 1:  # Ensure we don't get stuck in an infinite loop
                break
