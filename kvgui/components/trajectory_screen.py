from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('kvgui/kv/trajectory_screen.kv')


class TrajectoryScreen(Screen):
    def __init__(self, **kwargs):
        super(TrajectoryScreen, self).__init__(**kwargs)
        self.name = 'traj_screen'
