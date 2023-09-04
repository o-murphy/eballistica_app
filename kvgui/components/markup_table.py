from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.utils import get_hex_from_color
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

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

        self._font_resolution = 1

        Window.bind(on_resize=self.on_window_resize)

    @property
    def header_data(self):
        return self._header_data

    @header_data.setter
    def header_data(self, data: list):
        self._header_data = data
        self.update_texture()

    @property
    def rows_data(self):
        return self._rows_data

    @rows_data.setter
    def rows_data(self, data: list):
        self._rows_data = data
        self.update_texture()

    def append_rows(self, data: list):
        self._rows_data += data
        self.update_texture()

    def append_row(self, data: list):
        self._rows_data.append(data)
        self.update_texture()

    def pop_row(self, index: int):
        self._rows_data.pop(index)
        self.update_texture()

    def insert_row(self, index, data):
        self._rows_data.insert(index, data)
        self.update_texture()

    def remove_row(self, data):
        self._rows_data.remove(data)
        self.update_texture()

    # def update1(self):
    #     # left align, fit
    #     def make_markup(data_part):
    #         text = ''
    #         for row in data_part:
    #             for item, width in zip(row, column_widths):
    #                 padding = f'{" " * (width - len(item))}[/color]'
    #                 item = padding + item
    #                 text += f"[b]{item}[/b]  "
    #             text += '\n'
    #             text += '–' * row_width + '\n'
    #         return text
    #
    #     full_data = self._header_data + self._rows_data
    #     bg = get_hex_from_color(self.md_bg_color)
    #
    #     column_widths = [max(len(item) for item in col) for col in zip(*full_data)]
    #     row_width = sum(column_widths) + len(column_widths) * 2
    #     self.ids.header.text = make_markup(self._header_data)
    #     self.ids.sheet.text = make_markup(self._rows_data)

    def on_window_resize(self, *args):
        self.update_texture()

    def update_texture(self):
        # right align, adjusted
        def make_markup(data_part):
            pair = False
            text = ''
            for row in data_part:
                for item, width in zip(row, column_widths):
                    padding = f'[color={bg}]{"_" * (max_col_w - len(item))}[/color]'
                    item = item + padding
                    if pair:
                        text += f"[color={bg}]__[/color][b]{item}[/b]"
                    else:
                        text += f"[color={bg}]__[/color][color=#008080][b]{item}[/b][/color]"
                text += '\n'
                text += '–' * max_row_w + '\n'
                pair = not pair
            return text

        def calc_letter_width(font_size):
            header = self.ids.header
            label = Label(text='W', font_name=header.font_name, font_size=font_size)
            label.texture_update()
            return label.texture_size[0]

        def autosize_font():
            initial_font_size = 30

            row_width_px = max_row_w * calc_letter_width(initial_font_size)
            width = self.width - self.padding[0] - self.padding[2]

            while row_width_px >= width:
                # self.ids.header.font_size -= 0.5
                # self.ids.sheet.font_size -= 0.5
                initial_font_size -= 0.5
                row_width_px = max_row_w * calc_letter_width(initial_font_size)

                if initial_font_size <= 1:
                    break

            self.ids.header.font_size = initial_font_size
            self.ids.sheet.font_size = initial_font_size

        full_data = self._header_data + self._rows_data
        bg = get_hex_from_color(self.md_bg_color)

        column_widths = [max(len(item) for item in col) for col in zip(*full_data)]
        max_col_w = max(column_widths)
        max_row_w = len(column_widths) * (max_col_w + 2)

        autosize_font()

        self.ids.header.text = make_markup(self._header_data)
        self.ids.sheet.text = make_markup(self._rows_data)
