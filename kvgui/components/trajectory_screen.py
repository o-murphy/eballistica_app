import threading

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.spinner import MDSpinner

from kvgui.components.datatables import MDDataTableFit
from kvgui.components.mixines import MapIdsMixine
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr

Builder.load_file('kvgui/kv/trajectory_screen.kv')

spinner = """
MDSpinner:
    size_hint: None, None
    size: dp(46), dp(46)
    pos_hint: {'center_x': .5, 'center_y': .5}
    # active: True if check.active else False
"""


class TrajectoryScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(TrajectoryScreen, self).__init__(**kwargs)
        self.name = 'traj_screen'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(TrajectoryScreen, self).init_ui()

        self.spinner: MDSpinner = Builder.load_string(spinner)

        column_data = [
            ("Range", dp(15), None),
            ("Path", dp(15), None),
            ("Path", dp(15), None),
            ("Wind.", dp(15), None),
            ("Wind.", dp(15), None),
            ("V", dp(15), None),
            ("E", dp(15), None),
        ]

        self.table = MDDataTableFit(
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data=column_data,
            rows_num=100,
            elevation=0,

            # use_pagination = True
        )

        app = MDApp.get_running_app()
        self.table.background_color = app.theme_cls.bg_light
        self.table.background_color_header = app.theme_cls.bg_light

        self.table.add_widget(self.spinner)
        self.table_tab.add_widget(self.table)

    def on_pre_enter(self, *args):

        def spin(dt):
            self.spinner.active = True

        Clock.schedule_once(spin, 0)

    def set_table_data(self, data=None):

        subheader = [
            ['m', 'cm/100m', 'MIL', 'cm/100m', 'MIL', 'm/s', 'J']
        ]
        self.table.row_data = subheader + [[str(i)] * 7 for i in range(3000, -1, -50)]

    def set_graph_data(self, data=None):
        ...

    def on_enter(self):

        try:
            # TODO: trajectory calculation

            self.set_table_data()
            self.set_graph_data()
        except Exception:
            sig.toast.emit(text=tr("Error: Can't calculate trajectory", 'Trajectory'))

        self.spinner.active = False

    def on_leave(self, *args):
        self.table.row_data = []

    def bind_ui(self):
        ...
