from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar

from signalslot import Signal


Builder.load_string("""
<AppTopBar>
    orientation: "vertical"
    spacing: "12dp"
    pos_hint: {"top": 1}
    adaptive_height: True

<TopBar>:
    type_height: 'medium'
    headline_text: "Rifles /"
    title: "eBallistica"
    anchor_title: "left"
    elevation: 3
""")


class TopBar(MDTopAppBar):
    action_click = Signal(args=['action'], name='action_click')
    settings_cicked = Signal(name='settings_cicked')

    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.right_action_items = [
            ["cog-outline", lambda action: self.action_click.emit(action=action)]
        ]
        self.action_click.connect(self.action_reciever)

    def action_reciever(self, action, **kwargs):
        if action.icon.find('cog') >= 0:
            self.settings_cicked.emit()


class AppTopBar(MDBoxLayout):
    def __init__(self, **kwargs):
        super(AppTopBar, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        self.bar = TopBar()
        self.add_widget(self.bar)
