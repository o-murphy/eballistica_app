from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar

from signalslot import Signal


class TopBar(MDTopAppBar):
    action_click = Signal(args=['action'], name='action_click')
    settings_clicked = Signal(name='settings_cicked')
    apply_clicked = Signal(name='apply_clicked')

    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.show_cog()

    def bind_ui(self):
        self.action_click.connect(self.action_reciever)

    def show_cog(self):
        self.right_action_items = [
            ["cog-outline", lambda action: self.action_click.emit(action=action)]
        ]

    def show_check(self):
        self.right_action_items = [
            ["check", lambda action: self.action_click.emit(action=action)]
        ]

    def hide_all(self):
        self.right_action_items = []

    def action_reciever(self, action, **kwargs):
        if action.icon.find('cog') >= 0:
            self.settings_clicked.emit()
        elif action.icon.find('check') >= 0:
            self.apply_clicked.emit()


class AppTopBar(MDBoxLayout):
    def __init__(self, **kwargs):
        super(AppTopBar, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.bar = TopBar()
        self.add_widget(self.bar)

    def show_check(self):
        self.bar.hide_all()
        self.bar.show_check()

    def show_cog(self):
        self.bar.hide_all()
        self.bar.show_cog()

    def hide_all(self):
        self.bar.hide_all()


