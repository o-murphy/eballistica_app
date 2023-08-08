from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDActionBottomAppBarButton, MDFabBottomAppBarButton, MDBottomAppBar
from kivy.lang import Builder
from kivymd.uix.widget import MDWidget

from signalslot import Signal

Builder.load_string("""
#:import MDActionBottomAppBarButton kivymd.uix.toolbar.MDActionBottomAppBarButton

<AppBottomBar>
    orientation: 'vertical'
    adaptive_height: True

    MDBottomAppBar:
        id: bottom_bar
        md_bg_color: "#191c1a"
        icon_color: "#8a938c"
        # elevation: 2

        MDFabBottomAppBarButton:
            id: bottom_bar_fab
            md_bg_color: "#1f352a"
            icon: "plus"
            icon_color: "#8a938c"
            # elevation: 2

""")


class BottomAction(MDActionBottomAppBarButton):
    pass


class AppBottomBar(MDBoxLayout):
    action_clicked = Signal(args=['action'], name='action_clicked')
    back_act_clicked = Signal(args=['action'], name='back_act_clicked')
    fab_clicked = Signal(name='fab_clicked')

    def __init__(self, *args, **kwargs):
        super(AppBottomBar, self).__init__(*args, **kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.bar = self.ids.bottom_bar
        back_action = BottomAction(icon='arrow-left',
                                   on_release=lambda action: self.action_clicked.emit(action=action))
        self.bar.action_items = [back_action]
        self.fab = self.ids.bottom_bar_fab


    def bind_ui(self):
        self.action_clicked.connect(self.on_action)

    def on_action(self, action, **kwargs):
        if action.icon.find('left') >= 0:
            self.back_act_clicked.emit()

