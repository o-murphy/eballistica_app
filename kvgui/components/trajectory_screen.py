from functools import partial

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar

from kvgui.components.datatables import MDDataTableFit
from kvgui.components.mixines import MapIdsMixine
from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr


Builder.load_file('kvgui/kv/trajectory_screen.kv')


class TrajectoryScreen(Screen, MapIdsMixine):
    def __init__(self, **kwargs):
        super(TrajectoryScreen, self).__init__(**kwargs)
        self.name = 'traj_screen'
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(TrajectoryScreen, self).init_ui()

        column_data = [
            ("Range", dp(10), None),
            ("Path", dp(10), None),
            ("Path", dp(10), None),
            ("Wind.", dp(10), None),
            ("Wind.", dp(10), None),
            ("V", dp(10), None),
            ("E", dp(10), None),
        ]

        self.table = MDDataTableFit(
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data=column_data,
            rows_num=20,
            use_pagination=True,
            elevation=0,

            # use_pagination = True
        )

        app = MDApp.get_running_app()
        self.table.background_color = app.theme_cls.bg_light
        self.table.background_color_header = app.theme_cls.bg_light

        self.table_tab.add_widget(self.table)

    def on_pre_enter(self, *args):
        ...

    def set_table_data(self, data, *args):
        self.table.add_row(data)

    def update_progress(self, *args):
        progress = 100 * len(self.table.row_data) / (len(self.row_data))
        self.progress.value = progress
        if progress == 100:
            self.event.cancel()

    def on_enter(self, *args):
        self.progress.value = 0
        self.event = None
        try:
            # TODO: trajectory calculation

            subheader = [
                ['m', 'cm/100m', 'MIL', 'cm/100m', 'MIL', 'm/s', 'J']
            ]
            self.row_data = subheader + [[str(i)] * 7 for i in range(3000, -1, -50)]
            rate = 1 / 30

            self.event = Clock.schedule_interval(partial(self.update_progress), rate)

            for i, data in enumerate(self.row_data):
                Clock.schedule_once(partial(self.set_table_data, data), rate * 2 * i)


            self.set_graph_data()

        except Exception as exc:
            Clock.unschedule(self.event)
            sig.toast.emit(text=tr("Error: Can't calculate trajectory", 'Trajectory'))
            self.progress.stop()
            print(exc)



    def set_graph_data(self, data=None):
        ...

    # def on_enter(self):
        # sig.wait_me.emit()
        # try:
        #     # TODO: trajectory calculation
        #
        #     subheader = [
        #         ['m', 'cm/100m', 'MIL', 'cm/100m', 'MIL', 'm/s', 'J']
        #     ]
        #     row_data = subheader + [[str(i)] * 7 for i in range(3000, -1, -50)]
        #
        #     for i, data in enumerate(row_data):
        #         Clock.schedule_once(partial(self.set_table_data, data), 1 / 10 * i)
        #     Clock.schedule_once(lambda *args: sig.unwait_me.emit(), 1 / 10 * len(row_data))
        #
        #     self.set_graph_data()
        #
        # except Exception as exc:
        #     print(exc)
        #     sig.toast.emit(text=tr("Error: Can't calculate trajectory", 'Trajectory'))
        #     sig.unwait_me.emit()

    def on_leave(self, *args):
        self.table.row_data = []

    def bind_ui(self):
        ...
