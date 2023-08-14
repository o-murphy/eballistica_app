from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDActionBottomAppBarButton

from kvgui.components.mapid import MapIdsMixine
from kvgui.modules import signals as sig

Builder.load_file('kvgui/kv/bottom_bar.kv')


class BottomAction(MDActionBottomAppBarButton):
    pass


class AppBottomBar(MDBoxLayout, MapIdsMixine):

    def __init__(self, *args, **kwargs):
        super(AppBottomBar, self).__init__(*args, **kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        super(AppBottomBar, self).init_ui()
        back_action = BottomAction(icon='arrow-left', on_release=self.on_action)
        self.bottom_bar.action_items = [back_action]

    def bind_ui(self):
        self.bottom_bar_fab.bind(on_release=lambda caller: sig.bot_bar_fab_act.emit(caller=caller))

    def on_action(self, action, **kwargs):
        if action.icon.find('left') >= 0:
            # self.back_act_clicked.emit()
            sig.bot_bar_back_act.emit()

    def fab_hide(self):
        self.bottom_bar_fab.opacity = 0
        self.bottom_bar_fab.disabled = True
        # self.bottob_bar.allow_hidden = True

    def fab_show(self):
        self.bottom_bar_fab.opacity = 1
        self.bottom_bar_fab.disabled = False
        # self.bottob_bar.allow_hidden = False

    def fab_applying(self):
        self.fab_show()
        self.bottom_bar_fab.icon = 'check'
        self.bottom_bar_fab._md_bg_color = "teal"

    def fab_add_new(self):
        self.fab_show()
        self.bottom_bar_fab.icon = 'plus'
        self.bottom_bar_fab._md_bg_color = "orange"
