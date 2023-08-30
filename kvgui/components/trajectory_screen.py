from functools import partial

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
from kivy_garden.graph import Graph, LinePlot
from kivymd.uix.boxlayout import MDBoxLayout
from py_ballisticcalc.trajectory_data import TrajectoryData

from kvgui.components.mixines import MapIdsMixine
from units.ext import *

Builder.load_file('kvgui/kv/trajectory_screen.kv')


class TrajectoryGraph(MDBoxLayout):
    def __init__(self):
        super(TrajectoryGraph, self).__init__()
        self.padding = '20dp'
        self.graph = Graph(
            xlabel='Range, m', ylabel='Drop, cm', x_ticks_minor=100, x_ticks_major=500, y_ticks_major=2000,
            y_ticks_minor=500,
            y_grid_label=True, x_grid_label=True, padding=10, x_grid=True, y_grid=True,
            xmin=-0, xmax=100, ymin=-2, ymax=2, border_color=get_color_from_hex('#008080'),
            label_options={
                'color': get_color_from_hex('#008080'), 'bold': False
            }
        )

        self.add_widget(self.graph)
        self.plot = LinePlot(color=get_color_from_hex('#008080'), line_width=1.1)
        self.graph.add_plot(self.plot)

    #     self.add_plot()
    #
    # def add_plot(self):
    #     points = [(x, math.sin(x * 0.1)) for x in range(0, 101)]
    #     self.plot.points = points

    def display_data(self, data: list[TrajectoryData]):
        if data:
            points = [
                (item.travelled_distance().get_in(Distance.Meter), item.drop().get_in(Distance.Centimeter))
                for item in data
            ]
            max_tuple = max(points, key=lambda x: x[0])

            self.graph.xmin = -0
            self.graph.xmax = max_tuple[0] + 100
            self.graph.ymin = max_tuple[1] // 1000 * 1000
            self.graph.ymax = -0

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
        ...

    def display_data(self, data):
        self.markup_table.header_data = [
            ["Range", "Path", "Path", "Wind.", "Wind.", "V", "E"],
            ['m', 'cm/100m', 'MIL', 'cm/100m', 'MIL', 'm/s', 'J']
        ]

        rows_data = []

        def fmt(value, accuracy):
            return "{:.{}f}".format(value, accuracy)

        d_accuracy = BigDistance.accuracy(Distance.Meter)
        cm_accuracy = Angular.accuracy(Angular.CmPer100M)
        mil_accuracy = Angular.accuracy(Angular.Mil)
        v_accuracy = Velocity.accuracy(Velocity.MPS)
        e_accuracy = Energy.accuracy(Energy.Joule)
        for item in data:
            t_range = item.travelled_distance()
            drop_adj = item.drop_adjustment()
            wind_adj = item.drop_adjustment()
            velocity = item.velocity()
            energy = item.energy()

            rows_data.append([
                fmt(t_range.get_in(Distance.Meter), d_accuracy),
                fmt(drop_adj.get_in(Angular.CmPer100M), cm_accuracy) if drop_adj else '---',
                fmt(drop_adj.get_in(Angular.Mil), mil_accuracy) if drop_adj else '---',
                fmt(wind_adj.get_in(Angular.CmPer100M), cm_accuracy) if drop_adj else '---',
                fmt(wind_adj.get_in(Angular.Mil), mil_accuracy) if drop_adj else '---',
                fmt(velocity.get_in(Velocity.MPS), v_accuracy),
                fmt(energy.get_in(Energy.Joule), e_accuracy)
            ])

        # self.markup_table.rows_data = [[str(i)] * 7 for i in range(3000, -1, -50)]
        # for i, row in enumerate(rows_data):
        #     Clock.schedule_once(partial(self.append_table_data, row), 1 / 60 * i)

        rows_data.reverse()
        Clock.schedule_once(partial(self.set_table_data, rows_data), 0.5)

        self.set_graph_data(data)

    def set_table_data(self, data, *args):
        self.markup_table.rows_data = data

    def append_table_data(self, data, *args):
        self.markup_table.insert_row(0, data)

    def set_graph_data(self, data=None):
        self.graph.display_data(data)

    def on_leave(self, *args):
        self.markup_table.rows_data = []

    def bind_ui(self):
        ...
