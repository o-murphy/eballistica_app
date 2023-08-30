import math
from functools import partial

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
from kivy_garden.graph import Graph, LinePlot
from kivymd.uix.boxlayout import MDBoxLayout

from kvgui.components.mixines import MapIdsMixine

Builder.load_file('kvgui/kv/trajectory_screen.kv')


class TrajectoryGraph(MDBoxLayout):
    def __init__(self):
        super(TrajectoryGraph, self).__init__()
        self.padding = '20dp'
        self.graph = Graph(
            xlabel='Range, m', ylabel='Drop, cm', x_ticks_minor=10, x_ticks_major=100, y_ticks_major=1,
            y_ticks_minor=0.1,
            y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
            xmin=-0, xmax=100, ymin=-2, ymax=2, border_color=get_color_from_hex('#008080'),
            label_options={
                'color': get_color_from_hex('#008080'), 'bold': False
            }
        )

        self.add_widget(self.graph)
        self.plot = LinePlot(color=get_color_from_hex('#008080'), line_width=1.1)
        self.graph.add_plot(self.plot)

        self.add_plot()

    def add_plot(self):
        points = [(x, math.sin(x * 0.1)) for x in range(0, 101)]
        self.plot.points = points


class TrajectoryScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(TrajectoryScreen, self).__init__(**kwargs)
        self.name = 'traj_screen'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(TrajectoryScreen, self).init_ui()

        self.graph = TrajectoryGraph()
        self.graph_tab.add_widget(self.graph)

    def on_pre_enter(self, *args):
        ...

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
