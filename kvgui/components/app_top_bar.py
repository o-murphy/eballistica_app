from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar


from kvgui.modules import signals as sig


class TopBar(MDTopAppBar):

    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.show_cog()

    def bind_ui(self):
        ...

    def show_cog(self):
        self.right_action_items = [
            ["cog-outline", self.action_reciever]
        ]

    def show_check(self):
        self.right_action_items = [
            ["check", self.action_reciever]
        ]

    def hide_all(self):
        self.right_action_items = []

    def action_reciever(self, action, **kwargs):
        if action.icon.find('cog') >= 0:
            sig.top_bar_cog_act.emit()
        elif action.icon.find('check') >= 0:
            sig.top_bar_apply_act.emit()


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


