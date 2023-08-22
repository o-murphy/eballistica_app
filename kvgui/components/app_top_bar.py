from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar

from kvgui.modules import signals as sig
from kvgui.modules.translator import translate as tr


Builder.load_file('kvgui/kv/top_bar.kv')


class TopBar(MDTopAppBar):

    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.init_ui()
        self.bind_ui()

    def init_ui(self):
        self.show_cog()
        self.ids.label_headline.font_style = 'Subtitle1'

    def set_headline_font_style(self, interval=None, font_style=None) -> None:
        # Skip default font_styles
        pass

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
        self.bind_ui()

        self._breadcrumb_value = None

    def init_ui(self):
        self.top_bar = TopBar()
        self.add_widget(self.top_bar)

    def bind_ui(self):
        sig.translator_update.connect(self.update_breadcrumb)

    def update_breadcrumb(self, **kwargs):
        self.breadcrumb = self._breadcrumb_value

    @property
    def headline_text(self):
        return self.top_bar.headline_text

    @headline_text.setter
    def headline_text(self, text):
        self.top_bar.headline_text = text

    @property
    def breadcrumb(self):
        return self._breadcrumb_value

    @breadcrumb.setter
    def breadcrumb(self, texts: list[str]):
        if texts is not None:
            self._breadcrumb_value = texts
            texts = [tr(string, 'Breadcrumb') for string in texts]
            self.top_bar.headline_text = ' / '.join(texts)

    def show_check(self):
        self.top_bar.hide_all()
        self.top_bar.show_check()

    def show_cog(self):
        self.top_bar.hide_all()
        self.top_bar.show_cog()

    def hide_all(self):
        self.top_bar.hide_all()
