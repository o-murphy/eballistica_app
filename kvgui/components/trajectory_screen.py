from functools import partial

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
from kivy_garden.graph import Graph, LinePlot
from kivymd.uix.boxlayout import MDBoxLayout
from py_ballisticcalc.trajectory_data import TrajectoryData

from kvgui.components.mixines import MapIdsMixine
from units.ext import *


class TrajectoryGraph(MDBoxLayout):
    def __init__(self):
        super(TrajectoryGraph, self).__init__()
        self.padding = '20dp'
        self.graph = Graph(
            xlabel='Range, m', ylabel='Drop, m',
            x_ticks_major=500, x_ticks_minor=5,
            y_ticks_major=25, y_ticks_minor=5,
            y_grid_label=True, x_grid_label=True, padding=10, x_grid=True, y_grid=True,
            xmin=-0, xmax=100, ymin=-2, ymax=2, border_color=get_color_from_hex('#008080'),
            label_options={
                'color': get_color_from_hex('#008080'), 'bold': False
            }
        )

        self.add_widget(self.graph)
        self.plot = LinePlot(color=get_color_from_hex('#008080'), line_width=1.1)
        self.graph.add_plot(self.plot)

    def display_data(self, data: list[TrajectoryData]):
        if data:
            points = tuple(
                (item.travelled_distance().get_in(int(Distance.Meter)), item.drop().get_in(int(Distance.Meter)))
                for item in data
            )

            max_tuple = max(points, key=lambda x: x[0])

            self.graph.xmin = -0
            self.graph.xmax = max_tuple[0] + 100
            self.graph.ymin = max_tuple[1] // 25 * 25
            self.graph.ymax = 25

            self.plot.points = points


class DragMachGraph(MDBoxLayout):
    def __init__(self):
        super(DragMachGraph, self).__init__()
        self.padding = '20dp'
        self.graph = Graph(
            xlabel='Mach', ylabel='CD',
            x_ticks_minor=5,
            x_ticks_major=1,
            y_ticks_major=0.1,
            y_ticks_minor=5,
            y_grid_label=True, x_grid_label=True, padding=10, x_grid=True, y_grid=True,
            xmin=0, xmax=5, ymin=0, ymax=1,
            border_color=get_color_from_hex('#008080'),
            label_options={
                'color': get_color_from_hex('#008080'), 'bold': False
            }
        )

        self.add_widget(self.graph)
        self.plot = LinePlot(color=get_color_from_hex('#008080'), line_width=1.1)
        self.graph.add_plot(self.plot)

    def display_data(self, data):
        if data:
            points = tuple((round(item['A'], 4), round(item['B'], 4)) for item in data)
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
        self.drag_mach = DragMachGraph()
        self.graph_tab.add_widget(self.graph)
        self.drag_mach_tab.add_widget(self.drag_mach)

    def on_pre_enter(self, *args):
        ...

    def on_enter(self, *args):
        ...

    def display_data(self, data, drag_mach):
        self.markup_table.header_data = [
            ["Range", "Hold", "Hold", "Wind.", "Wind.", "V", "E"],
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
            wind_adj = item.windage_adjustment()
            velocity = item.velocity()
            energy = item.energy()

            rows_data.append([
                fmt(t_range.get_in(int(Distance.Meter)), d_accuracy),
                fmt(drop_adj.get_in(int(Angular.CmPer100M)), cm_accuracy) if drop_adj else '---',
                fmt(drop_adj.get_in(int(Angular.Mil)), mil_accuracy) if drop_adj else '---',
                fmt(wind_adj.get_in(int(Angular.CmPer100M)), cm_accuracy) if drop_adj else '---',
                fmt(wind_adj.get_in(int(Angular.Mil)), mil_accuracy) if drop_adj else '---',
                fmt(velocity.get_in(int(Velocity.MPS)), v_accuracy),
                fmt(energy.get_in(int(Energy.Joule)), e_accuracy)
            ])

        # self.markup_table.rows_data = [[str(i)] * 7 for i in range(3000, -1, -50)]
        # for i, row in enumerate(rows_data):
        #     Clock.schedule_once(partial(self.append_table_data, row), 1 / 60 * i)

        rows_data.reverse()
        Clock.schedule_once(partial(self.set_table_data, rows_data), 0.5)
        # Clock.schedule_once(partial(self.set_graph_data, data), 0.6)
        # Clock.schedule_once(partial(self.set_drag_mach, drag_mach), 0.7)

        self.set_graph_data(data)
        self.set_drag_mach(drag_mach)

    def set_drag_mach(self, data=None, *args):
        self.drag_mach.display_data(data)

    def set_table_data(self, data=None, *args):
        self.markup_table.rows_data = data

    def append_table_data(self, data=None, *args):
        self.markup_table.insert_row(0, data)

    def set_graph_data(self, data=None, *args):
        self.graph.display_data(data)

    def on_leave(self, *args):
        self.markup_table.rows_data = []

    def bind_ui(self):
        ...
