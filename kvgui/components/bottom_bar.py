from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDActionBottomAppBarButton, MDFabBottomAppBarButton, MDBottomAppBar
from kivy.lang import Builder
from signalslot import Signal

Builder.load_file('kvgui/kv/bottom_bar.kv')


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
        self.fab: MDFabBottomAppBarButton = self.ids.bottom_bar_fab


    def bind_ui(self):
        self.action_clicked.connect(self.on_action)

    def on_action(self, action, **kwargs):
        if action.icon.find('left') >= 0:
            self.back_act_clicked.emit()

    def fab_hide(self):
        self.fab.opacity = 0
        self.fab.disabled = True
        # self.bar.allow_hidden = True

    def fab_show(self):
        self.fab.opacity = 1
        self.fab.disabled = False
        # self.bar.allow_hidden = False

    def fab_applying(self):
        self.fab.icon = 'check'
        self.fab._md_bg_color = "teal"

    def fab_add_new(self):
        self.fab.icon = 'plus'
        self.fab._md_bg_color = "orange"

