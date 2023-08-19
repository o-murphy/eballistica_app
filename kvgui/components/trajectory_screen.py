from functools import partial

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from kvgui.components.datatables import MDDataTableFit
from kvgui.components.mixines import MapIdsMixine

Builder.load_file('kvgui/kv/trajectory_screen.kv')


class TrajectoryScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(TrajectoryScreen, self).__init__(**kwargs)
        self.name = 'traj_screen'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(TrajectoryScreen, self).init_ui()

    def on_pre_enter(self, *args):
        ...

    def set_table_data(self, data, *args):
        self.table.add_row(data)

    def on_enter(self, *args):
        self.markup_table.header_data = [
            ["Range", "Path", "Path", "Wind.", "Wind.", "V", "E"],
            ['m', 'cm/100m', 'MIL', 'cm/100m', 'MIL', 'm/s', 'J']
        ]

        rows_data = [[str(i)] * 7 for i in range(3000, -1, -50)][::-1]

        # self.markup_table.rows_data = [[str(i)] * 7 for i in range(3000, -1, -50)]
        for i, row in enumerate(rows_data):
            Clock.schedule_once(partial(self.append_table_data, row), 1 / 60 * i)

    def append_table_data(self, data, *args):
        self.markup_table.insert_row(0, data)

    def set_graph_data(self, data=None):
        ...

    def on_leave(self, *args):
        self.markup_table.rows_data = []

    def bind_ui(self):
        ...
