from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDActionBottomAppBarButton, MDFabBottomAppBarButton

from kvgui.modules import signals as sig

Builder.load_file('kvgui/kv/bottom_bar.kv')


class BottomAction(MDActionBottomAppBarButton):
    pass


class AppBottomBar(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super(AppBottomBar, self).__init__(*args, **kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.bar = self.ids.bottom_bar
        back_action = BottomAction(icon='arrow-left', on_release=self.on_action)
        self.bar.action_items = [back_action]
        self.fab: MDFabBottomAppBarButton = self.ids.bottom_bar_fab

    def bind_ui(self):
        self.fab.bind(on_release=lambda caller: sig.bot_bar_fab_act.emit(caller=caller))

    def on_action(self, action, **kwargs):
        if action.icon.find('left') >= 0:
            # self.back_act_clicked.emit()
            sig.bot_bar_back_act.emit()

    def fab_hide(self):
        self.fab.opacity = 0
        self.fab.disabled = True
        # self.bar.allow_hidden = True

    def fab_show(self):
        self.fab.opacity = 1
        self.fab.disabled = False
        # self.bar.allow_hidden = False

    def fab_applying(self):
        self.fab_show()
        self.fab.icon = 'check'
        self.fab._md_bg_color = "teal"

    def fab_add_new(self):
        self.fab_show()
        self.fab.icon = 'plus'
        self.fab._md_bg_color = "orange"
