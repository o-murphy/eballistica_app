from kivy.lang import Builder
from kivy.utils import get_hex_from_color
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from kvgui.components.mixines import MapIdsMixine

Builder.load_file('kvgui/kv/markup_table.kv')


class MarkupTableHeader(MDLabel):
    def __init__(self, *args, **kwargs):
        super(MarkupTableHeader, self).__init__(*args, **kwargs)
        self.text = "Header"
        self.id = 'header'


class MarkupTableSheet(MDLabel):
    def __init__(self, *args, **kwargs):
        super(MarkupTableSheet, self).__init__(*args, **kwargs)
        self.text = "Sheet"
        self.id = 'sheet'



class MarkupTable(MDBoxLayout, MapIdsMixine):
    def __init__(self, *args, **kwargs):
        super(MarkupTable, self).__init__(*args, **kwargs)
        self._header_data = []
        self._rows_data = []
        # self.init_ui()
        # print(self.ids)

    # def init_ui(self):
    #     super(MarkupTable, self).init_ui()

    @property
    def header_data(self):
        return self._header_data

    @header_data.setter
    def header_data(self, data: list):
        self._header_data = data
        self.update()
        
    @property
    def rows_data(self):
        return self._rows_data

    @rows_data.setter
    def rows_data(self, data: list):
        self._rows_data = data
        self.update()

    def append_row(self, data: list):
        self._rows_data.append(data)
        self.update()

    def pop_row(self, index: int):
        self._rows_data.pop(index)
        self.update()

    def insert_row(self, index, data):
        self._rows_data.insert(index, data)
        self.update()

    def remove_row(self, data):
        self._rows_data.remove(data)
        self.update()

    def update1(self):
        # left align, fit
        def make_markup(data_part):
            text = ''
            for row in data_part:
                for item, width in zip(row, column_widths):
                    padding = f'[color={bg}]{"_" * (width - len(item))}[/color]'
                    item = padding + item
                    text += f"[b]{item}[/b]  "
                text += '\n'
                text += '–' * row_width + '\n'
            return text

        full_data = self._header_data + self._rows_data
        bg = get_hex_from_color(self.md_bg_color)

        column_widths = [max(len(item) for item in col) for col in zip(*full_data)]
        row_width = sum(column_widths) + len(column_widths) * 2
        self.ids.header.text = make_markup(self._header_data)
        self.ids.sheet.text = make_markup(self._rows_data)

    def update(self):
        # right align, adjusted
        def make_markup(data_part):
            pair = False
            text = ''
            for row in data_part:
                for item, width in zip(row, column_widths):
                    padding = f'[color={bg}]{"_" * (max_col_w - len(item))}[/color]'
                    item = item + padding
                    if pair:
                        text += f"  [b]{item}[/b]"
                    else:
                        text += f"  [color=#008080][b]{item}[/b][/color]"
                text += '\n'
                text += '–' * max_row_w + '\n'
                pair = not pair
            return text

        full_data = self._header_data + self._rows_data
        bg = get_hex_from_color(self.md_bg_color)

        column_widths = [max(len(item) for item in col) for col in zip(*full_data)]
        max_col_w = max(column_widths)
        max_row_w = len(column_widths) * (max_col_w + 2)
        row_width = sum(column_widths) + len(column_widths) * 2
        self.ids.header.text = make_markup(self._header_data)
        self.ids.sheet.text = make_markup(self._rows_data)
